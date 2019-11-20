# Research Infrastructure

The research infrastructure's goal is to create automatable research reports. Instead of updating reports manually by re-creating charts and tables, the research infrastructure allows you re-run reports with fresh data, and instantly create updated visuals.

It also makes it easy to create different variations of reports, e.g. Coinbase report for different assets.

... export Jupyter Notebooks, PDFs, etc. 

## Reports

Reports are the ultimate output of the research infrastructure.

ResearchInfraABC()
    @abstract
    implement()
    @abstract
    run()

Report()
    init()
        self.data_sources
        self.visuals
    @abstract
    implement_report()
        load_data_sources()
        load_visuals()
    update_data_sources()
    combine_reports()
        - combine together multiple reports, i.e. mix and match different reports in a modular fashion
    render_visuals(sections:[int]='all')
    exports_report_as_pngs(sections:[int]='all', export_path=str)
    export_report_as_pdf(sections:[int]='all', export_path=str)
    export_report_as_dash(sections:[int]='all', export_path=str)
    run()

Reports are composed of charts and tables, which are represented as Visual objects.

DataLoader

Transformer

DataPipe
    init()
        self.data_sources
        self.visuals

DataSource(id:int, title:str, data_loader:[DataLoader or Pipeline])

Visual(title:str, data_source: ReportDataSource.id, visualizer: Visualizer, section:str, order:int, custom_formatting:str)

Visual()
    init()
        self.id:int
        self.title:str
        self.fig:[Plotly, Matlab, etc.]
        self.custom_formatting:str=None
        self.section:str=None
        self.order:int=None

    @abstract
    implement()
    show()
        - show method should be able to detect the type of fig (e.g plotly, matlab, etc.) and show it accordingly
    export()
        - export method should be able to detect the type of fig (e.g plotly, matlab, etc.) and export it accordingly
    run()