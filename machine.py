import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
from datetime import datetime

class Machine:
    def __init__(self, df: pd.DataFrame, target_column='Rarity'):
        self.name = "Random Forest Classifier"
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.target = df[target_column]
        self.features = df.drop(columns=[target_column])
        self.model = RandomForestClassifier(random_state=42)
        self.train_model()

    def train_model(self):
        self.model.fit(self.features, self.target)
        print(f"{self.name} trained successfully.")

    def __call__(self, pred_basis: pd.DataFrame):
        prediction = self.model.predict(pred_basis)
        confidence = max(self.model.predict_proba(pred_basis)[0])  # Get confidence
        return prediction[0], confidence

    def save(self, filepath: str):
        joblib.dump(self, filepath)

    @staticmethod
    def open(filepath: str):
        return joblib.load(filepath)

    def info(self):
        # Format the timestamp to a more human-readable format
        formatted_timestamp = datetime.strptime(self.timestamp, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %I:%M:%S %p")
        return {
            "name": self.name,
            "timestamp": formatted_timestamp,
        }
