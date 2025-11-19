import streamlit as st
import pandas as pd

from ui.results_ui import choose_results, add_filters, apply_filters, filter_results
from utils.results import explode_indicator_strings
from core.graphsandstats import show_heatmap, heatmap_selector
from core.strategy_holder import strategy_classes
from utils.session import init_results_session_state


            






init_results_session_state()

#---CHOOSE DATAFRAME
choose_results() # Sets current_optimiser_results
#st.write(st.session_state.current_strategy)

st.session_state.current_optimiser_results = explode_indicator_strings(st.session_state.current_optimiser_results) # Shouldn't be changing any session state here


if isinstance(st.session_state.current_optimiser_results, pd.DataFrame) and not st.session_state.current_optimiser_results.empty:
    st.dataframe(st.session_state.current_optimiser_results)



#---APPLY FILTERS---
filter_results(st.session_state.current_optimiser_results)


#---PLOTTING HEATMAP---
df = st.session_state.filtered_results
if isinstance(df, pd.DataFrame) and not df.empty:
    st.subheader("Filtered Results:")
    st.dataframe(df)
    heatmap_selector(df, show_heatmap)









#---CHANGES---
# want to be able to choose filters on the results - ie require > 4 trades WIP
# Change to more bins in heatmap DONE 
# Combine heatmap with filtered dataframe, so if we have three variables we can isolate one and look at the heatmap for the other two DONE


#---BUGS--- 
# Max/min change need fixing, they dont account for the final trade.