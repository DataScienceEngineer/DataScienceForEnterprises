from ml_automation.model_predictors.ModelPredictorTemplate import ModelPredictorTemplate
from typing import Dict
from ml_automation.core.contexts import ModelPredictorContext
from ml_automation.housing_price_prediction.core_functions import *


class HousePredictionPredictor(ModelPredictorTemplate):
    """
    Implementation example of ModelPredictor by extending ModelPredictorTemplate
    """
    def performModelPredictions(self,model_file_paths:Dict,preprocessed_df:pd.DataFrame,additional_params:Dict,model_predictor_context:ModelPredictorContext):
        return pd.DataFrame(np.exp(predict(filename=model_file_paths['lasso_file'],
                              scalerfile=additional_params['scaler_file'],
                              df=preprocessed_df[additional_params['features']])))
