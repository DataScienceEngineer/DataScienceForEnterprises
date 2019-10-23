import os
import json
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso



def load_data(df_path):
    return pd.read_csv(df_path)


def divide_train_test(filename="Housing_Data.csv"):
    df = load_data(filename)
    train, test = train_test_split(df, test_size=0.2, random_state=0)
    train.to_csv("train.csv", index=False)
    test.to_csv("test.csv", index=False)
    return train, test

def remove_categorical_na(df, var):
    return df[var].fillna('Blank')


def savejsonfile(data, filename):
    with open(filename, 'w') as f:
      json.dump(data, f, ensure_ascii=False)


def readjsonfile(filename):
    with open(filename, encoding='utf-8', errors='ignore') as f:
        data = json.load(f, strict=False)
        return data


def find_frequent_labels(df, var,predictor_var, rare_perc):
    df = df.copy()
    tmp = df.groupby(var)[predictor_var].count() / len(df)
    return tmp[tmp>rare_perc].index


def remove_rare_labels(df, var, frequent_labels):
    return np.where(df[var].isin(frequent_labels), df[var], 'Rare')


def ordinal_encoding(df, var, target, ordinal_label=None):
    if ordinal_label == None:
        ordered_labels = df.groupby([var])[target].mean().sort_values().index
        ordinal_label = {k: i for i, k in enumerate(ordered_labels, 0)}
        df[var] = df[var].map(ordinal_label)
        return df[var], ordinal_label
    df[var] = df[var].map(ordinal_label)
    return df[var]


def elapsed_years(df, var, basevar):
    df[var] = df[basevar] - df[var]
    return df[var]


def remove_numerical_na(df, var, repl_type="mode"):
    if repl_type == "mode":
        repl_val = df[var].mode()[0]
        return df[var].fillna(repl_val), repl_val
    elif repl_type == "mean":
        repl_val = df[var].mean()
        return df[var].fillna(repl_val), repl_val
    else:
        repl_val = repl_type
        return df[var].fillna(repl_val)

def transform_skewed_variables(df, var):
    return np.log(df[var])


def cap_outliers(df, var, cap, bigger_than=False):
    if bigger_than:
        capped_var = np.where(df[var] > cap, cap, df[var])
    else:
        capped_var = np.where(df[var] < cap, cap, df[var])
    return capped_var


#Data Loading
def load_modeldata(folder_path, predictor_var, type="train", filename=None, testfilename=None):
    if type == "train":
        df = load_data(os.path.join(folder_path, filename))
        train, test, y_train, y_test = divide_train_test(df, predictor_var)  # Split the data
        test.to_csv(os.path.join(folder_path, testfilename), index=False)
        return train, test, y_train, y_test
    elif type == "predict":
        df = load_data(os.path.join(folder_path, filename))   # Just separate columns and send the DF
        y_train = df[predictor_var]
        # train = df.drop([predictor_var], axis=1)
        return df, y_train
    else:
        print("Wrong argument chosen for type in function load_modeldata")

#Categorical Variable Engineering
# Categorical ['MSZoning', 'LotShape', 'Functional']
def feature_enggCatvars(catvars, df, cat_freq_labels_json, ordinal_labels_json, predictor_var, type="train"):
    if type == "train":
        catvarslabelsidct = {}
        ordinal_labeldict = {}
        for var in catvars:
            df[var] = remove_categorical_na(df, var)   # Replace na with "Blank" in the Categorical DFs

            frequent_ls = find_frequent_labels(df, var,predictor_var, 0.05) # Replace rare labels with "rare" category
            df[var] = remove_rare_labels(df, var, frequent_ls)
            catvarslabelsidct[var]=frequent_ls.values.tolist()   # Persist the labels to use during testing

            df[var], ordinal_label = ordinal_encoding(df, var, predictor_var) # Ordinal Encoding
            ordinal_labeldict[var]=ordinal_label

        savejsonfile(catvarslabelsidct, filename=cat_freq_labels_json)  # Save categorical labels list for using in prediction
        savejsonfile(ordinal_labeldict, filename=ordinal_labels_json)  # Save ordinal labels list for using in prediction
        return df[catvars]
    elif type == "predict":
        catvarslabelsidct = readjsonfile(filename=cat_freq_labels_json)
        ordinal_labeldict = readjsonfile(filename=ordinal_labels_json)
        for var in catvars:
            df[var] = remove_categorical_na(df, var)   # Replace na with "Blank" in the Categorical DFs

            frequent_ls = catvarslabelsidct.get(var)
            df[var] = remove_rare_labels(df, var, frequent_ls)

            ordinal_label =  ordinal_labeldict.get(var)
            df[var] = ordinal_encoding(df, var, predictor_var, ordinal_label=ordinal_label) # Ordinal Encoding
        return  df[catvars]
    else:
        print("Wrong argument chosen for type in function feature_enggCatvars")

#Temporal variable engineering
def feature_enggTemporalvars(df, temporalvars, basevar):
    for var in temporalvars:
        df[var] = elapsed_years(df, var, basevar)
    return  df

#Extra features addition
def feature_enggExtrafeature(df):
    return np.where(df.isnull(), 1, 0)

#Numerical variable engineering
def feature_enggNumvars(df, numvars,mean_value_json, type):
    if type == "train":
        meanvaldict = {}
        for var in numvars:
            df[var], meanval = remove_numerical_na(df, var, repl_type="mode")
            meanvaldict[var] = float(meanval)
        savejsonfile(meanvaldict, filename=mean_value_json)
        return df
    elif type == "predict":
        meanvaldict = readjsonfile(filename=mean_value_json)
        for var in numvars:
            meanval = meanvaldict.get(var)
            df[var] = remove_numerical_na(df, var, repl_type=meanval)
        return df
    else:
        print("Wrong argument chosen for type in function feature_enggNumvars")

#Skewed variable engineering
def feature_enggSkewedvars(df, skewedvars):
    for var in skewedvars:
        df[var] = transform_skewed_variables(df, var)
    return df

#Training and Deploying Model
def train_scaler(df, filename):
    scaler = MinMaxScaler()
    scaler.fit(df)
    joblib.dump(scaler, filename)
    return scaler


def train_model(df, features, target, scaler, filename):
    lin_model = Lasso(alpha=0.005, random_state=0)
    lin_model.fit(scaler.transform(df[features]), target)
    joblib.dump(lin_model,filename)
    return lin_model


def scale_features(df, folder_path, filename):
    scaler = joblib.load(os.path.join(folder_path, filename))  # with joblib
    return scaler.transform(df)


def predict(filename, scalerfile, df=None):
    lin_model = joblib.load(filename)
    scaler = joblib.load(scalerfile)
    return lin_model.predict(scaler.transform(df))