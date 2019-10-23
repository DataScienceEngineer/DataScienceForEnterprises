from common_utils import ServiceHelper
from prediction_service.constants import Constants


class PipelinePredictionContext(object):
    """Perform Basic Load,Predict Labels and get probabilities distributions from a Pipeline.
     Override this class to perform predictions on a pipeline"""
    def __init__(self):
        self.pipeLineFileName=None
        self.loadedPipeLine=None
        self.predictionLabels=None
        self.predictionProbabilities=None
        self.classes=None
        self.leafNumber=None

    def pipeline_load(self):
        """
        Load the Pipeline via a LRU cache

        :return: Pickle Object
        """
        self.loadedPipeLine= ServiceHelper.load_pipeline_cache(self.pipeLineFileName)

    def pipeline_predictLabels(self,dataFrame):
        """
        Perform Predictions based on the dataFrame

        :param dataFrame: feature list

        :return: Prediction lables
        """
        if hasattr(self.loadedPipeLine,'predict'):
            self.predictionLabels=self.loadedPipeLine.predict(dataFrame).tolist()
        else:
            raise PredictionContextError("predict method is not defined in the estimator algorithm "+str(type(self.loadedPipeLine.named_steps[Constants.PIPELINE_NAMED_STEP_MODEL])))

    def pipeline_probabilityDistribution(self,dataFrame):
        """
        Fetch Prediction Probababilities

        :param dataFrame: feature list

        :return: Prediction Probabilities
        """
        if hasattr(self.loadedPipeLine, "predict_proba"):
            self.predictionProbabilities = self.loadedPipeLine.predict_proba(dataFrame).tolist()
        else:
            raise PredictionContextError("predict_proba method is not defined in the estimator algorithm "+str(type(self.loadedPipeLine.named_steps[Constants.PIPELINE_NAMED_STEP_MODEL])))
        if hasattr(self.loadedPipeLine.named_steps[Constants.PIPELINE_NAMED_STEP_MODEL], "classes_"):
            self.classes=self.loadedPipeLine.named_steps[Constants.PIPELINE_NAMED_STEP_MODEL].classes_.tolist()
        else:
            raise PredictionContextError("classes_ variable is not defined in the estimator algorithm "+str(type(self.loadedPipeLine.named_steps[Constants.PIPELINE_NAMED_STEP_MODEL])))

    def getLeafNumber(self,dataFrame):
        """
        Return leaf numbers

        :param dataFrame: get leafnumbers from dataframe

        :return: returns leaf numbers
        """
        if hasattr(self.loadedPipeLine.named_steps[Constants.PIPELINE_NAMED_STEP_MODEL],"apply"):
            self.leafNumber =self.loadedPipeLine.named_steps[Constants.PIPELINE_NAMED_STEP_MODEL].apply(self.loadedPipeLine.named_steps[Constants.PIPELINE_NAMED_STEP_MAPPER].transform(dataFrame)).tolist()
        else:
            raise PredictionContextError("apply method is not defined in the estimator algorithm "+str(type(self.loadedPipeLine.named_steps[Constants.PIPELINE_NAMED_STEP_MODEL])))

class PredictionContextError(Exception):
    """
    Custom Exception Class
    """
    pass