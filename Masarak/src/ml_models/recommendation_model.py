from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
import joblib

class RecommendationModel:
    def __init__(self, data_path):
        self.data_path = data_path
        self.model = RandomForestClassifier()
        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None

    def load_data(self):
        data = pd.read_csv(self.data_path)
        X = data.drop('target', axis=1)
        y = data['target']
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    def train(self):
        self.load_data()
        self.model.fit(self.X_train, self.y_train)

    def predict(self, input_data):
        return self.model.predict(input_data)

    def save_model(self, model_path):
        joblib.dump(self.model, model_path)

    def load_model(self, model_path):
        self.model = joblib.load(model_path)