# Re-shoot the live project sites with headless Edge (no extra downloads).
# Usage: powershell -File scripts\capture-shots.ps1 -Out .\raw
param([string]$Out = ".\raw")
$edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
New-Item -ItemType Directory -Force $Out | Out-Null
$sites = [ordered]@{
  'penbisa-home'='https://penbisa.id'; 'penbisa-karya'='https://penbisa.id/karya'
  'orbita-home'='https://orbitacrm.my.id'; 'orbita-modul'='https://orbitacrm.my.id/modul'
  'cosmos-home'='https://cosmosriset.org'; 'cosmos-products'='https://cosmosriset.org/products'
  'cc-home'='https://compassionate-companion.com'
}
foreach ($k in $sites.Keys) {
  & $edge --headless=new --disable-gpu --hide-scrollbars --window-size=1440,900 --virtual-time-budget=12000 "--screenshot=$Out\$k.png" $sites[$k] 2>$null | Out-Null
}
# orbita tall capture is sliced into extra frames by make_shots.py
& $edge --headless=new --disable-gpu --hide-scrollbars --window-size=1440,3000 --virtual-time-budget=15000 "--screenshot=$Out\orbita-tall.png" https://orbitacrm.my.id 2>$null | Out-Null
# CHE-VERSE is local-only: run `npm run dev` in solo-sam\3D-Web first (port 8046).
