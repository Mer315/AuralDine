import time
import json
import os
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from app.model_service import ModelService
from app.config import settings
from app.utils import read_audio_bytes, extract_mfcc

router = APIRouter()
model_service = ModelService()
model_service.load_model()

# Load image URIs from JSON file
def load_image_uris():
    """Load image URIs from image_uris.json."""
    try:
        # Try to load from project root
        image_uri_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'image_uris.json')
        if os.path.exists(image_uri_path):
            with open(image_uri_path, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load image_uris.json: {e}")
    return {}

IMAGE_URIS = load_image_uris()

# Mapping of states to languages
STATE_LANGUAGES = {
    "andhrapradesh": "Telugu/Urdu",
    "gujarath": "Gujarati",
    "kerala": "Malayalam",
    "karnataka": "Kannada",
    "jharkhand": "Hindi (North Indian)",
    "tamilnadu": "Tamil"
}

# Helper function to get image URI
def get_image_uri(filename):
    """Get image URI from IMAGE_URIS or return placeholder."""
    # Prefer returning the static frontend-served path first. The frontend
    # nginx server serves files under /images/, and we expect project
    # maintainers to place overrides in `frontend/images/` before build.
    # Returning the static path avoids container filesystem checks and
    # makes it straightforward for the frontend to fetch the file.
    try:
        return f"/images/{filename}"
    except Exception:
        pass

    # Fallback to embedded data URIs from IMAGE_URIS
    if filename in IMAGE_URIS:
        return IMAGE_URIS[filename]

    # Final fallback: tiny placeholder SVG data URI
    return "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgZmlsbD0iI2YzZjRmNiIvPjwvc3ZnPg=="

# Mapping of states to cuisine recommendations (5 per state)
STATE_CUISINES = {
  "andhrapradesh": [
    {"name": "Telangana Biryani", "image": get_image_uri("telangana_biryani.png"), "price": "₹350-450", "description": "Aromatic rice with tender meat cooked with saffron and spices."},
    {"name": "Telangana Chickencurry", "image": get_image_uri("telangana_chickencurry.png"), "price": "₹280", "description": "Spicy chili-based curry from the Guntur region."},
    {"name": "Telangana Pesarattu", "image": get_image_uri("telangana_pesarattu.png"), "price": "₹40-60", "description": "Green moong pancake with ginger-chili chutney."},
    {"name": "Telangana Gongura", "image": get_image_uri("telangana_gongura.png"), "price": "₹200", "description": "Tangy sorrel leaves curry with meat."},
    {"name": "Telangana Halim", "image": get_image_uri("telangana_halim.png"), "price": "₹200-250", "description": "Slow-cooked minced meat with lentils and wheat."}
  ],
  "gujarath": [
    {"name": "Gujarath Dhokla", "image": get_image_uri("gujarath_dhokla.png"), "price": "₹30-50", "description": "Light, steamed savory cake made from gram flour."},
    {"name": "Gujarath Undhiyu", "image": get_image_uri("gujarath_undhiyu.png"), "price": "₹120-150", "description": "Mixed vegetables with groundnuts and spices."},
    {"name": "Gujarath Fafda", "image": get_image_uri("gujarath_fafda.png"), "price": "₹40-60", "description": "Crispy gram flour noodles with sweet jalebi."},
    {"name": "Gujarath Khichiyu", "image": get_image_uri("gujarath_khichiyu.png"), "price": "₹80-100", "description": "Savory rice and lentil porridge."},
    {"name": "Gujarath Thepla", "image": get_image_uri("gujarath_thepla.png"), "price": "₹20-40", "description": "Thin spiced flatbread with methi leaves."}
  ],
  "kerala": [
    {"name": "Kerala Appam", "image": get_image_uri("kerala_appam.png"), "price": "₹80-100", "description": "Soft rice pancakes with creamy coconut curry."},
    {"name": "Kerala Fishcurry", "image": get_image_uri("kerala_fishcurry.png"), "price": "₹200-250", "description": "Tangy and spicy fish in coconut-based gravy."},
    {"name": "Kerala Puttu", "image": get_image_uri("kerala_puttu.png"), "price": "₹60-80", "description": "Steamed rice cake with chickpea curry."},
    {"name": "Kerala Avial", "image": get_image_uri("kerala_avial.png"), "price": "₹100", "description": "Mixed vegetable medley with coconut and spices."},
    {"name": "Kerala Dosa", "image": get_image_uri("kerala_dosa.png"), "price": "₹40-60", "description": "Crispy rice and lentil crepe with sambar."}
  ],
  "karnataka": [
    {"name": "Karnataka Bisibele", "image": get_image_uri("karnataka_bisibele.png"), "price": "₹80-100", "description": "Spiced rice and lentil dish with vegetables."},
    {"name": "Karnataka Dosa", "image": get_image_uri("karnataka_dosa.png"), "price": "₹60-80", "description": "Crispy dosa with spicy potato filling and sambar."},
    {"name": "Karnataka Uttapam", "image": get_image_uri("karnataka_uttapam.png"), "price": "₹50-70", "description": "Thick savory rice cake with toppings."},
    {"name": "Karnataka Joladaroti", "image": get_image_uri("karnataka_joladaroti.png"), "price": "₹30-40", "description": "Sorghum flour flatbread with spices."},
    {"name": "Karnataka Mysorepak", "image": get_image_uri("karnataka_mysorepak.png"), "price": "₹100-150", "description": "Buttery gram flour fudge with cashews."}
  ],
  "jharkhand": [
    {"name": "Jharkhand Thekua", "image": get_image_uri("jharkhand_thekua.png"), "price": "₹100-150", "description": "Sweet wheat flour cookies with jaggery."},
    {"name": "Jharkhand Rugra", "image": get_image_uri("jharkhand_rugra.png"), "price": "₹80", "description": "Millet-based porridge with vegetables."},
    {"name": "Jharkhand Dhuska", "image": get_image_uri("jharkhand_dhuska.png"), "price": "₹40-50", "description": "Rice and lentil fritter with spices."},
    {"name": "Jharkhand Pua", "image": get_image_uri("jharkhand_pua.png"), "price": "₹30-40", "description": "Sweet pancake with jaggery and banana."},
    {"name": "Jharkhand Litti", "image": get_image_uri("jharkhand_litti.png"), "price": "₹50-70", "description": "Wheat dough balls with roasted gram flour stuffing."}
  ],
  "tamilnadu": [
    {"name": "Tamilnadu Idli", "image": get_image_uri("tamilnadu_idli.png"), "price": "₹40-60", "description": "Steamed rice cakes with spiced lentil stew."},
    {"name": "Tamilnadu Chettinad", "image": get_image_uri("tamilnadu_chettinad.png"), "price": "₹250-300", "description": "Rich and spicy chicken with aromatic spices."},
    {"name": "Tamilnadu Dosa", "image": get_image_uri("tamilnadu_dosa.png"), "price": "₹50-70", "description": "Crispy rice-lentil crepe with sambar."},
    {"name": "Tamilnadu Vadai", "image": get_image_uri("tamilnadu_vadai.png"), "price": "₹20-30", "description": "Crispy urad dal fritters."},
    {"name": "Tamilnadu Rasam", "image": get_image_uri("tamilnadu_rasam.png"), "price": "₹40", "description": "Spiced tamarind and pepper soup."}
  ]
}


# Filter STATE_CUISINES to only include entries for which an image file
# exists in the frontend images directory. This allows maintainers to add
# or remove PNGs in `frontend/images/` and have the API automatically
# return only cuisines with available images.
def _load_frontend_image_set():
    """Return a set of filenames present in frontend/images or listed in manifest.json."""
    try:
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        frontend_images_dir = os.path.join(project_root, 'frontend', 'images')

        # Prefer manifest.json if present (faster, avoids reading many files)
        manifest_path = os.path.join(frontend_images_dir, 'manifest.json')
        files = set()
        if os.path.exists(manifest_path):
            try:
                with open(manifest_path, 'r', encoding='utf-8') as mf:
                    data = json.load(mf)
                    for f in data:
                        files.add(os.path.basename(f))
                    return files
            except Exception:
                pass

        # Fallback: list directory contents
        if os.path.isdir(frontend_images_dir):
            for fn in os.listdir(frontend_images_dir):
                if os.path.isfile(os.path.join(frontend_images_dir, fn)):
                    files.add(fn)
        return files
    except Exception:
        return set()


# Apply filtering
_available_images = _load_frontend_image_set()
if _available_images:
    _filtered = {}
    for state, cuisines in STATE_CUISINES.items():
        kept = []
        for c in cuisines:
            img = c.get('image') or ''
            # extract basename if path-like
            base = os.path.basename(img) if isinstance(img, str) else ''
            # also accept images referenced without extension
            if base in _available_images:
                kept.append(c)
        if kept:
            _filtered[state] = kept
    # Only replace if we actually filtered something
    if _filtered:
        STATE_CUISINES = _filtered



@router.post("/predict/")
async def predict(file: UploadFile = File(...)):
    """Accept an uploaded audio file and return predicted language and confidence."""
    start_time = time.time()
    try:
        if not file.filename:
            raise ValueError("No file uploaded")
        
        contents = await file.read()
        if not contents:
            raise ValueError("File is empty")
        
        print(f"[PREDICT] Received {len(contents)} bytes from {file.filename}")
        
        # Read audio bytes
        y, sr = read_audio_bytes(contents)
        print("Received audio:", file.filename)
        print(f"[PREDICT] Audio loaded: {y.shape}, sr={sr}")

        # Run preprocessing pipeline to obtain windows and per-window MFCC means
        from app.utils import preprocess_audio
        summary = preprocess_audio(y, sr, window_sec=1.0, n_mfcc=13, fast=settings.FAST_PREPROCESS)
        print("Processed segments:", summary.get('num_segments'))
        print("Processed windows:", summary.get('num_windows'))

        # If we have per-window embeddings, average them to form final features
        mfcc_means = summary.get('mfcc_means', [])
        import numpy as _np
        if len(mfcc_means) > 0:
            features = _np.mean(_np.array(mfcc_means), axis=0)
        else:
            # Fallback to existing extract_mfcc which returns an aggregated vector
            features = extract_mfcc(y, sr=sr, n_mfcc=13, fast=settings.FAST_PREPROCESS)

        print(f"[PREDICT] Features prepared: shape={getattr(features, 'shape', None)}")

        state, confidence = model_service.predict_from_features(_np.asarray(features))
        print("Final prediction:", state, confidence)
        
        # Get language from state
        language = STATE_LANGUAGES.get(state, "Unknown")
        cuisines = STATE_CUISINES.get(state, [])
        
        # Calculate processing time
        duration_ms = int((time.time() - start_time) * 1000)
        print(f"[PREDICT] Processing time: {duration_ms}ms")

        return JSONResponse({
            "language": language,
            "confidence": float(confidence),
            "duration_ms": duration_ms,
            "state": state,
            "cuisines": cuisines
        })
    except Exception as e:
        import traceback
        print(f"[PREDICT] Error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/recommend-cuisine/")
async def recommend_cuisine(state: str = None):
    """Return cuisine recommendations for a given state.
    
    If state is provided, return cuisines for that state.
    Otherwise, return all available cuisines grouped by state.
    """
    if state and state in STATE_CUISINES:
        cuisines = STATE_CUISINES[state]
        return JSONResponse({
            "state": state,
            "cuisines": cuisines,
            "count": len(cuisines)
        })
    
    # Return all cuisines
    return JSONResponse({
        "all_cuisines": STATE_CUISINES,
        "total_states": len(STATE_CUISINES)
    })


@router.post("/preprocess/")
async def preprocess(file: UploadFile = File(...)):
    """Accept an uploaded audio file and return preprocessing summary.

    The endpoint returns a JSON object containing sample rate, original
    sample count, number of segments, number of fixed windows, per-window
    MFCC mean vectors and a small WAV preview (base64) for the first window.
    """
    try:
        contents = await file.read()
        if not contents:
            raise ValueError("File is empty")

        y, sr = read_audio_bytes(contents)
        # Use util helper
        from app.utils import preprocess_audio
        summary = preprocess_audio(y, sr, window_sec=1.0, n_mfcc=13, fast=settings.FAST_PREPROCESS)

        # Prepare a WAV preview for the first window (if available)
        preview_b64 = None
        if summary['num_windows'] > 0:
            import io, base64, wave, struct
            first_w = summary['windows'][0]
            # Convert float32 [-1,1] to int16
            max_amp = max(1e-9, float(max(abs(first_w))))
            scaled = (first_w * 32767).astype('int16')
            buf = io.BytesIO()
            with wave.open(buf, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(int(sr))
                wf.writeframes(struct.pack('<' + 'h'*len(scaled), *scaled))
            buf.seek(0)
            preview_b64 = base64.b64encode(buf.read()).decode('ascii')

        # Convert mfcc_means numpy lists to plain lists are already lists
        return JSONResponse({
            'sr': summary['sr'],
            'original_samples': summary['original_samples'],
            'num_segments': summary['num_segments'],
            'num_windows': summary['num_windows'],
            'mfcc_means': summary['mfcc_means'],
            'preview_wav_b64': preview_b64,
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))
