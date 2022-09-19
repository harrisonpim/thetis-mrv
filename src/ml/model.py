import pickle
from typing import Optional

import numpy as np
from sklearn.utils.class_weight import compute_class_weight,compute_sample_weight
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
        class_weights = compute_class_weight(
            class_weight="balanced", classes=np.unique(y), y=y
        )
        sample_weight = compute_sample_weight(class_weights, y)
        self.model.fit(X=X,y=y,sample_weight=sample_weight)
        return None

    def predict(self, x: np.ndarray) -> np.ndarray:
        return np.around(self.model.predict(x))

    def save(self, path: str):
        with open(path, "wb") as f:
            pickle.dump(self, f)

    def load(self, path: str):
        with open(path, "rb") as f:
            self = pickle.load(f)
