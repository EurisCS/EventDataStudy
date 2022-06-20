import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

import plotly.express as px
import plotly.graph_objects as go

from Utilities.FileManipulation import get_extension_into_path
from FileManipulation import store_object_as_pickle


class VisualiseDataPlotlyExpress:

    # STORE ############################################################################################

    def store_or_return_object(self, figure, save_path):
        if save_path is None:
            return figure
        self.store_figure(figure, save_path)

    @staticmethod
    def store_figure(figure, save_path):

        # recover the extension with the dot
        extension = get_extension_into_path(save_path)

        if extension in ['html', '.html']:
            figure.write_html(save_path)
        elif extension in ['json', '.json']:
            figure.write_json(save_path)
        elif extension in ['png', '.png']:
            figure.write_image(save_path)
        elif extension in ['pickle', '.pickle']:
            store_object_as_pickle(figure, save_path)

    # SCATTER PLOT : 1D - 2D - 3D - TERNARY - MATRIX #################################################################

    # 1D
    def create_scatter_plot_1D(self, series_x, series_color=None, save_path=None):
        figure = px.scatter(x=series_x, color=series_color)
        return self.store_or_return_object(figure, save_path)

    # 2D
    def create_scatter_plot_2D(self, series_x, series_y, series_color=None, save_path=None):
        figure = px.scatter(x=series_x, y=series_y, color=series_color, symbol=series_color,
                            color_continuous_scale='Portland') # ,template="seaborn")
        figure.update(layout_showlegend=False)
        figure.update(layout_coloraxis_showscale=True)
        return self.store_or_return_object(figure, save_path)

    # 3D
    def create_scatter_plot_3D(self, series_x, series_y, series_z, series_color=None, save_path=None):
        figure = px.scatter_3d(x=series_x, y=series_y, z=series_z, color=series_color, symbol=series_color,
                               color_continuous_scale='Portland')
        return self.store_or_return_object(figure, save_path)

    # 2D
    def create_scatter_ternary(self, series_x, series_y, series_z, series_color=None, save_path=None):
        figure = px.scatter_ternary(a=series_x, b=series_y, c=series_z, color=series_color)
        return self.store_or_return_object(figure, save_path)

    # 2D
    def create_scatter_matrix(self, data, series_color=None, save_path=None):
        figure = px.scatter_matrix(data, color=series_color)
        figure.update_traces(diagonal_visible=False)
        return self.store_or_return_object(figure, save_path)

    # SCATTER LINE : 2D - 3D #########################################################################################

    def create_scatter_line_2D_old(self, series_x, series_y, series_color=None, save_path=None):
        figure = px.line(x=series_x, y=series_y, color=series_color, symbol=series_color)
        return self.store_or_return_object(figure, save_path)

    def create_scatter_line_3D_old(self, series_x, series_y, series_z, series_color=None, save_path=None):
        figure = px.line_3d(x=series_x, y=series_y, z=series_z, markers=True, color=series_color, symbol=series_color)
        return self.store_or_return_object(figure, save_path)

    def create_scatter_line_2D_3D_color_discrete(self, series_x, series_y, series_z=None, series_color=None,
                                                 save_path=None):

        # convert series_x to pd.Series
        if type(series_x) in [list, np.ndarray]:
            series_x = pd.Series(series_x)

        # convert series_y to pd.Series
        if type(series_y) in [list, np.ndarray]:
            series_y = pd.Series(series_y)

        if series_z is None:
            dict_marker = dict(size=10)
        else:
            dict_marker = dict(size=3)
            if type(series_z) in [list, np.ndarray]:
                series_z = pd.Series(series_z)  # convert series_z to pd.Series

        # create figure
        figure = go.Figure()

        if series_color is not None:  # colored case

            # convert series_color to pd.Series
            if type(series_color) in [list, np.ndarray]:
                series_color = pd.Series(series_color)

            # encode series_color
            encoder = LabelEncoder()
            series_color_encoded = pd.Series(encoder.fit_transform(series_color))

            # add a scatter line in grey
            if series_z is None:  # 2D case
                figure.add_scatter(x=series_x, y=series_y, mode='lines', line={'color': 'grey'}, name='state_change')
            else:  # 3D case
                figure.add_scatter3d(x=series_x, y=series_y, z=series_z,
                                     mode='lines', line={'color': 'grey'}, name='state_change')

            # for each labels in series_color : add lines+markers colored
            for value_encoded, value in zip(series_color_encoded.value_counts().keys(),
                                            series_color.value_counts().keys()):

                if series_z is None:  # 2D case
                    figure.add_scatter(x=series_x.where(series_color_encoded == value_encoded),
                                       y=series_y.where(series_color_encoded == value_encoded),
                                       mode='lines+markers', marker=dict_marker, name=value)
                else:  # 3D case
                    figure.add_scatter3d(x=series_x.where(series_color_encoded == value_encoded),
                                         y=series_y.where(series_color_encoded == value_encoded),
                                         z=series_z.where(series_color_encoded == value_encoded),
                                         mode='lines+markers', marker=dict_marker, name=value)

        else:  # non colored case
            if series_z is None:  # 2D case
                figure.add_scatter(x=series_x, y=series_y, mode='lines+markers', line={'color': 'blue'}, )
            else:  # 3D case
                figure.add_scatter3d(x=series_x, y=series_y, z=series_z, mode='lines+markers', line={'color': 'blue'}, )

        return self.store_or_return_object(figure, save_path)

    def create_scatter_line_2D_3D_color_scale(self, series_x, series_y, series_z=None, series_color=None,
                                              save_path=None):

        color_bar_name = 'scale_values'

        # series color
        if series_color is not None:

            if type(series_color) is pd.core.series.Series:
                color_bar_name = series_color.name
                series_color = np.array(series_color)

            elif type(series_color) is list:
                series_color = np.array(series_color)

            series_color = LabelEncoder().fit_transform(series_color)

            dict_marker = dict(cmax=max(series_color), cmin=min(series_color),
                               color=series_color, symbol=series_color, colorscale='Portland',
                               colorbar=dict(title=color_bar_name))
        else:
            dict_marker = dict()

        # series z
        if series_z is None:
            dict_marker['size'] = 8
            scatter = go.Scatter(x=series_x, y=series_y, mode='lines+markers', marker=dict_marker,
                                 line={'color': 'grey'}, )
        else:
            dict_marker['size'] = 3
            scatter = go.Scatter3d(x=series_x, y=series_y, z=series_z, mode='lines+markers', marker=dict_marker,
                                   line={'color': 'grey'}, )

        figure = go.Figure()
        figure.add_trace(scatter, )

        return self.store_or_return_object(figure, save_path)

    # MULTIPLE SCATTER LINE : 2D  #####################################################################################

    def create_multiple_scatter_line(self, series_x, df_y, mode='lines+markers', save_path=None):

        figure = go.Figure()
        for column_name in df_y.columns:
            figure.add_trace(go.Scatter(x=series_x, y=df_y[column_name], mode=mode, name=column_name))

        return self.store_or_return_object(figure, save_path)

    # HISTOGRAM ######################################################################################################

    def create_histogram(self, series_x, series_y, series_color=None, save_path=None):
        figure = px.histogram(x=series_x, y=series_y, color=series_color)
        return self.store_or_return_object(figure, save_path)

    # HEATMAP ########################################################################################################

    def create_heatmap(self, data, save_path=None):
        figure = px.imshow(data, text_auto=True)
        return self.store_or_return_object(figure, save_path)

    # SUBPLOT ########################################################################################################
    '''
    def make_subplot(self, list_figure):

        for figure in list_figure:
            if type(figure) is list:
                for fig in figure:
                    make_subplot()
            else:
                make_subplot()

    '''
    #
    #
    #
    #
    # AUTOMATIC SCATTER : 3D - 2D - MATRIX ################################################################

    def __NONE_USED_create_automatic_scatter_plot(self, data, column_color_name=None, marginal_x=None, marginal_y=None,
                                                  save_path=None):
        # colored scatter
        if column_color_name is not None:
            data = data.drop([column_color_name], axis=1)

        # marginal x & y
        list_subplot_name = [None, "histogram", "rug", "box", "violin"]
        if marginal_x not in list_subplot_name:
            marginal_x = None
        if marginal_y not in list_subplot_name:
            marginal_y = None

        # dimension scatter
        scatter_dimension = data.shape[1]

        if scatter_dimension == 3:
            figure = px.scatter_3d(data, x=data.columns[0], y=data.columns[1], z=data.columns[2],
                                   color=column_color_name)
        elif scatter_dimension == 2:
            figure = px.scatter(data, x=data.columns[0], y=data.columns[1],
                                marginal_x=marginal_x, marginal_y=marginal_y, color=column_color_name)
        else:
            figure = px.scatter_matrix(data, dimensions=list(data.columns),
                                       color=column_color_name)

        # save or return
        if save_path is None:
            return figure
        self.store_figure(figure, save_path)

    # PLOT BY COLUMN ARGUMENTS - 2D & 3D #############################################################################

    def __NONE_USED__create_automatic_scatter_line(self, series_x, series_y, series_z=None, markers=True,
                                                   series_color=None, save_path=None):
        if series_z is None:
            figure = px.line(x=series_x, y=series_y, markers=markers, color=series_color)
        else:
            figure = px.line_3d(x=series_x, y=series_y, z=series_z, markers=markers, color=series_color)

        if save_path is None:
            return figure
        self.store_figure(figure, save_path)
