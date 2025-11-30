# Docker Build & Run Guide

## Quick Start

```bash
# From AuralDine root directory
docker-compose up --build

# Access:
# Frontend: http://localhost:3000
# Backend: http://localhost:5000
# Health check: curl http://localhost:5000/
```

## What Was Fixed ✅

### 1. Port Mapping
- **Backend**: Now exposed on `5000` (maps container port 8000 → host port 5000)
- **Frontend**: Exposed on `3000` (maps container port 80 → host port 3000)

### 2. Service Communication
- Added `app-network` for proper Docker networking
- Frontend can now communicate with backend via `http://backend:8000`
- Added health check so frontend waits for backend to be ready

### 3. Nginx Configuration
- Created `nginx.conf` for frontend to proxy API requests
- Frontend automatically uses `/predict/` which gets proxied to backend
- Handles CORS and proper request forwarding

### 4. Backend Health Check
- Added health check endpoint that Docker monitors
- Frontend service waits for backend to be healthy before starting
- Automatic retry and timeout handling

### 5. API URL Auto-Detection
- Frontend API automatically detects if running in Docker
- Uses relative paths in Docker (proxied through nginx)
- Uses `http://localhost:5000` for local development

## File Changes

### New Files Created:
- `frontend/nginx.conf` - Nginx configuration for proxy and static serving

### Modified Files:
- `docker-compose.yml` - Fixed port mapping, added health check, networking
- `backend/Dockerfile` - Added curl for health check
- `frontend/Dockerfile` - Added nginx config handling
- `frontend/scripts/api.js` - Auto-detect backend URL

## Build & Run

### Option 1: Full Stack Docker (Recommended)

```bash
# Build and start
docker-compose up --build

# In another terminal, test:
curl http://localhost:5000/
curl http://localhost:3000

# Stop
docker-compose down
```

### Option 2: Build Only (Don't Start)

```bash
docker-compose build

# Then run:
docker-compose up
```

### Option 3: Rebuild Specific Service

```bash
# Rebuild backend only
docker-compose build backend

# Rebuild frontend only
docker-compose build frontend

# Then start
docker-compose up
```

## Verify It Works ✅

### Check Backend Health:
```bash
# Should return: {"message":"native-language-id backend running"}
curl http://localhost:5000/
```

### Check Frontend Loads:
```bash
# Should return HTML content
curl http://localhost:3000/

# Or open in browser:
# http://localhost:3000
```

### Check Logs:
```bash
# View all logs
docker-compose logs

# View backend logs only
docker-compose logs backend

# View frontend logs only
docker-compose logs frontend

# Follow logs in real-time
docker-compose logs -f
```

### Check Running Containers:
```bash
docker ps

# Should show:
# native-language-backend (port 5000)
# native-language-frontend (port 3000)
```

## Troubleshooting

### Issue: "Port 3000 already in use"
```bash
# Find process on port 3000
lsof -i :3000

# Kill it
kill -9 <PID>

# Or use different port in docker-compose.yml:
# ports:
#   - '3001:80'
```

### Issue: "Backend not responding"
```bash
# Check backend logs
docker-compose logs backend

# Check if backend is healthy
curl http://localhost:5000/

# If not starting, rebuild:
docker-compose down
docker-compose build --no-cache backend
docker-compose up
```

### Issue: "Frontend can't connect to backend"
1. Check that both services are running: `docker ps`
2. Check logs: `docker-compose logs frontend`
3. Frontend should auto-detect Docker environment
4. Health check must pass for frontend to start

### Issue: "Build fails with 'model not found'"
- This is normal - backend uses dummy predictions if model missing
- App still works without a trained model
- Check backend logs for warning but continue anyway

### Clear Everything & Start Fresh:
```bash
# Stop all containers
docker-compose down

# Remove volumes (if needed)
docker-compose down -v

# Remove images (if needed)
docker image rm native-language-backend native-language-frontend

# Start fresh
docker-compose up --build
```

## Network Communication

### Frontend → Backend (Inside Docker):
```
nginx (port 80)
  ↓ (relative path /predict/)
nginx proxy (forwards to backend:8000)
  ↓
backend service (port 8000 internally)
```

### Local Development (No Docker):
```
Frontend (http://localhost:8000)
  ↓ (POST /predict/)
Backend (http://localhost:5000)
```

## Environment Variables

Automatically set in docker-compose.yml:

- `MODEL_PATH=/app/../ml/saved_models/cnn_bn_final.pt` - Backend
- `BACKEND_URL=http://backend:8000` - Frontend (for reference)

## Performance Tips

- Use `docker-compose up --build` only when dependencies change
- Use `docker-compose up` for subsequent runs (much faster)
- Add `-d` flag to run in background: `docker-compose up -d`
- View logs with: `docker-compose logs -f`

## Production Notes

For production, consider:
- Use specific Python version pins in requirements.txt
- Add restart policy to services
- Use health checks with longer timeouts
- Mount volumes for logs
- Use .dockerignore to exclude unnecessary files
- Use multi-stage builds to reduce image size

## Cleanup

```bash
# Stop and remove containers
docker-compose down

# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Full cleanup (be careful!)
docker system prune -a
```

## Testing Inside Docker

### Access Backend Container:
```bash
docker exec -it native-language-backend bash
# Inside container:
curl http://localhost:8000/
python -m pytest  # If tests exist
```

### Access Frontend Container:
```bash
docker exec -it native-language-frontend bash
# Inside container:
ls -la /usr/share/nginx/html
nginx -t  # Test nginx config
```

## Next Steps

1. ✅ Ensure Docker is installed: `docker --version && docker-compose --version`
2. ✅ Run: `docker-compose up --build`
3. ✅ Wait for services to start (check logs)
4. ✅ Test: `curl http://localhost:5000/` and `http://localhost:3000`
5. ✅ Open browser: http://localhost:3000
6. ✅ Test recording and predictions
7. ✅ Check console (F12) for any errors
