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

# Create a dash application
app = dash.Dash(__name__)
dropdown_options=[{'label': 'All Sites', 'value': 'ALL'}
        ,{'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'}
        ,{'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ,{'label': 'KSC LC-39A', 'value': 'KSC LC-39A'}
        ,{'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}]

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                  dcc.Dropdown(id='site-dropdown',
                                               options=dropdown_options,
                                               value='ALL',
                                               placeholder="place holder here",
                                               searchable=True
                                               ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                  dcc.RangeSlider(id='payload-slider',
                                                 min=0, 
                                                 max=10000, 
                                                 step=1000,
                                                 marks={0: '0', 1000: '1000', 2000: '2000', 3000:'3000', 4000:'4000', 5000: '5000', 6000:'6000',7000:'7000',8000:'8000', 9000:'9000',10000:'10000'},
                                                 value=[min_payload, max_payload]
                                               ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df[spacex_df['class']==1]
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total success launches by site')
        return fig
        print(filtered_df.head())
    else:
        filtered_df2 = spacex_df[spacex_df['Launch Site']==entered_site].groupby('class')['class'].count()
        fig2 = px.pie(filtered_df2, values = 'class',names ='class', color='class', title = 'Total success launches for site ' + entered_site)
        return fig2
        print(filtered_df.head())
        # return the outcomes piechart for a selected site
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
               Input(component_id='payload-slider', component_property='value')])

def get_line_chart(entered_site, payload_range):
    #print(spacex_df.dtypes,payload_range[1].dtypes)
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload_range[0],payload_range[1])]
    if entered_site == 'ALL':
       #filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload_range[0],payload_range[1])]
        scatter = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
        title='Correlation between payload and success for all sites')
        return scatter
        #print(filtered_df.head())
    else:
        data = filtered_df[filtered_df['Launch Site']==entered_site]
        scatter2 = px.scatter(data, x = 'Payload Mass (kg)',y='class', color='Booster Version Category',title ='Correlation between payload and success for site' + entered_site)
        return scatter2
       # print(filtered_df.head())

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

