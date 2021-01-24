import pandas as pdimport numpy as npimport plotly.express as pximport dashimport dash_core_components as dccimport dash_html_components as htmlfrom dash.dependencies import Input, Outputimport dash_tableimport dash_bootstrap_components as dbcdesired_width = 320pd.set_option('display.max_columns', 20)pd.set_option('display.width', desired_width)bStats = pd.read_csv('./assets/BattingWar.csv')people = pd.read_csv('./assets/People.csv')teams = pd.read_csv('./assets/Teams.csv')salaries = pd.read_csv('./assets/Salaries.csv')salaries = pd.merge(salaries, teams, on=['yearID', 'teamID'], how='left')position = pd.read_csv('./assets/Fielding.csv')pitching = pd.read_csv('./assets/PitchingWar.csv')transactions = pd.read_csv('./assets/Transactions.csv')# WAR BY PAYROLL# Merging Batting Stats with Position￿ˀBatProll = pd.merge(bStats, position, on=['teamID', 'yearID', 'playerID'], how='outer')# Removing all pitchersBatProll = BatProll[BatProll.POS != 'P']# Merging BatProll and SalariesBatProll = pd.merge(BatProll, salaries, on=['teamID', 'yearID', 'playerID'], how='outer').reset_index()BatProll = BatProll[['name_common', 'playerID', 'yearID', 'teamID', 'age', 'WAR', 'salary']]# Merging Pitchers and SalariesPitchProll = pd.merge(pitching, salaries, on=['teamID', 'yearID', 'playerID'], how='outer').reset_index()PitchProll = PitchProll[['name_common', 'playerID', 'yearID', 'teamID', 'age', 'WAR', 'salary']]# Merging Bat Payroll and Pitch Payrollproll = pd.merge(BatProll, PitchProll, how='outer')proll = proll[(proll['yearID'] >= 1995) & (proll['yearID'] <= 2016)]proll = proll.drop_duplicates()proll = pd.merge(proll, teams, on=['teamID', 'yearID'])proll = proll[['name_common', 'playerID', 'yearID', 'teamIDBR', 'age', 'WAR', 'salary']]# AVG WARsumWAR = proll.groupby(['playerID']).WAR.sum().reset_index()# Trasaction/Draft# changing teamstransactions = pd.merge(transactions, teams, on=['yearID', 'teamIDretro'], how='left')transactions = pd.merge(transactions, people, on=['retroID'], how='left')transactions = transactions[['yearID', 'playerID', 'teamIDBR', 'to-league8', 'type', 'draft-round', 'pick-number10']]transactions = transactions[transactions.type.isin(["Dv", "D", "Da", "Df", "Dm"])]transactions = transactions[(transactions['yearID'] >= 1990) & (transactions['yearID'] <= 2019)]transactions = pd.merge(transactions, sumWAR, on=['playerID'], how='left')transactions = transactions[['yearID', 'playerID', 'teamIDBR', 'WAR', 'draft-round', 'pick-number10']]transactions = transactions.dropna(axis=0, subset=['draft-round', 'WAR']).reset_index(drop=True)# print(transactions)# WarbyYearyearWAR = transactions.groupby(['yearID']).WAR.sum().reset_index()fig = px.bar(yearWAR, x="yearID", y="WAR", hover_data=['WAR', 'yearID'], text='yearID', color='WAR', labels={    'yearID': 'Year', 'WAR': 'WAR'})# WARtablebyYeartransactionspicks = transactions[['yearID', 'playerID', 'teamIDBR', 'WAR', 'draft-round']]transactionspicks = pd.merge(transactionspicks, people, on=['playerID'], how='right')transactionspicks = transactionspicks.dropna(axis=0, subset=['draft-round', 'WAR']).reset_index(drop=True)transactionspicks['Full_Name'] = transactionspicks["nameFirst"] + " " + transactionspicks["nameLast"]transactionspicks= transactionspicks.rename(columns = {'yearID':'Draft_Year', 'teamIDBR':'Team',                                                       'draft-round': 'Round','War': 'Total War'})transactionspicks = transactionspicks[['Full_Name', 'Draft_Year', 'Team', 'Total War', 'Round']]transactionspicks = transactionspicks.round(3)# fig2.show()# get non null salriesbool_series1 = pd.notnull(proll["salary"])nonnullsalary = proll[bool_series1]nonnullsalary = nonnullsalary[['playerID', 'yearID', 'salary']]final = proll.merge(nonnullsalary, on=['playerID', 'yearID'], how='left')final['salary'] = np.where(final['salary_x'].isnull(), final['salary_y'], final['salary_x'])final = final.drop_duplicates()del final['salary_y']del final['salary_x']final = final.dropna(axis=0, subset=['name_common']).reset_index(drop=True)# print(final)# payrollvsWinssal = salaries[(salaries['yearID'] >= 1995) & (salaries['yearID'] <= 2016)]teamyeargroup = sal.groupby(['yearID', 'teamIDBR']).salary.sum().reset_index()salaryWL = pd.merge(teamyeargroup, teams, on=['teamIDBR', 'yearID'], how='inner')team = sorted(final.teamIDBR.unique())year_id = sorted(final.yearID.unique())draftRound = sorted(transactionspicks.Round.unique())dyear = sorted(transactionspicks.Draft_Year.unique())app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])server = app.serverapp.layout = html.Div([    dbc.Jumbotron([        html.H2("The Power of WAR - Interactive data visualizations & analytics"),        html.P(            "Analyze and explore how WAR can impact a MLB players and teams.",            className="lead",        ),        html.Hr(className="my-2"),        html.P([html.Small(            "By Edric Wong")            ])        ]),    dbc.Container([        dbc.Row([            html.H3('Interactive payroll charts based on WAR and Wins'),        ]),        dbc.Row([            dcc.Markdown(                """                **Chart 1**: Association between WAR and Player Salary                * Use the pulldown to select a year and filter by team.                                **Chart 2**: Association between Wns and Payroll                * Use the pulldown to select a year.                """            ),        ]),    dbc.Row([        dbc.Col([            html.Div([                dcc.Dropdown(                    id='year', options=[{'label': i, 'value': i} for i in year_id],                             value=1995, style={                        'textAlign': 'center',                        'margin': 'auto'})],                style={'width': '150px', 'display': 'inline-block'}            ),            html.Div([                dcc.Dropdown(                    id='team', options=[{'label': i, 'value': i} for i in team],                    value='BOS', style={                        'textAlign': 'center',                        'margin': 'auto'})],                    style={'width': '90px', 'display': 'inline-block'}            ),            dcc.Graph('shot-chart-1', config={'displayModeBar': False})        ], lg =6, md =12),        dbc.Col([           html.Div([               dcc.Dropdown(id='year2', options=[{'label': i, 'value': i} for i in year_id],                                    value = 1995, style={                               'textAlign': 'center',                               'width': '150px',                               'margin': 'auto',                               'whiteSpace': 'pre-wrap'})], style={'width': '90px', 'display': 'inline-block'}           ),            dcc.Graph('random_graph')        ], lg =6, md =12)]        ),    ]),    dbc.Container([        dbc.Row([            html.H3('Yearly MLB Draft by Total War'),        ]),        dbc.Row([            dcc.Markdown(                """                **Table 1**: MLB draft from 1990 to 2015                 * Use the pulldown to select draft round and toggle by Draft Year.                                **Chart 3**: WAR by Draft Year                """            ),        ]),        dbc.Row([            html.Div([                dcc.Markdown(                    """                    Round:                    """                )            ], style= {                'line-height': 1.5,                'margin-left': '15px'            })        ]),        dbc.Row([            dbc.Col([                html.Div([                    dcc.Dropdown(id = 'dround', options=[{'label': i, 'value': i} for i in draftRound],                                 value=1,                                style={                                          'textAlign': 'center',                                          'width': '100px',                                          'margin': 'auto',                                          'whiteSpace': 'pre-wrap'})],                    style={'width': '90px', 'display': 'inline-block'}                ),                html.Div(id ='yeet'),                html.Div([                    dcc.Slider(                             id='year-slider',                             min=1990,                             max=2015,                             value=1990,                             marks={1990: {'label': '1990'},                                    1991: {'label': ''},                                    1992: {'label': ''},                                    1993: {'label': ''},                                    1994: {'label': ''},                                    1995: {'label': '1995'},                                    1996: {'label': ''},                                    1997: {'label': ''},                                    1998: {'label': ''},                                    1999: {'label': ''},                                    2000: {'label': '2000'},                                    2001: {'label': ''},                                    2002: {'label': ''},                                    2003: {'label': ''},                                    2004: {'label': ''},                                    2005: {'label': '2005'},                                    2006: {'label': ''},                                    2007: {'label': ''},                                    2008: {'label': ''},                                    2009: {'label': ''},                                    2010: {'label': '2010'},                                    2011: {'label': ''},                                    2012: {'label': ''},                                    2013: {'label': ''},                                    2014: {'label': ''},                                    2015: {'label': '2015'}},                             step=None)]),            ]),            dbc.Container([dbc.Col([                html.Div([                    dcc.Graph(id='draftWar', figure=fig)                ])            ])            ])        ])        ])    ])@app.callback(    Output('shot-chart-1', 'figure'),    [Input('year', 'value'),     Input('team', 'value')])def update_figure(selected_year, teamIDBR):    final_df = final[final.yearID == selected_year]    final_df = final_df[final_df.teamIDBR == teamIDBR]    import plotly.express as px    return px.scatter(final_df, x="salary", y="WAR", hover_data=['salary', 'WAR', 'name_common'],                     trendline='ols', color='WAR',                     labels={                         'salary': 'Salary'})@app.callback(    Output('random_graph', 'figure'),    [Input('year2', 'value')])def update_graph(year):    import plotly.express as px    return px.scatter(salaryWL[salaryWL.yearID == year], x='salary', y='W', trendline='ols',                      hover_data=['salary', 'W', 'teamIDBR'],                      size='salary', color='W',                      labels={                          'salary': 'Payroll', 'W': 'Wins'                      })@app.callback(    Output('yeet', 'children'),    [Input('dround', 'value'),     Input('year-slider', 'value')])def get_data_table(option, selected_year):    drafts = transactionspicks[transactionspicks.Round == option]    drafts = drafts.sort_values('Round')    drafts = drafts.sort_values('Total War')    drafts = drafts[drafts.Draft_Year == selected_year]    yeet = dash_table.DataTable(columns=[{"name": i, "id": i} for i in drafts.columns],                                data=drafts.to_dict('records'),                                fixed_rows={'headers': True},                                page_size=100,                                style_cell={'minWidth': 80, 'maxWidth': 80, 'width': 80},                                style_table={'overflowX': 'auto'},                                css=[{'selector': '.row', 'rule': 'margin: 0'}]                                )    return yeetif __name__ == '__main__':    app.run_server(debug=True)