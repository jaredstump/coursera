import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

spacex_df = pd.read_csv("spacex_launch_dash.csv")
#i didnt use these variables instead i defined them explicitly
#max_payload = spacex_df['Payload Mass (kg)'].max()
#min_payload = spacex_df['Payload Mass (kg)'].min()
min_value = 0
max_value = 10000

app = dash.Dash(__name__)
dropdown_options = [
    {'label': 'ALL Sites', 'value': 'ALL'},
    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}]


app.layout = html.Div(
    children=[
        html.H1(
            'SpaceX Launch Records Dashboard', 
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}), 
        dcc.Dropdown(
            id='site-dropdown',
            options = dropdown_options,
            value='ALL',
            placeholder='Select a Launch Site here',
            searchable=True),    
        html.Br(),

        html.Div(
            dcc.Graph(
                id='success-pie-chart')),
        html.Br(),
        html.P('Payload Range (kg):'),
        dcc.RangeSlider(
            id='payload-slider',
            min=0, max=10000, step=1000,
            marks={0:'0',100:'100'},
            value=[min_value, max_value]),
        html.Div(
            dcc.Graph(
                id='success-payload-scatter-chart'))])
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
    if entered_site == 'ALL':
        fig = px.pie(
            spacex_df.groupby('Launch Site')['class'].sum().reset_index(), 
            values='class', names='Launch Site', title='Total Success Launches by Site')
        return fig
    else:
        fig = px.pie(
            filtered_df, 
            values=filtered_df.groupby('class')['class'].count(),
            names=['Failure', 'Success'],
            title=f"Successful Launch Rate at Site: {entered_site}")
        return fig
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site, entered_range):
    slider_min, slider_max = entered_range
    if entered_site == 'ALL':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= slider_min) &
                                (spacex_df['Payload Mass (kg)'] <= slider_max)]
    else:
        filtered_df = spacex_df[(spacex_df['Launch Site'] == entered_site) &
                                (spacex_df['Payload Mass (kg)'] >= slider_min) &
                                (spacex_df['Payload Mass (kg)'] <= slider_max)]
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version')
    return fig
    
if __name__ == '__main__':
    app.run_server()
