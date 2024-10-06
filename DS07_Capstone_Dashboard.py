# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

sitenames = spacex_df.groupby(["Launch Site"])["class"].mean().index.tolist()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Div(dcc.Dropdown(id='site-dropdown',options=[{'label': 'All Sites', 'value': 'ALL'},{'label': sitenames[0], 'value': sitenames[0]},{'label': sitenames[1], 'value': sitenames[1]},{'label': sitenames[2], 'value': sitenames[2]},{'label': sitenames[3], 'value': sitenames[3]}],
                                value='ALL',
                                placeholder="Select a Launch Site here",
                                searchable=True,
                                clearable=False)),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Div(dcc.RangeSlider(id='payload-slider',
                                min=0, max=10000, step=500,
                                marks={0: '0', 1000: '1000', 2000: '2000', 3000: '3000', 4000: '4000', 5000: '5000', 6000: '6000', 7000: '7000', 8000: '8000', 9000: '9000', 10000: '10000'},
                                value=[min_payload, max_payload])),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        df = spacex_df.groupby(['Launch Site']).sum()['class']
        fig = px.pie(df, values='class', 
        names=df.index.tolist(), 
        title='Total Success Launches by Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        dfp = spacex_df[spacex_df['Launch Site'] == entered_site]
        df = dfp.groupby(['class']).count()['Flight Number']
        fig = px.pie(df, values='Flight Number', 
        names=['Failure', 'Success'], 
        title='Total Success Launches for Site '+entered_site)
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
               Input(component_id="payload-slider", component_property="value")]
              )

def get_scatter_chart(entered_site,entered_payload):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        low, high = entered_payload
        mask = (spacex_df["Payload Mass (kg)"] > low) & (spacex_df["Payload Mass (kg)"] < high)
        df = spacex_df[mask]
        fig = px.scatter(df, x="Payload Mass (kg)", y="class", color="Booster Version Category", title='Correlation between Payload and Success for ALL Sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        low, high = entered_payload
        mask = (spacex_df["Payload Mass (kg)"] > low) & (spacex_df["Payload Mass (kg)"] < high) & (spacex_df["Launch Site"] == entered_site)
        df = spacex_df[mask]
        fig = px.scatter(df, x="Payload Mass (kg)", y="class", color="Booster Version Category", title='Correlation between Payload and Success at Site '+entered_site)
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
