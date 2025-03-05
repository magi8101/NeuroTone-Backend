# api/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import numpy as np
from pathlib import Path


MODELS_DIR = Path(__file__).parent.parent / "models"


try:
    model = joblib.load(MODELS_DIR / "trained_model.joblib")
    scaler = joblib.load(MODELS_DIR / "scaler.joblib")
    feature_names = joblib.load(MODELS_DIR / "feature_names.joblib")
    feature_thresholds = joblib.load(MODELS_DIR / "feature_thresholds.joblib")
    print("Model loaded successfully!")
except FileNotFoundError:
    print("Error: Model files not found. Please run training script first.")
    raise

class ParkinsonsInput(BaseModel):
    """Input features for Parkinson's prediction"""

    mdvp_fo_hz: float = Field(..., alias="MDVP:Fo(Hz)")
    mdvp_fhi_hz: float = Field(..., alias="MDVP:Fhi(Hz)")
    mdvp_flo_hz: float = Field(..., alias="MDVP:Flo(Hz)")
    mdvp_jitter_percent: float = Field(..., alias="MDVP:Jitter(%)")
    mdvp_jitter_abs: float = Field(..., alias="MDVP:Jitter(Abs)")
    mdvp_rap: float = Field(..., alias="MDVP:RAP")
    mdvp_ppq: float = Field(..., alias="MDVP:PPQ")
    jitter_ddp: float = Field(..., alias="Jitter:DDP")
    mdvp_shimmer: float = Field(..., alias="MDVP:Shimmer")
    mdvp_shimmer_db: float = Field(..., alias="MDVP:Shimmer(dB)")
    shimmer_apq3: float = Field(..., alias="Shimmer:APQ3")
    shimmer_apq5: float = Field(..., alias="Shimmer:APQ5")
    mdvp_apq: float = Field(..., alias="MDVP:APQ")
    shimmer_dda: float = Field(..., alias="Shimmer:DDA")
    nhr: float = Field(..., alias="NHR")
    hnr: float = Field(..., alias="HNR")
    rpde: float = Field(..., alias="RPDE")
    dfa: float = Field(..., alias="DFA")
    spread1: float
    spread2: float
    d2: float = Field(..., alias="D2")
    ppe: float = Field(..., alias="PPE")

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "MDVP:Fo(Hz)": 120.552,
                "MDVP:Fhi(Hz)": 148.790,
                "MDVP:Flo(Hz)": 80.901,
                "MDVP:Jitter(%)": 0.00502,
                "MDVP:Jitter(Abs)": 0.00003,
                "MDVP:RAP": 0.00285,
                "MDVP:PPQ": 0.00296,
                "Jitter:DDP": 0.00855,
                "MDVP:Shimmer": 0.02895,
                "MDVP:Shimmer(dB)": 0.282,
                "Shimmer:APQ3": 0.01552,
                "Shimmer:APQ5": 0.01765,
                "MDVP:APQ": 0.02198,
                "Shimmer:DDA": 0.04655,
                "NHR": 0.01397,
                "HNR": 24.678,
                "RPDE": 0.385,
                "DFA": 0.744,
                "spread1": -5.684,
                "spread2": 0.187,
                "D2": 2.054,
                "PPE": 0.199
            }
        }

class ParkinsonsResponse(BaseModel):
    prediction: int
    probability: float
    diagnosis: str
    analysis: dict

def analyze_features(input_data, feature_mapping):
    analysis = {}
    for original_name, mapped_name in feature_mapping.items():
        value = getattr(input_data, mapped_name)
        healthy_stats = feature_thresholds['healthy'][original_name]
        parkinsons_stats = feature_thresholds['parkinsons'][original_name]
        

        healthy_zscore = abs((value - healthy_stats['mean']) / healthy_stats['std'])
        parkinsons_zscore = abs((value - parkinsons_stats['mean']) / parkinsons_stats['std'])

        closer_to = 'Healthy' if healthy_zscore < parkinsons_zscore else 'Parkinson\'s'
        
        analysis[original_name] = {
            'value': value,
            'healthy_mean': healthy_stats['mean'],
            'parkinsons_mean': parkinsons_stats['mean'],
            'closer_to': closer_to,
            'deviation_from_healthy': f"{healthy_zscore:.2f} std",
            'deviation_from_parkinsons': f"{parkinsons_zscore:.2f} std"
        }
    
    return analysis

app = FastAPI(
    title="Parkinson's Disease Detection API",
    description="API for detecting Parkinson's Disease",
    version="1.0.0"
)

@app.post("/predict", response_model=ParkinsonsResponse)
async def predict_parkinsons(input_data: ParkinsonsInput):
    try:

        feature_mapping = {
            "MDVP:Fo(Hz)": "mdvp_fo_hz",
            "MDVP:Fhi(Hz)": "mdvp_fhi_hz",
            "MDVP:Flo(Hz)": "mdvp_flo_hz",
            "MDVP:Jitter(%)": "mdvp_jitter_percent",
            "MDVP:Jitter(Abs)": "mdvp_jitter_abs",
            "MDVP:RAP": "mdvp_rap",
            "MDVP:PPQ": "mdvp_ppq",
            "Jitter:DDP": "jitter_ddp",
            "MDVP:Shimmer": "mdvp_shimmer",
            "MDVP:Shimmer(dB)": "mdvp_shimmer_db",
            "Shimmer:APQ3": "shimmer_apq3",
            "Shimmer:APQ5": "shimmer_apq5",
            "MDVP:APQ": "mdvp_apq",
            "Shimmer:DDA": "shimmer_dda",
            "NHR": "nhr",
            "HNR": "hnr",
            "RPDE": "rpde",
            "DFA": "dfa",
            "spread1": "spread1",
            "spread2": "spread2",
            "D2": "d2",
            "PPE": "ppe"
        }


        features = []
        for feature in feature_names:
            attr_name = feature_mapping[feature]
            value = getattr(input_data, attr_name)
            features.append(value)
        

        features = np.array(features).reshape(1, -1)
        

        features_scaled = scaler.transform(features)

        prediction = model.predict(features_scaled)[0]
        probability = model.predict_proba(features_scaled)[0]
        
 
        analysis = analyze_features(input_data, feature_mapping)
        
        return ParkinsonsResponse(
            prediction=int(prediction),
            probability=float(probability[1] if prediction == 1 else probability[0]),
            diagnosis="Parkinson's Disease Detected" if prediction == 1 else "No Parkinson's Disease Detected",
            analysis=analysis
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")



    