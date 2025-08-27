# backend/app/ml_models/train_model.py
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

# Create synthetic dataset (replace with your real student features later)
X, y = make_classification(n_samples=600, n_features=5, random_state=42)

# Split into train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a simple logistic regression
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

print("Test accuracy:", model.score(X_test, y_test))

# Save model to disk where the backend expects it
joblib.dump(model, "backend/app/ml_models/model.pkl")
