from plotly.subplots import make_subplots
from plotly.offline import plot
import plotly.graph_objects as go
from random import sample


## RAJOUTER DANS SETUP DATA ANALYSE :
# -sublpot 2D  / 3D
# - subplot data
# other ...

class Dashboard:

    def __init__(self, list_discrete_color=None):
        self.subplot = SubPlots(list_discrete_color=list_discrete_color)

    @staticmethod
    def store_or_return_figure(figure, save_path=None):
        if save_path is None:
            return figure
        plot(figure, filename=save_path, auto_open=False)

    #
    def plot_reduced_2D_data_markers__reduced_1D_data_ts_line(self, reduced_2D_data, reduced_1D_data, series_timestamp,
                                                              series_color, name_scatter='', mapped_series_color=None,
                                                              save_path=None):
        figure = self.subplot.create_subplots(1, 2, set_title=('reduced 2D data',
                                                               'reduced 1D data with time in x-axis'))

        figure = self.subplot.create_scatter_plot_2D(reduced_2D_data.iloc[:, 0], reduced_2D_data.iloc[:, 1],
                                                     series_color, 'markers', True, mapped_series_color, figure, 1, 1)
        figure = self.subplot.create_scatter_plot_2D(series_timestamp, reduced_1D_data.iloc[:, 0], series_color,
                                                     'lines+markers', False, mapped_series_color, figure, 1, 2)

        figure.update_layout(title=name_scatter)

        self.store_or_return_figure(figure, save_path)

    #
    def NOT_WORK_plot_reduced_3D_data_markers__reduced_2D_data_ts_line(self, reduced_3D_data, reduced_2D_data,
                                                                       series_timestamp,
                                                                       series_color, name_scatter='', save_path=None):
        figure = self.subplot.create_subplots(1, 2, set_title=('reduced 1D data with time in x-axis',
                                                               'reduced 2D data'))

        figure = self.subplot.create_scatter_plot_3D(reduced_3D_data.iloc[:, 0], reduced_3D_data.iloc[:, 1],
                                                     reduced_3D_data.iloc[:, 2], series_color, 'markers', True)
        # figure, 1, 1)

        figure = self.subplot.create_scatter_plot_3D(series_timestamp, reduced_2D_data.iloc[:, 0],
                                                     reduced_2D_data.iloc[:, 1],
                                                     series_color, 'lines+markers', True)  # , figure, 1, 2)

        figure.update_layout(title=name_scatter)

        self.store_or_return_figure(figure, save_path)

    #
    def histograms_features(self, data, series_color, opacity=0.8, bar_mode='overlay', name_scatter=None,
                            save_path=None):
        show_legend = True
        list_column_name = list(data.columns)

        figure = self.subplot.create_subplots(rows=1, cols=len(list_column_name))

        for index_col in range(len(list_column_name)):
            self.subplot.create_histogram(data[list_column_name[index_col]], series_color,
                                          opacity, show_legend, figure, 1, index_col + 1)

            figure.update_layout(barmode=bar_mode)
            show_legend = False

        self.store_or_return_figure(figure, save_path)

    def dataframe__heatmap_correlation__scatter_features(self, data, correlated_data, series_timestamp,
                                                         save_path=None):
        specs = [[{'type': 'table', 'rowspan': 2}, {'type': 'heatmap'}], [None, {'type': 'scatter'}]]
        figure = self.subplot.create_subplots(2, 2, specs=specs)

        figure = self.subplot.create_table_figure(data, figure, 1, 1)
        figure = self.subplot.create_heatmap(correlated_data, True, True, figure, 1, 2)
        figure = self.subplot.create_multiple_scatter_line(series_timestamp, data, 'lines+markers', figure, 2, 2)

        self.store_or_return_figure(figure, save_path)


class SubPlots:

    def __init__(self, list_discrete_color=None):

        if list_discrete_color is None:

            self.list_discrete_color = ['blue', 'yellow', 'purple', 'brown',
                                        'violet', 'cyan']
            l = ['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure',
                 'beige', 'bisque', 'blanchedalmond', 'black',
                 'blueviolet', 'brown', 'burlywood', 'cadetblue',
                 'chartreuse', 'chocolate', 'coral', 'cornflowerblue',
                 'cornsilk', 'crimson', 'darkblue', 'darkcyan',
                 'darkgoldenrod', 'darkgray', 'darkgrey', 'darkgreen',
                 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange',
                 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen',
                 'darkslateblue', 'darkslategray', 'darkslategrey',
                 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue',
                 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick',
                 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro',
                 'ghostwhite', 'gold', 'goldenrod', 'gray', 'grey',
                 'greenyellow', 'honeydew', 'hotpink', 'indianred', 'indigo',
                 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen',
                 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan',
                 'lightgoldenrodyellow', 'lightgray', 'lightgrey',
                 'lightgreen', 'lightpink', 'lightsalmon', 'lightseagreen',
                 'lightskyblue', 'lightslategray', 'lightslategrey',
                 'lightsteelblue', 'lightyellow', 'lime', 'limegreen',
                 'linen', 'magenta', 'maroon', 'mediumaquamarine',
                 'mediumblue', 'mediumorchid', 'mediumpurple',
                 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen',
                 'mediumturquoise', 'mediumvioletred', 'midnightblue',
                 'mintcream, mistyrose', 'moccasin', 'navajowhite', 'navy',
                 'oldlace', 'olive', 'olivedrab', 'orangered',
                 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise',
                 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink',
                 'plum', 'powderblue', 'rosybrown',
                 'royalblue', 'rebeccapurple', 'saddlebrown', 'salmon',
                 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver',
                 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow',
                 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato',
                 'turquoise', 'wheat', 'whitesmoke', 'yellowgreen']

            self.list_discrete_color.extend(sample(l, len(l)))

        else:
            self.list_discrete_color = list_discrete_color

    @staticmethod
    def create_subplots(rows=1, cols=1, horizontal_spacing=0.1, vertical_spacing=0.1, set_title=None, specs=None):

        return make_subplots(rows, cols, horizontal_spacing=horizontal_spacing, vertical_spacing=vertical_spacing,
                             subplot_titles=set_title, specs=specs)

    @staticmethod
    def check_existing_figure(figure, row, col):
        if None in [figure, row, col]:
            row, col = 1, 1
            figure = make_subplots(row, col)
        return figure, row, col

    # SCATTER PLOT 2D - Lines & markers ###############################################################################

    def create_scatter_plot_2D(self, series_x, series_y, series_color=None, mode='lines+markers',
                               show_legend=True, mapped_series_color=None, figure=None, row=None, col=None):

        figure, row, col = self.check_existing_figure(figure, row, col)

        if series_color is None:
            figure.add_scatter(x=series_x, y=series_y, line_color='blue', legendgroup=1, showlegend=show_legend,
                               mode=mode, row=row, col=col)
        else:

            if mode != 'markers':
                figure.add_scatter(x=series_x, y=series_y, mode='lines', line_color='grey',
                                   name='state change', row=row, col=col)

            list_labels = list(dict(series_color.value_counts()).keys())
            if mapped_series_color is None:
                mapped_series_color = dict(zip(list_labels, self.list_discrete_color))

            for label in list_labels:
                figure.add_scatter(x=series_x.where(series_color == label),
                                   y=series_y.where(series_color == label),
                                   marker_color=mapped_series_color[label], marker_size=10,
                                   name=label, legendgroup=label,
                                   mode=mode, showlegend=show_legend,
                                   row=row, col=col)
        return figure

    # SCATTER PLOT 3D - Lines & markers ###############################################################################

    def create_scatter_plot_3D(self, series_x, series_y, series_z, series_color=None, mode='lines+markers',
                               show_legend=True):  # , figure=None, row=None, col=None):

        # figure, row, col = self.check_existing_figure(figure, row, col)

        figure = go.Figure()
        if series_color is None:
            figure.add_scatter3d(x=series_x, y=series_y, mode=mode, line_color=self.list_discrete_color[0])
            # row=row, col=col)
        else:

            if mode != 'markers':
                figure.add_scatter3d(x=series_x, y=series_y, mode='lines', line_color='grey',
                                     name='state change')  # , row=row, col=col)

            list_labels = list(dict(series_color.value_counts()).keys())

            for index in range(len(list_labels)):
                figure.add_scatter3d(x=series_x.where(series_color == list_labels[index]),
                                     y=series_y.where(series_color == list_labels[index]),
                                     z=series_z.where(series_color == list_labels[index]),
                                     marker_color=self.list_discrete_color[index], marker_size=3,
                                     name=list_labels[index], legendgroup=list_labels[index],
                                     mode=mode, showlegend=show_legend)
                # row=row, col=col)

        return figure

    # MULTIPLE SCATTER LINE : 2D  #####################################################################################

    def create_multiple_scatter_line(self, series_x, df_y, mode='lines+markers', figure=None, row=None, col=None):

        figure, row, col = self.check_existing_figure(figure, row, col)

        for column_name in df_y.columns:
            figure.add_scatter(x=series_x, y=df_y[column_name], mode=mode, name=column_name, row=row, col=col)

        return figure

    #  SCATTER PLOT MATRIX FROM DATAFRAME : 2D  ####################################################################

    @staticmethod
    def create_scatter_plot_matrix(data, series_color, show_diagonal=False, show_upper_half=False,
                                   show_scale=False):
        # figure=None, row=None, col=None):

        # figure, row, col = self.check_existing_figure(figure, row, col)

        color = None
        if series_color is not None:
            color = series_color.astype('category').cat.codes
            # color = self.list_discrete_color[0:len(list(series_color.value_counts().keys()))]

        figure = go.Figure(data=go.Splom(
            dimensions=[dict(label=column_name, values=data[column_name]) for column_name in list(data.columns)],
            showupperhalf=show_upper_half, text=series_color,
            marker=dict(color=color, showscale=show_scale, line_color='white',
                        line_width=0.5, size=7, colorscale='Portland'),
            diagonal=dict(visible=show_diagonal)))
        # row=row, col=col)

        figure.update_layout()
        return figure

    # HISTOGRAM FOR ONE SERIES DECLINED BY SERIES COLOR ############################################################

    def create_histogram(self, series_x, series_color=None, opacity=0.8, show_legend=True, figure=None, row=None,
                         col=None):

        figure, row, col = self.check_existing_figure(figure, row, col)

        if series_color is None:
            figure.add_histogram(x=series_x, opacity=opacity, showlegend=show_legend, row=row, col=col)

        else:
            list_labels = list(dict(series_color.value_counts()).keys())

            for index in range(len(list_labels)):
                figure.add_histogram(x=series_x.where(series_color == list_labels[index]),
                                     name=list_labels[index], legendgroup=list_labels[index],
                                     marker_color=self.list_discrete_color[index], opacity=opacity,
                                     showlegend=show_legend, row=row, col=col)

        return figure

    # HEATMAP FOR A DATAFRAME #################################################################################

    def create_heatmap(self, data, correlation_matrix=True, show_scale=True, figure=None, row=None, col=None):

        figure, row, col = self.check_existing_figure(figure, row, col)

        if correlation_matrix:
            figure.add_heatmap(z=data.applymap(lambda x: abs(x)),
                               text=data.applymap(lambda x: (round(x, 4))),
                               texttemplate="%{text}", colorscale='Portland', showscale=show_scale,
                               textfont={"size": 15, 'color': 'white'}, row=row, col=col)
        else:
            figure.add_heatmap(z=data, text=data, texttemplate="%{text}", colorscale='Portland', show_scale=show_scale,
                               textfont={"size": 15, 'color': 'white'}, row=row, col=col)

        figure.update_yaxes(autorange="reversed", row=row, col=col)

        return figure

    def create_table_figure(self, data, figure=None, row=None, col=None):

        figure, row, col = self.check_existing_figure(figure, row, col)

        figure.add_table(header=dict(values=list(data.columns), align='left'),
                         cells=dict(values=[data[column_name] for column_name in list(data.columns)], align='left'))

        return figure
############################################################################################################
