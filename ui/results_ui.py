from os import remove
import streamlit as st
import pandas as pd

from ui.sidebar import data_select_box
from core.strategy_holder import strategy_classes
from utils.results import get_results_df, filters_dict





def choose_results():
    '''
    Select data and strategy
    '''
    with st.sidebar.expander("Select Data"):
        strategy_type = st.selectbox("Strategy", ["None"] + list(strategy_classes.keys()), key='results_strategy')
        crypto, period, interval = data_select_box(key="Results_Selection")

        if st.button("Fetch Results", key="fetch_results"):
            # Refresh Filters
            st.session_state.filters = {}

            # Use correct data_name
            data_name = f"{crypto}_{interval}_{period}"
            
            st.session_state.current_strategy = strategy_type
            st.session_state.current_data_name = data_name
    # Load results
    if (
        "current_strategy" in st.session_state 
        and st.session_state.current_strategy != "None"
        and "current_data_name" in st.session_state
    ):
        StrategyClass = strategy_classes[st.session_state.current_strategy]
        data_name = st.session_state.current_data_name
        df = get_results_df(StrategyClass, data_name)
        if df is None:
            st.warning("No results found for this selection.")
            st.session_state.current_optimiser_results = pd.DataFrame()
        else:
            st.session_state.current_optimiser_results = df




#---FILTER RESULTS---

def add_filters(df):
    # this could be a lot better...
    with st.sidebar.expander("Apply Filter"):
        condition = None
        strategy_params = filters_dict[st.session_state.current_strategy]
        col_name = st.selectbox("Column", ["None"] + [k for k in strategy_params.keys()])

        if col_name == "None":
            return 
        
        if col_name == "Number of Trades":
            condition = st.number_input("Minimum Trades:", value=0, step=1)

        if strategy_params[col_name] == "discrete":
            strategy = strategy_classes[st.session_state.current_strategy]
            s = col_name.replace("_type", "")
            condition = st.selectbox("Indicator Type:", [k for k in strategy.param_config[s]["allowed"]])

        if strategy_params[col_name] == "float":
            condition = st.number_input("Fix value:", value=0.0, step=0.01)
           

        if st.button("Apply Filter"):
            if col_name != "None" and condition is not None:
                st.session_state.filters[col_name] = condition





def apply_filters(df):
    st.session_state.filtered_results = df
    for col_name, condition in st.session_state.filters.items():
        if col_name == "Number of Trades":
            st.session_state.filtered_results = st.session_state.filtered_results[st.session_state.filtered_results[col_name] >= condition]
        if type(condition) == str:
            st.session_state.filtered_results = st.session_state.filtered_results[st.session_state.filtered_results[col_name] == condition]
        if filters_dict[st.session_state.current_strategy][col_name] == "float":
            st.session_state.filtered_results = st.session_state.filtered_results[st.session_state.filtered_results[col_name] == condition]

def remove_filter():
    with st.sidebar.expander("Remove Filter"):
        filter = st.selectbox("Filter", ["None"] + [k for k in st.session_state.filters.keys()])
        if filter != "None":
            if st.button("Remove"):
                del st.session_state.filters[filter]

def filter_results(df):
    add_filters(df)
    apply_filters(df)
    remove_filter()
    