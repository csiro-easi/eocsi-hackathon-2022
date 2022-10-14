# Streamlit app
# View time layers from an xarray cube and allow the user to select layers for further processing / download.
# Use-case is broadly to manually filter a stack of satellite images base on clouds, sun-glint or whatever

# Run from EASI JupyterLab:
# 1. Open a Terminal and `cd` to this directory
# 2. `streamlit run xarray_image_select`
# 3. Open browser to https://hub.asia.easi-eo.solutions/user/USERNAME/proxy/8501/

import streamlit as st
import matplotlib.pyplot as plt
import dashboard_utils as app  # All the data manipulation functions are here

# Session variables
def refresh_state(input_file):
    if not is_state() or st.session_state['input_file'] != input_file:
        st.session_state['input_file'] = input_file
        ds = app.read_user_xarray(input_file)  # xr.Dataset or Read error string
        if isinstance(ds, str):  # If not a read error
            st.session_state['ds_error'] = ds
            if 'times' in st.session_state: del st.session_state['times']
        else:
            if 'ds_error' in st.session_state: del st.session_state['ds_error']
            st.session_state['times'] = app.xr_times(input_file)
            st.session_state['band'] = app.xr_bands(input_file)[0]
            st.session_state['vrange'] = (0,1)
            st.session_state['selected'] = dict()  # times-index: bool
            st.session_state['do_grid'] = True
def is_state():
    return 'input_file' in st.session_state
def is_valid():
    return 'times' in st.session_state
def do_grid():
    return st.session_state.get('do_grid', False)

def format_selected():
    return {
        st.session_state['times'][i] : st.session_state['selected'][i]
        for i in range(len(st.session_state['times']))
    }


# Headers
st.markdown(app.get_title())
st.sidebar.image(app.get_logo())

# Sidebar: Select file
# v1: text input JH file path and form submit button
# v2: upload_file widget. Will this upload from JH or desktop?
select_file_form = st.sidebar.form('select_file')
select_file = select_file_form.text_input(
    label = 'Xarray file name',
    help = 'Enter an xarray file name that can be read from your JupyterLab home directory.'
)
if select_file_form.form_submit_button('Read file'):
    refresh_state(select_file)


# Sidebar: Select display options
if is_state() and is_valid():
    select_band_form = st.sidebar.form('select_options')
    # Band
    bands = app.xr_bands(st.session_state['input_file'])
    band = select_band_form.radio(
        'Select variable',
        bands,
        index = bands.index(st.session_state['band'])
    )
    # Set colour range
    vmin = select_band_form.number_input(
        'Colour Min',
        value = st.session_state['vrange'][0]
    )
    vmax = select_band_form.number_input(
        'Colour Max',
        min_value = vmin,
        value = st.session_state['vrange'][1]
    )
    gridindex = 0
    if not do_grid(): gridindex = 1
    grid = select_band_form.radio(
        'Layer display',
        ['Grid', 'Slider'],
        index = gridindex
    )
    # Button
    if select_band_form.form_submit_button('Update'):
        st.session_state['band'] = band
        st.session_state['vrange'] = (vmin, vmax)
        st.session_state['do_grid'] = True
        if grid == 'Slider': st.session_state['do_grid'] = False


# Sidebar: Write file to JH
if is_state() and is_valid():
    selected = [k for k, v in st.session_state['selected'].items() if v]
    if len(selected) == 0:
        selected = range(len(st.session_state['times']))
    write_file_form = st.sidebar.form('write file')
    write_file = write_file_form.text_input(
        label = 'Output file name',
        help = 'Enter an output file name that can be written to your JupyterLab home directory.'
    )
    overwrite_file = write_file_form.checkbox(
        'Overwrite (if exists)'
    )
    if write_file_form.form_submit_button('Write file'):
        success, result = app.write_file(
            st.session_state['input_file'],
            st.session_state['band'],
            selected,
            write_file,
            overwrite_file
        )
        if success:
            write_file_form.write(f'Success! {result}')
        else:
            write_file_form.write(result)


# Expander: File summary
if is_state():
    with st.expander(f"File summary: {st.session_state['input_file']}"):
        if is_valid():
            st.code(app.xr_summary(st.session_state['input_file']))
            # st.markdown(ds.info(), unsafe_allow_html=True)
        else:
            st.code(app.xr_summary(st.session_state['ds_error']))


# Container-like: Slider, Full image, Checkbox, Button
# Accumulate checked items in the st.session_state['selected'] dict
if is_state() and is_valid() and not do_grid():
    # Slider
    view_time = st.select_slider(
        'Choose a timeslice',
        options = st.session_state['times'],
    )
    view_index = st.session_state['times'].index(view_time)

    # Image
    st.write(
        app.get_plot_for_timeslice(
            st.session_state['input_file'],
            st.session_state['band'],
            view_index,
            st.session_state['vrange']
        )
    )

    # Checkbox
    view_check = st.checkbox(
        'Select time layer',
        key = f"select_image_{view_index}",
        value = st.session_state['selected'].get(view_index, False)
    )
    st.session_state['selected'][view_index] = view_check

    # Submit button: show selected layers in a grid
    if st.button('Show selected layers'):
        st.write(format_selected())
        
        selected = [k for k, v in st.session_state['selected'].items() if v]
        num_cols = 3
        for i, view_index in enumerate(selected):
            if i % num_cols == 0:
                cols = st.columns(num_cols)
            fig = app.get_plot_for_timeslice(
                st.session_state['input_file'],
                st.session_state['band'],
                view_index,
                st.session_state['vrange']
            )
            cols[i % num_cols].pyplot(fig, dpi=100)


# Container-like: Form, Subplots, Checkboxes
if is_state() and is_valid() and do_grid():
    select_images_form = st.form('select_images')

    # Subplots
    num_cols = 3
    for view_index in range(len(st.session_state['times'])):
        if view_index % num_cols == 0:
            cols = select_images_form.columns(num_cols)

        # Image
        fig = app.get_plot_for_timeslice(
            st.session_state['input_file'],
            st.session_state['band'],
            view_index,
            st.session_state['vrange']
        )
        cols[view_index % num_cols].pyplot(fig, dpi=100)

        # Checkbox
        view_check = cols[view_index % num_cols].checkbox(
            'Select',
            key = f'select_image_{view_index}',
            value = st.session_state['selected'].get(view_index, False)
        )
        st.session_state['selected'][view_index] = view_check

    if select_images_form.form_submit_button('Update selected layers'):
        st.write(format_selected())
