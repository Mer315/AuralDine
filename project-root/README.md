# AuralDine

AI-powered accent recognition system with intelligent dining recommendations.

## Project Overview

AuralDine combines machine learning and mobile technology to:
- Recognize user accents from audio input
- Provide personalized restaurant recommendations based on accent and cuisine preferences
- Deliver a seamless user experience across web and mobile

## Project Structure

```
project-root/
├── backend/          # FastAPI backend with ML models
├── frontend/         # React Native mobile app
├── deployment/       # Docker and deployment configs
└── README.md         # This file
```

## Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Backend runs on `http://localhost:8000`

### Frontend

```bash
cd frontend
npm install
npm run android  # or npm run ios
```

### Docker

```bash
cd deployment
docker-compose up -d
```

## Features

- **Accent Detection**: CNN model using MFCC features
- **Audio Processing**: Real-time audio capture and preprocessing
- **Recommendations**: Intelligent dining suggestions
- **Mobile First**: React Native cross-platform app
- **API-Driven**: RESTful FastAPI backend

## API Endpoints

- `GET /api/health` - Health check
- `POST /api/predict` - Predict accent from audio file

## Technology Stack

### Backend
- FastAPI - Web framework
- PyTorch - Deep learning
- Librosa - Audio processing
- Docker - Containerization

### Frontend
- React Native - Mobile framework
- Axios - HTTP client

### Deployment
- Docker & Docker Compose
- Nginx - Reverse proxy
- Render.com / Railway.app - Cloud deployment

## Models

### MFCC Model
- CNN with Batch Normalization
- Input: MFCC features (13 coefficients)
- Output: Accent classification

## Contributing

1. Create a feature branch
2. Make your changes
3. Submit a pull request

## License

MIT License

## Contact

For questions or support, please contact the development team.
