# Machine Learning Module

Contains models, training scripts, and preprocessing utilities for accent recognition.

## Structure

- `models/` - Trained model files
- `data/` - Datasets
- `training/` - Training notebooks
- `preprocessing/` - Data preprocessing scripts
- `inference/` - Inference utilities
- `utils/` - Helper utilities

## Models

### MFCC Model
- File: `models/cnn_bn_final.pt`
- Type: CNN with Batch Normalization
- Input: MFCC features

## Data

- `label_mfcc_dataset.csv` - MFCC features dataset with labels

## Training

Run training notebooks in `training/` directory:
- `mfcc_model_training.ipynb` - MFCC model training
- `hubert_ml_training.ipynb` - HuBERT model training
- `evaluation.ipynb` - Model evaluation

## Preprocessing

- `extract_mfcc.py` - Extract MFCC features from audio
- `hubert_preprocess.py` - Prepare data for HuBERT model
