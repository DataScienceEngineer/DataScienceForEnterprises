# ==== EXAMPLE OF PREPROC FUNCTIONS SCRIPT ========

import pandas as pd
import numpy as np

# to divide train and test set
from sklearn.model_selection import train_test_split

# feature scaling
from sklearn.preprocessing import StandardScaler

# to build the models
from sklearn.linear_model import LinearRegression, Lasso

# to evaluate the models
from sklearn.metrics import mean_squared_error

from preprocessing_functions import *
#=========== training pipeline ======
# First lets get the file path
DATASET_FOLDER = "DataSets"    # Read from yaml file
data_filename = "Housing_Data.csv"   # Read from yaml file
yaml_target_name = "SalePrice"   # Read from yaml file
df_path = os.path.join(os.getcwd(), DATASET_FOLDER, data_filename)   # Path to read data file
output_path_in_yaml = os.path.join(os.getcwd(), DATASET_FOLDER)

df = load_data(df_path)   # Load the data
train, test, y_train, y_test = divide_train_test(df, yaml_target_name)  # Split the data

features_list = ['MSSubClass', 'MSZoning', 'LotArea', 'LotShape', 'OverallQual', 'OverallCond',
            'YearBuilt', 'YearRemodAdd', 'MasVnrArea', 'BsmtFinSF1', '1stFlrSF', '2ndFlrSF',
            'GrLivArea', 'BsmtFullBath', 'FullBath', 'HalfBath', 'Functional', 'Fireplaces',
            'GarageCars', 'WoodDeckSF', 'ScreenPorch', 'GarageYrBlt_na', 'LotFrontage']


# Categorical ['MSZoning', 'LotShape', 'Functional']
train['MSZoning'] = remove_categorical_na(train['MSZoning'])
train['LotShape'] = remove_categorical_na(train['LotShape'])
train['Functional'] = remove_categorical_na(train['Functional'])


# Numerical ['MSSubClass', 'LotFrontage', 'LotArea', 'OverallQual',
# 'OverallCond', 'YearBuilt', 'YearRemodAdd', 'MasVnrArea', 'BsmtFinSF1',
# '1stFlrSF', '2ndFlrSF', 'GrLivArea', 'BsmtFullBath', 'FullBath', 'HalfBath',
# 'Fireplaces', 'GarageCars', 'WoodDeckSF', 'ScreenPorch']
train['MSSubClass'] = remove_numerical_na(train, 'MSSubClass', mean_val1_in_yaml)
train['LotFrontage'] = remove_numerical_na(train, 'LotFrontage', mean_val1_in_yaml)
train['LotArea'] = remove_numerical_na(train, 'LotArea', mean_val1_in_yaml)
train['OverallQual'] = remove_numerical_na(train, 'OverallQual', mean_val1_in_yaml)
train['OverallCond'] = remove_numerical_na(train, 'OverallCond', mean_val1_in_yaml)
train['MasVnrArea'] = remove_numerical_na(train, 'MasVnrArea', mean_val1_in_yaml)
train['BsmtFinSF1'] = remove_numerical_na(train, 'BsmtFinSF1', mean_val1_in_yaml)
train['1stFlrSF'] = remove_numerical_na(train, '1stFlrSF', mean_val1_in_yaml)
train['2ndFlrSF'] = remove_numerical_na(train, '2ndFlrSF', mean_val1_in_yaml)
train['GrLivArea'] = remove_numerical_na(train, 'GrLivArea', mean_val1_in_yaml)
train['BsmtFullBath'] = remove_numerical_na(train, 'BsmtFullBath', mean_val1_in_yaml)
train['FullBath'] = remove_numerical_na(train, 'FullBath', mean_val1_in_yaml)
train['HalfBath'] = remove_numerical_na(train, 'HalfBath', mean_val1_in_yaml)
train['Fireplaces'] = remove_numerical_na(train, 'Fireplaces', mean_val1_in_yaml)
train['GarageCars'] = remove_numerical_na(train, 'GarageCars', mean_val1_in_yaml)
train['WoodDeckSF'] = remove_numerical_na(train, 'WoodDeckSF', mean_val1_in_yaml)
train['ScreenPorch'] = remove_numerical_na(train, 'ScreenPorch', mean_val1_in_yaml)

_junk, train['GarageYrBlt_na'] = remove_numerical_na_extravar(train, "GarageYrBlt", repl_type="mode")

train['YearBuilt'] = elapsed_years(train, 'YearBuilt', 'YrSold')
train['YearRemodAdd'] = elapsed_years(train, 'YearRemodAdd', 'YrSold')


# Skewed cols ['LotFrontage', 'LotArea', '1stFlrSF', 'GrLivArea', 'SalePrice']
train['LotFrontage'] = transform_skewed_variables(train, "LotFrontage")
train['LotArea'] = transform_skewed_variables(train, "LotArea")
train['1stFlrSF'] = transform_skewed_variables(train, "1stFlrSF")
train['GrLivArea'] = transform_skewed_variables(train, "GrLivArea")
train['SalePrice'] = transform_skewed_variables(train, "SalePrice")


# Replace rare labels with "rare" category, ['MSZoning', 'LotShape', 'Functional']
frequent_ls = find_frequent_labels(train, "MSZoning", 0.05)
train['MSZoning'] = remove_rare_labels(train, "MSZoning", frequent_ls)

frequent_ls = find_frequent_labels(train, "LotShape", 0.05)
train['LotShape'] = remove_rare_labels(train, "LotShape", frequent_ls)

frequent_ls = find_frequent_labels(train, "LotShape", 0.05)
train['LotShape'] = remove_rare_labels(train, "LotShape", frequent_ls)


# Ordinal Encoding, ['MSZoning', 'LotShape', 'Functional']
train["MSZoning"] = ordinal_encoding(train, "MSZoning", yaml_target_name)
train["LotShape"] = ordinal_encoding(train, "LotShape", yaml_target_name)
train["Functional"] = ordinal_encoding(train, "Functional", yaml_target_name)


# Feature scaling of variables
scaler = train_scaler(train[features], output_path_in_yaml)

lin_model = train_model(train, y_train, features, scaler, output_path_in_yaml)

#== END
# train[var5] = cap_outliers(train, var5, cap_value_in_yaml, bigger_than=False)
