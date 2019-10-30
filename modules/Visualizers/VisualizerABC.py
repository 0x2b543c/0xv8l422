from abc import ABC, abstractmethod

class Visualizer(ABC):
    def __init__(self, title:str):
        self.title = title
        self.fig = None

    @abstractmethod
    def implement_visualization(self, df):
        pass

    def create_visual(self, df):
        self.implement_visualization(df)
        self.fig.update_layout(
            title=self.title
        )
        return self


