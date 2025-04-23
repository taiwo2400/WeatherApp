import numpy as np
from sklearn.linear_model import LinearRegression
import joblib


X = np.array([[10], [12], [14], [16], [18], [20]])  # Past temperatures (e.g., previous day's temp)
y = np.array([12, 14, 16, 18, 20, 22])  # Future temperatures (e.g., next day's temp)

# Train a simple linear regression model
model = LinearRegression()
model.fit(X, y)

# Save the trained model
joblib.dump(model, 'temperature_predictor.pkl')
