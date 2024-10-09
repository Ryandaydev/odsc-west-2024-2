import streamlit as st
import pandas as pd
import logging
import nfl_data_py as nfl
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__) 

st.header("SportWorldCentral Data App")
st.subheader("Team Touchdown Totals")

try:

    flat_team_df_ordered = st.session_state['flat_team_df_ordered']

    unique_leagues = st.session_state['unique_leagues']
    selected_league = st.sidebar.selectbox('Pick league ID',unique_leagues)

    st.sidebar.divider()
    st.sidebar.subheader(":blue[Data sources]")
    st.sidebar.text("SportsWorldCentral")
    st.sidebar.text("NFLDataPy")


    flat_team_df_ordered['league_id'] = flat_team_df_ordered['league_id'].astype(str)
    flat_team_df_ordered = flat_team_df_ordered[
        flat_team_df_ordered['league_id'] == selected_league]

    nfl_data_2023_df = nfl.import_seasonal_data([2023], 'REG')
    columns_to_select = ['player_id', 'passing_tds', 'rushing_tds', 'receiving_tds']
    nfl_data_2023_subset_df = nfl_data_2023_df[columns_to_select].copy()

    nfl_data_2023_subset_df['total_tds'] = (
        nfl_data_2023_subset_df['passing_tds'] + 
        nfl_data_2023_subset_df['rushing_tds'] + 
        nfl_data_2023_subset_df['receiving_tds']
    )

    merged_df = pd.merge(
        flat_team_df_ordered,
        nfl_data_2023_subset_df,
        how='left',   
        left_on='gsis_id',
        right_on='player_id'
    )

    grouped_df = merged_df.groupby('team_name')['total_tds'].sum()
    fig, ax = plt.subplots()
    grouped_df.plot(kind="barh", xlabel='Total TDs', 
                    ylabel="Team Name", title="Total TDs - 2023", ax=ax)
    st.pyplot(fig)

except Exception as e:
    st.write(f"An unexpected error occurred: {str(e)}")
