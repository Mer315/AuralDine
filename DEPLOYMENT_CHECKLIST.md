# AuralDine Docker Deployment Checklist

## Pre-Deployment Verification

### System Requirements
- [ ] Docker Desktop installed (Windows)
- [ ] Docker Desktop running (check system tray)
- [ ] At least 4GB RAM available
- [ ] At least 5GB free disk space
- [ ] PowerShell or Command Prompt available

### Project Structure
- [ ] `backend/` folder exists with Dockerfile and requirements.txt
- [ ] `frontend/` folder exists with Dockerfile, nginx.conf, and HTML/CSS/JS files
- [ ] `ml/saved_models/cnn_bn_final.pt` exists (model file)
- [ ] `docker-compose.yml` present in project root
- [ ] `.dockerignore` present in project root

### Configuration Files
- [ ] `backend/Dockerfile` - Contains curl in dependencies
- [ ] `frontend/Dockerfile` - Properly copies nginx.conf
- [ ] `frontend/nginx.conf` - Routes /predict/ to backend:8000
- [ ] `docker-compose.yml` - Port mapping 5000:8000 for backend, 3000:80 for frontend
- [ ] `frontend/scripts/api.js` - Contains auto-environment detection

### All Required Files Present
```
✓ backend/
  ✓ Dockerfile
  ✓ requirements.txt
  ✓ app/
    ✓ __init__.py
    ✓ main.py
    ✓ routes.py
    ✓ config.py
    ✓ model_service.py
    ✓ utils.py
✓ frontend/
  ✓ Dockerfile
  ✓ nginx.conf
  ✓ index.html
  ✓ style.css
  ✓ scripts/
    ✓ api.js
    ✓ recorder.js
    ✓ ui.js
✓ ml/
  ✓ saved_models/
    ✓ cnn_bn_final.pt
✓ docker-compose.yml
✓ .dockerignore
```

## Deployment Steps

### Step 1: Prepare Environment
- [ ] Open PowerShell or Command Prompt
- [ ] Navigate to `C:\Users\Admin\OneDrive\Documents\AuralDine`
- [ ] Command: `cd "C:\Users\Admin\OneDrive\Documents\AuralDine"`

### Step 2: Check Docker Status
- [ ] Docker Desktop is running
- [ ] Command: `docker --version` (should show version number)
- [ ] Command: `docker-compose --version` (should show version number)

### Step 3: Build and Start Services
- [ ] Run: `docker-compose up --build`
- [ ] Wait for output to stabilize (2-3 minutes)
- [ ] Look for: `native-language-backend | INFO: Uvicorn running on http://0.0.0.0:8000`
- [ ] Look for: `native-language-frontend | worker process started`

### Step 4: Verify Backend Health
- [ ] Open new PowerShell window
- [ ] Command: `docker-compose ps`
- [ ] Verify backend status shows `(healthy)` with checkmark
- [ ] Command: `curl http://localhost:5000/` (should get a response)

### Step 5: Verify Frontend
- [ ] Open browser (Chrome, Firefox, Edge)
- [ ] Navigate to: `http://localhost:3000`
- [ ] Page should load with brown/orange theme
- [ ] Should see "Try AuralDine" button
- [ ] Should see region selection cards

### Step 6: Test Microphone (Browser Permissions)
- [ ] Click "Try AuralDine"
- [ ] Browser should ask for microphone permission
- [ ] Click "Allow"
- [ ] Click "🎤 Start Recording"
- [ ] Speak for 3-5 seconds
- [ ] Recording should stop automatically after 5 seconds

### Step 7: Test Submission
- [ ] After recording stops, click "Analyze Accent"
- [ ] Results should appear below (may be mock or real)
- [ ] Check browser console (F12) for any red errors
- [ ] If results appear, backend is working!

### Step 8: Verify Logging
- [ ] Go back to terminal with `docker-compose up` running
- [ ] Look for: `"POST /predict/ HTTP/1.1" 200` entries
- [ ] These indicate successful backend processing

### Step 9: Check Logs for Errors
- [ ] New terminal: `docker-compose logs backend` (check for Python errors)
- [ ] New terminal: `docker-compose logs frontend` (check for nginx errors)
- [ ] Should only see INFO and DEBUG messages, no ERROR or CRITICAL

## Testing Checklist

### Functionality Tests
- [ ] Frontend loads at http://localhost:3000
- [ ] Page displays brown/orange theme correctly
- [ ] All buttons are clickable
- [ ] Microphone recording works
- [ ] Recording stops after 5 seconds
- [ ] Results display properly
- [ ] No console errors in browser (F12)

### Backend Tests
- [ ] Backend responds to health checks
- [ ] Backend processes audio files
- [ ] Returns predictions in correct format
- [ ] Handles errors gracefully

### Docker Tests
- [ ] Both containers start without errors
- [ ] Backend shows as "healthy" within 1 minute
- [ ] Frontend waits for backend before starting
- [ ] Services communicate via Docker network
- [ ] Port mappings work (5000 and 3000 accessible)

### Performance Tests
- [ ] Initial build completes in under 10 minutes
- [ ] Services start in under 3 minutes
- [ ] Audio processing takes less than 10 seconds
- [ ] No memory errors or crashes

## Troubleshooting Quick Reference

### If Backend Won't Start
```powershell
# Check logs
docker-compose logs backend

# Look for: Python errors, missing dependencies, permission issues

# Solution: Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache backend
docker-compose up
```

### If Frontend Can't Reach Backend
```powershell
# Check nginx configuration
docker-compose exec frontend cat /etc/nginx/conf.d/default.conf

# Check backend is actually running
docker-compose logs backend | Select-Object -Last 5

# Verify network
docker network inspect app-network

# Solution: Restart both services
docker-compose restart
```

### If Port is Already in Use
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual PID)
taskkill /PID <PID> /F

# Or change port in docker-compose.yml to 5001:8000 and 3001:80
```

### If Build Takes Too Long
```
This is normal! Librosa compilation can take 5-10 minutes on first build.
Let it complete. Subsequent builds will use cache.
```

### If "Docker daemon is not running"
```powershell
# Open Docker Desktop from Start menu
# Wait 30 seconds for daemon to start
# Retry command
```

## Post-Deployment

### Keep Services Running
- [ ] Leave terminal with `docker-compose up` running
- [ ] Or run in background: `docker-compose up -d`

### Access Points
- [ ] Frontend: `http://localhost:3000`
- [ ] Backend API: `http://localhost:5000`

### Check Logs Anytime
```powershell
# All logs
docker-compose logs

# Real-time logs
docker-compose logs -f

# Specific service
docker-compose logs backend
docker-compose logs frontend
```

### Stop Services
```powershell
# Stop (containers remain, can restart)
docker-compose stop

# Stop and remove
docker-compose down

# Stop, remove, and delete volumes
docker-compose down -v
```

## Success Indicators

✅ **Deployment Successful When:**
- [ ] `docker-compose up --build` completes without errors
- [ ] Both containers show as "running" in `docker ps`
- [ ] Backend shows as "(healthy)" in `docker-compose ps`
- [ ] Frontend accessible at http://localhost:3000
- [ ] Browser console has no red errors
- [ ] Microphone button works
- [ ] Recording functionality works
- [ ] Results display (even if mock data)

## Disaster Recovery

### If Everything Goes Wrong

```powershell
# Complete clean slate
docker-compose down -v
docker system prune -a --volumes -f
docker-compose up --build
```

This will:
1. Stop and remove all containers
2. Delete all volumes
3. Remove all unused images
4. Clear Docker system
5. Fresh build from scratch

Then re-verify with checklist above.

## Performance Expectations

| Operation | Expected Time |
|-----------|---------------|
| Initial build | 5-10 minutes |
| Subsequent starts | 2-3 minutes |
| Backend health check | ~40 seconds |
| Audio processing | < 10 seconds |
| Page load | < 1 second |

## Documentation Reference

| File | Purpose |
|------|---------|
| `DOCKER_COMPLETE_GUIDE.md` | Comprehensive deployment guide |
| `TROUBLESHOOTING.md` | Detailed troubleshooting guide |
| `QUICK_START.md` | Quick reference |
| `FIXED_ISSUES.md` | Summary of fixes |
| `README.md` | Project overview |
| `docker-commands.bat` | Easy command menu |

---

**Last Updated**: $(date)

**Status**: ✅ Ready for Deployment

**Next Action**: Run `docker-compose up --build` and follow the testing checklist
