# predictor.py
import pickle
import pandas as pd

def is_failure(sensor_data, threshold=0.4):
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    X_new = pd.DataFrame([sensor_data])
    prob = model.predict_proba(X_new)[0][1]
    return prob > threshold, prob

def get_risk_level(prob):
    if prob > 0.8:
        return "🔴 Critical"
    elif prob > 0.5:
        return "🟠 High"
    elif prob > 0.3:
        return "🟡 Moderate"
    else:
        return "🟢 Low"