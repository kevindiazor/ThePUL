import streamlit as st
import plotly.express as px

st.title("Player Statistics")

# Player search and filters
col1, col2 = st.columns([2, 1])
with col1:
    search_term = st.text_input("Search Players", "")
with col2:
    stat_filter = st.selectbox("Sort By", ["points", "assists", "completions", "throws", "catches"])

# Filter players based on search
filtered_players = st.session_state.players_df[
    st.session_state.players_df['name'].str.contains(search_term, case=False)
]

# Sort players
sorted_players = filtered_players.sort_values(stat_filter, ascending=False)

# Display players table
st.dataframe(
    sorted_players[['name', 'team', 'points', 'assists', 'completions', 'throws', 'catches']],
    use_container_width=True
)

# Top performers visualization
st.subheader("Top 10 Players by Selected Stat")
top_10 = sorted_players.head(10)
fig = px.bar(
    top_10,
    x='name',
    y=stat_filter,
    title=f"Top 10 Players by {stat_filter.title()}",
    color='team'
)
st.plotly_chart(fig, use_container_width=True)
