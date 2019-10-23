from abc import ABC,abstractmethod
from typing import Dict
class CustomFunctionTemplate(ABC):
    @abstractmethod
    def performOperation(self,arguments:Dict):
        """
        Perform user defined operations in this function

        :param arguments: Contains arguments for the function

        :return: optional string with arguments
        """
        pass