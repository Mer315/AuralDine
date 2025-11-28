from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from app.model_service import ModelService
from app.utils import read_audio_bytes, extract_mfcc

router = APIRouter()
model_service = ModelService()
model_service.load_model()

# Mapping of states to cuisine recommendations
STATE_CUISINES = {
    "andhrapradesh": [
        {"name": "Hyderabadi Biryani", "price": "$$", "description": "Aromatic rice and tender meat cooked with spices."},
        {"name": "Guntur Chicken Curry", "price": "$$", "description": "Spicy curry from the Guntur region."}
    ],
    "gujarath": [
        {"name": "Dhokla", "price": "$", "description": "Light, steamed savory cake."},
        {"name": "Undhiyu", "price": "$$", "description": "Mixed vegetable delicacy."}
    ],
    "kerala": [
        {"name": "Appam & Stew", "price": "$$", "description": "Soft rice pancakes with coconut stew."},
        {"name": "Kerala Fish Curry", "price": "$$", "description": "Tangy and spicy fish curry."}
    ],
    "karnataka": [
        {"name": "Bisi Bele Bath", "price": "$$", "description": "Spiced rice and lentil dish."},
        {"name": "Mysore Masala Dosa", "price": "$$", "description": "Crispy dosa with spicy filling."}
    ],
    "jharkhand": [
        {"name": "Thekua", "price": "$", "description": "Sweet snack made from wheat flour."},
        {"name": "Rugra", "price": "$$", "description": "Millet-based local dish."}
    ],
    "tamilnadu": [
        {"name": "Idli & Sambar", "price": "$", "description": "Steamed rice cakes with lentil stew."},
        {"name": "Chettinad Chicken", "price": "$$$", "description": "Rich and spicy chicken preparation."}
    ]
}

@router.post("/predict/")
async def predict(file: UploadFile = File(...)):
    """Accept an uploaded audio file and return predicted state and cuisines."""
    try:
        if not file.filename:
            raise ValueError("No file uploaded")
        
        contents = await file.read()
        if not contents:
            raise ValueError("File is empty")
        
        # Read audio bytes and extract features
        y, sr = read_audio_bytes(contents)
        features = extract_mfcc(y, sr=sr, n_mfcc=13)

        state, confidence = model_service.predict_from_features(features)
        cuisines = STATE_CUISINES.get(state, [])

        return JSONResponse({
            "state": state,
            "confidence": confidence,
            "cuisines": cuisines
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))
