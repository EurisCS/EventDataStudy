from dataclasses import dataclass


@dataclass
class PipelineOptimizeModel:

    name_optimizer: str = None
    name_model_to_optimize: str = None
    maximise_metric: bool = False

    def __post_init__(self):
        pass

    def run_optimisation(self):
        pass

    def make_dashboard_optimisation(self):
        pass


