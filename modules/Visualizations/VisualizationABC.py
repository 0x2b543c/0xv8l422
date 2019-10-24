from abc import ABC, abstractmethod

class Visualization(ABC):
    @abstractmethod
    def implement_visualization(self, df):
        pass

    def create_visualization(self, df):
        fig = self.implement_visualization(df)
        return fig

    # def export_as_png(self, df, file_name):
    #     fig = self.implement_visualization(df)
    #     file_path = "{}.png".format(file_name)
    #     fig.write_image(file_path)
    #     print('Exported to ' file_path)

