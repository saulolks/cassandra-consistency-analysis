import pandas as pd


class Monitor:
    def __init__(self) -> None:
        pass

    def get_data(self, container_name: str = None) -> dict:
        data = pd.DataFrame(self._data)

        if container_name:
            data = data[(data["container_name"] == container_name)]

        return data
