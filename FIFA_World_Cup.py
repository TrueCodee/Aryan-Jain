# FIFA World Cup Dashboard
# Deployed at: [Insert Render.com URL here]
# Password: Not required 

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# Load the data
df = pd.read_csv('data.csv')

# Standardize Germany - ensure West Germany and Germany are treated as the same country
df['Winner'] = df['Winner'].replace('West Germany', 'Germany')
df['Runner_Up'] = df['Runner_Up'].replace('West Germany', 'Germany')

# Count the number of wins per country
wins_per_country = df['Winner'].value_counts().reset_index()
wins_per_country.columns = ['Country', 'Wins']

# Count the number of runner-ups per country
runner_ups_per_country = df['Runner_Up'].value_counts().reset_index()
runner_ups_per_country.columns = ['Country', 'Runner_Ups']

# Creating a dashboard
app = Dash(__name__)
server = app.server  # Needed for Render deployment

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1('FIFA World Cup Dashboard (1930-2022)', style={'textAlign': 'center'}),
    
    html.Div([
        html.Div([
            html.H3('Select View Option:'),
            dcc.RadioItems(
                id='view-option',
                options=[
                    {'label': 'All World Cup Winners', 'value': 'all_winners'},
                    {'label': 'Wins by Country', 'value': 'by_country'},
                    {'label': 'Winners by Year', 'value': 'by_year'}
                ],
                value='all_winners',
                style={'marginBottom': '20px'}
            ),
            
            html.Div(id='dynamic-controls', style={'marginBottom': '20px'})
        ], style={'width': '25%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'}),
        
        html.Div([
            dcc.Graph(id='choropleth-map')
        ], style={'width': '70%', 'display': 'inline-block', 'verticalAlign': 'top'}),
    ]),
    
    html.Div(id='details-display', style={'margin': '20px', 'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '5px'})
])

# Callback to update dynamic controls based on view option
@app.callback(
    Output('dynamic-controls', 'children'),
    Input('view-option', 'value')
)
def update_controls(view_option):
    if view_option == 'all_winners':
        return []
    
    elif view_option == 'by_country':
        # Create a dropdown for countries that have won the World Cup
        unique_winners = sorted(df['Winner'].unique())
        return [
            html.H4('Select a Country:'),
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': country, 'value': country} for country in unique_winners],
                value=unique_winners[0]
            )
        ]
    
    elif view_option == 'by_year':
        # Create a dropdown for years when World Cups were held
        years = sorted(df['Year'].unique())
        return [
            html.H4('Select a Year:'),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': str(year), 'value': year} for year in years],
                value=years[-1]  # Default to most recent World Cup
            )
        ]

# Callback to update the choropleth map
@app.callback(
    Output('choropleth-map', 'figure'),
    Output('details-display', 'children'),
    Input('view-option', 'value'),
    Input('country-dropdown', 'value', allow_missing=True),
    Input('year-dropdown', 'value', allow_missing=True)
)
def update_map(view_option, selected_country, selected_year):
    details_display = []
    
    if view_option == 'all_winners':
        # Prepare data for the choropleth map - all countries that won
        win_counts = df['Winner_Country_Code'].value_counts().reset_index()
        win_counts.columns = ['iso_alpha3', 'Wins']
        
        # Create the choropleth map
        fig = px.choropleth(
            win_counts, 
            locations='iso_alpha3',
            color='Wins',
            color_continuous_scale='Viridis',
            range_color=[0, win_counts['Wins'].max()],
            title='Number of World Cup Wins by Country (1930-2022)'
        )
        
        # Add detailed information about all winners
        details_display = [
            html.H3('World Cup Winners (1930-2022)'),
            html.Table([
                html.Thead(html.Tr([html.Th('Country'), html.Th('Number of Wins')])),
                html.Tbody([
                    html.Tr([html.Td(country), html.Td(wins)]) 
                    for country, wins in zip(wins_per_country['Country'], wins_per_country['Wins'])
                ])
            ], style={'width': '100%', 'textAlign': 'left', 'borderCollapse': 'collapse'})
        ]
        
    elif view_option == 'by_country' and selected_country:
        # Filter data for the selected country
        country_wins = df[df['Winner'] == selected_country]
        country_code = country_wins['Winner_Country_Code'].iloc[0] if not country_wins.empty else None
        
        # Count total wins for the selected country
        win_count = len(country_wins)
        
        # Prepare data for the choropleth map - highlighting the selected country
        country_data = pd.DataFrame({
            'iso_alpha3': [country_code],
            'Wins': [win_count]
        })
        
        # Create the choropleth map
        fig = px.choropleth(
            country_data, 
            locations='iso_alpha3',
            color='Wins',
            color_continuous_scale='Viridis',
            range_color=[0, wins_per_country['Wins'].max()],
            title=f'World Cup Wins: {selected_country} ({win_count} wins)'
        )
        
        # Add detailed information about wins
        details_display = [
            html.H3(f'World Cup Wins for {selected_country}'),
            html.Table([
                html.Thead(html.Tr([html.Th('Year'), html.Th('Runner-Up')])),
                html.Tbody([
                    html.Tr([html.Td(year), html.Td(runner_up)]) 
                    for year, runner_up in zip(country_wins['Year'], country_wins['Runner_Up'])
                ])
            ], style={'width': '100%', 'textAlign': 'left', 'borderCollapse': 'collapse'})
        ]
        
    elif view_option == 'by_year' and selected_year:
        # Filter data for the selected year
        year_data = df[df['Year'] == selected_year]
        
        if not year_data.empty:
            winner = year_data['Winner'].iloc[0]
            runner_up = year_data['Runner_Up'].iloc[0]
            winner_code = year_data['Winner_Country_Code'].iloc[0]
            runner_up_code = year_data['Runner_Up_Country_Code'].iloc[0]
            
            # Prepare data for the choropleth map - highlighting winner and runner-up
            world_cup_data = pd.DataFrame({
                'iso_alpha3': [winner_code, runner_up_code],
                'Country': [winner, runner_up],
                'Result': ['Winner', 'Runner-Up'],
                'Value': [2, 1]  # 2 for winner, 1 for runner-up for color differentiation
            })
            
            # Create the choropleth map
            fig = px.choropleth(
                world_cup_data, 
                locations='iso_alpha3',
                color='Result',
                color_discrete_map={'Winner': 'gold', 'Runner-Up': 'silver'},
                title=f'World Cup {selected_year}: {winner} (Winner) vs {runner_up} (Runner-Up)'
            )
            
            # Add detailed information about the selected year
            details_display = [
                html.H3(f'World Cup {selected_year}'),
                html.Table([
                    html.Tr([html.Th('Winner'), html.Td(winner)]),
                    html.Tr([html.Th('Runner-Up'), html.Td(runner_up)])
                ], style={'width': '100%', 'textAlign': 'left', 'borderCollapse': 'collapse'})
            ]
        else:
            fig = go.Figure()
            details_display = [html.P(f"No data available for {selected_year}")]
    
    else:
        fig = go.Figure()
        details_display = [html.P("Please select a view option")]
    
    # Improve map appearance
    fig.update_geos(
        showcoastlines=True,
        coastlinecolor="RebeccaPurple",
        showland=True,
        landcolor="LightGreen",
        showocean=True,
        oceancolor="LightBlue",
        showlakes=True,
        lakecolor="Blue",
        showrivers=True,
        rivercolor="Blue"
    )
    
    fig.update_layout(
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        height=600
    )
    
    return fig, details_display

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)