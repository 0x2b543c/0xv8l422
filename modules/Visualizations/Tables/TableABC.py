from abc import ABC, abstractmethod

class Table(ABC):
    @abstractmethod
    def create_table(self, df):
        pass

    def render_table(self, df):
        fig = self.create_table(df)
        return fig.show()

    def export_as_png(self, df, file_name):
        fig = self.create_table(df)
        fig.write_image("{}.png".format(file_name))
