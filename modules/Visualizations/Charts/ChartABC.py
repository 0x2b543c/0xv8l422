from abc import ABC, abstractmethod

class Chart(ABC):
    @abstractmethod
    def create_chart(self, df):
        pass

    def render_chart(self, df):
        fig = self.create_chart(df)
        return fig.show()

    def export_as_png(self, df, file_name):
        fig = self.create_chart(df)
        fig.write_image("{}.png".format(file_name))

