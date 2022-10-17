import random

# from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.model_selection import cross_validate, StratifiedKFold, learning_curve

from statistics import stdev
from numpy import linspace
from Utilities.FileManipulation import store_object_as_pickle, create_directory

from LibrarySupervisedLearning import LoadObjectsForSupervisedLearning

class SupervisedLearning:

    def __init__(self, name_model, classification=True, dict_param_model=None):

        if dict_param_model is None:
            dict_param_model = {}

        self.name_model = name_model

        self.objects_loader = LoadObjectsForSupervisedLearning()
        self.model = self.objects_loader.load_supervised_model(name_model, classification)()
        self.model.set_params(**dict_param_model)

    # BASC FITTING  #################################################################################################

    def fit(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    # CROSS VALIDATE FITTING  #####################################################################################

    def repeated_cross_validate_fitting(self, X_train, y_train, repeat_experience=10, nb_cv=5,
                                        type_cv_or_name_type_cv='StratifiedKFold', metric_scoring='accuracy',
                                        save_path_estimator=None):

        type_cv_or_name_type_cv = self.objects_loader.load_cross_validation_object(type_cv_or_name_type_cv)

        if repeat_experience is None:
            repeat_experience = 1

        if save_path_estimator is not None:
            create_directory(save_path_estimator)

        list_dict_results = []
        for counter in range(repeat_experience):
            # random_state = random.randint(1, 5 * repeat_experience),
            list_dict_results.append(self.cross_validate_fitting(X_train, y_train, nb_cv, type_cv_or_name_type_cv,
                                                                 metric_scoring,save_path_estimator, counter))
        return list_dict_results

    def cross_validate_fitting(self, X_train, y_train, nb_cv=5, name_type_cv_or_type_cv=StratifiedKFold,
                               scoring='accuracy', path_store_estimator=None, counter_repeat=None):

        return_estimator = False if path_store_estimator is None else True

        type_cv = self.objects_loader.load_cross_validation_object(name_type_cv_or_type_cv)
        cross_val = nb_cv
        if type_cv is not None:
            cross_val = type_cv(nb_cv, shuffle=True)

        dict_results = cross_validate(self.model, X=X_train, y=y_train, cv=cross_val, scoring=(scoring, 'r2'),
                                      return_train_score=True, return_estimator=return_estimator)
        print(scoring)
        for i in dict_results:
            print(f'{i} : {dict_results[i]}')
        dict_results = self.treatment_results_cross_validate(dict_results)

        if path_store_estimator is not None:
            self.store_list_estimators_object(dict_results.pop('list_estimator'),
                                              f'{path_store_estimator}_{counter_repeat}')

        dict_results['name_model'] = f'{self.name_model}_{counter_repeat}'
        return dict_results

    @staticmethod
    def treatment_results_cross_validate(dict_results):

        # train score
        dict_results['train_score_mean'] = dict_results['train_score'].mean()
        dict_results['st_dev_train_score'] = stdev(dict_results['train_score'])

        # validate score
        dict_results['validate_score'] = dict_results.pop('test_score')
        dict_results['validate_score_mean'] = dict_results['validate_score'].mean()
        dict_results['st_dev_validate_score'] = stdev(dict_results['validate_score'])

        return dict_results

    # LEARNING CURVE  #####################################################################################

    def learning_curve(self, X_train, y_train, nb_cv=5, type_cv=StratifiedKFold, nb_slot=10):

        cv = nb_cv
        if type_cv is not None:
            cv = type_cv(nb_cv)

        nb_data_by_slot, train_score, val_score = learning_curve(self.model, X_train, y_train, cv=cv,
                                                                 train_sizes=linspace(0.1, 1.0, nb_slot))

        return nb_data_by_slot, train_score, val_score

    def predict(self, X_test):
        return self.model.predict(X_test)

    # STORE ESTIMATORS / MODELS  #####################################################################################

    @staticmethod
    def store_list_estimators_object(list_estimator, save_path):
        create_directory(save_path)
        for counter in range(len(list_estimator)):
            store_object_as_pickle(list_estimator[counter], f'{save_path}/estimator_{counter}.pickle')


'''
# TO move : the main pipeline
class TestPipelineSupervisedLearning:


    def __init__(self):
        pass


    def create_dataframe_results(self):
        pass

    def save_model_as_pickle(self, model):
        pass


    def make_stdev_results_scatter(self):
        import plotly.graph_objects as go

        fig = go.Figure()

        fig.add_scatter(x='', y='', mode='markers',name='',
                        error_y=dict(type='data', array=list(dict_stdev_train_score.values()), visible=True)))

        fig.add_scatter(x=list(dict_validate_score.keys()), y=list(dict_validate_score.values()), mode='markers',
                        name='validate_score',
                        error_y=dict(type='data', array=list(dict_stdev_validate_score.values()), visible=True))
        fig.show()
'''
