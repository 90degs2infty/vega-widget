import anywidget
from pathlib import Path
import traitlets
from typing import Any
import json
from ._to_records import to_records as _to_records


class VegaWidget(anywidget.AnyWidget):
    _esm: Path = Path(__file__).parent / "static" / "index.js"
    _css: str = ""

    # Un-sanitized raw user-input
    spec = traitlets.Dict(key_trait=traitlets.Unicode(), default_value={})
    data = traitlets.Dict(key_trait=traitlets.Unicode(), default_value={})

    # Sanitized output towards js
    _spec_json = traitlets.Unicode(default_value="").tag(sync=True)
    _records_json = traitlets.Unicode(default_value={}).tag(sync=True)

    def __init__(self, spec: dict[str, Any] = {}, data: dict[str, Any] = {}) -> None:
        self.spec = spec
        self.data = data
        super().__init__()

    @traitlets.observe("spec")
    def _on_spec_change(self, change: dict):
        new_spec = VegaWidget._patch_spec(change["new"], self.data.keys())

        self._spec_json = json.dumps(new_spec)

    @traitlets.observe("data")
    def _on_data_change(self, change: dict):
        new_data = change["new"]
        old_data = change["old"]

        record_dict = {
            name: _to_records(df) for name, df in new_data.items()
        }
        self._records_json = json.dumps(record_dict)

        # Trigger re-patching the data section of spec
        if len(set(new_data.keys()).symmetric_difference(old_data.keys())) > 0:
            new_spec = VegaWidget._patch_spec(self.spec, new_data.keys())
            self._spec_json = json.dumps(new_spec)
    
    @staticmethod
    def _patch_spec(spec: dict[str, Any], datasets: list[str]) -> dict[str, Any]:
        spec["data"] = {"name": d for d in datasets}
        return spec
