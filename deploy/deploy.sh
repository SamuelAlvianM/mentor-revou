#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------------------
# deploy.sh — Deploy mentor-revou (Next.js + Flask) ke server `samyth` (PM2 + Cloudflare Tunnel, tanpa nginx)
# Jalankan dari root mentor-revou:
#   bash deploy/deploy.sh [--init] [--seed] [--skip-build]
#
# Tujuan = alias Host `samyth` di ~/.ssh/config (HostName, User, key diambil dari
# sana — tidak ada IP/user yang dipaku di skrip ini). Override: REMOTE=lain bash ...
#
# --init       : SEKALI saja di server baru. Pasang Node 22 (NodeSource), pm2, cloudflared,
#                python3-venv dan swap 2 GB (jaga-jaga untuk pm2/pip). Server `samyth`
#                awalnya kosong: tanpa node/pm2.
# --seed       : paksa isi ulang DB dari backend/seed.py. ⚠️ seed.py men-DROP semua
#                tabel — pesan kontak (tabel messages) ikut hilang. Tanpa flag ini seed
#                hanya jalan otomatis kalau DB masih kosong (deploy pertama).
# --skip-build : pakai .next/standalone yang sudah ada (tidak build ulang).
#
# ARSITEKTUR:
#  - Gaya Orbita: frontend di-build DI LOKAL (next build, output: "standalone"), lalu
#    server hanya menerima hasil build (.next/standalone + static + public) — tanpa
#    npm install dan tanpa build di server (RAM-nya cuma 2 GB). Flask tidak punya
#    langkah build; hanya source kecilnya yang dikirim, dependensi lewat pip di server.
#  - SQLite (backend/instance/mentor_revou.db) hidup di server dan TIDAK ikut dikirim —
#    deploy tidak menimpa pesan kontak yang masuk.
#  - Tanpa nginx dan tanpa port publik: Cloudflare Tunnel (cloudflared) → Next :3010
#    (hanya 127.0.0.1). HTTPS ditangani Cloudflare. Browser hanya bicara ke Next; Next
#    meneruskan /api/* ke Flask (gunicorn) di 127.0.0.1:5010 lewat rewrites di next.config.ts.
#    Semua proses dijalankan pm2.
# ---------------------------------------------------------------------------

_DEPLOY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$_DEPLOY_DIR/.." && pwd)"

# deploy/.env (opsional, gitignored) boleh mengisi DOMAIN / REMOTE / REMOTE_DIR.
if [[ -f "$_DEPLOY_DIR/.env" ]]; then set -a; source "$_DEPLOY_DIR/.env"; set +a; fi

REMOTE="${REMOTE:-samyth}"
REMOTE_DIR="${REMOTE_DIR:-mentor-revou}"   # relatif ke $HOME server
DOMAIN="${DOMAIN:-}"                       # hanya untuk pesan akhir (hostname tunnel di Cloudflare)
WEB_PORT=3010
API_PORT=5010

INIT=false; SEED=false; SKIP_BUILD=false
for arg in "$@"; do
  case "$arg" in
    --init)       INIT=true ;;
    --seed)       SEED=true ;;
    --skip-build) SKIP_BUILD=true ;;
    *) echo "flag tidak dikenal: $arg"; exit 1 ;;
  esac
done

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
log()  { echo -e "${GREEN}[deploy]${NC} $*"; }
warn() { echo -e "${YELLOW}[warn]${NC} $*"; }
err()  { echo -e "${RED}[error]${NC} $*"; exit 1; }

# --- Sanity checks ---
[[ -d "$ROOT/frontend" && -d "$ROOT/backend" ]]      || err "jalankan dari repo mentor-revou (frontend/ dan backend/ tidak ada)."
[[ -f "$_DEPLOY_DIR/ecosystem.config.cjs" ]]         || err "deploy/ecosystem.config.cjs tidak ditemukan."
ssh -o BatchMode=yes -o ConnectTimeout=15 "$REMOTE" true 2>/dev/null \
  || err "tidak bisa SSH ke '$REMOTE'. Cek Host $REMOTE di ~/.ssh/config."
HOST_ADDR="$(ssh -G "$REMOTE" | awk '/^hostname /{print $2}')"
log "Target: $REMOTE ($HOST_ADDR) → ~/$REMOTE_DIR"

# ============================================================
# INIT — bootstrap server baru (sekali saja)
# ============================================================
if [[ "$INIT" == true ]]; then
  log "=== INIT SERVER ==="
  ssh "$REMOTE" "bash -s" <<'ENDINIT'
set -euo pipefail
sudo apt-get update -y
sudo apt-get install -y python3-venv python3-pip curl ca-certificates

# Swap: server 2 GB, `next build` bisa menembus RAM tanpa ini.
if [[ -z "$(swapon --show --noheadings)" ]]; then
  echo "[init] membuat swap 2 GB..."
  sudo fallocate -l 2G /swapfile && sudo chmod 600 /swapfile
  sudo mkswap /swapfile >/dev/null && sudo swapon /swapfile
  grep -q '^/swapfile' /etc/fstab || echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab >/dev/null
fi

# Node 22 LTS dari NodeSource (apt bawaan Ubuntu 24.04 = Node 18, terlalu lama untuk Next 16).
if ! command -v node >/dev/null || [[ "$(node -v | cut -d. -f1 | tr -d v)" -lt 20 ]]; then
  curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
  sudo apt-get install -y nodejs
fi
command -v pm2 >/dev/null || sudo npm install -g pm2

# cloudflared (Cloudflare Tunnel): HTTPS ditangani Cloudflare, tanpa certbot dan tanpa membuka port.
# Paket resmi dari repo apt pkg.cloudflare.com. Tunnel-nya dibuat di dashboard Zero Trust
# (butuh token akun, jadi tidak dibuat skrip ini): lihat pesan di akhir deploy.
if ! command -v cloudflared >/dev/null; then
  sudo mkdir -p --mode=0755 /usr/share/keyrings
  curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | sudo tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null
  echo 'deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared any main' | sudo tee /etc/apt/sources.list.d/cloudflared.list >/dev/null
  sudo apt-get update -y && sudo apt-get install -y cloudflared
fi

# Autostart pm2 setelah reboot.
sudo env PATH="$PATH" pm2 startup systemd -u "$USER" --hp "$HOME" >/dev/null || true
echo "[init] selesai: node $(node -v), pm2 $(pm2 -v), cloudflared $(cloudflared --version | head -1)."
ENDINIT
fi

# ============================================================
# BUILD LOKAL — next build (standalone). Gagal build → stop sebelum mengirim apa pun.
# API_URL ikut terbaked di rewrites, jadi harus alamat Flask DI SERVER.
# ============================================================
if [[ "$SKIP_BUILD" == false ]]; then
  log "[1/4] Build frontend lokal (npm run build)..."
  ( cd "$ROOT/frontend" && API_URL="http://127.0.0.1:$API_PORT" npm run build ) || err "build frontend gagal"
else
  warn "[1/4] Build di-skip (--skip-build) — pakai .next/standalone yang ada."
fi
[[ -f "$ROOT/frontend/.next/standalone/server.js" ]] || err ".next/standalone tidak ditemukan. Build dulu (jangan pakai --skip-build)."

# ============================================================
# KIRIM — backend: source saja; frontend: hanya hasil build
# ============================================================
log "[2/4] Kirim backend (source) + frontend (hasil build)..."
ssh "$REMOTE" "mkdir -p ~/'$REMOTE_DIR'/backend ~/'$REMOTE_DIR'/_incoming"
tar czf - -C "$ROOT" --exclude='.venv' --exclude='__pycache__' --exclude='instance' --exclude='.env' backend   | ssh "$REMOTE" "tar xzf - -C ~/'$REMOTE_DIR'"
# `sharp-win32-x64` = binary Windows yang ikut terlacak; tidak dipakai (tanpa next/image).
tar czf - -C "$ROOT/frontend" --exclude='sharp-win32-x64' .next/standalone .next/static public   | ssh "$REMOTE" "rm -rf ~/'$REMOTE_DIR'/_incoming && mkdir -p ~/'$REMOTE_DIR'/_incoming && tar xzf - -C ~/'$REMOTE_DIR'/_incoming"
scp -q "$_DEPLOY_DIR/ecosystem.config.cjs" "$REMOTE:$REMOTE_DIR/ecosystem.config.cjs"
ssh "$REMOTE" "bash -s" <<ENDSWAP
set -euo pipefail
cd ~/$REMOTE_DIR
rm -rf frontend && mkdir -p frontend/.next
cp -a _incoming/.next/standalone/. frontend/
cp -a _incoming/.next/static frontend/.next/static
cp -a _incoming/public frontend/public
rm -rf _incoming
ENDSWAP

# ============================================================
# BACKEND — venv, dependensi, seed (hanya DB kosong / --seed)
# ============================================================
log "[3/4] Backend (Flask + SQLAlchemy)..."
ssh "$REMOTE" "FORCE_SEED='$SEED' REMOTE_DIR='$REMOTE_DIR' bash -s" <<'ENDBE'
set -euo pipefail
cd "$HOME/$REMOTE_DIR/backend"
[[ -d .venv ]] || python3 -m venv .venv
.venv/bin/pip install --quiet --upgrade pip
.venv/bin/pip install --quiet -r requirements.txt
EMPTY=$(.venv/bin/python -c "from app import app; from models import Project
with app.app_context(): print(int(Project.query.count() == 0))")
if [[ "$FORCE_SEED" == true || "$EMPTY" == 1 ]]; then
  echo "[backend] seed.py (DB kosong atau --seed)..."
  .venv/bin/python seed.py
else
  echo "[backend] DB sudah berisi — seed dilewati."
fi
ENDBE

# ============================================================
# RESTART PM2
# ============================================================
log "[4/4] Restart PM2..."
ssh "$REMOTE" "bash -s" <<ENDPM2
set -euo pipefail
cd ~/$REMOTE_DIR
export WEB_PORT=$WEB_PORT API_PORT=$API_PORT
# delete+start, bukan startOrRestart: restart memakai definisi lama dan mengabaikan
# perubahan script/args di ecosystem (pernah bikin web crash setelah ganti ke standalone).
pm2 delete mentor-revou-api mentor-revou-web 2>/dev/null || true
pm2 start ecosystem.config.cjs --update-env
pm2 save
pm2 status
ENDPM2

# Cek cepat lewat jalur yang sama dengan browser (Next → Flask). Tunggu Next siap, maks 30 dtk.
OK=false
for _ in $(seq 1 15); do
  if ssh "$REMOTE" "curl -fsS http://127.0.0.1:$WEB_PORT/api/health" 2>/dev/null; then OK=true; echo; break; fi
  sleep 2
done
[[ "$OK" == true ]] || warn "health check belum menjawab — lihat: ssh $REMOTE 'pm2 logs --lines 40'"

log "Deploy selesai! Web hanya mendengar di 127.0.0.1:$WEB_PORT (tanpa port publik)."
if [[ -n "$DOMAIN" ]]; then
  log "Alamat publik lewat Cloudflare Tunnel: https://$DOMAIN"
  log "  (sekali saja) tunnel di Cloudflare: public hostname $DOMAIN → http://localhost:$WEB_PORT,"
  log "  lalu di server: sudo cloudflared service install <token>"
fi
