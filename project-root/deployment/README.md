# Deployment Configuration

Contains deployment configurations for various platforms.

## Docker Compose

Run the entire stack locally:

```bash
docker-compose up -d
```

This will start:
- FastAPI backend on port 8000
- Nginx reverse proxy on port 80

## Render

Deploy to Render.com using `render.yaml`:

1. Connect your repository to Render
2. Create a new web service
3. Select the root directory
4. Render will automatically detect and deploy using `render.yaml`

## Railway

Deploy to Railway.app using `railway.json`:

1. Connect your repository to Railway
2. Railway will detect the configuration
3. Deploy with a single click

## Environment Variables

Set these on your deployment platform:

```
DEBUG=false
MODEL_PATH=ml/models/cnn_bn_final.pt
DATASET_PATH=ml/data/label_mfcc_dataset.csv
```

## Health Check

Verify deployment is working:

```bash
curl http://your-deployed-url/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```
