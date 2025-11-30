# 🚀 AuralDine - Quick Start Guide

## What Was Fixed ✅

1. **Backend Endpoint** - Now uses `/predict/` (with trailing slash)
2. **Response Mapping** - State codes converted to region names automatically
3. **Button Handlers** - Added error checking and logging
4. **UI Initialization** - Safe class checking before instantiation
5. **Microphone Errors** - Better error messages for permission issues

---

## Run Backend (Required for Real Predictions)

### Method 1: Direct Python
```bash
# Navigate to AuralDine folder
cd backend

# Install dependencies (first time only)
pip install -r requirements.txt

# Start server
python -m uvicorn app.main:app --reload --port 5000

# Should show:
# INFO:     Uvicorn running on http://127.0.0.1:5000
```

### Method 2: Docker
```bash
cd ..
docker-compose up

# Backend will be at http://localhost:5000
# Frontend will be at http://localhost:3000 or :8080
```

---

## Run Frontend

### Method 1: Direct Browser (Demo Mode - Works Without Backend)
```
Open: file:///c:/Users/Admin/OneDrive/Documents/AuralDine/frontend/index.html
```

### Method 2: Local HTTP Server
```bash
# Using Python
cd frontend
python -m http.server 8000

# Then open: http://localhost:8000
```

### Method 3: Using Node.js
```bash
cd frontend
npx http-server . -p 8000

# Then open: http://localhost:8000
```

---

## Test It Works ✅

### 1. Check Backend Running (Terminal)
```bash
curl http://localhost:5000/
# Should return: {"message":"native-language-id backend running"}
```

### 2. Check Frontend Loads (Browser)
- Open http://localhost:8000 (or your frontend URL)
- You should see the brown/orange AccentCuisine AI interface
- "Where language meets flavor" headline
- Orange microphone button in the center

### 3. Test Buttons (Browser Console - F12)
- Click "Listen" button
- Check Console tab - should see: `Get Started clicked` or `Header Listen clicked`
- Click microphone - should see: `Mic button clicked`
- If you see these messages, buttons are working ✅

### 4. Test Recording
- Click microphone button
- Allow microphone access (browser will ask)
- Should say "Recording..." for up to 5 seconds
- Results will show with detected region and cuisine

---

## Troubleshooting

### ❌ "Backend connection refused"
```bash
# Check if backend is running:
curl http://localhost:5000/

# If not, start it:
cd backend
python -m uvicorn app.main:app --reload --port 5000
```

### ❌ "Microphone not accessible"
1. Check browser permissions (Settings → Privacy → Microphone)
2. Make sure microphone physically works
3. Try allowing permission when browser asks
4. If still blocked, use mock data (app works without real audio)

### ❌ "Results show wrong data"
1. Backend might not have model loaded
2. This is normal - app uses dummy predictions as fallback
3. Train model for better accuracy (see `ml/` folder)

### ❌ "Buttons don't respond"
1. Open browser console: Press `F12`
2. Go to Console tab
3. Click button and look for error messages
4. Report errors in console

---

## Full Stack - Both Backend & Frontend

### Terminal 1 - Backend
```bash
cd AuralDine/backend
python -m uvicorn app.main:app --reload --port 5000
```

### Terminal 2 - Frontend
```bash
cd AuralDine/frontend
python -m http.server 8000
```

### Browser
```
http://localhost:8000
```

---

## Environment Variables (Optional)

Create `.env` file in `backend/` folder:
```
MODEL_PATH=/path/to/model.pt
DEVICE=cpu  # or 'cuda' if GPU available
```

---

## File Structure

```
AuralDine/
├── backend/              # FastAPI server
│   ├── app/
│   │   ├── main.py      # FastAPI app
│   │   ├── routes.py    # Endpoints (/predict/)
│   │   └── model_service.py  # Model loading
│   ├── requirements.txt  # Dependencies
│   └── Dockerfile
├── frontend/            # Web interface
│   ├── index.html       # HTML templates
│   ├── styles.css       # Animations
│   └── scripts/
│       ├── recorder.js  # Audio recording
│       ├── api.js       # Backend communication
│       └── ui.js        # Page navigation
├── ml/
│   └── saved_models/
│       └── cnn_bn_final.pt  # Model file
├── docker-compose.yml   # Full stack setup
└── TROUBLESHOOTING.md   # Detailed help
```

---

## Console Debugging

### Enable Full Logging
All console messages are already set up. Just check:
1. Press `F12` in browser
2. Go to **Console** tab
3. You'll see:
   - ✓ `Button clicked` - Shows buttons work
   - ✓ `Recording started` - Microphone works
   - ✓ `Backend response: {...}` - API works
   - ✗ `Error: ...` - Shows what failed

---

## API Endpoints

### Backend Endpoints:
```
GET  /               # Health check
POST /predict/       # Analyze audio
GET  /dish-info      # Get cuisine info
```

### Frontend Modules:
```
scripts/recorder.js  - Audio recording with Web Audio API
scripts/api.js       - Backend calls + region mapping
scripts/ui.js        - Page navigation + button handlers
```

---

## Demo Data (No Backend Needed)

Frontend has built-in demo data for 6 regions:
- 🔴 **Mumbai** - Marathi cuisine
- 🟠 **Delhi** - Mughlai cuisine
- 🟡 **Bangalore** - Kannada cuisine
- 🟢 **Kolkata** - Bengali cuisine
- 🔵 **Chennai** - Tamil cuisine
- 🟣 **Hyderabad** - Hyderabadi cuisine

Click "Listen" → "Try Again" to test different regions.

---

## Quick Commands

```bash
# Test backend setup
python test_backend.py

# Start everything with Docker
docker-compose up

# Kill stuck process on port 5000 (Windows)
taskkill /F /PID <pid>

# Check what's running on port 5000 (Linux/Mac)
lsof -i :5000

# View backend logs in Docker
docker logs auraldin-backend
```

---

## Next Steps

1. ✅ Start backend: `python -m uvicorn app.main:app --reload --port 5000`
2. ✅ Start frontend: `python -m http.server 8000` (in frontend folder)
3. ✅ Open browser: http://localhost:8000
4. ✅ Test buttons and recording
5. ✅ Check console (F12) for any errors
6. ✅ If no errors, everything is working! 🎉

---

## Support

For detailed troubleshooting: See `TROUBLESHOOTING.md`
For implementation details: See `FRONTEND_IMPLEMENTATION.md`
