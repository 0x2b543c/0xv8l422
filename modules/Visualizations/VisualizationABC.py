from abc import ABC, abstractmethod

class Visualization(ABC):
    @abstractmethod
    def create_visualization(self, df):
        pass

    def render_visualization(self, df):
        fig = self.create_visualization(df)
        return fig.show()

    def export_as_png(self, df, file_name):
        fig = self.create_visualization(df)
        fig.write_image("{}.png".format(file_name))

