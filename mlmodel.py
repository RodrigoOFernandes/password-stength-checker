import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from checker import has_sequence 
from checker import has_keyboard_walk
import joblib
from utils import extract_features, has_sequence, has_keyboard_walk

try:
    data = pd.read_csv("data.csv", on_bad_lines='skip')
except pd.errors.ParserError as e:
    print(f"Error reading CSV file: {e}")
    exit(1)

if data.empty:
    print("The dataset is empty or could not be loaded.")
    exit(1)

data = data.dropna(subset=["password"])
data = data[data["password"].apply(lambda x: isinstance(x, str))]

valid_strengths = [0, 1, 2]
data = data[data["strength"].isin(valid_strengths)]

if data.empty:
    print("The dataset is empty after cleaning.")
    exit(1)

data["features"] = data["password"].apply(extract_features)

X = pd.DataFrame(data["features"].tolist())
y = data["strength"]

if y.isna().any():
    print("Warning: NaN values found in the target variable (y). Dropping corresponding rows.")
    X = X[~y.isna()]
    y = y.dropna()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred, target_names=["weak", "medium", "strong"]))

joblib.dump(model, "password_strength_model.pkl")
print("Model saved as password_strength_model.pkl")