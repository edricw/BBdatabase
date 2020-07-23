import plotly.express as px
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


bStats = pd.read_csv('./assets/BattingWar.csv')
people = pd.read_csv('./assets/People.csv')
teams = pd.read_csv('./assets/Teams.csv')
salaries = pd.read_csv('./assets/Salaries.csv')
salaries = pd.merge(salaries, teams, on = ['yearID','teamID'], how = 'left')
position = pd.read_csv('./assets/Fielding.csv')
pitching= pd.read_csv('./assets/PitchingWar.csv')
transactions = pd.read_csv('./assets/Transactions.csv')






#WAR BY PAYROLL

#Merging Batting Stats with Position￿ˀ
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
proll = pd.merge(proll, teams, on = ['teamID','yearID'])
proll = proll[['name_common','playerID','yearID','teamIDBR','age','WAR','salary']]

#AVG WAR
avgWAR = proll.groupby(['playerID']).WAR.sum().reset_index()

#Trasaction/Draft
#changing teams
transactions = pd.merge(transactions, teams, on = ['yearID', 'teamIDretro'], how = 'left')
transactions = pd.merge(transactions, people, on = ['retroID'], how = 'left')
transactions = transactions[['yearID','playerID','teamIDBR','to-league8','type','draft-round','pick-number10']]
transactions = transactions[transactions.type.isin(["Dv", "D","Da","Df","Dm"])]
transactions = transactions[(transactions['yearID'] >= 1985) & (transactions['yearID'] <= 2019)]
transactions = pd.merge(transactions,avgWAR, on= ['playerID'], how = 'left')
transactions = transactions[['yearID','playerID','teamIDBR','WAR','draft-round','pick-number10']]
transactions = transactions.dropna(axis=0, subset=['draft-round','WAR']).reset_index(drop = True)
#print(transactions)


#WarbyYear
yearWAR = transactions.groupby(['yearID']).WAR.sum().reset_index()
fig = px.bar(yearWAR, x="yearID", y="WAR", hover_data= ['WAR','yearID'], text = 'yearID', color = 'WAR', labels = {
                          'yearID':'Year', 'WAR':'WAR'
                      })
#fig.show()

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
teamyeargroup = sal.groupby(['yearID','teamIDBR']).salary.sum().reset_index()
salaryWL = pd.merge(teamyeargroup,teams, on = ['teamIDBR','yearID'], how = 'inner')


team = sorted(final.teamIDBR.unique())
year_id = sorted(final.yearID.unique())

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(
    [html.H1(children = "Welcome to the Baseball Stat Sheet!", style = {'textAlign': 'center'}),html.Div([
        html.Div([
            html.H3(children ='WAR by Player Salary', style = {'fontSize': 30, 'textAlign': 'center'}),
            html.Label('Year',style = {'textAlign': 'center'}),
            dcc.Dropdown(id='year', options=[{'label': i, 'value': i} for i in year_id],
                 value ='1995', style={
              'textAlign':'center',
              'width': '300px',
              'margin':'auto'}),
            html.Label('Team',style = {'textAlign': 'center'}),
            dcc.Dropdown(id='team', options=[{'label': i, 'value': i} for i in team],
                         value='SFN', style={
              'textAlign':'center',
              'width': '300px',
              'margin':'auto'}),
            dcc.Graph(id='graph', style = {'display': 'inline-block', 'height':'850', 'width':"700px"})
        ], className="six columns"),
        html.Div([
            html.H3(children ='Wins by Payroll ', style = {'fontSize': 30, 'textAlign': 'center'}),
            html.Br(),
            html.Label('Year',style = {'textAlign': 'center'}),
            dcc.Dropdown(id='year2', options=[{'label': i, 'value': i} for i in year_id],
                 value='1995', style={
              'textAlign':'center',
              'width': '300px',
              'margin':'auto'}),
            html.Br(),
            dcc.Graph(id = 'random_graph', style = {'display': 'inline-block','height':'850', 'width':"700px"})
        ], className="six columns"),
    ], className="row"),
                       html.Div(children='WAR by Draft Year', style={'fontSize': 30, 'textAlign': 'center'}),
                       dcc.Graph(id='draftWar', figure=fig)])



@app.callback(
    Output('graph', 'figure'),
    [Input('year', 'value'),
     Input('team', 'value')])
def update_figure(selected_year, teamIDBR):
    final_df = final[final.yearID == selected_year]
    final_df = final_df[final_df.teamIDBR == teamIDBR]
    fig = px.scatter(final_df, x="salary", y="WAR", hover_data= ['salary','WAR','name_common'],
                     trendline = 'ols', color = 'WAR',
                     labels={
                         'salary': 'Salary'})
    return fig
@app.callback(
    Output('random_graph', 'figure'),
    [Input('year2', 'value')]
)
def update_graph(year):
    import plotly.express as px
    return px.scatter(salaryWL[salaryWL.yearID == year], x = 'salary', y = 'W', trendline='ols',
                      hover_data= ['salary','W','teamIDBR'],
                      size = 'salary', color = 'W',
                      labels = {
                          'salary':'Payroll', 'W':'Wins'
                      })


if __name__ == '__main__':
    app.run_server(debug=True)


