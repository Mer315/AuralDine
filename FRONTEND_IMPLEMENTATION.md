# AccentCuisine AI - Frontend Implementation Complete

## Overview
The frontend has been successfully rebuilt to match the Figma design from the "Dynamic Front Page Design" folder. The application now features a brown/orange color scheme with complete accent detection functionality.

## Project Structure
```
frontend/
├── index.html              # Main HTML file with templates
├── styles.css              # Custom CSS animations and styling
├── script.js              # [Old file - can be removed]
├── style.css              # [Old file - can be removed]
├── scripts/
│   ├── recorder.js        # Audio recording and visualization
│   ├── api.js             # Backend communication and accent data
│   └── ui.js              # Page navigation and state management
├── Dockerfile
└── index.html.backup      # Backup of old version
```

## Color Scheme (Extracted from Design)
- **Background**: `#4A2C1A` (Dark Brown)
- **Primary**: `#F97316` (Orange)
- **Secondary**: `#FBBF24` (Amber)
- **Text**: `#FFF8E7` (Cream)
- **Dark**: `#1C1410` (Charcoal)
- **Medium**: `#5A3B25` (Medium Brown)
- **Light**: `#2A1A0F` (Light Brown)

## Features Implemented

### 1. Home Page (`homePageTemplate`)
- **Hero Section**: "Where language meets flavor" headline with orange gradient
- **Animated Regions**: 6 orbiting region badges (Mumbai, Delhi, Bangalore, Kolkata, Chennai, Hyderabad)
- **Features Grid**: Voice Analysis, Regional Mapping, Cuisine Match
- **Background Animations**: Floating elements, rotating mandala patterns, pulsing effects
- **Navigation**: Listen button to access detector

### 2. Accent Detector Page (`accentDetectorTemplate`)
- **Microphone Interface**: Large 160px button with pulsing effects
- **Recording Status**: Real-time feedback with auto-stop after 5 seconds
- **Results Display**: 
  - Detected language and confidence score
  - Accent characteristics tags
  - Detected region
  - Cuisine recommendations
- **Cuisine Cards**: Shows cuisine name, description, and dish suggestions
- **Navigation**: Back to home and try again buttons

### 3. JavaScript Modules

#### `recorder.js` - Audio Recording
- MediaRecorder API integration
- Web Audio API for frequency analysis
- Real-time audio level monitoring
- 5-second recording timeout
- WAV/WebM audio format support

#### `api.js` - Backend Integration
- Accent database with 6 Indian regions:
  - Mumbai (Marathi)
  - Delhi (Hindi/North Indian)
  - Bangalore (Kannada)
  - Kolkata (Bengali)
  - Chennai (Tamil)
  - Hyderabad (Telugu/Urdu)
- Cuisine recommendations with dishes
- Backend communication methods
- Mock data fallback for testing

#### `ui.js` - State Management
- Page navigation (Home ↔ Detector)
- Event handler setup
- Results display logic
- Audio level visualization during recording
- Error handling and user feedback

### 4. CSS Animations
- **Float**: Smooth vertical floating (±20px)
- **Rotate**: Continuous rotation (360°, 20s)
- **Pulse Scale**: Pulsing scale effect (1 → 1.1 → 1)
- **Slide**: Entrance animations
- **Orbit**: Region badges orbiting animation
- **Stagger**: Delayed animations for sequential reveal

## Color Mapping for Tailwind
```
bg-[#4A2C1A]    - Background
bg-[#1C1410]    - Dark sections
bg-[#5A3B25]    - Medium sections
bg-[#2A1A0F]    - Light sections
text-[#FFF8E7]  - Primary text
text-[#D4C4B0]  - Secondary text
text-orange-500 - Orange accents
text-amber-500  - Amber accents
```

## How to Run

### Option 1: Local File (Development)
1. Open `frontend/index.html` in a web browser
2. App works in demo mode (mocked predictions)

### Option 2: With Backend Server
1. Ensure backend is running on `http://localhost:5000`
2. Backend should expose:
   - `POST /predict` - Analyze audio and return accent prediction
   - `GET /dish-info` - Get cuisine information by region

### Option 3: Docker (Recommended)
```bash
cd AuralDine
docker-compose up
```

## Key Integration Points

### With Backend
1. **Audio Upload**: POST multipart form-data to `/predict`
2. **Response Format**:
   ```json
   {
     "region": "Mumbai",
     "language": "Marathi",
     "confidence": 0.92,
     "characteristics": ["Nasal vowels", "Retroflex consonants", "Rhythm variation"]
   }
   ```

### Browser APIs Used
- **MediaRecorder API**: Audio recording
- **Web Audio API**: Frequency analysis
- **Fetch API**: Backend communication
- **DOM API**: Dynamic content rendering
- **Template API**: HTML templates

## Accent Database (Built-in)

Each region includes:
- **Language**: Detected language/dialect
- **Characteristics**: Unique accent features
- **Cuisine**: Regional food profile with 6 signature dishes
- **Confidence**: Baseline detection confidence

## Testing Checklist
- ✅ Home page loads with animations
- ✅ Region badges orbit around center microphone
- ✅ Features section displays correctly
- ✅ Listen button navigates to detector page
- ✅ Microphone button can be clicked
- ✅ Recording works and stops after 5 seconds
- ✅ Results display with mock data
- ✅ Cuisine recommendations show correctly
- ✅ Try Again button resets interface
- ✅ Back to Home button returns to home page
- ✅ Color scheme matches design (#4A2C1A brown/orange)
- ✅ Animations run smoothly

## Browser Compatibility
- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ⚠️ Web Audio API may require user gesture
- Mobile: ✅ Responsive design supported

## Next Steps
1. Connect to working backend for real predictions
2. Add audio playback functionality
3. Implement user analytics
4. Add PWA support
5. Optimize for mobile devices
6. Add accessibility features (ARIA labels)

## Files to Clean Up
- `frontend/script.js` - Old implementation
- `frontend/style.css` - Old styling
- `frontend/index.html.backup` - Backup file

## Notes
- App uses Tailwind CSS CDN (no build step needed)
- Microphone requires HTTPS or localhost
- Recording auto-stops at 5 seconds
- All animations use CSS keyframes for performance
- Fallback to mock data if backend unavailable
