import os
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier

# Define BASE_DIR correctly
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load dataset
data_path = os.path.join(BASE_DIR, "datasets", "data.csv")
if not os.path.exists(data_path):
    raise FileNotFoundError(f"❌ Dataset not found: {data_path}")

df = pd.read_csv(data_path)  # Ensure dataset is loaded

# Convert column names to lowercase
df.columns = df.columns.str.lower()

# Ensure required columns exist
required_columns = {"symptom1", "symptom2", "symptom3", "disease", "severity", "treatment", "diagnosis"}
if not required_columns.issubset(df.columns):
    raise ValueError(f"Incorrect dataset format. Expected columns: {required_columns}, Found: {df.columns}")

# Fill missing values
df.fillna("", inplace=True)

# Combine symptoms into a single text column
df["all_symptoms"] = df[['symptom1', 'symptom2', 'symptom3']].astype(str).agg(' '.join, axis=1)

# Group disease information
disease_info_dict = df.groupby("disease").agg({
    "severity": lambda x: list(x.unique()), 
    "treatment": lambda x: list(x.unique()),
    "diagnosis": lambda x: list(x.unique())
}).to_dict(orient="index")

# Convert symptoms into numerical vectors
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["all_symptoms"])
y = df["disease"]

# Train KNN Classifier
model = KNeighborsClassifier(n_neighbors=3)
model.fit(X, y)

# Ensure models directory exists
models_dir = os.path.join(BASE_DIR, "models")
os.makedirs(models_dir, exist_ok=True)

# Save trained model
joblib.dump(model, os.path.join(models_dir, "symptom_model.pkl"))
joblib.dump(vectorizer, os.path.join(models_dir, "symptom_vectorizer.pkl"))
joblib.dump(disease_info_dict, os.path.join(models_dir, "disease_info.pkl"))

print("✅ Model training complete and saved successfully!")
