from ml_automation.model_predictors.ModelPredictorTemplate import ModelPredictorTemplate
from typing import Dict
import pandas as pd
from ml_automation.core.contexts import ModelPredictorContext


class TestModelPredictor(ModelPredictorTemplate):
    """
    Implementation example of ModelPredictor by extending ModelPredictorTemplate
    """
    def performModelPredictions(self,model_file_paths:Dict,preprocessed_df:pd.DataFrame,additional_params:Dict,model_predictor_context:ModelPredictorContext):
        pass
        return preprocessed_df