import pytest
from src.monitoring_plotter import MonitoringPlotter


class TestMonitoringPlotter:
    def test_multiline_plot(self, mock_ps_monitoring_data):
        plotter = MonitoringPlotter()
        plotter.multiline_plot(mock_ps_monitoring_data, "timestamp", ["cpu", "mem"])

        assert True

    def test_line_plot(self, mock_ps_monitoring_data):
        plotter = MonitoringPlotter()
        plotter.line_plot(mock_ps_monitoring_data, "timestamp", "cpu")

        assert True

    def test_multiline_and_multiscale_plot(self, mock_ps_monitoring_data):
        plotter = MonitoringPlotter()
        scales = [
            {"title": "Percent", "down": 0, "top": 100},
            {"title": "Usage", "down": 0, "top": 10000},
        ]
        y_axises = [
            {"name": "cpu", "scale": "primary"},
            {"name": "mem", "scale": "primary"},
            {"name": "virt", "scale": "secondary"},
        ]

        plotter.multiline_and_multiscale_plot(mock_ps_monitoring_data, "timestamp", y_axises, scales)

        assert True
