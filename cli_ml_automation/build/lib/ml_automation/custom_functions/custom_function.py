from ml_automation.custom_functions.CustomFunctionTemplate import CustomFunctionTemplate
from common_utils.MLLogger import MLLogging
from typing import Dict
logger=MLLogging.getLog()
class DummyCustomTemplate(CustomFunctionTemplate):
    """
    Implementation example of Custom Function by extending CustomFunctionTemplate
    """
    def performOperation(self, arguments:Dict):
        return None