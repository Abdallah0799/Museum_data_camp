from sklearn.ensemble import RandomForestClassifier
from sklearn.base import BaseEstimator
from sklearn.decomposition import PCA


class Classifier(BaseEstimator):
    def __init__(self):
        self.classifier = RandomForestClassifier(
            n_estimators=100, max_depth=20, random_state=0)
        

    def fit(self, X, y):
        """
        ['Medium', 'Classification', 'Culture',
       'Object Begin Date', 'height', 'diam', 'width', 'depth']
        """
        # selected features: 'Medium', 'Classification', 'Culture'
        X = X[:,:3]
        pca = PCA(n_components=2, random_state=1)
        X_train_pca=pca.fit_transform(X)
        # store the preprocessor
        self.preprocessor = pca
        self.classifier.fit(X_train_pca, y)

    def predict_proba(self, X):
        X = X[:,:3]
        X_test_pca = self.preprocessor.transform(X)
        return self.classifier.predict_proba(X_test_pca)

