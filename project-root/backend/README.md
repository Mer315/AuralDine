# AuralDine Backend

FastAPI-based backend for accent recognition and restaurant recommendations.

## Features

- Accent detection from audio input
- Restaurant recommendations based on accent
- MFCC and HuBERT model support
- RESTful API endpoints

## Setup

### Prerequisites
- Python 3.11+
- pip or conda

### Installation

```bash
pip install -r requirements.txt
```

### Running Locally

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Docker

```bash
docker build -t auraldine-backend .
docker run -p 8000:8000 auraldine-backend
```

## API Endpoints

- `GET /api/health` - Health check
- `POST /api/predict` - Predict accent from audio

## Project Structure

- `app/` - Main application code
- `ml/` - Machine learning models and training
- `requirements.txt` - Python dependencies
- `Dockerfile` - Docker configuration

## Configuration

Set environment variables in `.env` file:

```env
DEBUG=False
MODEL_PATH=ml/models/cnn_bn_final.pt
DATASET_PATH=ml/data/label_mfcc_dataset.csv
```
