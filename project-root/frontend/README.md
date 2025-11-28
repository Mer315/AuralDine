# AuralDine Frontend

React Native mobile application for accent recognition and dining recommendations.

## Features

- Real-time audio recording
- Accent detection
- Restaurant recommendations based on accent
- Clean and intuitive UI

## Setup

### Prerequisites
- Node.js 16+
- React Native CLI
- Android Studio (for Android) or Xcode (for iOS)

### Installation

```bash
npm install
```

### Running

#### iOS
```bash
npm run ios
```

#### Android
```bash
npm run android
```

#### Development Server
```bash
npm start
```

## Project Structure

- `src/components/` - Reusable UI components
- `src/screens/` - Application screens
- `src/api/` - API integration
- `src/assets/` - Images, icons, etc.
- `src/styles/` - Global styles and theme

## Configuration

Create a `.env` file in the project root:

```env
API_BASE_URL=http://localhost:8000/api
```

## Building

### Android
```bash
cd android && ./gradlew assembleRelease
```

### iOS
```bash
cd ios && pod install
xcodebuild -scheme AuralDine -configuration Release
```
