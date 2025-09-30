# Step 1: Import libraries
import pandas as pd
import sklearn
from sklearn.model_selection import StratifiedKFold, cross_val_score, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# Step 2: Load dataset
df = pd.read_csv("C:\\Users\\lenovo\\Downloads\\smart-crop-recommendation\\crop_dataset_final_.csv")

# Step 3: Inspect dataset
print(df.head())
print(df.info())

# Step 4: Preprocessing
label_encoders = {}
for col in df.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Step 5: Define features (X) and target (y)
X = df.drop("crop", axis=1)   # all columns except 'crop'
y = df["crop"]                # target = crop

# Step 6: Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 7: Stratified K-Fold Cross Validation
model = RandomForestClassifier(n_estimators=200, random_state=42)

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X_scaled, y, cv=skf, scoring='accuracy')

print("Cross-validation scores:", scores)
print("Mean CV Accuracy:", scores.mean())

# Step 8: Train Final Model on Full Dataset
model.fit(X_scaled, y)

# Step 9: Save model bundle
bundle = {
    "model": model,
    "scaler": scaler,
    "label_encoders": label_encoders,
    "feature_columns": X.columns.tolist(),
    "sklearn_version": sklearn.__version__
}

joblib.dump(bundle, "crop_model_bundle.pkl")
print("Saved crop_model_bundle.pkl (model, scaler, encoders, feature order)")
