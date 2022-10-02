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



credentials = service_account.Credentials.from_service_account_file('emerald-cacao-363700-f7930738c1a0.json')
project_id = 'emerald-cacao-363700'  



app = dash.Dash(__name__)

query_raw = """
    SELECT
        *
    FROM
        `bigquery-public-data.iowa_liquor_sales.sales`
    LIMIT 10000
"""


df = pd.read_gbq(query=query_raw,dialect='standard',credentials=credentials,project_id=project_id)
df['Date'] = pd.to_datetime(df['date'])
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day

def sales_per_liq_cat():
  df_plot = df.fillna('NA').groupby(['category_name','pack','date'])['sale_dollars'].sum().groupby(
              ['category_name','pack']).max().sort_values().groupby(
              ['category_name']).sum().sort_values(ascending=False)
  top_count = pd.DataFrame(df_plot)
  top_count1 = pd.DataFrame(df_plot.head(10))  
  fig_reg = px.bar(top_count1,x=top_count1.index, y='sale_dollars',color='sale_dollars')
  df_plot = df.fillna('NA').groupby(['category_name','pack','date'])['sale_dollars'].sum().groupby(
              ['category_name','pack']).max().sort_values().groupby(
              ['category_name']).sum().sort_values(ascending=False)
  top_count = pd.DataFrame(df_plot)
  top_count1 = pd.DataFrame(df_plot.head(10))
  return fig_reg

def sales_per_city():
  df_plot = df.fillna('NA').groupby(['city','pack','date'])['sale_dollars'].sum().groupby(
              ['city','pack']).max().sort_values().groupby(
              ['city']).sum().sort_values(ascending=False)
  top_count1 = pd.DataFrame(df_plot)
  top_count1 = pd.DataFrame(df_plot.head(20))

  fig_reg = px.bar(top_count1,x=top_count1.index, y='sale_dollars',color='sale_dollars')
  fig_reg.update_layout(
      title="Sales of liquor per city",
      xaxis_title=" City Name",
      yaxis_title="Sales in dollars",
      )
  return fig_reg

def sales_per_month():
  df_plot = df.fillna('NA').groupby(['Month','pack','Date'])['sale_dollars'].sum().groupby(
              ['Month','pack']).max().sort_values().groupby(
              ['Month']).sum().sort_values(ascending=False)
  top_count1 = pd.DataFrame(df_plot)
  top_count1 = pd.DataFrame(df_plot.head(50))

  fig_reg = px.bar(top_count1,x=top_count1.index, y='sale_dollars',color='sale_dollars')
  fig_reg.update_layout(
      title="Sales of liquor per Month",
      xaxis_title=" Month Number",
      yaxis_title="Sales in dollars",
      )
  return fig_reg


def scatter_plot():
  df_scatter = df[["item_description","sale_dollars","volume_sold_liters",]].groupby(by="item_description",as_index=False).sum()
  df_scatter = df_scatter[df_scatter["sale_dollars"] <= 80000]
  fig = px.scatter(df_scatter,x="sale_dollars", y="volume_sold_liters" ,color='item_description',trendline="ols",trendline_scope="overall",trendline_color_override="black")
  fig.show()
  return fig

def histogram_plot():
  fig = px.histogram(df, x="pack", nbins=15)
  return fig

def line_plot():
  grouped_on_sales_df = df[["city","sale_dollars","Month"]].groupby(by = ['city',"Month"],as_index = False).sum()

  grouped_on_sales_df = grouped_on_sales_df.sort_values(by = "sale_dollars", axis=0, ascending=False)

  grouped_on_sales_df = grouped_on_sales_df.sort_values(by = "Month", axis=0, ascending=False)

  cities = grouped_on_sales_df[["city","sale_dollars"]].groupby(by ='city',as_index = False).sum()
  cities = cities.sort_values(by="sale_dollars",ascending=False).head(10)

  new_df=pd.DataFrame()
  for c in cities['city']:
      print(c)
      temp_df = grouped_on_sales_df[grouped_on_sales_df["city"] == c ]
      new_df = new_df.append(temp_df, ignore_index=True)
  
  new_df = new_df.sort_values(by = ["Month","city"], axis=0, ascending=False)
  fig = px.line(new_df, x="Month", y="sale_dollars" 
              , color="city")
  return fig

def corr_plot():
    df_int = df[['pack','bottle_volume_ml','state_bottle_cost','state_bottle_retail','bottles_sold','sale_dollars','volume_sold_liters','volume_sold_gallons']]
    fig = go.Figure(data=go.Heatmap(z = df_int.corr(),x=['pack','bottle_volume_ml','state_bottle_cost','state_bottle_retail','bottles_sold','sale_dollars','volume_sold_liters','volume_sold_gallons'],y=['pack','bottle_volume_ml','state_bottle_cost','state_bottle_retail','bottles_sold','sale_dollars','volume_sold_liters','volume_sold_gallons']))
    return fig

plt_1 = line_plot()
plt_1.write_image('Plots/Line_Plot_Cities.pdf',scale = 1,height=600,width=1200)

plt_2 = sales_per_city()
plt_2.write_image('Plots/Bar_Plot_Cities.pdf',scale=1,height=600,width=1200)

plt_3 = sales_per_liq_cat()
plt_3.write_image('Plots/Bar_Plot_Cat.pdf',scale=1,height=600,width=1200)

plt_4 = scatter_plot()
plt_4.write_image('Plots/Scatter_Sales_Vol.pdf',scale=1,height=600,width=1200)

plt_5 = sales_per_month()
plt_5.write_image('Plots/Bar_Sales_Monthly.pdf',scale=1,height=600,width=1200)

app.layout = html.Div(id = 'parent', children = [
    html.H1(children="CMPE 255 Assignment 1",style = {'color':'Blue'}),
    html.H2(children = "Name: Farazuddin Mohammad (farazuddin.mohammad@sjsu.edu)",style = {'color':'Blue'}),
    html.H2(children = "Student Id: 016176836",style = {'color':'Blue'}),
    html.H1(id = 'H1', children = 'Iowa Liquor Sales Data Mining Dashboard', style = {'textAlign':'center',\
                                            'marginTop':40,'marginBottom':40}),
    html.H2(children = "Bar Plot for Sales of Liquor per Category"),
        dcc.Graph(id = 'bar_plot1', figure = sales_per_liq_cat()),
    html.H2(children = "Bar Plot for Sales of Liquor per City"),
        dcc.Graph(id = 'bar_plot2', figure = sales_per_city()),
    html.H2(children = "Line Plot for Sales of Liquor per City"),
        dcc.Graph(id = 'line_plot',figure = line_plot()),
    html.H2(children = "Bar Plot Liquor Sales per month"),
        dcc.Graph(id = 'bar_plot3', figure=sales_per_month()),
    html.H2(children = "Scatter Plot Sales(USD) Vs Volume(Liters)"),
        dcc.Graph(id = 'scatter_plot1',figure = scatter_plot()),
    html.H2(children = "Histogram Plot for Pack Size Sold"),
        dcc.Graph(id = 'histogram_plot',figure = histogram_plot()),
    html.H2(children = "Correlation Matrix Heatmap"),
        dcc.Graph(id = 'heat_map',figure = corr_plot())
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
