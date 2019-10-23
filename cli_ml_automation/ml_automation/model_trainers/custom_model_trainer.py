from ml_automation.model_trainers.ModelTrainerTemplate import ModeltrainerTemplate
from sklearn.externals import joblib
from sklearn import svm
from sklearn import datasets
from sklearn import tree
from common_utils.MLLogger import MLLogging
from typing import Dict
import pandas as pd
from ml_automation.core.contexts import ModelGeneratorContext
logger=MLLogging.getLog()
class TestModelTrainer(ModeltrainerTemplate):
    """
    Implementation example of Modeltrainer by extending ModeltrainerTemplate
    """
    def performModelTraining(self, preprocessed_df:pd.DataFrame, model_target_file_path:str, additional_params:Dict, model_generator_context:ModelGeneratorContext):
        model_generator_context.variable=[1, 2, 3]
        clf = svm.SVC()
        iris = datasets.load_iris()
        X, y = iris.data, iris.target
        clf.fit(X, y)
        joblib.dump(clf, model_target_file_path)
        model_generator_context.model=clf
        #print(training_dfs)
        return "Success"

class TestModelTrainer2(ModeltrainerTemplate):
    """
    Implementation example of Modeltrainer by extending ModeltrainerTemplate
    """
    def performModelTraining(self,preprocessed_df:pd.DataFrame,model_target_file_path:str,additional_params:Dict,model_generator_context:ModelGeneratorContext):
        model_generator_context.variable.append(5)
        #print(modelGeneratorContext.model)
        model_generator_context.model=tree.DecisionTreeClassifier()
        joblib.dump(model_generator_context.model, model_target_file_path)
        #raise Exception("Failed to create model file")
        return "Success"
class TestModelTrainer3(ModeltrainerTemplate):
    """
    Implementation example of Modeltrainer by extending ModeltrainerTemplate
    """
    def performModelTraining(self,preprocessed_df:pd.DataFrame,model_target_file_path:str,additional_params:Dict,model_generator_context:ModelGeneratorContext):
        #print(modelGeneratorContext.variable)
        #print(modelGeneratorContext.model)
        joblib.dump(model_generator_context.model, model_target_file_path)
        return "Success"

