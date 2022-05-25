import plotly.express as px
from Utilities.FileManipulation import get_extension_into_path, add_extension


class VisualiseDataPlotly:

    # STORE ############################################################################################

    @staticmethod
    def store_figure(figure, save_path):

        extension = get_extension_into_path(save_path)  # recover the extension whitout the dot

        if extension == 'html':
            figure.write_html(save_path)
        elif extension == 'json':
            figure.write_json(save_path)
        elif extension == 'png':
            figure.write_image(save_path)

    # MATRIX ############################################################################################

    def create_scatter_matrix(self, data, column_color_name=None, save_path=None):

        # colored scatter
        if column_color_name is not None:
            data.drop([column_color_name], axis=1, inplace=True)

        figure = px.scatter_matrix(data, dimensions=list(data.columns), color=column_color_name)

        # save or return
        if save_path is None:
            return figure
        self.store_figure(figure, save_path)

    # AUTOMATIC SCATTER : 3D - 2D - MATRIX ###########################################################################

    def create_automatic_scatter_plot(self, data, column_color_name=None, marginal_x=None, marginal_y=None,
                                      save_path=None):

        # colored scatter
        if column_color_name is not None:
            data.drop([column_color_name], axis=1, inplace=True)

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

