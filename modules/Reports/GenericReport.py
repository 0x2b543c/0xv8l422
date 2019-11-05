from .ReportABC import Report as Rep

class GenericReport(Rep):
    def __init__(self, report_title:str, pipelines:list=[]):
        super().__init__(report_title=report_title, pipelines=pipelines)

    def implement_plumbing(self):
        pass

   
