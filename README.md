# `vega_widget`

Plain `vega` visualizations as `marimo`-compatible `anywidget`.

## Getting started

### Pre-requisites

- `marimo`
- (optional) some dataframe library from `pandas`, `polars` and `ibis`

#### :warning: A note on `npm`

This package is currently not published to any package index.
This means that installation (as detailed in [Install](#install)) is currently limited to installation from source.
Given that this package works at the boundary between `python` and `javascript`, this introduces the additional requirement of having `npm` available in your `$PATH` to transpile the provided `typescript` code into `javascript`.

### Install

From inside some `uv` managed project, add `vega_widget` as in

```console
> uv add 'git+https://github.com/90degs2infty/vega-widget[pandas]'
```

Replace/Append whatever dataframe library you're using.

### Usage

Inside a `marimo` notebook:

```py
import marimo as mo
from vega_widget.ui import VegaWidget

import json

# This is the bar chart example from Vega's documentation at https://vega.github.io/vega/examples/bar-chart/
# For convenience, the spec is copied verbatim and loaded using `json`. You can build a dict directly instead.
#
# Note how the spec does not feature the `data` key - it is injected by `vega_widget` instead.
example_json = """{
    "$schema": "https://vega.github.io/schema/vega/v6.json",
    "description": "A basic bar chart example, with value labels shown upon pointer hover.",
    "width": 400,
    "height": 200,
    "padding": 5,

    "signals": [
    {
        "name": "tooltip",
        "value": {},
        "on": [
        {"events": "rect:pointerover", "update": "datum"},
        {"events": "rect:pointerout",  "update": "{}"}
        ]
    }
    ],

    "scales": [
    {
        "name": "xscale",
        "type": "band",
        "domain": {"data": "table", "field": "category"},
        "range": "width",
        "padding": 0.05,
        "round": true
    },
    {
        "name": "yscale",
        "domain": {"data": "table", "field": "amount"},
        "nice": true,
        "range": "height"
    }
    ],

    "axes": [
    { "orient": "bottom", "scale": "xscale" },
    { "orient": "left", "scale": "yscale" }
    ],

    "marks": [
    {
        "type": "rect",
        "from": {"data":"table"},
        "encode": {
        "enter": {
            "x": {"scale": "xscale", "field": "category"},
            "width": {"scale": "xscale", "band": 1},
            "y": {"scale": "yscale", "field": "amount"},
            "y2": {"scale": "yscale", "value": 0}
        },
        "update": {
            "fill": {"value": "steelblue"}
        },
        "hover": {
            "fill": {"value": "red"}
        }
        }
    },
    {
        "type": "text",
        "encode": {
        "enter": {
            "align": {"value": "center"},
            "baseline": {"value": "bottom"},
            "fill": {"value": "#333"}
        },
        "update": {
            "x": {"scale": "xscale", "signal": "tooltip.category", "band": 0.5},
            "y": {"scale": "yscale", "signal": "tooltip.amount", "offset": -2},
            "text": {"signal": "tooltip.amount"},
            "fillOpacity": [
            {"test": "datum === tooltip", "value": 0},
            {"value": 1}
            ]
        }
        }
    }
    ]
}
"""
example = json.loads(example_json)

values = pandas.DataFrame(
    [
        {"category": "A", "amount": 28},
        {"category": "B", "amount": 55},
        {"category": "C", "amount": 43},
        {"category": "D", "amount": 91},
        {"category": "E", "amount": 81},
        {"category": "F", "amount": 53},
        {"category": "G", "amount": 19},
        {"category": "H", "amount": 87},
    ]
)
data = {"table": values}
vega = VegaWidget(spec=example, data=data)
mo.ui.anywidget(vega)
```

Find more examples in [examples/widget.py](./examples/widget.py).

## Limitations

As of now, the entire package remains rather basic.

Currently, only dataframe datasources are supported.
There is no support for e.g. URLs (yet).

## Prior art

### Wigglystuff

This repository is heavily inspired by [koaning/wigglystuff](https://github.com/koaning/wigglystuff), licensed under MIT license.
Find their full license on [github.org](https://github.com/koaning/wigglystuff/blob/main/LICENSE).

## Development

### Bundling javascript

```console
> npm run build
```

## Failed attempts

I initially considered checking `vega` specs at the `python` side or to even provide a typed abstraction to build specs.
Here, the idea was to derive a `pydantic` model using [`datamodel-code-generator`](https://datamodel-code-generator.koxudaxi.dev/) from [the official spec](https://vega.github.io/schema/vega/v6.json).
However, I found the resulting model to be broken, so I abandoned this idea for the moment.
