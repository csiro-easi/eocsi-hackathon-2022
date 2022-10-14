# Dashboards <img align="right" src="../resources/csiro_easi_logo.png">

This folder contains dashboards that can be run in EASI. A dashboard is a simple user-interface or webapp that allows a user to interact with data by setting and changing options that may affect the processing, display or selection of the data.

Typically we use notebooks to develop our code and methods that process the data. A dashboard can be designed that allow users to interact with the data and methods without needing to know the code.

## Let's get started

To run a Streamlit dashboard in EASI JupyterLab:
1. Open a Terminal and `cd` to this directory
1. `streamlit run ui_xarray_image_select.py`
1. Open browser to https://hub.asia.easi-eo.solutions/user/USERNAME/proxy/8501/. Replace USERNAME with your username.
1. `Ctrl-c` in the Terminal to stop the streamlit process

## Available dashboards

| Framework | Name | Purpose |
| --- | --- | --- |
| streamlit | `ui_xarray_image_select.py` | View time layers from an xarray cube and allow the user to select layers for further processing or download. An example use-case is to manually filter a stack of satellite images base on clouds, sun-glint or whatever. |
 
## Resources

Dashboards operate at the interface between visualisation and data processing libraries and require consideration of data transfers between the server (EASI) and the client (browser). Typically most libraries transfer data to the client and render images in the client. For large data arrays this can be inefficient and slow. This page has an execellent description of the problem: https://datashader.org/getting_started/Pipeline.html.

When designing data-intensive notebooks, dashboards and user-interfaces we want to consider libraries and workflows that retain the source data on the server and only transfer the results (images, summaries) to the client where possible.

### Steamlit

[Streamlit](https://docs.streamlit.io/) - Mid-level dashboard library.

Matt's tips & tricks:
- Easy to use widgets and tools, see [Streamlit API reference](https://docs.streamlit.io/library/api-reference) and the examples.
- It is good practice to separate the UI code from the data processing code, e.g. consider the [model-view-controller](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller) software pattern.
- The UI page is reloaded on each widget interaction. Some ways to manage this are
  - Use the `session_state` variable (dict-like) to save the state or value of widgets between page reloads.
  - Use a `form` container to collect inputs from multiple widgets, which are then applied (and teh page refreshed) when the corresponding `form_submit_button` is pressed.
  - Use server-side caching for objects that may take a noticable amount of time to construct (e.g., data arrays and images). The `dashboard_utils.py` file has some information and examples for difference caching options.
- Events between widgets is not available, which means that a click in one widget can not send an event that another widget can respond to. Instead the page would need to be refereshed with a new state.

Examples
- http://awesome-streamlit.org

### Holoviz

[Holoviz](https://holoviz.org/) - Higher level tools that take advantage of data labelling features of `pandas` and `xarray`.

Examples
- https://awesome-panel.org

### Dash

[Plotly Dash](https://dash.plotly.com/) - Mid to lower-level dashboard tools.

Examples
- https://github.com/ucg8j/awesome-dash
