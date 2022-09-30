import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input, State
from datetime import date
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from google.oauth2 import service_account  # pip install google-auth
import pandas_gbq  # pip install pandas-gbq

import pandas as pd
import numpy as np

import plotly.io as pio
pio.templates.default = "plotly_dark"


credentials = service_account.Credentials.from_service_account_file('C:/Users/Checkout/Documents/GitHub/Dash-by-Plotly/Dash_More_Advanced_Shit/BigQuery/assets\emerald-cacao-363700-f7930738c1a0.json')
project_id = 'emerald-cacao-363700'  

query1 = """SELECT
    *
    FROM
        `bigquery-public-data.covid19_nyt.us_states`
    ORDER BY
        date
"""

df_covid = pd.read_gbq(query1,project_id=project_id,dialect='standard',credentials=credentials)

is_california = df_covid['state_name']=='California'
df_ca = df_covid[is_california]


sql_covid19_jhu = """
SELECT
  *
FROM
  `bigquery-public-data.covid19_jhu_csse.summary` 
WHERE
  country_region = "US"
AND 
  confirmed > 10
LIMIT 300
"""

df_covid19 = pd.read_gbq(sql_covid19_jhu,project_id=project_id,dialect='standard',credentials=credentials)





df_covid19['date'] = pd.to_datetime(df_covid19['date'])


df_covid19['latitude'] = df_covid19['latitude'].replace(np.nan,'nan')
df_covid19['longitude'] = df_covid19['longitude'].replace(np.nan,'nan')
df_covid19['deaths'] = df_covid19['deaths'].replace(np.nan,'nan')

df_covid19['deaths'] = df_covid19['deaths'].replace(np.nan,0)
df_covid19['deaths'] = df_covid19['deaths'].replace('nan',0)
df_covid19['deaths'] = df_covid19['deaths'].replace('NaN',0)

df_covid19 = df_covid19.sort_values(by=['date', 'province_state'])

# print(df_covid19.info())
# df_covid19.tail(100)

# first_day = min(df_covid19['date'])
# last_day = max(df_covid19['date'])
# print('First day {}, Last day {}, Number of days {}'.format(first_day, last_day, (last_day - first_day).days + 1))

# ddd=df_covid19.groupby('date')[['confirmed','deaths']]
# ddd.sum()

# info_us = pd.DataFrame(ddd.sum()).reset_index().sort_values(by='date')
# info_us.tail(10)

df_country = df_covid19[df_covid19['date'] == max(df_covid19['date'])].copy()

print("----------")
print(df_country['confirmed'])
def usa_map_plot():

    fig = px.scatter_geo(df_country,
                        lat='latitude', lon='longitude', color="country_region",
                        hover_name="country_region",
                        projection="natural earth")

    fig.update_geos(scope="north america",
        showcountries=True, countrycolor="Black",
        showsubunits=True, subunitcolor="Blue"
    )
    fig.update_layout(title='US Confirmed Cases - {}'.format(max(df_covid19['date'])), title_x=0.5)
    return fig


# print(df_ca.head())
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

def cases_confirmed_ca_line():
    # Function for creating line chart showing Google stock prices over time 
    fig = go.Figure([go.Scatter(x = df_ca['date'], y = df_ca['confirmed_cases'],name='Covid_Cases')])
    fig.update_layout(title = '#Cases over time Line Plot',
                      xaxis_title = 'Dates',
                      yaxis_title = 'Cases'
                      )
    return fig

def cases_confirmed_ca_bar():
    # Function for creating line chart showing Google stock prices over time 
    fig = go.Figure([go.Bar(x = df_ca['date'], y = df_ca['confirmed_cases'],name = 'Covid_Cases')])
    fig.update_layout(title = '#Cases over time Bar Plot',
                      xaxis_title = 'Dates',
                      yaxis_title = 'Cases'
                      )
    return fig        



app.layout = html.Div(id = 'parent', children = [
    html.H1(children="CMPE 255 Assignment 1",style = {'color':'Blue'}),
    html.H2(children = "Name: Farazuddin Mohammad (farazuddin.mohammad@sjsu.edu)",style = {'color':'Blue'}),
    html.H2(children = "Student Id: 016176836",style = {'color':'Blue'}),
    html.H1(id = 'H1', children = 'COVID-19 Info Dash Board', style = {'textAlign':'center',\
                                            'marginTop':40,'marginBottom':40}),
                                            
        dcc.Graph(id = 'line_plot', figure = cases_confirmed_ca_line()),
        dcc.Graph(id = 'bar_plot',figure = cases_confirmed_ca_bar()),
        dcc.Graph(id = 'map_plot',figure = usa_map_plot())    
    ],style={'font-family':'Arial'}
                     )


if __name__=='__main__':
    app.run_server(debug=False)



# Must Use: Python, Numpy, Pandas, Matplotlib, Seaborn, Google Cloud BigQuery, or Colab.
# Upload your Document and Google Colab link to the Canvas
# figures added to your document should be in vector-format in pdf.
# Since google doc doesn't support pdf then lets do it in latex
# Option2: Choose your own dataset from bigquery
# Re-use and modify sample code for data exploration ** NEEDS TO BE DONE **
# => YOU NEED TO HAVE A NEW SECTION IN YOU DOC AND CODE TO SPECIFY AREA OF CHANGES
# => INCLUDE DETAILED INFORMATION OF CODE SECTIONS AND LINES
# If using external dataset upload it to bigquery and reference it
# Set up Colab Notebook and access data from Bigquery for processing-visualization
# # ** AND SAVE THE RESULT DATA BACK TO BIGQUERY **
# Use the follwoing : Python, Numpy, Pandas, Matplotlib, Seaborn
# ** Build one simple web/mobile data dashboard and visualize the result data from Google BigQuery **
# You need to have atleast 3 plots: bar-graph, line graph, map(geolocation), and any statistical graph eg: Histogram
# For Document:
# # 1. Goal
# # 2. Visualization Figures
# # 3. Reference Link
# # 4. Write Down what you have observed from your visualization document 
