from turtle import title
from black import main
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots


class MonitoringPlotter:
    def __init__(self) -> None:
        pass

    def multiline_plot(self, data: dict, x_axis: str, y_axises: list) -> None:
        if len(y_axises) < 2:
            raise ValueError

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data[x_axis], y=data[y_axises[0]], name=y_axises[0], mode="lines"))

        for y_axis in y_axises[1:]:
            fig.add_trace(go.Scatter(x=data[x_axis], y=data[y_axis], name=y_axis, mode="lines"))

        fig.show()

    def line_plot(self, data: dict, x_axis: str, y_axis: str) -> None:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data[x_axis], y=data[y_axis], name=y_axis, mode="lines"))
        fig.show()

    def multiline_and_multiscale_plot(self, data: dict, x_axis: str, first_y_axis: str, sec_y_axis: str) -> None:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Scatter(x=data[x_axis], y=data[first_y_axis], name=first_y_axis, mode="lines"), secondary_y=False
        )
        fig.add_trace(go.Scatter(x=data[x_axis], y=data[sec_y_axis], name=sec_y_axis, mode="lines"), secondary_y=True)

        fig.update_yaxes(title_text=first_y_axis, secondary_y=False)
        fig.update_yaxes(title_text=sec_y_axis, secondary_y=True)

        fig.show()
