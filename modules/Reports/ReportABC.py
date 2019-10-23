from abc import ABC, abstractmethod

class Report(ABC):
    @abstractmethod
    def create_report(self, df):
        pass
