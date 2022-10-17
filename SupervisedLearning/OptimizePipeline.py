
class OptimizePipeline:

    def __init__(self, pipeline_to_tune, algorithm_genetic_or_RL_optimizer):
        self.model_to_optimize = pipeline_to_tune

        self.optimizer_function = algorithm_genetic_or_RL_optimizer

        self.list_params_scores = []
        self.max_len_list_scores = None # factor of cpu_count()

        self.threshold_score_stop = 0.99
        self.max_run = 10000

    def reset_object(self, threshold_score_stop=None, max_run=None):

        self.list_params_scores = []

        if threshold_score_stop is not None:
            self.threshold_score_stop = threshold_score_stop

        if max_run is not None:
            self.max_run = max_run

    def optimize_model(self, list_dict_param, data):

        # run the model
        for dict_param in list_dict_param:
            scores = self.model_to_optimize.run(dict_param)
            self.list_params_scores.append((dict_param,scores))

        # optimizer function -> generate new dict_params from the existing scores
        list_dict_param = self.optimizer_function.run(self.list_params_scores, self.max_len_list_scores)

        # exit condition
        if len(self.list_params_scores) < self.max_run or max(self.list_params_scores) > self.threshold_score_stop:
            return self.list_params_scores

        # do recursively
        return self.optimize_model(list_dict_param, data)


class GeneticOptimizer:

    def __init__(self):
        pass

    def sort_list_scores(self, list_params_scores, maximise=True):
        pass
# To move


# to dataclass to improve perf
class list_params_score:

    def __init__(self, maximise=True):
        self.list_dicts_params = []
        self.list_scores = []
        self.maximise = True

    def append(self, dict_params, score):
        self.list_dicts_params.append(dict_params)
        self.list_scores.append(score)

    def sort_list(self):
        pass

    # faire pour n
    def get_best_dict_param(self):
        if self.maximise:
            index_best = max(self.list_scores)
        else:
            index_best = min(self.list_scores)

        return self.list_dicts_params[index_best]
