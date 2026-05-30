import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

matches = pd.read_csv('data/matches.csv')
deliveries = pd.read_csv('data/deliveries.csv')

team_wins = matches['winner'].value_counts().head(10).reset_index()
team_wins.columns = ['team', 'wins']

fig1 = px.bar(team_wins, x='wins', y='team', orientation='h',
              title='Top 10 IPL Teams by Total Wins',
              color='wins', color_continuous_scale='Reds')
fig1.update_layout(yaxis={'categoryorder':'total ascending'})
fig1.show()

csk_wins = matches[matches['winner'] == 'Chennai Super Kings']
csk_season = csk_wins['season'].value_counts().sort_index().reset_index()
csk_season.columns = ['season', 'wins']

fig2 = px.line(csk_season, x='season', y='wins',
               title='CSK Wins Per Season',
               markers=True, line_shape='spline')
fig2.update_traces(line_color='#FFD700', marker_color='blue')
fig2.show()

toss = matches['toss_decision'].value_counts().reset_index()
toss.columns = ['decision', 'count']

fig3 = px.pie(toss, values='count', names='decision',
              title='Toss Decision — Bat vs Field',
              color_discrete_sequence=['#00BFFF', '#FF6347'])
fig3.show()

potm = matches['player_of_match'].value_counts().head(10).reset_index()
potm.columns = ['player', 'awards']

fig4 = px.bar(potm, x='player', y='awards',
              title='Top 10 Player of the Match Awards',
              color='awards', color_continuous_scale='Blues')
fig4.show()

print("All charts generated successfully!")