#!/bin/bash

# AuralDine Backend Run Script

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
