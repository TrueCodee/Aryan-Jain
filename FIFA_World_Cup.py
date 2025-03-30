# Link to deployed app: https://fifa-world-cup-dashboard.onrender.com
# Link to github http (in case render doesn't work): 
# No password required

import pandas as pd
import numpy as np
import dash
from dash import dcc, html, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Create a Flask app
app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server

# Reads the data
df = pd.read_csv('data.csv')

# Dataframe with the count of wins for each country
winners_count = df['Winner'].value_counts().reset_index()
winners_count.columns = ['Country', 'Wins']

# Dataframe with the count of runner-ups for each country
runner_ups_count = df['Runner_Up'].value_counts().reset_index()
runner_ups_count.columns = ['Country', 'Runner_Ups']

# List of unique years
years = df['Year'].unique().tolist()
years.sort()

# List of unique countries that have won or been runner-up
countries = list(set(df['Winner'].unique().tolist() + df['Runner_Up'].unique().tolist()))
countries.sort()

# Dataframe with ISO country codes for mapping
country_codes = pd.DataFrame({
    'Country': df['Winner'].unique().tolist() + df['Runner_Up'].unique().tolist(),
    'ISO': df['Winner_Country_Code'].unique().tolist() + df['Runner_Up_Country_Code'].unique().tolist()
}).drop_duplicates()

# App layout
app.layout = html.Div([
    html.H1("FIFA World Cup Dashboard", style={'textAlign': 'center'}),
    
    html.Div([
        html.Div([
            html.H3("Select View"),
            dcc.RadioItems(
                id='view-selector',
                options=[
                    {'label': 'All World Cup Winners', 'value': 'all_winners'},
                    {'label': 'Select Country', 'value': 'by_country'},
                    {'label': 'Select Year', 'value': 'by_year'}
                ],
                value='all_winners',
                labelStyle={'display': 'block'}
            ),
            
            html.Div(id='country-selector-container', children=[
                html.H4("Select Country"),
                dcc.Dropdown(
                    id='country-dropdown',
                    options=[{'label': country, 'value': country} for country in countries],
                    value=countries[0]
                )
            ], style={'display': 'none'}),
            
            html.Div(id='year-selector-container', children=[
                html.H4("Select Year"),
                dcc.Dropdown(
                    id='year-dropdown',
                    options=[{'label': year, 'value': year} for year in years],
                    value=years[0]
                )
            ], style={'display': 'none'})
        ], className="four columns"),
        
        html.Div([
            dcc.Graph(id='world-map'),
            html.Div(id='info-display')
        ], className="eight columns")
    ], className="row")
])

# Callback to update the visibility of selectors
@app.callback(
    [Output('country-selector-container', 'style'),
     Output('year-selector-container', 'style')],
    [Input('view-selector', 'value')]
)
def update_selectors_visibility(selected_view):
    if selected_view == 'by_country':
        return {'display': 'block'}, {'display': 'none'}
    elif selected_view == 'by_year':
        return {'display': 'none'}, {'display': 'block'}
    else:
        return {'display': 'none'}, {'display': 'none'}

# Callback to update the map and info display
@app.callback(
    [Output('world-map', 'figure'),
     Output('info-display', 'children')],
    [Input('view-selector', 'value'),
     Input('country-dropdown', 'value'),
     Input('year-dropdown', 'value')]
)
def update_map(selected_view, selected_country, selected_year):
    if selected_view == 'all_winners':
        # choropleth map showing all World Cup winners
        fig = px.choropleth(
            winners_count,
            locations=winners_count['Country'].map(lambda x: country_codes[country_codes['Country'] == x]['ISO'].values[0]),
            color='Wins',
            hover_name='Country',
            color_continuous_scale=px.colors.sequential.Blues,
            title='World Cup Winners',
            labels={'Wins': 'Number of World Cup Wins'},
            projection='natural earth'
        )
        
        info = html.Div([
            html.H4("World Cup Winners"),
            html.Table([
                html.Thead(
                    html.Tr([html.Th("Country"), html.Th("Number of Wins")])
                ),
                html.Tbody([
                    html.Tr([html.Td(row['Country']), html.Td(row['Wins'])])
                    for index, row in winners_count.iterrows()
                ])
            ])
        ])
        
    elif selected_view == 'by_country':
        # Choropleth map highlighting the selected country
        country_iso = country_codes[country_codes['Country'] == selected_country]['ISO'].values[0]
        # Count wins for the selected country
        wins = winners_count[winners_count['Country'] == selected_country]['Wins'].values
        wins = wins[0] if len(wins) > 0 else 0
        # Count runner-ups for the selected country
        runner_ups = runner_ups_count[runner_ups_count['Country'] == selected_country]['Runner_Ups'].values
        runner_ups = runner_ups[0] if len(runner_ups) > 0 else 0
        
        # Create a dataframe for the selected country
        selected_df = pd.DataFrame({
            'Country': [selected_country],
            'ISO': [country_iso],
            'Value': [1]  # Just to highlight the country
        })
        
        fig = px.choropleth(
            selected_df,
            locations='ISO',
            color='Value',
            hover_name='Country',
            color_continuous_scale=px.colors.sequential.Blues,
            title=f'{selected_country} World Cup Performance',
            projection='natural earth'
        )
        
        # Get years when the country won or was runner-up
        won_years = df[df['Winner'] == selected_country]['Year'].tolist()
        runner_up_years = df[df['Runner_Up'] == selected_country]['Year'].tolist()
        
        info = html.Div([
            html.H4(f"{selected_country} World Cup Performance"),
            html.P(f"World Cup Wins: {wins}"),
            html.P(f"World Cup Runner-ups: {runner_ups}"),
            html.H5("Years Won:"),
            html.Ul([html.Li(str(year)) for year in won_years]) if won_years else html.P("None"),
            html.H5("Years Runner-up:"),
            html.Ul([html.Li(str(year)) for year in runner_up_years]) if runner_up_years else html.P("None")
        ])
        
    elif selected_view == 'by_year':
        # Get the winner and runner-up for the selected year
        year_data = df[df['Year'] == selected_year]
        winner = year_data['Winner'].values[0]
        runner_up = year_data['Runner_Up'].values[0]
        winner_iso = year_data['Winner_Country_Code'].values[0]
        runner_up_iso = year_data['Runner_Up_Country_Code'].values[0]
        
        # Create a dataframe for the winner and runner-up
        year_df = pd.DataFrame({
            'Country': [winner, runner_up],
            'ISO': [winner_iso, runner_up_iso],
            'Result': ['Winner', 'Runner-up'],
            'Value': [2, 1]  # Winner gets a higher value for darker color
        })
        
        fig = px.choropleth(
            year_df,
            locations='ISO',
            color='Value',
            hover_name='Country',
            hover_data=['Result'],
            color_continuous_scale=px.colors.sequential.Blues,
            title=f'{selected_year} FIFA World Cup',
            projection='natural earth'
        )
        
        info = html.Div([
            html.H4(f"{selected_year} FIFA World Cup Final"),
            html.P(f"Winner: {winner}"),
            html.P(f"Runner-up: {runner_up}")
        ])
    
    # Update the layout of the figure
    fig.update_layout(
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        coloraxis_showscale=True,
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular'
        )
    )
    
    return fig, info

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
