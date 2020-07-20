
import plotly.express as px
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


bStats = pd.read_csv('./assets/BattingWar.csv')
draft = pd.read_csv('./assets/draft.csv')
salaries = pd.read_csv('./assets/Salaries.csv')
teams = pd.read_csv('./assets/Teams.csv')
position = pd.read_csv('./assets/Fielding.csv')
pitching= pd.read_csv('./assets/PitchingWar.csv')



#WAR BY PAYROLL

#Merging Batting Stats with Position
BatProll = pd.merge(bStats, position, on = ['teamID','yearID','playerID'], how = 'outer')
#Removing all pitchers
BatProll = BatProll[BatProll.POS != 'P']
#Merging BatProll and Salaries
BatProll = pd.merge(BatProll, salaries, on = ['teamID','yearID','playerID'], how= 'outer').reset_index()
BatProll = BatProll[['name_common','playerID','yearID','teamID','age','WAR','salary']]
#Merging Pitchers and Salaries
PitchProll = pd.merge(pitching, salaries, on = ['teamID','yearID','playerID'], how = 'outer').reset_index()
PitchProll = PitchProll[['name_common','playerID','yearID','teamID','age','WAR','salary']]
#Merging Bat Payroll and Pitch Payroll
proll = pd.merge(BatProll,PitchProll, how = 'outer')
proll = proll[(proll['yearID'] >= 1995) & (proll['yearID'] <= 2016)]
proll = proll.drop_duplicates()



#get non null salries
bool_series1 = pd.notnull(proll["salary"])
nonnullsalary = proll[bool_series1]
nonnullsalary = nonnullsalary[['playerID','yearID','salary']]
final = proll.merge(nonnullsalary, on=['playerID','yearID'], how='left')
final['salary'] = np.where(final['salary_x'].isnull(),final['salary_y'],final['salary_x'])
final = final.drop_duplicates()
del final['salary_y']
del final['salary_x']
final = final.dropna(axis=0, subset=['name_common']).reset_index(drop = True)
#print(final)



#payrollvsWins
sal = salaries[(salaries['yearID'] >= 1995) & (salaries['yearID'] <= 2016)]
teamyeargroup = sal.groupby(['yearID','teamID']).salary.sum().reset_index()
salaryWL = pd.merge(teamyeargroup,teams, on = ['teamID','yearID'], how = 'inner')
#print(salaryWL[['yearID','teamID','salary','W','L']])



external_stylesheets = []

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
team = sorted(final.teamID.unique())
year_id = sorted(final.yearID.unique())
app.layout = html.Div(children = [html.H1(children = "Welcome to the Baseball Stat Sheet!"),
    html.Div(children ='WAR by Player Salary', style = {'fontSize': 30}),
    html.Label('Year'),
    dcc.Dropdown(id='year', options=[{'label': i, 'value': i} for i in year_id],
                 value ='1995', style={'width': '300px'}),
    html.Label('Team'),
    dcc.Dropdown(id='team', options=[{'label': i, 'value': i} for i in team],
                 value = 'SFN', style={'width': '300px'}),
    dcc.Graph(id='graph'),
    html.Div(children ='Wins by Payroll ', style = {'fontSize': 30}),
    html.Label('Year'),
    dcc.Dropdown(id='year2', options=[{'label': i, 'value': i} for i in year_id],
                 value='1995', style={'width': '300px'}),
    dcc.Graph(id ='random_graph')])


@app.callback(
    Output('graph', 'figure'),
    [Input('year', 'value'),
     Input('team', 'value')])
def update_figure(selected_year, teamID):
    final_df = final[final.yearID == selected_year]
    final_df = final_df[final_df.teamID == teamID]
    fig = px.scatter(final_df, x="salary", y="WAR", hover_data= ['salary','WAR','name_common'],
                     trendline = 'ols', color = 'WAR')
    return fig
@app.callback(
    Output('random_graph', 'figure'),
    [Input('year2', 'value')]
)
def update_graph(year):
    import plotly.express as px
    return px.scatter(salaryWL[salaryWL.yearID == year], x = 'salary', y = 'W', trendline='ols',
                      hover_data= ['salary','W','teamID'],
                      size = 'salary', color = 'W',
                      labels = {
                          'salary':'Payroll', 'W':'Wins'
                      })


if __name__ == '__main__':
    app.run_server(debug=True)




