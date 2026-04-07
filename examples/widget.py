import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from vega_widget.ui import VegaWidget
    import marimo as mo

    import json

    return VegaWidget, json, mo


@app.cell
def _(json):
    example_json = """{
      "$schema": "https://vega.github.io/schema/vega/v6.json",
      "description": "A basic bar chart example, with value labels shown upon pointer hover.",
      "width": 400,
      "height": 200,
      "padding": 5,

      "data": [
        {
          "name": "table",
          "values": [
            {"category": "A", "amount": 28},
            {"category": "B", "amount": 55},
            {"category": "C", "amount": 43},
            {"category": "D", "amount": 91},
            {"category": "E", "amount": 81},
            {"category": "F", "amount": 53},
            {"category": "G", "amount": 19},
            {"category": "H", "amount": 87}
          ]
        }
      ],

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
    example
    return (example,)


@app.cell
def _(VegaWidget, example, mo):
    def visualize_list():
        values = [
            {"category": "A", "amount": 28},
            {"category": "B", "amount": 55},
            {"category": "C", "amount": 43},
            {"category": "D", "amount": 91},
            {"category": "E", "amount": 81},
            {"category": "F", "amount": 53},
            {"category": "G", "amount": 19},
            {"category": "H", "amount": 87},
        ]
        data = {"table": values}
        vega = VegaWidget(spec=example, data=data)
        return mo.ui.anywidget(vega)


    visualize_list()
    return


@app.cell
def _(VegaWidget, example, mo):
    import ibis


    def visualize_ibis():
        values = ibis.memtable(
            [
                {"category": "A", "amount": 28},
                {"category": "B", "amount": 55},
                {"category": "C", "amount": 43},
                {"category": "D", "amount": 91},
                {"category": "E", "amount": 81},
                {"category": "F", "amount": 53},
                {"category": "G", "amount": 19},
                {"category": "H", "amount": 87},
            ],
            schema={"category": "!string", "amount": "uint64"},
        )
        data = {"table": values}
        vega = VegaWidget(spec=example, data=data)
        return mo.ui.anywidget(vega)


    visualize_ibis()
    return


@app.cell
def _(VegaWidget, example, mo):
    import pandas


    def visualize_pandas():
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
        return mo.ui.anywidget(vega)


    visualize_pandas()
    return


@app.cell
def _(VegaWidget, example, mo):
    import polars


    def visualize_polars():
        values = polars.DataFrame(
            {
                "category": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "amount": [28, 55, 43, 91, 81, 53, 19, 87],
            }
        )
        data = {"table": values}
        vega = VegaWidget(spec=example, data=data)
        return mo.ui.anywidget(vega)


    visualize_polars()
    return


if __name__ == "__main__":
    app.run()
