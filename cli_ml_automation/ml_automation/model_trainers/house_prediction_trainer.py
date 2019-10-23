from ml_automation.model_trainers.ModelTrainerTemplate import ModeltrainerTemplate
from common_utils.MLLogger import MLLogging
from typing import Dict
from ml_automation.core.contexts import ModelGeneratorContext
from ml_automation.housing_price_prediction.core_functions import *
logger=MLLogging.getLog()
class HousePredictionTrainer(ModeltrainerTemplate):
    """
    Implementation example of Modeltrainer by extending ModeltrainerTemplate
    """
    def performModelTraining(self, preprocessed_df:pd.DataFrame, model_target_file_path:str, additional_params:Dict, model_generator_context:ModelGeneratorContext):
        scaler = train_scaler(preprocessed_df[additional_params['features']],
                              filename=additional_params["scaler_file"])
        train_model(preprocessed_df[additional_params['features']],
                    additional_params['features'],
                    target=preprocessed_df[additional_params['predictor_var']],
                    scaler=scaler,
                    filename=model_target_file_path)

