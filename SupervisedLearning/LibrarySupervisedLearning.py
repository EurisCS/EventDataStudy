
class LoadObjectsForSupervisedLearning:

    @staticmethod
    def load_supervised_model(name_supervised_model, classification=True):

        if name_supervised_model is not None:
            name_supervised_model = name_supervised_model.replace('_', '').replace(' ', '').lower()

        # CLASSIFIER ##############################################################################################
        if classification:

            if name_supervised_model in ['svm', 'svc', None]:
                from sklearn.svm import SVC
                return SVC

            if name_supervised_model in ['rf', 'rfc', 'randomforest', 'randomforestclassifier']:
                from sklearn.ensemble import RandomForestClassifier
                return RandomForestClassifier

            if name_supervised_model in ['logreg', 'lr', 'logisticregression']:
                from sklearn.linear_model import LogisticRegression
                return LogisticRegression

            if name_supervised_model in ['xgb','xgbc' 'xgboost','xgboostc','xgboostclassifier']:
                from xgboost import XGBClassifier
                return XGBClassifier

            if name_supervised_model in ['xgbrf','xgboostrf', 'xgbrfc', 'xgboostrfc','xgboostrandomforestclassifier']:
                from xgboost import XGBRFClassifier
                return XGBRFClassifier

        # REGRESSOR ##############################################################################################
        else:
            if name_supervised_model in ['svm', 'svr', None]:
                from sklearn.svm import SVR
                return SVR

            if name_supervised_model in ['rf', 'rfr' 'randomforest', 'randomforestregressor']:
                from sklearn.ensemble import RandomForestRegressor
                return RandomForestRegressor

            if name_supervised_model in ['xgb','xgbr','xgboost','xgboostr','xgboostregressor']:
                from xgboost import XGBClassifier
                return XGBClassifier

            if name_supervised_model in ['xgbrf','xgboostrf', 'xgbrfr', 'xgboostrfr','xgboostrandomforestregressor']:
                from xgboost import XGBRFClassifier
                return XGBRFClassifier

    @staticmethod
    def load_cross_validation_object(name_type_cv):

        if type(name_type_cv) is not str:
            return name_type_cv

        name_type_cv = name_type_cv.replace('_', '').replace(' ', '').lower()

        if name_type_cv in ['skf', 'stratifiedkfold']:
            from sklearn.model_selection import StratifiedKFold
            return StratifiedKFold
        if name_type_cv in ['sss', 'stratifiedshufflesplit']:
            from sklearn.model_selection import StratifiedShuffleSplit
            return StratifiedShuffleSplit
        if name_type_cv in ['sgkf', 'stratifiedgroupkfold']:
            from sklearn.model_selection import StratifiedGroupKFold
            return StratifiedGroupKFold
        if name_type_cv in ['gkf', 'groupkfold']:
            from sklearn.model_selection import GroupKFold
            return GroupKFold
        if name_type_cv in ['kf', 'kfold']:
            from sklearn.model_selection import KFold
            return KFold