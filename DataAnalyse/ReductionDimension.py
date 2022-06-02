import pandas as pd


# can add other reduction dimension with this method

class ReductionDimensionUmap:

    def __init__(self, type_reduction='umap', dict_param=None):

        # chose r_dim algorithm

        if type_reduction.lower() in ['umap', None]:
            from umap import UMAP
            self.reducer = UMAP

        elif type_reduction.lower() in ['aligned', 'aligned_umap']:
            from umap import AlignedUMAP
            self.reducer = AlignedUMAP

        elif type_reduction.lower() in ['parametric', 'parametric_umap']:
            from umap import ParametricUMAP
            self.reducer = ParametricUMAP

        # dict param  (change ?)
        self.dict_param = dict_param
        if self.dict_param in [None, '']:
            self.dict_param = {}

    def run(self, data_to_transform, output_dimension=3, raw_output_returned=True, column_color=None):

        X_transformed = \
            self.reducer(n_components=output_dimension, **self.dict_param).fit_transform(data_to_transform)

        # raw output has priority over column color
        if raw_output_returned:
            return X_transformed

        if column_color is None:
            return pd.DataFrame(X_transformed)

        return self.concatenate_column_color_to_transformed_data(X_transformed, column_color)

    @staticmethod
    def concatenate_column_color_to_transformed_data(X_transformed, column_color):
        df_color = pd.DataFrame(column_color).reset_index(drop=True).rename(columns={0: 'color'})
        return pd.concat([pd.DataFrame(X_transformed), df_color], axis=1)

