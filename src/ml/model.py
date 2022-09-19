import pickle
from typing import Optional

import numpy as np
from sklearn.ensemble import RandomForestClassifier


class Model:
    def __init__(
        self,
        path: Optional[str] = None,
    ):
        if path:
            self.load(path)
        else:
            self.model = RandomForestClassifier()

    def train(self, X: np.ndarray, y: np.ndarray):
        self.model.fit(X=X, y=y)
        return None

    def predict(self, x: np.ndarray) -> np.ndarray:
        return self.model.predict(x)

    def save(self, path: str):
        with open(path, "wb") as f:
            pickle.dump(self, f)

    def load(self, path: str):
        with open(path, "rb") as f:
            self = pickle.load(f)
