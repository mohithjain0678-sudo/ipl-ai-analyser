import streamlit as st
import pandas as pd
import plotly.express as px
from groq import Groq

st.set_page_config(page_title="IPL Analyser", page_icon="🏏", layout="wide")

matches = pd.read_csv('data/matches.csv')
deliveries = pd.read_csv('data/deliveries.csv')

import os
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

st.title("🏏 IPL Data Analyser")
st.markdown("Analysing IPL data from 2008 to 2024")

teams = sorted(matches['team1'].unique().tolist())
selected_team = st.selectbox("Select a Team", teams)

team_matches = matches[(matches['team1'] == selected_team) | (matches['team2'] == selected_team)]
team_wins = matches[matches['winner'] == selected_team]
total = len(team_matches)
wins = len(team_wins)
losses = total - wins
win_rate = round(wins/total*100, 1)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Matches", total)
col2.metric("Wins", wins)
col3.metric("Losses", losses)
col4.metric("Win Rate", f"{win_rate}%")

season_wins = team_wins['season'].value_counts().sort_index().reset_index()
season_wins.columns = ['season', 'wins']
fig1 = px.line(season_wins, x='season', y='wins',
               title=f'{selected_team} Wins Per Season',
               markers=True, line_shape='spline')
st.plotly_chart(fig1, width='stretch')

potm = matches[matches['winner'] == selected_team]['player_of_match'].value_counts().head(8).reset_index()
potm.columns = ['player', 'awards']
fig2 = px.bar(potm, x='player', y='awards',
              title=f'Top Players of the Match for {selected_team}',
              color='awards', color_continuous_scale='Greens')
st.plotly_chart(fig2, width='stretch')

venue_wins = team_wins['venue'].value_counts().head(6).reset_index()
venue_wins.columns = ['venue', 'wins']
fig3 = px.bar(venue_wins, x='wins', y='venue', orientation='h',
              title=f'{selected_team} Wins by Venue',
              color='wins', color_continuous_scale='Blues')
fig3.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig3, width='stretch')

st.divider()
st.subheader("🤖 Ask AI About IPL")

ipl_summary = f"""
You are an IPL cricket expert assistant. Here is some IPL data to help answer questions:
- Total matches in dataset: {len(matches)}
- Seasons covered: 2008 to 2024
- Top 5 teams by wins: {matches['winner'].value_counts().head(5).to_dict()}
- Top 5 Player of the Match: {matches['player_of_match'].value_counts().head(5).to_dict()}
- Total matches in Chennai: {len(matches[matches['city'] == 'Chennai'])}
- CSK win rate: 58%
- Toss winners win only 50.6% of matches
Answer questions based on this data. Be concise and friendly.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask anything about IPL..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": ipl_summary},
            {"role": "user", "content": prompt}
        ]
    )

    answer = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)