#!/usr/bin/env bash
# Install or update the backend and Nginx config on the Compute Engine VM.
# Run on the VM:  sudo bash setup_vm.sh
# Safe to re-run: it pulls the latest code and restarts the service.
set -euo pipefail

REPO_URL="https://github.com/bujari09/ai-student-feedback-system.git"
BASE=/opt/ai-feedback
APP=$BASE/app
VENV=$BASE/venv
WEB_ROOT=/var/www/feedback
PUBLIC_IP=$(curl -s -H "Metadata-Flavor: Google" \
  "http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip")

echo "==> System user and folders"
id feedback >/dev/null 2>&1 || useradd --system --home "$BASE" --shell /usr/sbin/nologin feedback
mkdir -p "$BASE" "$WEB_ROOT"

echo "==> Code from GitHub"
if [ -d "$APP/.git" ]; then
  git -C "$APP" pull --ff-only
else
  git clone "$REPO_URL" "$APP"
fi

echo "==> Python virtual environment and dependencies"
[ -d "$VENV" ] || python3 -m venv "$VENV"
"$VENV/bin/pip" install --quiet --upgrade pip
"$VENV/bin/pip" install --quiet -r "$APP/backend/requirements.txt"

echo "==> Backend configuration (.env, no secrets – credentials come from the VM service account)"
if [ ! -f "$APP/backend/.env" ]; then
  sed -e "s/^APP_ENV=.*/APP_ENV=production/" \
      -e "s#^CORS_ORIGINS=.*#CORS_ORIGINS=http://${PUBLIC_IP}#" \
      "$APP/backend/.env.example" > "$APP/backend/.env"
fi
chown -R feedback:feedback "$BASE"

echo "==> systemd service"
cp "$APP/deploy/systemd/feedback-backend.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now feedback-backend
systemctl restart feedback-backend

echo "==> Nginx"
cp "$APP/deploy/nginx/feedback.conf" /etc/nginx/sites-available/feedback
ln -sf /etc/nginx/sites-available/feedback /etc/nginx/sites-enabled/feedback
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx

echo "==> Health check"
for i in $(seq 1 15); do
  if curl -fsS http://127.0.0.1:8000/api/health; then echo; break; fi
  sleep 2
done
echo "Done. Frontend files go to $WEB_ROOT; app: http://${PUBLIC_IP}"
