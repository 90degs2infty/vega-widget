import  embed from 'vega-embed';
import { type View } from 'vega';


function render({ model, el }) {
  el.classList.add("vega-widget-root");
  const container = document.createElement("div");
  container.className = "vega-widget-container";
  el.appendChild(container);

  let currentView: View | null = null;

  async function handleSpecChange() {
    if (currentView) {
      currentView.finalize();
      currentView = null;
    }

    const spec = model.get("_spec_json");

    if (spec.length === 0) {
      container.textContent = "Spec empty - specify a different spec instead";

      return;
    }

    // TODO not particularily resource friendly to rebuild the entire view on each spec change - but
    // sufficient for the moment.
    try {
      const _spec = JSON.parse(spec);

      const result = await embed(
        container,
        _spec
      );
      currentView = result.view;
    } catch(err) {
      container.textContent = "Vega embed error: " + err.message;
    }
  }

  async function handleDataChange() {
    if (!currentView) {
      return;
    }

    const record_dict = JSON.parse(model.get("_records_json"));

    for (const [name, records] of Object.entries(record_dict)) {
      await currentView.data(name, records).runAsync();
    }

    // Do a final resize to also update axes, if needed.
    await currentView.resize().runAsync();
  }

  //TODO in case both spec and data change, how to make sure the data change is processed _after_ the spec change?
  model.on("change:_spec_json", handleSpecChange);
  model.on("change:_records_json", handleDataChange);

  handleSpecChange().then(() => handleDataChange());

  return () => {
    if (currentView) {
      currentView.finalize();
      currentView = null;
    }
  };
}

export default { render };