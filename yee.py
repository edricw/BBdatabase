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
)