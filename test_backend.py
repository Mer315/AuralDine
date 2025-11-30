#!/usr/bin/env python3
"""
Quick test script to verify backend setup and model loading
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    print("Testing imports...")
    try:
        import torch
        print("✓ PyTorch imported successfully")
    except ImportError as e:
        print("✗ PyTorch import failed:", e)
        return False
    
    try:
        import librosa
        print("✓ Librosa imported successfully")
    except ImportError as e:
        print("✗ Librosa import failed:", e)
        return False
    
    try:
        from fastapi import FastAPI
        print("✓ FastAPI imported successfully")
    except ImportError as e:
        print("✗ FastAPI import failed:", e)
        return False
    
    return True

def test_model():
    print("\nTesting model loading...")
    try:
        from app.model_service import ModelService
        from app.config import settings
        
        service = ModelService()
        model = service.load_model()
        
        if model is not None:
            print("✓ Model loaded successfully")
            print(f"  Device: {service.device}")
            return True
        else:
            print("⚠ Model not found, will use dummy predictions")
            return True
    except Exception as e:
        print("✗ Model loading failed:", e)
        return False

def test_routes():
    print("\nTesting routes...")
    try:
        from app.main import app
        print("✓ App initialized successfully")
        return True
    except Exception as e:
        print("✗ App initialization failed:", e)
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("AuralDine Backend Test Suite")
    print("=" * 50)
    
    all_pass = True
    all_pass &= test_imports()
    all_pass &= test_model()
    all_pass &= test_routes()
    
    print("\n" + "=" * 50)
    if all_pass:
        print("✓ All tests passed! Backend ready to run")
        print("\nTo start the server, run:")
        print("  cd backend")
        print("  python -m uvicorn app.main:app --reload --port 5000")
    else:
        print("✗ Some tests failed. Please check the errors above.")
    print("=" * 50)
