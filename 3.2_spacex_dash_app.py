# spacex_dash_app.py

import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX dataset
spacex_df = pd.read_csv("/Users/romeromusadat/Library/CloudStorage/OneDrive-Personal/OneDrive/0.IBM Data Science Course/C10/3/spacex_launch_geo.csv")

# Extract unique launch sites
launch_sites = spacex_df['Launch Site'].unique().tolist()

# Determine the payload range
min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36',
                   'font-size': 40}),
    
    # Task 1: Launch Site Drop-down Input Component
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'}
        ] + [{'label': site, 'value': site} for site in launch_sites],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    
    html.Br(),
    
    # Task 2: Placeholder for the pie chart
    html.Div(dcc.Graph(id='success-pie-chart')),
    
    html.Br(),
    
    # Task 3: Payload Range Slider
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={i: f'{i}' for i in range(0, 10001, 1000)},
        value=[min_payload, max_payload]
    ),
    
    html.Br(),
    
    # Task 4: Placeholder for the scatter plot
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Task 2: Callback to Render Success-Pie-Chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(
            spacex_df,
            names='class',
            title='Total Launch Successes for All Sites',
            labels={'class': 'Launch Outcome'},
            color_discrete_map={'0': 'red', '1': 'green'},
            hover_data=['Launch Site']
        )
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Total Launch Outcomes for site {selected_site}',
            labels={'class': 'Launch Outcome'},
            color_discrete_map={'0': 'red', '1': 'green'},
            hover_data=['Payload Mass (kg)']
        )
    return fig

# Task 4: Callback to Render Success-Payload-Scatter-Chart
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]
)
def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range
    mask = (spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)
    filtered_df = spacex_df[mask]
    
    if selected_site == 'ALL':
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version',
            hover_data=['Launch Site'],
            title='Correlation between Payload and Launch Outcome for All Sites'
        )
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version',
            hover_data=['Launch Site'],
            title=f'Correlation between Payload and Launch Outcome for {selected_site}'
        )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
