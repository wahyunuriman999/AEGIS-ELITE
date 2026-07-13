# Deployment guide (example)

This folder contains example manifests to run AEGIS locally or on a VM using Docker Compose and Nginx as a reverse proxy.

Quick steps (Ubuntu VM):

1. Copy repository to `/opt/aegis` on the VM:

```bash
sudo mkdir -p /opt/aegis
sudo rsync -a . /opt/aegis/
cd /opt/aegis
```

2. Install Docker & docker-compose (if not installed):

```bash
sudo apt update
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker $USER
```

3. Start stack:

```bash
sudo docker-compose up -d --build
```

4. (Optional) Use systemd unit:

```bash
sudo cp deploy/aegis.service /etc/systemd/system/aegis.service
sudo systemctl daemon-reload
sudo systemctl enable --now aegis.service
```

Notes & next steps:
- The `api` service uses the local `Dockerfile` and exposes port `8000`.
- `studio` service runs the included `AEGIS-Studio/web_server.py` for local UI.
- `proxy` runs Nginx and proxies `/api/` to the API and `/studio/` to the Studio.
- For production, add TLS (Let's Encrypt), environment secrets (GHCR credentials, STUDIO_PROXY_SECRET), and pin image tags.
