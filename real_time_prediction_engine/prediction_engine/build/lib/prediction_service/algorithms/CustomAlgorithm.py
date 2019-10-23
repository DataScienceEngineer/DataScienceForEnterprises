from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin,TransformerMixin
import numpy as np

class Transform1(TransformerMixin):
    """
    An Example of custom Transformation. It must extend TransformerMixin class from sklearn.base and override fit() transform() method
    """
    def transform(self, X, *_):
        """
        perform transformation on X and return the transformed value

        :param X: Input arguments

        :param _: *_ ignore rest of the arguments if any

        :return: Transformed value
        """
        print("Inside Transform 1")
        return X
    def fit(self, *_):
        """
        fit() method

        :param _: *_ ignore arguments if any

        :return: class object itself
        """
        return self

class Transform2(TransformerMixin):
    """
    An Example of custom Transformation. It must extend TransformerMixin class from sklearn.base and override transform() method
    """
    def transform(self, X, *_):
        """
        perform transformation on X and return the transformed value

        :param X: Input arguments

        :param _: *_ ignore rest of the arguments if any

        :return: Transformed value
        """
        print("Inside Transform 2")
        return X
    def fit(self, *_):
        """
        fit() method

        :param _: *_ ignore arguments if any

        :return: class object itself
        """
        return self

class DummyClassifier(BaseEstimator,ClassifierMixin):
    """
    A Dummy Classifier algorithm extending BaseEstimator,ClassifierMixin from sklearn.base.
    It needs to override fit() and predict() method
    """
    def __init__(self):
        """
        Constructor of DummyClassifier.
        Initialize the member variables which can be used as model parameters during fitting and predicting
        """
        self.classes_=np.array([1,2])
    def fit(self, X, y=None):
        """
        Perform fitting with X features and y variable and update model params

        :param X: X features

        :param y: output variable

        :return: None
        """
        X = np.array(X).ravel()
        print("Inside fit() of DummyClassifier ")

    def predict(self,X):
        """
        Perform predictions for the fitted model

        :param X: features to predict labels

        :return: predictions
        """
        X = np.array(X).ravel()
        print("Inside predict() of DummyClassifier ")
        return np.array([1])

    def predict_proba(self,X):
        """
        Classification specific Function to generate probabilities of classes

        :param X: features to predict y

        :return: prediction probabilities
        """
        X = np.array(X).ravel()
        print("Inside predict_proba() of DummyClassifier")
        return np.array([0.7,0.6])


    def xyz(self):
        """
        User defined functions
        """
        print("Inside xyz")


class DummyRegressor(BaseEstimator,RegressorMixin):
    """
    A DummyRegressor algorithm extending BaseEstimator,RegressorMixin from sklearn.base.
    It needs to override fit() and predict() method
    """
    def __init__(self):
        """
        Constructor of DummyRegressor.
        Initialize the member variables which can be used as model parameters during fitting and predicting
        """
        print("HI")

    def fit(self, X, y=None):
        """
        Perform fitting with X features and y variable and update model params

        :param X: X features

        :param y: output variable

        :return: None
        """
        pass

    def predict(self,X):
        """
        Perform predictions for the fitted model

        :param X: features to predict labels

        :return: predictions
        """
        return np.array([{"status":"done"}])


