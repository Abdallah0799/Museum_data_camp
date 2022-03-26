from sklearn.ensemble import RandomForestClassifier

from sklearn.base import BaseEstimator


class Classifier(BaseEstimator):
    def __init__(self):
        self.classifier = RandomForestClassifier(
            n_estimators=100, max_depth=50, max_features=3)

    def fit(self, X, y):
        self.classifier.fit(X, y)

    def predict(self, X):
        return self.classifier.predict(X)