from ml_automation.custom_functions.CustomFunctionTemplate import CustomFunctionTemplate
from common_utils.MLLogger import MLLogging
from typing import Dict
import pandas as pd
logger=MLLogging.getLog()

class send_dict_from_csvfile(CustomFunctionTemplate):
    """
    Implementation example of Custom Function by extending CustomFunctionTemplate
    """
    def performOperation(self, arguments:Dict):
        df= pd.read_csv(filepath_or_buffer=arguments['filepath'])
        return df.to_dict('list')