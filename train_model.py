import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle

# Simulated training data
data = pd.DataFrame({
    'temperature': [70, 85, 90, 95, 100, 65],
    'vibration': [0.3, 0.8, 1.2, 1.4, 1.5, 0.2],
    'failure': [0, 0, 1, 1, 1, 0]
})

X = data[['temperature', 'vibration']]
y = data['failure']

model = LogisticRegression()
model.fit(X, y)

with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)