from tkinter import Y
from turtle import title
from black import main
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots


class MonitoringPlotter:
    def __init__(self) -> None:
        pass

    def multiline_plot(self, data: dict, x_axis: str, y_axises: list, file_path: str = None) -> None:
        if len(y_axises) < 2:
            raise ValueError("At least two y-axises are required")

        fig = go.Figure()

        for y_axis in y_axises:
            fig.add_trace(go.Scatter(x=data[x_axis], y=data[y_axis], name=y_axis, mode="lines"))

        if file_path:
            fig.write_image(f"{file_path}")
        else:
            fig.show()

    def line_plot(self, data: dict, x_axis: str, y_axis: str, file_path: str = None) -> None:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data[x_axis], y=data[y_axis], name=y_axis, mode="lines"))

        if file_path:
            fig.write_image(f"{file_path}")
        else:
            fig.show()

    def multiline_and_multiscale_plot(
        self, data: dict, x_axis: str, y_axises: list, scales: list, file_path: str = None
    ) -> None:
        """
        y_axises: list of objects {name: str, scale: int (primary or secondary)}
        scales: list of 2 objects: first is the left and primary y axis {title: str, down: int, top: int},
        """

        if len(scales) > 2:
            raise ValueError("Only two scales are supported")

        fig = go.Figure()

        for y_axis in y_axises:
            if y_axis["scale"] == "primary":
                fig.add_trace(
                    go.Scatter(x=data[x_axis], y=data[y_axis["name"]], name=y_axis["name"], mode="lines", yaxis="y")
                )
            else:
                fig.add_trace(
                    go.Scatter(x=data[x_axis], y=data[y_axis["name"]], name=y_axis["name"], mode="lines", yaxis="y2")
                )

        fig.update_layout(
            yaxis=dict(title=scales[0]["title"], range=[scales[0]["down"], scales[0]["top"]], side="left"),
            yaxis2=dict(title=scales[1]["title"], range=[scales[1]["down"], scales[1]["top"]], side="right"),
        )

        if file_path:
            fig.write_image(f"{file_path}")
        else:
            fig.show()
