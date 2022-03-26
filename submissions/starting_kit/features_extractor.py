from rampwf.workflows import FeatureExtractor
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.impute import SimpleImputer
import numpy as np

class FeatureExtractor(object):
    
    def __init__(self):
        self.map_period = {"Contemporary Era":1., "Modern Times": 2., "Middle Ages":3., "Antiquity":4.}
        
    def fit(self, X, y):
        
        # feature selection on the Medium column
        
        def medium_extraction(X):
            val_medium = X['Medium'].values
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
            
            X['Medium'] = Medium
            X[X['Medium']==""]=pd.NA
            
            return X['Medium']
        
        def mean_target_encoding_classif(df):
            
            df["num_period"] = [self.map_period[period] for period in y]
            tmp_classif = df.groupby(["Classification"]).describe()
            map_classif = {classif_cat: classif_num for (classif_cat, classif_num) in zip(tmp_classif.index, tmp_classif[('num_period', 'mean')])}
            
            Classification = [map_classif[m] for m in df["Classification"]]
            return np.array(Classification).reshape(-1,1)
        
        def mean_target_encoding_medium(df):
            df["num_period"] = [self.map_period[period] for period in y]
            tmp_medium = df.groupby(["Medium"]).describe()
            map_medium = {medium_cat: medium_num for (medium_cat, medium_num) in zip(tmp_medium.index, tmp_medium[('num_period', 'mean')])}
            
            Medium = [map_medium[m] for m in df["Medium"]]
            return np.array(Medium).reshape(-1,1)
        
        def mean_target_encoding_culture(df):
            df["num_period"] = [self.map_period[period] for period in y]
            tmp_culture = df.groupby(["Culture"]).describe()
            map_culture = {culture_cat: culture_num for (culture_cat, culture_num) in zip(tmp_culture.index, tmp_culture[('num_period', 'mean')])}
            
            Culture = [map_culture[m] for m in df["Culture"]]
            return np.array(Culture).reshape(-1,1)
        
        MTE_classif = FunctionTransformer(mean_target_encoding_classif, validate=False)
        MTE_medium = FunctionTransformer(mean_target_encoding_medium, validate=False)
        MTE_culture =  FunctionTransformer(mean_target_encoding_culture, validate=False)
        
        #column transformer
        preprocessor = ColumnTransformer(
            transformers=[
                ('medium_extraction', make_pipeline(MTE_medium, SimpleImputer(strategy="constant", fill_value=-1)), ['Medium']),
                ('mte_classif', MTE_classif, ['Classification']),
                ('mte_culture', MTE_culture,  ['Culture'])
            ])
        
        X['Medium'] = medium_extraction(X)
        
        self.prepocessor = preprocessor
        
        self.prepocessor.fit(X, y)
    
    def transform(self, X):
        print(X.shape)
        transformation = self.prepocessor.transform(X)
        X[['Medium', 'Classification', 'Culture']] = transformation
        
        return X.values
        
        
        