import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)
server = app.server

root_path = "/home/eguimard/PycharmProjects/DataStudy/DataStorage/Results/DataAnalyse/FunctionalTest/"
folders = [f"{root_path}/cpu/dbscan"]

controls = [
    dcc.Dropdown(
        id="dropdown",
        options=[{"label": x, "value": x} for x in folders],
        value=folders[0],
    )
]

app.layout = html.Div(
    [html.H1("File Browser"), html.Div(controls), html.Div(id="folder-files")]
)


@app.callback(Output("folder-files", "children"), Input("dropdown", "value"))
def list_all_files(folder_name):
    # This is relative, but you should be able
    # able to provide the absolute path too
    file_names = os.listdir(folder_name)

    file_list = html.Ul([html.Li(file) for file in file_names])

    return file_list


if __name__ == "__main__":
    app.run_server(debug=True)