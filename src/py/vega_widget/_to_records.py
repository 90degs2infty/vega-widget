from typing import Any

try:
    import ibis
except ImportError:
    ibis = None

try:
    import pandas
except ImportError:
    pandas = None

try:
    import polars
except ImportError:
    polars = None

def to_records(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return data
    if pandas and isinstance(data, pandas.DataFrame):
        return [row._asdict() for row in data.itertuples(index=False)]
    if polars and isinstance(data, polars.DataFrame):
        return data.to_dicts()
    if ibis and isinstance(data, ibis.Table):
        return to_records(data.to_pandas())

    raise ValueError(f"data object of type {type(data)} not supported")