from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI()

class PredictionInput(BaseModel):
    age: float
    hypertension: int
    heart_disease: int
    bmi: float
    HbA1c_level: float
    blood_glucose_level: float
    gender_encoded: int
    smoking_encoded: int
    gender_name_Male: int
    smoking_status_former: int
    smoking_status_never: int
    smoking_status_unknown: int

try:
    model = joblib.load("random_forest_model.joblib")
    preprocessor = joblib.load("preprocessor.joblib")
    print("Model and preprocessor loaded successfully.")
except FileNotFoundError as e:
    print(f"Model or preprocessor file not found: {e}")
    raise
except Exception as e:
    print(f"Error loading model or preprocessor: {e}")
    raise

@app.post("/predict")
def predict(input_data: PredictionInput):
    try:
        input_df = pd.DataFrame([input_data.dict()])

        expected_columns = [
            'age', 'hypertension', 'heart_disease', 'bmi', 'HbA1c_level',
            'blood_glucose_level', 'gender_encoded', 'smoking_encoded',
            'gender_name_Male', 'smoking_status_former', 'smoking_status_never',
            'smoking_status_unknown'
        ]
        missing_columns = set(expected_columns) - set(input_df.columns)
        if missing_columns:
            raise HTTPException(status_code=400, detail=f"Missing input columns: {missing_columns}")

        input_preprocessed = preprocessor.transform(input_df)
        prediction = model.predict(input_preprocessed)

        return {"diabetes": int(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {e}")

@app.get("/")
def root():
    return {"message": "FastAPI is running. Use the /predict endpoint to make predictions."}
