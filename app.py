import dash
#import dash_core_components as dcc
from dash import dcc
from dash import html
#import dash_html_components as html
import dash_bootstrap_components as dbc
import json
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from dash.dependencies import Output, Input
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
server = app.server
#-----------------------------------------------------------------
#Import and clean data (import csv into pandas)
#open State Geojson file
#with open('states.json') as f:
#    jdata = json.load(f)
#print(jdata['features'][0].keys())
#dict_keys(['type', 'properties', 'geometry'])  #display the definition of a feature
df = pd.read_csv("https://drive.google.com/uc?export=download&id=1AEP2jQ4nB_4paWFLXqd2WWLSKujveP-A",
                    dtype={'fips': str})
#print(df.head())
df_combined = pd.read_csv("https://drive.google.com/uc?export=download&id=1fs6PHcGNLhB0jVDGMvKanQxevXQh6czC")
agg_5 = df_combined['title'].value_counts()[:5]
df_combined = df_combined.drop_duplicates()
class salary:
    def __init__(self, base, max, time):
        self.base = base
        self.max = max
        self.time = time
    def pay(self):
        return pay(self)
def pay(sal):
    if sal.base == False:
        sal.pay = sal.max * sal.time
    elif sal.max == True:
        sal.pay = sal.base * sal.time
    else:
        sal.pay = (sal.base + sal.max) / 2 * sal.time
    return sal.pay
def parse_salary(arr):
    arr = arr.replace('$', '')
    arr = arr.replace(',', '').lower()
    arr = arr.split()
    base_salary = False
    max_salary = False
    for i in arr:
        try:
            i = float(i)
            if max_salary:
                max_salary = i
            else:
                base_salary = i
                max_salary = True
        except:
            if i == 'up':
                max_salary = True
        if i == 'hour':
            rate = 2080
        elif i == 'month':
            rate = 12
        elif i == 'year':
            rate = 1
    return salary(base = base_salary, max = max_salary, time = rate)
def parse_pay(arr):
    new_sal = []
    for i in arr:
        try:
            new_sal.append(pay(parse_salary(i)))
        except:
            new_sal.append(float("NaN"))
    return new_sal
df_combined['salary'] = parse_pay(df_combined['salary'])
ind_df = df_combined.groupby(['industry'])
ind_sal = ind_df.mean()
ind = ind_df.count()
ind.rename(columns={'salary':'salary_ind'}, inplace=True)
ind['ratio'] = ind['salary_ind'] / ind['title']
ind = pd.concat([ind, ind_sal], axis = 1).reset_index()
nonnan = df_combined[df_combined['industry'] == df_combined['industry']]
size_df = df_combined.groupby(['title', 'remote']).size()
sal_df = df_combined.groupby(['title', 'remote']).mean()
gdf = pd.concat([size_df, sal_df], axis = 1).reset_index()
yes_sal = df_combined['salary'].count() / df_combined['title'].count()
no_sal = 1 - yes_sal
yn = pd.DataFrame([['yes', yes_sal], ['no', no_sal]])
yn.set_index(0)
#-------------------------------------------------------------------
#Links to Google Drive where the data are stored
# jobs_count_state.csv
# https://drive.google.com/uc?export=download&id=1AEP2jQ4nB_4paWFLXqd2WWLSKujveP-A
#combined_G_K_A_J.csv
# https://drive.google.com/uc?export=download&id=1fs6PHcGNLhB0jVDGMvKanQxevXQh6czC
#graham's word cloud link
#https://drive.google.com/uc?export=download&id=1dpnDnB6Bmv6ZagJRAbh1XmwHmrShpmSI
#-------------------------------------------------------------------
#Figures
fig_map = px.choropleth(df, locations='state', locationmode="USA-states", color='count',
                             scope="usa",
                             hover_data = ['state', 'count'],
                             color_continuous_scale = 'Emrld',
                             labels={'count':'Job Listings'}, title = 'Job Count Across the US')
fig_bar = px.bar(agg_5, title = "Top 5 Job Titles", color_discrete_sequence=["#007467"],
                labels=None)
fig_pie = px.pie(yn, values = 1, labels= 0)
fig_tree = px.treemap(ind, path = ['industry'], values = 'title', color = 'salary', color_continuous_scale='Emrld')
fig_tree2 = px.treemap(ind, path = ['industry'], values = 'title', color = 'ratio', color_continuous_scale='Burg')
fig_tree3 = px.treemap(nonnan, path = ['title','industry'], color_continuous_scale='Emrld')
fig_tree4 = px.treemap(gdf, path = ['title', 'remote'], values = 0, color='salary', color_continuous_scale='Emrld')
plt.tight_layout()
#----------------------------------------------------------------------
#Colors
colors = {
    'background': '#272b30',
    'text': '#e9ecef'
}
fig_map.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
fig_bar.update_layout(showlegend=False,
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
fig_pie.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
fig_tree.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
fig_tree2.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
fig_tree3.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
fig_tree4.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
#design for map
#bgcolor = "#f3f3f1"  # mapbox light map land color
#row_heights = [150, 500, 300]
#template = {"layout": {"paper_bgcolor": bgcolor, "plot_bgcolor": bgcolor}}
#-----------------------------------------------------------------------
#Figure design
fig_bar.update_yaxes(showline=True, linewidth=.5, linecolor="black", title_text="Count")
fig_bar.update_xaxes(showline=True, linewidth=.5, linecolor="black", title_text="")
#-----------------------------------------------------------------------
#App Layout
app.layout = html.Div([
    dbc.Row([
        dbc.Col(html.H1("Where to find your next Data Science Job!", style={'textAlign':'center'}), width=12)
    ]),
    dbc.Row(
        [
            dbc.Col(dcc.Graph(id='state-choropleth', figure=fig_map), width = '5'),
                        #config={'displayModeBar':False}), xs=8, sm=10, md=10, lg=10, xl=6),
            dbc.Col(dcc.Graph(id='job_count_5', figure=fig_bar), width = '3'),
                        #config={'displayModeBar':False}), xs=6, sm=6, md=6, lg=4, xl=4),
            dbc.Col(dcc.Graph(id='pie_chart', figure = fig_pie), width = '3'),
                        #config={'displayModeBar':False}), xs=6, sm=6, md=6, lg=4, xl=4),
        ],
        align='start',
    ),
    dbc.Row(
        [
            dcc.Graph(id = 'salary-treemap', figure = fig_tree,
                config={'displayModeBar':False}),
        ],
        align="end",
    ),
    dbc.Row(
        [
            dcc.Graph(id = 'salary-treemap2', figure = fig_tree2,
                config={'displayModeBar':False}),
        ],
        align="end",
    ),
    dbc.Row(
        [
            dcc.Graph(id = 'salary-treemap3', figure = fig_tree3,
                config={'displayModeBar':False}),
        ],
        align="end",
    ),
    dbc.Row(
        [
            dcc.Graph(id = 'salary-treemap4', figure = fig_tree4,
                config={'displayModeBar':False}),
        ],
        align="end",
    ),
    dbc.Row([
            dbc.Col(html.H4("Hypothesis: We expect to see words related to data in the most frequently used words for the job title 'Data Scientist' Result: As expected, all five of the most frequently used words for 'Data Scientist' contain the word data.", style={'textAlign':'lef$    ]),
    html.A([
            html.Img(
                src='https://drive.google.com/uc?export=download&id=1dpnDnB6Bmv6ZagJRAbh1XmwHmrShpmSI',
                style={
                    'height' : '75%',
                    'width' : '75%',
                    'float' : 'center',
                    'position' : 'relative',
                    'padding-top' : 5,
                    'padding-right' : 0
                })
    ], href='https://colab.research.google.com/drive/1NNcPUkv8SvBjdaHN_9kMSVwHAPN1O6Fc#scrollTo=uwe-LV_MIn54')
])
#------------------------------------------------------------------------
#Callback
#-----------------------------------------------------------------------
if __name__ == '__main__':
        app.run_server(debug=False, host='0.0.0.0', port = 8050)
