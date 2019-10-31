import requests
from datetime import date, datetime
from typing import List, NamedTuple


class MetricRow(NamedTuple):
    time: date
    value: float


def parse_iso8601(iso8601: str) -> datetime:
    return datetime.strptime(iso8601, "%Y-%m-%dT%H:%M:%S.%fZ")


def get_metric_data(api_key: str, asset: str, metric: str) -> List[MetricRow]:
    url = "https://api.coinmetrics.io/v3/assets/{}/metricdata?metrics={}&start=2009-01-01&end=2020-01-01&timeAggregation=day&api_key={}".format(
        asset, metric, api_key
    )

    json = requests.get(url).json()
    return list(map(lambda x: MetricRow(parse_iso8601(x["time"]).date(), float(x["values"][0])), json["metricData"]["series"]))

if __name__ == "__main__":
    for x in get_metric_data("your-api-key-here", "btc", "TxCnt"):
        print(x)