# Cloud Install Guide

Use the Dockerfile and docker-compose under `docker/`.

## Quick deploy
```bash
cd docker
docker compose up --build -d
```

Then open port 8787 on your host and put the public URL into the app settings.
