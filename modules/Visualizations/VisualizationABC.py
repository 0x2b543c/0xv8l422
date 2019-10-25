from abc import ABC, abstractmethod

class Visualization(ABC):
    def __init__(self, title:str):
        self.title = title
        self.fig = None

    @abstractmethod
    def implement_visualization(self, df):
        pass

    def execute_visualization(self, df):
        self.implement_visualization(df)
        return self

    # def export_as_png(self, df, file_name):
    #     fig = self.implement_visualization(df)
    #     file_path = "{}.png".format(file_name)
    #     fig.write_image(file_path)
    #     print('Exported to ' file_path)

