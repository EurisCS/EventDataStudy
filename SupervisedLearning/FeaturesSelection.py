
## NOT USED --> SHIT

class FeaturesSelection:

    @staticmethod
    def __call__(name_test):
        if name_test is not  None:
            name_test = name_test.replace('_', '').replace(' ', '').lower()

        if name_test in ['rfe', None]:
            from sklearn.feature_selection import RFE
            return RFE

        if name_test in ['rfecv']:
            from sklearn.feature_selection import RFECV
            return RFECV

        if name_test in ['kbest' ,'selectkbest']:
            from sklearn.feature_selection import SelectKBest
            return SelectKBest


class StatisticTest:

    def __init__(self, name_test, dict_param=None):

        self.statistic_test = FeaturesSelection()(name_test)

        if dict_param is not None:
            self.statistic_test.set_params(dict_param)

    def fit_transform(self, data, label=None):
        return self.statistic_test.fit_transform(data, label)
