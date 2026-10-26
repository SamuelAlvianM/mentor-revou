// Dibaca pm2 di server. Port datang dari env (di-export oleh deploy.sh);
// jalur app = folder file ini, jadi tidak ada path absolut yang dipaku.
const root = __dirname

module.exports = {
  apps: [
    {
      name: 'mentor-revou-api',
      script: '.venv/bin/gunicorn',
      args: `-w 2 -b 127.0.0.1:${process.env.API_PORT || 5010} app:app`,
      cwd: `${root}/backend`,
      interpreter: 'none',
      max_memory_restart: '300M',
      env_production: { PYTHONUNBUFFERED: '1' },
    },
    {
      name: 'mentor-revou-web',
      script: 'server.js', // hasil `next build` mode standalone

      cwd: `${root}/frontend`,
      max_memory_restart: '600M',
      env: {
        NODE_ENV: 'production',
        PORT: String(process.env.WEB_PORT || 3010),
        HOSTNAME: '127.0.0.1',
        API_URL: `http://127.0.0.1:${process.env.API_PORT || 5010}`,
      },
    },
  ],
}
