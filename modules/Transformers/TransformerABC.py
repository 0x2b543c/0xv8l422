from abc import ABC, abstractmethod

class Transformer(ABC):
    @abstractmethod
    def implement_transformation(self, df):
        pass

    def transform(self, df):
        return self.implement_transformation(df)