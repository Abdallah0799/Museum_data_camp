import os
import pandas as pd
import rampwf as rw
from rampwf.workflows import FeatureExtractorClassifier
from rampwf.score_types.base import BaseScoreType
from sklearn.model_selection import StratifiedShuffleSplit
import numpy as np

problem_title = 'Museum object estimation'
_target_column_name = 'Historical Period'

_prediction_label_names = ["Antiquity", "Contemporary Era", "Middle Ages", "Modern Times"] 

Predictions = rw.prediction_types.make_multiclass(label_names=_prediction_label_names)

class Workflow(FeatureExtractorClassifier):
    def __init__(self, workflow_element_names=[
            'features_extractor', 'classifier']):
        super(Workflow, self).__init__(workflow_element_names[:2])
        self.element_names = workflow_element_names

workflow = Workflow()

score_types = [rw.score_types.Accuracy("accuracy"), rw.score_types.NegativeLogLikelihood("nll")]

def _read_data(path, f_name):
    data = pd.read_csv(os.path.join(path, 'data', f_name))
    y_array = data[_target_column_name].values
    #X_df = data.drop([_target_column_name], axis=1)
    #return X_df, y_array
    return data, y_array


def get_train_data(path='.'):
    f_name = 'data_train.csv'
    return _read_data(path, f_name)


def get_test_data(path='.'):
    f_name = 'data_test.csv'
    return _read_data(path, f_name)


def get_cv(X, y):
    cv = StratifiedShuffleSplit(n_splits=10, test_size=0.2, random_state=0)
    return cv.split(X, y)
