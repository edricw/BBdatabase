app.layout = html.Div([
    dbc.Jumbotron([
        html.H2("Hindsights on the NBA - Interactive data visualizations & analytics"),
        html.P(
            "Analyse and compare each NBA teams' tendencies, strengths and weaknesses.",
            className="lead",
        ),
        html.Hr(className="my-2"),
        html.P([html.Small(
            "By JP Hwang - Find me on "), html.A(html.Small("twitter"), href="https://twitter.com/_jphwang", title="twitter")
        ])
    ]),
    dbc.Container([
        dbc.Row([
            html.H3('Interactive shot charts'),
        ]),
        dbc.Row([
            dcc.Markdown(
                """
                Use the pulldown to select a team, filter by quarter, and a shot quality measure.
                * **Frequency**: How often a team shoots from a spot, indicated by **size**.
                * **Quality**: Good shot or bad shot? Measured by shot accuracy
                or by points per 100 shots, indicated by **colour**. League avg: ~105.
                """
            ),
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Dropdown(
                        id='team-select-1',
                        options=[{'label': i, 'value': i} for i in shots_teams_list],
                        value='NBA',
                    )],
                    style={'width': '90px', 'display': 'inline-block'}
                ),
                html.Div([
                dcc.Dropdown(
                    id='period-select-1',
                    options=[{'label': i, 'value': i} for i in avail_periods],
                    value=1,
                    )],
                    style={'width': '90px', 'display': 'inline-block'}
                ),
                html.Div([
                    dcc.Dropdown(
                        id='stat-select-1',
                        options=[
                            {'label': 'Accuracy', 'value': 'acc_abs'},
                            {'label': 'Accuracy vs NBA avg', 'value': 'acc_rel'},
                            {'label': 'Points per shot', 'value': 'pps_abs'}
                        ],
                        value='pps_abs',
                    )],
                    style={'width': '250px', 'display': 'inline-block'}
                ),
                html.Div([
                    dcc.DatePickerRange(
                        id='date-picker-1',
                        min_date_allowed=min(pd.to_datetime(shots_df.date)).date(),
                        max_date_allowed=max(pd.to_datetime(shots_df.date)).date(),
                        initial_visible_month=max(pd.to_datetime(shots_df.date)).date(),
                        start_date_placeholder_text='From',
                        end_date_placeholder_text='To',
                        clearable=True,
                        # start_date=min(pd.to_datetime(shots_df.date)).date(),
                        # end_date=max(pd.to_datetime(shots_df.date)).date(),
                    )
                ]),
                dcc.Graph('shot-chart-1', config={'displayModeBar': False})
            ], lg=6, md=12),
            dbc.Col([
                html.Div([
                    dcc.Dropdown(
                        id='team-select-2',
                        options=[{'label': i, 'value': i} for i in shots_teams_list],
                        value='NBA',
                    )],
                    style={'width': '90px', 'display': 'inline-block'}
                ),
                html.Div([
                    dcc.Dropdown(
                        id='period-select-2',
                        options=[{'label': i, 'value': i} for i in avail_periods],
                        value=4,
                    )],
                    style={'width': '90px', 'display': 'inline-block'}
                ),
                html.Div([
                    dcc.Dropdown(
                        id='stat-select-2',
                        options=[
                            {'label': 'Accuracy', 'value': 'acc_abs'},
                            {'label': 'Accuracy vs NBA avg', 'value': 'acc_rel'},
                            {'label': 'Points per shot', 'value': 'pps_abs'}
                        ],
                        value='pps_abs',
                    )],
                    style={'width': '250px', 'display': 'inline-block'}
                ),
                html.Div([
                    dcc.DatePickerRange(
                        id='date-picker-2',
                        min_date_allowed=min(pd.to_datetime(shots_df.date)).date(),
                        max_date_allowed=max(pd.to_datetime(shots_df.date)).date(),
                        initial_visible_month=max(pd.to_datetime(shots_df.date)).date(),
                        start_date_placeholder_text='From',
                        end_date_placeholder_text='To',
                        clearable=True,
                        # start_date=min(pd.to_datetime(shots_df.date)).date(),
                        # end_date=max(pd.to_datetime(shots_df.date)).date(),
                    )
                ]),
                dcc.Graph('shot-chart-2', config={'displayModeBar': False})
            ], lg=6, md=12)]
        ),
    ]),
    dbc.Container([
        dbc.Row([
            html.H3('Offensive loads & efficiency per player, by minute:'),
        ]),
        dbc.Row([
            dcc.Markdown(
                """
                This chart compares players based on shot *frequency* and *efficiency*, 
                divided up into minutes of regulation time for each team.
                Use the pulldown to select a team, or select 'Leaders' to see leaders from each team.
                * **Frequency**: A team's shots a player is taking, indicated by **size**.
                * **Efficiency**: Points scored per 100 shots, indicated by **colour** (red == better, blue == worse).
                * Players with <1% of team shots are shown under 'Others'
                """
            ),
        ]),
        html.Div([
            dcc.Dropdown(
                id='shot-dist-group-select',
                options=[{'label': i, 'value': i} for i in dist_teams_list],
                value='TOR',
                style={'width': '140px'}
            )
        ]),
        dcc.Graph(
            'shot-dist-graph',
            config={'displayModeBar': False}
        )
    ]),
    dbc.Container([
        html.H3('Related articles'),
        html.Ul([
            html.Li([html.A("Build a web data dashboard in just minutes with Python", href="https://towardsdatascience.com/build-a-web-data-dashboard-in-just-minutes-with-python-d722076aee2b", title="article link")]),
        ])
    ]),
    dbc.Container([
        html.Small('Data from games up to & including: ' + latest_data + '.')
    ]),
    dbc.Container([
        html.P([
            html.Small("© JP Hwang 2020 ("),
            html.A(html.Small("twitter"), href="https://twitter.com/_jphwang", title="twitter"),
            html.Small("), built using Python & Plotly Dash")
        ])
    ]),
])


@app.callback(
    Output('shot-chart-1', 'figure'),
    [Input('team-select-1', 'value'), Input('period-select-1', 'value'), Input('stat-select-1', 'value'),
     Input('date-picker-1', 'start_date'), Input('date-picker-1', 'end_date')]
)
def call_shotchart_1(teamname, period, stat_type, start_date, end_date):

    fig = viz.plot_shot_chart(shots_df, teamname, period, stat_type, start_date, end_date, title="Shot chart, " + seasonyr_str)

    return fig


@app.callback(
    Output('shot-chart-2', 'figure'),
    [Input('team-select-2', 'value'), Input('period-select-2', 'value'), Input('stat-select-2', 'value'),
     Input('date-picker-2', 'start_date'), Input('date-picker-2', 'end_date')]
)
def call_shotchart_2(teamname, period, stat_type, start_date, end_date):

    fig = viz.plot_shot_chart(shots_df, teamname, period, stat_type, start_date, end_date, title="Shot chart, " + seasonyr_str)

    return fig


@app.callback(
    Output('shot-dist-graph', 'figure'),
    [Input('shot-dist-group-select', 'value')]
)
def update_shot_dist_chart(grpname):

    fig = viz.make_shot_dist_chart(
        all_teams_df[all_teams_df.group == grpname], col_col='pl_pps', range_color=[90, 120], size_col='shots_freq')
    viz.clean_chart_format(fig)

    if len(grpname) > 3:
        fig.update_layout(height=850, width=1250)
    else:
        fig.update_layout(height=500, width=1250)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)