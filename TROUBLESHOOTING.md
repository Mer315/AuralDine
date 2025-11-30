# AuralDine - Quick Fix & Troubleshooting Guide

## Issues Fixed

### 1. ✅ Backend Endpoint Mismatch
- **Problem**: Frontend was calling `/predict` but backend endpoint is `/predict/` (with trailing slash)
- **Solution**: Updated `api.js` to use `/predict/` and map response format from backend

### 2. ✅ Response Format Mismatch  
- **Problem**: Backend returns `state` (e.g., "andhrapradesh") but frontend expects `region` (e.g., "Mumbai")
- **Solution**: Added helper functions to convert backend state codes to region names and map languages

### 3. ✅ Button Event Handlers Not Working
- **Problem**: Null reference errors when trying to add event listeners
- **Solution**: Added error checking for element existence before adding listeners, with console warnings

### 4. ✅ UI Module Initialization
- **Problem**: Scripts might not be loaded when UIManager constructor runs
- **Solution**: Added null checks for AudioRecorder and AccentAPI classes before instantiation

### 5. ✅ Microphone Access Issues
- **Problem**: Better error handling needed for microphone permission errors
- **Solution**: Added detailed error messages and fallback to mock predictions

## How to Run Everything

### Option 1: Backend Only (For Testing)

```bash
# From AuralDine directory
cd backend

# Install dependencies (one time)
pip install -r requirements.txt

# Run the backend server
python -m uvicorn app.main:app --reload --port 5000

# In another terminal, test it:
curl -X GET http://localhost:5000/
# Should return: {"message":"native-language-id backend running"}
```

### Option 2: Frontend Only (Demo Mode with Mock Data)

```bash
# Simply open in browser:
# file:///c:/Users/Admin/OneDrive/Documents/AuralDine/frontend/index.html
# Or use a local server:

# If you have Python installed:
cd frontend
python -m http.server 8000
# Open http://localhost:8000 in browser

# Or with Node.js:
npx http-server frontend/ -p 8000
```

### Option 3: Full Stack with Docker (Recommended)

```bash
# From AuralDine directory
docker-compose up

# Frontend: http://localhost:3000 (or http://localhost:8080)
# Backend: http://localhost:5000
```

### Option 4: Full Stack - Manual

**Terminal 1 - Start Backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload --port 5000
```

**Terminal 2 - Start Frontend Server:**
```bash
cd frontend
python -m http.server 8000
```

**Browser:**
Open http://localhost:8000 in your browser

## Debugging - Open Browser Console

1. Press `F12` in browser
2. Go to **Console** tab
3. Look for error messages
4. You'll see logs like:
   - `Get Started clicked` - button working
   - `Mic button clicked` - recording button working
   - `Backend response: {...}` - API call successful

## Common Issues & Solutions

### Issue: "Microphone not accessible"
- **Check**: Browser permissions (Settings → Privacy → Microphone)
- **Check**: HTTPS or localhost (browsers block microphone on http://non-localhost)
- **Check**: Microphone physically working
- **Solution**: Grant permission when browser asks, or use mock data mode

### Issue: "Backend connection refused"
- **Check**: Backend is running on port 5000
- **Check**: No firewall blocking port 5000
- **Check**: Frontend API URL is correct (should be `http://localhost:5000`)
- **Solution**: 
  ```bash
  # Test backend is running:
  curl http://localhost:5000/
  ```

### Issue: "Backend returns 404 or error"
- **Check**: Model file exists at correct path
- **Check**: All dependencies installed (`pip install -r requirements.txt`)
- **Solution**: Backend uses dummy predictions if model missing - still works!

### Issue: "Results not showing"
- **Check**: Browser console for errors (F12)
- **Check**: Network tab to see API response
- **Check**: Model/predictions are being generated (even with dummy model)
- **Solution**: Try recording again, check console for details

### Issue: Buttons not responding
- **Check**: Open browser console (F12)
- **Look for**: "Button not found" warnings
- **Solution**: Page might not have fully loaded - wait and try again

## Test Endpoints

### Test Backend is Running:
```bash
curl http://localhost:5000/
# Expected: {"message":"native-language-id backend running"}
```

### Test Audio Upload (with file):
```bash
# Create a dummy audio file or use real one
curl -X POST \
  -F "file=@audio_sample.wav" \
  http://localhost:5000/predict/

# Expected response:
# {"state":"andhrapradesh","confidence":0.85,"cuisines":[...]}
```

## File Changes Made

### Updated Files:
1. **frontend/scripts/ui.js** - Better error handling, button listeners
2. **frontend/scripts/api.js** - Fixed endpoint path, added state-to-region mapping
3. **frontend/scripts/recorder.js** - Already working, added console logs
4. **frontend/styles.css** - Already working
5. **frontend/index.html** - Already correct

### Created Files:
1. **test_backend.py** - Backend verification script
2. **TROUBLESHOOTING.md** - This file

## Performance Tips

- **Use Docker**: Simplest setup, all ports configured
- **Mock Mode**: Frontend works even without backend (uses demo data)
- **Check Logs**: Always check browser console (F12) for real errors
- **Test Offline**: Frontend can run completely offline
- **Background Process**: Run backend in tmux or screen for persistence

## API Response Format

Backend returns:
```json
{
  "state": "andhrapradesh",
  "confidence": 0.85,
  "cuisines": [
    {"name": "Hyderabadi Biryani", "price": "$$", "description": "..."}
  ]
}
```

Frontend converts to:
```json
{
  "region": "Hyderabad",
  "language": "Telugu/Urdu",
  "confidence": 0.85,
  "characteristics": ["Velar dominance", "Rhotic pronunciation", "Melodic rhythm"]
}
```

## Model Training Notes

- Current model path: `ml/saved_models/cnn_bn_final.pt`
- If model not found, backend returns random predictions
- States supported: andhrapradesh, gujarath, kerala, karnataka, jharkhand, tamilnadu
- App still works in demo mode without a trained model

## Next Steps

1. ✅ Verify backend starts without errors: `python -m uvicorn app.main:app --reload --port 5000`
2. ✅ Check browser console for initialization logs
3. ✅ Test buttons click and show feedback
4. ✅ Test microphone recording (may use mock data)
5. ✅ Check if results display correctly
6. ✅ Train model if needed for better predictions

## Support Commands

```bash
# Test Python environment
python --version  # Should be 3.8+

# Test backend dependencies
cd backend
pip list | grep -E "fastapi|torch|librosa"

# Run backend test script
cd ..
python test_backend.py

# Check open ports
netstat -tulpn | grep 5000  # Linux/Mac
netstat -ano | findstr :5000  # Windows

# Kill process on port 5000 if stuck
# Windows:
taskkill /F /PID <PID>
# Linux/Mac:
lsof -ti:5000 | xargs kill -9
```
