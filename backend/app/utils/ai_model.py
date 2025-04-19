import numpy as np
import joblib

model = joblib.load('backed/app/models/temperature_predictor.pkl')


def predict_temperature_trend(current_temp: float) -> float:
    prediction = model.predict(np.array([[current_temp]]))
    return prediction[0]