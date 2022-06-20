import numpy as np
import pandas as pd
from sklearn.compose import make_column_selector, make_column_transformer
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.preprocessing import RobustScaler, OneHotEncoder
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from scipy.sparse import hstack, coo_matrix


class LoadPreprocessorObjects:

    @staticmethod
    def load_scaler(scaler):
        if scaler is not None:
            scaler = scaler.replace('_', '').replace(' ', '').lower()

        if scaler in ['robust', 'robustscaler', None]:
            from sklearn.preprocessing import RobustScaler
            return RobustScaler(quantile_range=(25.0, 75.0))

        if scaler in ['standard', 'standardscaler']:
            from sklearn.preprocessing import StandardScaler
            return StandardScaler()

        if scaler in ['minmax', 'minmaxscaler']:
            from sklearn.preprocessing import MinMaxScaler
            return MinMaxScaler()

    @staticmethod
    def load_encoder(encoder):
        if encoder is not None:
            encoder = encoder.replace('_', '').replace(' ', '').lower()

        if encoder in ['onehot', 'onehotencoder']:
            from sklearn.preprocessing import OneHotEncoder
            return OneHotEncoder()
        if encoder in ['label', 'labelencoder']:
            from sklearn.preprocessing import LabelEncoder
            return LabelEncoder()

    @staticmethod
    def load_imputer(imputer):
        if imputer is not None:
            imputer = imputer.replace('_', '').replace(' ', '').lower()

        if imputer in ['knn', 'knnimputer']:
            from sklearn.impute import KNNImputer
            return KNNImputer()

        if imputer in ['simple', 'simpleimputer', None]:  # passer None si possible
            from sklearn.impute import SimpleImputer
            return SimpleImputer(strategy='constant', fill_value='null')


class Preprocessing:

    # PREPROCESSORS ################################################################################################

    # need to be change the init if you want another preprocessing
    def __init__(self, scaler='robust', encoder='onehot', impute_num='knn', impute_cat='simple'):

        loader = LoadPreprocessorObjects()

        self._num_features = make_column_selector(dtype_include=np.number)
        self._cat_features = make_column_selector(dtype_exclude=np.number)

        self.impute_missing_numerical_value = loader.load_imputer(impute_num)
        self.impute_missing_categorical_value = loader.load_imputer(impute_cat)

        self.scaler = loader.load_scaler(scaler)
        self.encoder = loader.load_encoder(encoder)

    def _create_numerical_preprocessor(self):
        numerical_pipeline = make_pipeline(self.impute_missing_numerical_value, self.scaler)
        return make_column_transformer((numerical_pipeline, self._num_features))

    def _create_categorical_preprocessor(self):
        categorical_pipeline = make_pipeline(self.impute_missing_categorical_value, self.encoder)
        return make_column_transformer((categorical_pipeline, self._cat_features))

    # UNLABELLED ################################################################################################

    def preprocessing_data_unlabelled(self, data, out_format='array'):

        numerical_preprocessor = self._create_numerical_preprocessor()
        data_num = numerical_preprocessor.fit_transform(data)

        categorical_preprocessor = self._create_categorical_preprocessor()
        data_cat = categorical_preprocessor.fit_transform(data)

        if out_format.lower() == 'dataframe':
            return pd.DataFrame(hstack([coo_matrix(data_num), coo_matrix(data_cat)], format='array'))

        return hstack([coo_matrix(data_num), coo_matrix(data_cat)], format=out_format)

    # LABELLED ################################################################################################

    def preprocessing_labelled_data_into_train_test_set(self, X_data, y_data, test_size=0.20, random_state=42,
                                                        out_format='array', for_classification=True):

        y_data = np.ravel(y_data)

        stratify = None
        if for_classification:
            stratify = y_data

        X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=test_size,
                                                            random_state=random_state, stratify=stratify)

        # NUM : fit on X_train & transform on X_train/X_test
        numerical_preprocessor = self._create_numerical_preprocessor()
        X_train_num = numerical_preprocessor.fit_transform(X_train)
        X_test_num = numerical_preprocessor.transform(X_test)

        # CAT : fit on X & transform on X_train/X_test
        categorical_preprocessor = self._create_categorical_preprocessor()
        categorical_preprocessor.fit(X_data)
        X_train_cat = categorical_preprocessor.transform(X_train)
        X_test_cat = categorical_preprocessor.transform(X_test)

        # merge categorical and numerical data ... NEED TO CHANGE THE FORMAT, can SCIPY MATRIX
        X_train = hstack([coo_matrix(X_train_cat), coo_matrix(X_train_num)], format='array')
        X_test = hstack([coo_matrix(X_test_cat), coo_matrix(X_test_num)], format='array')

        if out_format.lower() == 'dataframe':
            return pd.DataFrame(X_train), pd.DataFrame(X_test), pd.DataFrame(y_train), pd.DataFrame(y_test)

        return X_train, X_test, y_train, y_test

    def preprocessing_labelled_data_into_train_set(self, X_data, y_data, out_format='array'):

        y_data = np.ravel(y_data)

        # NUM : fit on X_train & transform on X_train/X_test
        numerical_preprocessor = self._create_numerical_preprocessor()
        X_num = numerical_preprocessor.fit_transform(X_data)

        # CAT : fit on X & transform on X_train/X_test
        categorical_preprocessor = self._create_categorical_preprocessor()
        X_cat = categorical_preprocessor.fit_transform(X_data)

        X_data = hstack([coo_matrix(X_cat), coo_matrix(X_num)], format='array')

        if out_format.lower() == 'dataframe':
            return pd.DataFrame(X_data), pd.DataFrame(y_data)

        return X_data, y_data



    #
    # can add after :
    #  from sklearn.model_selection import TimeSeriesSplit
