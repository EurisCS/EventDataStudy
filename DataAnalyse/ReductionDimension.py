import pandas as pd


# can add other reduction dimension with this method

class LoadReducerProgram:

    def __call__(self, name_reducer_program):

        if name_reducer_program.lower() in ['umap', None]:
            from umap import UMAP
            return UMAP

        elif name_reducer_program.lower() in ['aligned', 'aligned_umap']:
            from umap import AlignedUMAP
            return AlignedUMAP

        elif name_reducer_program.lower() in ['parametric', 'parametric_umap']:
            from umap import ParametricUMAP
            return ParametricUMAP

        elif name_reducer_program.lower() in ['tsne', ]:
            from sklearn.manifold import TSNE
            return TSNE


class ReductionDimensionUmap:

    def __init__(self, name_reducer_program='umap', dict_param=None):

        # chose r_dim program
        self.reducer = LoadReducerProgram()(name_reducer_program)

        # dict param
        self.dict_param = {} if dict_param in [None, ''] else dict_param

    def run(self, data_to_transform, output_dimension=3, raw_output_returned=True, column_color=None):

        X_transformed = \
            self.reducer(n_components=output_dimension, **self.dict_param).fit_transform(data_to_transform)

        # raw output has priority over column color
        if raw_output_returned:
            return X_transformed

        if column_color is None:
            return pd.DataFrame(X_transformed)

        return self.concatenate_column_labels_to_transformed_data(X_transformed, column_color)

    @staticmethod
    def concatenate_column_labels_to_transformed_data(X_transformed, column_labels):
        df_color = pd.DataFrame(column_labels).reset_index(drop=True).rename(columns={0: 'labels'})
        return pd.concat([pd.DataFrame(X_transformed), df_color], axis=1)
