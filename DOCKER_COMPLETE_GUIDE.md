# Complete Docker Deployment Guide

## Overview

Your AuralDine application is now fully configured for Docker deployment. All components work together seamlessly:

- **Backend**: FastAPI server on port 8000 (exposed as 5000 externally)
- **Frontend**: Nginx server on port 80 (exposed as 3000 externally)
- **Networking**: Both services communicate via Docker bridge network
- **Health Checks**: Automatic startup synchronization

## Prerequisites

- Docker Desktop installed and running
- PowerShell or Command Prompt
- Internet connection (for Docker image pulls)

## Quick Start (One Command)

From the `AuralDine` folder, run:

```bash
docker-compose up --build
```

This single command will:
1. Build backend image (Python + dependencies)
2. Build frontend image (Nginx + static files)
3. Create app-network bridge
4. Start backend container
5. Run backend health check
6. Start frontend container (waits for backend to be healthy)
7. Make application available at http://localhost:3000

## Detailed Build Process

### Step 1: Navigate to Project Directory

```powershell
cd "C:\Users\Admin\OneDrive\Documents\AuralDine"
```

### Step 2: Build Images

First, build without starting (optional, if you want to see build output separately):

```bash
docker-compose build --no-cache
```

**Expected output:**
```
Building backend
...
Successfully tagged auraldine-backend:latest

Building frontend
...
Successfully tagged auraldine-frontend:latest
```

### Step 3: Start Services

```bash
docker-compose up
```

**Expected output:**
```
Creating app-network
Creating native-language-backend
Creating native-language-frontend

native-language-backend  | INFO:     Uvicorn running on http://0.0.0.0:8000
native-language-frontend | 2024/XX/XX XX:XX:XX [notice] worker process started: XX
```

### Step 4: Verify Everything Started

**Option A: Check containers (while services are running)**

In a new PowerShell window:

```bash
docker ps
```

Should show both containers:
```
CONTAINER ID   IMAGE                              STATUS
abc123         auraldine:backend                  Up X seconds (healthy)
def456         auraldine:frontend                 Up X seconds
```

**Option B: Check service health**

```bash
docker-compose ps
```

Backend status should show `(healthy)` after ~40 seconds.

### Step 5: Access Application

Open browser and navigate to:
```
http://localhost:3000
```

## What Happens During Startup

### Backend Container Startup (40-60 seconds)

1. **Image Build** (~20s):
   - Pulls Python 3.10 slim image
   - Installs system dependencies: libsndfile1, ffmpeg, build-essential, curl
   - Copies requirements.txt
   - Installs Python packages: FastAPI, PyTorch, Librosa, etc.
   - Copies application code
   - Tag as `auraldine-backend:latest`

2. **Container Launch** (~5s):
   - Starts Uvicorn server on 0.0.0.0:8000
   - Listens for health check requests

3. **Health Check Running** (~40s):
   - Every 30 seconds: runs `curl -f http://localhost:8000/`
   - Retries up to 3 times with 10s timeout
   - Docker waits 40s before first check (start_period)
   - Status changes from "starting" to "healthy"

### Frontend Container Startup (10-20 seconds)

1. **Image Build** (~10s):
   - Pulls nginx:alpine image (5MB)
   - Copies custom nginx.conf (backend proxy configuration)
   - Copies frontend files (HTML, CSS, JS)
   - Tag as `auraldine-frontend:latest`

2. **Container Launch** (~5s):
   - Starts nginx daemon
   - Listens on 0.0.0.0:80

3. **Proxy Setup** (Instant):
   - Nginx automatically routes `/predict/` requests to backend:8000
   - Routes `/api/` requests to backend:8000
   - Serves static HTML/CSS/JS files

### Application Ready

Total time from `docker-compose up` to fully functional: **2-3 minutes**

## Verifying Each Component

### 1. Backend Health

```bash
curl http://localhost:5000/
```

Should return some response (even a 404 is fine - means backend is running)

### 2. Frontend Loading

Open http://localhost:3000 in browser. Should show:
- Brown/orange themed page
- "Try AuralDine" button
- Region selection cards (Mumbai, Delhi, Bangalore, etc.)
- Hero section with animations

### 3. Recording Functionality

1. Click "Try AuralDine"
2. Click "Allow" when browser asks for microphone permission
3. Click "🎤 Start Recording"
4. Speak for 5 seconds
5. Recording should stop automatically
6. Results should appear (either mock or real predictions)

### 4. Backend Processing

Check backend logs:

```bash
docker-compose logs backend
```

Look for lines like:
```
INFO:     "POST /predict/ HTTP/1.1" 200
```

## Stopping Services

### Stop (containers remain):

```bash
docker-compose stop
```

### Remove (containers destroyed):

```bash
docker-compose down
```

### Remove with volumes:

```bash
docker-compose down -v
```

### Remove images:

```bash
docker rmi auraldine-backend auraldine-frontend
```

## Troubleshooting

### Issue: "docker-compose: command not found"

**Solution**: Docker Desktop includes docker-compose. Ensure Docker Desktop is running.

### Issue: Port 5000 or 3000 already in use

**Solution A**: Stop conflicting services
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Solution B**: Change ports in docker-compose.yml
```yaml
backend:
  ports:
    - '5001:8000'  # Changed from 5000:8000
frontend:
  ports:
    - '3001:80'    # Changed from 3000:80
```

Then access at http://localhost:3001

### Issue: Backend shows "unhealthy" after 2 minutes

**Check logs:**
```bash
docker-compose logs backend
```

Look for Python/Librosa errors. Usually means model file not found.

**Verify model file exists:**
```bash
ls "ml/saved_models/"
```

Should show `cnn_bn_final.pt`

### Issue: Frontend can't reach backend (buttons don't work)

**Check nginx logs:**
```bash
docker-compose logs frontend
```

**Verify backend is actually running:**
```bash
docker-compose logs backend | tail -5
```

**Verify network:**
```bash
docker network inspect app-network
```

Should show both backend and frontend connected.

### Issue: Browser shows blank page

**Check browser console** (F12 → Console tab):
- Look for red errors
- Common: CORS, network errors, missing files

**Clear browser cache:**
```
Ctrl+Shift+Delete → Clear all time
```

Then refresh page.

### Issue: "Building wheel for librosa..." takes forever

This is normal! Librosa can take 5-10 minutes to compile on first build. 
Be patient and let it finish.

**To see progress:**
```bash
docker-compose build --no-cache --progress=plain
```

## Advanced Operations

### Rebuild from scratch (clear cache)

```bash
docker-compose down -v
docker system prune -a --volumes
docker-compose up --build
```

### View real-time logs from both services

```bash
docker-compose logs -f
```

### View only backend logs

```bash
docker-compose logs -f backend
```

### View only frontend logs

```bash
docker-compose logs -f frontend
```

### Execute command in running container

```bash
# Python shell in backend
docker-compose exec backend python -c "import librosa; print('OK')"

# Check frontend files
docker-compose exec frontend ls -la /usr/share/nginx/html
```

### Rebuild specific service only

```bash
docker-compose build --no-cache backend
```

or

```bash
docker-compose build --no-cache frontend
```

## Performance Tuning

### Reduce image size

The `.dockerignore` file already excludes:
- `__pycache__/` directories
- `.git` folder
- `node_modules/`
- `*.pyc` files

### Enable BuildKit for faster builds

```bash
set DOCKER_BUILDKIT=1
docker-compose build --no-cache
```

### Use existing images without rebuild

```bash
docker-compose up
```

(without `--build` flag)

## Production Considerations

### Current Setup (Development)

- Health check interval: 30s
- Start period: 40s
- Debug logs visible
- Microphone access allowed
- Relative paths for API calls

### For Production

1. **Use health check endpoint**:
   ```yaml
   test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
   ```

2. **Add restart policy**:
   ```yaml
   restart_policy:
     condition: on-failure
     delay: 5s
     max_attempts: 3
   ```

3. **Use environment variables**:
   ```yaml
   environment:
     - LOG_LEVEL=info
     - MODEL_PATH=/app/ml/saved_models/cnn_bn_final.pt
   ```

4. **Add resource limits**:
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '1'
         memory: 2G
   ```

## Next Steps

1. ✅ Run: `docker-compose up --build`
2. ✅ Wait for both services to start (2-3 minutes)
3. ✅ Open: http://localhost:3000
4. ✅ Test microphone recording
5. ✅ Test accent detection
6. ✅ Check backend logs for any errors

## Quick Reference

| Command | Purpose |
|---------|---------|
| `docker-compose up --build` | Build and start all services |
| `docker-compose up` | Start services (use existing images) |
| `docker-compose down` | Stop and remove containers |
| `docker-compose logs` | View all logs |
| `docker-compose ps` | Show container status |
| `docker ps` | Show all running containers |
| `docker-compose build` | Build images without starting |
| `docker-compose restart` | Restart all services |

## Support

If you encounter issues:

1. Check `TROUBLESHOOTING.md` for detailed solutions
2. Review `DOCKER_BUILD.md` for step-by-step guide
3. Check logs: `docker-compose logs`
4. Verify Docker Desktop is running
5. Ensure all files are present in the AuralDine folder

---

**Status**: ✅ Docker configuration complete and ready for deployment

**Last Updated**: $(date)

**Tested On**: Docker Desktop (Windows)
