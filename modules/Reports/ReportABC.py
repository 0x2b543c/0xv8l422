from abc import ABC, abstractmethod

class Report(ABC):
    @abstractmethod
    def implement_report(self, df):
        pass

    def run_report(self, df):
        pass
