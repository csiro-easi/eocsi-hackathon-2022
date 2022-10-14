# Dashboards <img align="right" src="../resources/csiro_easi_logo.png">

This folder contains dashboards that can be run in EASI. A dashboard is a simple user-interface or webapp that allows a user to interact with data by setting and changing options that may affect the processing, display or selection of the data.

Typically we use notebooks to develop our code and methods that process the data. A dashboard can be designed that allow users to interact with the data and methods without needing to know the code.

## Let's get started

To run a Streamlit dashboard in EASI JupyterLab:
1. Open a Terminal and `cd` to this directory
1. `streamlit run ui_xarray_image_select`
1. Open browser to https://hub.asia.easi-eo.solutions/user/USERNAME/proxy/8501/
1. `Ctrl-c` in the Terminal to stop the streamlit process

## Available dashboards

| Framework | Name | Purpose |
| --- | --- | --- |
| streamlit | `ui_xarray_image_select.py` | View time layers from an xarray cube and allow the user to select layers for further processing or download. An example use-case is to manually filter a stack of satellite images base on clouds, sun-glint or whatever. |
 
## Resources

Dashboards operate at the interface between visualisation and data processing libraries with consideration of data transfer between server (EASI) and client (browser). It is good practice for all dashboards to separate the UI code from the data processing code.

### Dash

[Plotly Dash](https://dash.plotly.com/) - Mid to lower level dashboard tools.

Examples
- https://github.com/ucg8j/awesome-dash

### Steamlit

[Streamlit](https://docs.streamlit.io/) - Mid level dashboard library.

Features
- Easy to use widgets and tools
- Page is reloaded on each interaction so:
  - record the state of widgets in the `session_state` variable
  - use server-side caching for objects that may take a noticable amount of time to construct (e.g., data arrays and images)

Examples
- http://awesome-streamlit.org

### Holoviz

[Holoviz](https://holoviz.org/) - Higher level tools that take advantage of data labelling features of `pandas` and `xarray`.

Examples
- https://awesome-panel.org
