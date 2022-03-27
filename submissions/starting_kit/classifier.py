from sklearn.ensemble import RandomForestClassifier
from sklearn.base import BaseEstimator


class Classifier(BaseEstimator):
    def __init__(self):
        self.classifier = RandomForestClassifier(n_estimators=100, max_depth=50, random_state=0)

    def fit(self, X, y):
        self.classifier.fit(X, y)

    def predict_proba(self, X):
        return self.classifier.predict_proba(X)

