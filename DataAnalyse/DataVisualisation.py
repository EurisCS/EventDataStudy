import plotly.express as px
from Utilities.FileManipulation import get_extension_into_path, add_extension


class VisualiseDataPlotlyExpress:

    # STORE ############################################################################################

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

    # MATRIX ############################################################################################

    def create_scatter_matrix(self, data, column_color_name=None, save_path=None):

        # colored scatter
        if column_color_name is not None:
            data = data.drop([column_color_name], axis=1)

        figure = px.scatter_matrix(data, dimensions=list(data.columns), color=column_color_name, )
        figure.update_traces(diagonal_visible=False)

        # save or return
        if save_path is None:
            return figure
        self.store_figure(figure, save_path)

    # AUTOMATIC SCATTER : 3D - 2D - MATRIX ################################################################

    def create_automatic_scatter_plot(self, data, column_color_name=None, marginal_x=None, marginal_y=None,
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

    def create_automatic_scatter_line(self, series_x, series_y, series_z=None, markers=True, series_color=None,
                                      save_path=None):

        if series_z is None:
            figure = px.line(x=series_x, y=series_y, markers=markers, color=series_color)
        else:
            figure = px.line_3d(x=series_x, y=series_y, z=series_z, markers=markers, color=series_color)

        if save_path is None:
            return figure
        self.store_figure(figure, save_path)

    def create_automatic_scatter_line(self, series_x, series_y, series_z=None, markers=True, series_color=None,
                                      save_path=None):

        if series_z is None:
            figure = px.line(x=series_x, y=series_y, markers=markers, color=series_color)
        else:
            figure = px.line_3d(x=series_x, y=series_y, z=series_z, markers=markers, color=series_color)

        if save_path is None:
            return figure
        self.store_figure(figure, save_path)

    # HISTOGRAM ######################################################################################################

    def create_histogram(self, series_x, series_y, save_path=None):
        figure = px.histogram(x=series_x, y=series_y)

        if save_path is None:
            return figure
        self.store_figure(figure, save_path)

    # TERNARY ########################################################################################################

    def create_scatter_ternary(self, data, column_color_name=None, save_path=None):

        figure = px.scatter_ternary(data, a=data.columns[0], b=data.columns[1], c=data.columns[2],
                                    color=column_color_name)

        if save_path is None:
            return figure
        self.store_figure(figure, save_path)

    # HEATMAP ########################################################################################################

    def create_heatmap(self, data, save_path=None):

        figure = px.imshow(data, text_auto=True)

        if save_path is None:
            return figure
        self.store_figure(figure, save_path)


# GRAPH OBJECT ######################################################################################################

from plotly import graph_objects as go


class VisualiseDataPlotlyGo:

    def __init__(self):
       pass

    def create_multiple_scatter_line(self, series_x, data_y, mode='lines+markers', save_path=None):

        figure = go.Figure()

        for column_name in data_y.columns:
            figure.add_trace(go.Scatter(x=series_x, y=data_y[column_name], mode=mode, name=column_name))

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