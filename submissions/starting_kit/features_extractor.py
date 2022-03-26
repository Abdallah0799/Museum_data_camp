import tarfile
from rampwf.workflows import FeatureExtractor
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.impute import SimpleImputer
import numpy as np
import warnings
warnings.filterwarnings('ignore')

TARGET_COL = 'Historical Period'

class FeatureExtractor(object):
    
    def __init__(self):
        self.map_period = {"Contemporary Era":1., "Modern Times": 2., "Middle Ages":3., "Antiquity":4.}
        
    def fit(self, X, y):
        
        # feature selection on the Medium column
        X_copy = X.copy()
        def medium_extraction(X):
            val_medium = X['Medium'].values.copy()
            Medium = []
            sep = ","

            vectorizer = CountVectorizer(stop_words="english", max_features=24)
            vectorizer.fit(val_medium)
            vectorized_input = vectorizer.transform(val_medium)
            inv_transform = vectorizer.inverse_transform(vectorized_input)
            
            for arr in inv_transform:
                arr = list(arr)
                arr = sorted(arr)
                arr = sep.join(arr)
                Medium.append(arr)
            
            Medium = np.array(Medium)
            Medium[Medium==""]=pd.NA
            
            return Medium
        
        def mean_target_encoding_classif(X):
            X["num_period"] = [self.map_period[period] for period in X[TARGET_COL]]
            tmp_classif = X.groupby(["Classification"]).describe()
            col_to_select = [col for col in tmp_classif.columns if "num_period" in col and "mean" in col][0]
            map_classif = {classif_cat: classif_num for (classif_cat, classif_num) in zip(tmp_classif.index, tmp_classif[col_to_select])}
            
            Classification = [map_classif[m] for m in X["Classification"]]
            return np.array(Classification).reshape(-1,1)
        
        def mean_target_encoding_medium(X):
            X["num_period"] = [self.map_period[period] for period in X[TARGET_COL]]
            tmp_medium = X.groupby(["Medium"]).describe()
            col_to_select = [col for col in tmp_medium.columns if "num_period" in col and "mean" in col][0]
            map_medium = {medium_cat: medium_num for (medium_cat, medium_num) in zip(tmp_medium.index, tmp_medium[col_to_select])}
            Medium = [map_medium[m] for m in X["Medium"]]
            return np.array(Medium).reshape(-1,1)
        
        def mean_target_encoding_culture(X):
            X["num_period"] = [self.map_period[period] for period in X[TARGET_COL]]
            tmp_culture = X.groupby(["Culture"]).describe()
            col_to_select = [col for col in tmp_culture.columns if "num_period" in col and "mean" in col][0]
            map_culture = {culture_cat: culture_num for (culture_cat, culture_num) in zip(tmp_culture.index, tmp_culture[col_to_select])}
            
            Culture = [map_culture[m] for m in X["Culture"]]
            return np.array(Culture).reshape(-1,1)
        
        MTE_classif = FunctionTransformer(mean_target_encoding_classif, validate=False)
        MTE_medium = FunctionTransformer(mean_target_encoding_medium, validate=False)
        MTE_culture =  FunctionTransformer(mean_target_encoding_culture, validate=False)
        
        #column transformer
        preprocessor = ColumnTransformer(
            transformers=[
                ('medium_extraction', make_pipeline(MTE_medium, SimpleImputer(strategy="constant", fill_value=-1)), ['Medium', 'Historical Period']),
                ('mte_classif', MTE_classif, ['Classification', 'Historical Period']),
                ('mte_culture', MTE_culture,  ['Culture', 'Historical Period'])
            ])
        
        X_copy['Medium'] = medium_extraction(X)
        self.prepocessor = preprocessor
        self.prepocessor.fit(X_copy, y)
    
    def transform(self, X):
        transformation = self.prepocessor.transform(X)
        X_output = X.copy()
        X_output[['Medium', 'Classification', 'Culture']] = transformation
        X_output.drop([TARGET_COL], axis=1, inplace=True)
        if 'Unnamed:  0' in X_output.columns:
            X_output.drop(['Unnamed:  0'], axis=1, inplace=True)
        return X_output[['Medium', 'Classification', 'Culture', 'height', 'diam', 'width','depth']].values
        
        
