# importing libraries 
import plotly.graph_objects as go       # plytly graph objects
from plotly.subplots import make_subplots       # plotly.subplots make subplots
import pandas as pd             # pandas
import numpy as np          # numpy
import dash         # Dash
import dash_core_components as dcc      # dash core components dcc 
import dash_html_components as html      # dash core component html
import requests         # requests
from datetime import datetime , timedelta
from dash.dependencies import Output , Input

ts_cases_path = "Data/time_series_cases (1).csv"
ts_deaths_path = "Data/time_series_deaths.csv"
ts_recovery_path = "Data/time_series_recovery.csv"

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]
# initialialize app ###############################################################
app3 = dash.Dash(__name__, external_stylesheets = external_stylesheets)
server = app3.server

app3.layout = html.Div([
        # html.Div(id = 'store-data' , style= {'display':'none'}),
        # dcc.Interval(id='update-data' , interval=1*1000 , n_intervals=0),
        # html.Div(id = 'store-data-total' , style= {'display':'none'}),
        # dcc.Interval(id='update-data-total' , interval=1*1000 , n_intervals=0),
        html.Div([
            html.H1(
                children = "COVID 19 LIVE TRACKING",
                style = {
                    'color': '#d486f0',
                    'backgroundColor': "#18191c",
                }
            )
        ], className = 'row'),
        html.Div([
            html.Div([
                dcc.Graph(id = 'fig_1' ,),
                dcc.Interval(id = 'fig_1_update' ,interval=360*1000 , n_intervals = 0)
            ], className = 'six columns'),
            html.Div([
                dcc.Graph(id = 'fig_2' ),
                dcc.Interval(id = 'fig_2_update', interval= 360*1000, n_intervals = 0)
            ], className = 'six columns')
        ], className = 'row'),
        html.Div([
            html.Div([
                dcc.Graph(id = 'fig_3'),
                dcc.Interval(id='fig_3_update' , interval = 360*1000 , n_intervals = 0)
            ], className = 'four columns'),
            html.Div([
                dcc.Graph(id = 'fig_4'),
                dcc.Interval(id = 'fig_4_update' , interval = 360*1000 , n_intervals = 0)
            ] , className = 'four columns'),
            html.Div([
                dcc.Graph(id = 'fig_5'),
                dcc.Interval(id = 'fig_5_update' , interval = 360*1000 , n_intervals = 0)
            ], className = 'four columns')
        ], className = 'row'),
        html.Div([
            html.Div([
                dcc.Graph(id = 'fig_6'),
                dcc.Interval(id= 'fig_6_update' , interval = 360*1000 , n_intervals= 0)
            ], className ='four columns'),
            html.Div([
                dcc.Graph(id = 'fig_7'),
                dcc.Interval(id = 'fig_7_update' , interval = 360*1000 , n_intervals=0)
            ], className = 'four columns'),
            html.Div([
                dcc.Graph(id = 'fig_8' ),
                dcc.Interval(id = 'fig_8_update' , interval = 360*1000 , n_intervals= 0)
            ], className = 'four columns')
        ], className = 'row'),
        html.Div([
            html.Div([
                html.H4(children = 'CURRENT STATS TOP 20 COUNTRIES' , style = {'color':'#d486f0' , 'backgroundColor':"#18191c"}),
                html.Div(id = 'table_data'),
                dcc.Interval(id='update_table' , interval= 480*1000 , n_intervals=0)
            ], className = 'container')
        ] , className = 'row'),
        html.Div([
            html.Div([
                'sources', html.Br(),
                html.A("Covid 19 Data by ESRI" , href = 'https://coronavirus-resources.esri.com/datasets/bbb2e4f589ba40d692fab712ae37b9ac_1/geoservice?geometry=131.565%2C-38.069%2C-114.177%2C63.033&orderBy=Country_Region&selectedAttribute=Confirmed&where=Last_Update%20%3E%3D%20TIMESTAMP%20%272020-02-23%2000%3A00%3A00%27%20AND%20Last_Update%20%3C%3D%20TIMESTAMP%20%272020-04-25%2023%3A59%3A59%27'), html.Br(),
                html.A('JHU CSS' , href = 'https://github.com/CSSEGISandData/COVID-19') ,html.Br() , html.Br(),
                'Created by ',
                html.A('@imzain448' , href = 'https://www.linkedin.com/in/zain-ahmad-15aa25162?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BAMhpXFhyRf2AuntShjhTIw%3D%3D')
            ] , className = 'container', style= {'color':'white'} , id = 'footer')
        ], className = 'row')
    ], style = {
    'backgroundColor' : "#18191c"
} , className = 'container-fluid')

###############################################################################################
#################################### updating and generating the figures ######################
###############################################################################################
@app3.callback([Output('fig_1' , 'figure'),
                Output('fig_2' , 'figure'),
                Output('fig_3', 'figure'),
                Output('fig_4' , 'figure'),
                Output('fig_5' , 'figure'),
                Output('fig_6' , 'figure'),
                Output('fig_7' , 'figure'),
                Output('fig_8' , 'figure'),
                Output('table_data' , 'children')],
                [Input('fig_1_update' , 'n_intervals')])
def update_data(n):
    data_raw = requests.get('https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/Coronavirus_2019_nCoV_Cases/FeatureServer/1/query?where=1%3D1&outFields=*&outSR=4326&f=json')
    data_raw_json = data_raw.json()
    data = pd.DataFrame(data_raw_json['features'])
    data_list = data['attributes'].tolist()

    data_final = pd.DataFrame(data_list)
    data_final.set_index('OBJECTID')
    data_final = data_final[['Country_Region' ,'Province_State' , 'Lat' , 'Long_', 'Confirmed' , 'Recovered' , 'Deaths','Last_Update' ]]

    def convertTime(t):
        t = int(t)
        return datetime.fromtimestamp(t)

    data_final = data_final.dropna(subset=['Last_Update'])
    data_final['Province_State'].fillna(value="" , inplace=True)

    data_final['Last_Update'] = data_final['Last_Update']/1000

    # data final
    data_final['Last_Update'] = data_final['Last_Update'].apply(convertTime)

    data_total = data_final.groupby('Country_Region' , as_index=False).agg(
        {
            'Confirmed':'sum',
            'Recovered' : 'sum',
            'Deaths' : 'sum'
        }
    )
    ts_cases = pd.read_csv(ts_cases_path, parse_dates=['Date'])
    ts_cases = ts_cases[['Date' , 'Cases']]
    ts_deaths = pd.read_csv(ts_deaths_path , parse_dates = ['Date'])
    ts_deaths = ts_deaths[['Date' , 'Deaths']]
    ts_recovery = pd.read_csv(ts_recovery_path , parse_dates = ['Date'])
    ts_recovery = ts_recovery[['Date' , 'Recovery']]
    total_confirmed = data_total['Confirmed'].sum()
    total_recovered = data_total['Recovered'].sum()
    total_deaths = data_total['Deaths'].sum()
    # current numbers
    current_date = data_final['Last_Update'].dt.date.max()
    c_cases = total_confirmed
    c_deaths = total_deaths
    c_recovery = total_recovered

    # function to update the csv files with current number
    def update_time_series(file , label, current_value , csvfile , current_date):
        last_date = csvfile['Date'].dt.date.max()
        if ( last_date == current_date):
            if (int(csvfile[csvfile.Date.dt.date == last_date][label].values) != current_value):
                csvfile.loc[csvfile['Date'] == last_date , label] = current_value
        else:
            csvfile = csvfile.append({'Date':current_date , label:current_value} , ignore_index=True)
        csvfile.to_csv(file)

    # updating the csv file
    update_time_series(ts_cases_path , label='Cases' , current_value=c_cases , csvfile=ts_cases , current_date=current_date)
    update_time_series(ts_deaths_path , label="Deaths" , current_value=c_deaths , csvfile=ts_deaths , current_date=current_date)
    update_time_series(ts_recovery_path , label='Recovery' , current_value=c_recovery , csvfile=ts_recovery , current_date=current_date)

    msg = data_final['Country_Region'] + " " + data_final['Province_State'] + "<br>"
    msg += "Confirmed : " + data_final['Confirmed'].astype(str)+ "<br>"
    msg += "Recovered : " + data_final['Recovered'].astype(str)+ "<br>"
    msg += "Deaths : " + data_final['Deaths'].astype(str)+ "<br>"
    msg += "Last_Updated : " + data_final['Last_Update'].astype(str) + "<br>"

    data_final['text'] = msg

    # top 10 
    df_top10_cases = data_total.nlargest(10 , 'Confirmed')
    df_top10_recovery = data_total.nlargest(10 , 'Recovered')
    df_top10_deaths = data_total.nlargest(10, 'Deaths')

    ####################### Creating the figure #############################
    fig_1 = go.Figure(
        data = go.Scattergeo(
            locationmode='country names',
            lon = data_final['Long_'],
            lat = data_final['Lat'],
            hovertext = data_final['text'],
            showlegend = False,
            opacity = 0.8,
            marker = dict(
                size = data_final['Deaths']/500,
                opacity = 0.8,
                colorscale = [(0 , '#d486f0') ,(0.5 , '#2979e3') , (1 , "#0b0624")],
                reversescale= False,
                autocolorscale = False,
                symbol = 'circle',
                line = dict(
                    width = 1,
                    color = 'rgba(102 ,102 ,102)'
                ),
                cmin = 0,
                color = data_final['Confirmed'],
                cmax = data_final['Confirmed'].max(),
                colorbar_title = 'Confirmed Caes <br>Last Update',
                colorbar_x = -0.05,
            )
        )
    )

    # tweaking the layout 
    fig_1.update_geos(projection_type='orthographic', landcolor='#7c7fa6' ,
                    showocean=True , oceancolor = '#d1d4cb' , bgcolor="#18191c" )
    fig_1.update_layout(paper_bgcolor ="#18191c" , 
                        plot_bgcolor="#18191c" , 
                        font = dict(color = '#d486f0') , 
                            title = 'Last Updated '+str(data_final.Last_Update.max()))
    
    ############################# creating fig_2 #######################################
    fig_2 = make_subplots(
        rows = 4 , cols = 3,
        specs = [
            [{'type':'indicator'} , {'type':'indicator'} , {'type':'indicator'}],
            [{'colspan':3 , 'type':'scatter'},None , None],
            [{'colspan':3 , 'type':'scatter'},None , None],
            [{'colspan':3 , 'type':'scatter'},None , None],
        ],
        horizontal_spacing = 0.2
    )
    # number indicators
    fig_2.add_trace(
        go.Indicator(
            mode = 'number',
            value = total_confirmed,
            title = "TOTAL CASES"
        ),
        row =1 , col= 1
    )

    fig_2.add_trace(
        go.Indicator(
            mode = 'number' ,
            value = total_recovered,
            title = "TOTAL RECOVERED"
        ),
        row = 1 , col = 2
    )

    fig_2.add_trace(
        go.Indicator(
            mode = 'number' ,
            value = total_deaths,
            title = "TOTAL DEATHS"
        ),
        row = 1 , col = 3
    )
    # daily cases
    daily_cases = ts_cases['Cases'].diff()
    fig_2.add_trace(
        go.Scatter(
            x = ts_cases.loc[1: ,'Date'],
            y = daily_cases[1:],
            mode = 'lines',
            name = 'Daily Cases'
        ),
        row = 2 , col= 1
    )

    # daily deaths
    daily_deaths = ts_deaths['Deaths'].diff()
    fig_2.add_trace(
        go.Scatter(
            x = ts_deaths.loc[1: , 'Date'],
            y = daily_deaths[1:],
            mode = 'lines',
            name = 'Daily Fatalities',
            marker = dict(
                color = 'red'
            )
        ),
        row = 3 , col=1
    )
    # daily recovery
    daily_recoveries = ts_recovery['Recovery'].diff()
    fig_2.add_trace(
        go.Scatter(
            x = ts_recovery.loc[1:, 'Date'],
            y = daily_recoveries[1:],
            mode = 'lines',
            name ='Daily Recoveries',
            marker = dict(
                color = 'green'
            )
        ),
        row = 4 , col = 1
    )
    # tweaking the layout
    fig_2.update_layout(paper_bgcolor ="#18191c" , 
                        plot_bgcolor="#18191c" , 
                        font = dict(color = '#d486f0'),
                        legend_orientation='h',
                        legend = dict(x = 0.05 , y = 0.8))
    fig_2.update_xaxes(showgrid = False , zeroline = False ,showline=False )
    fig_2.update_yaxes(showgrid = False , zeroline = False , showline = False)

    ################################ creating fig 3 ########################################
    fig_3 = go.Figure(
        data=    go.Scatter(
            x = ts_cases['Date'],
            y = ts_cases['Cases'],
            mode = 'lines',
            name = 'Cases Cumulative'
        )
    )
    fig_3.update_layout(title = 'CASES CUMULATIVE' , paper_bgcolor ="#18191c" , plot_bgcolor="#18191c" , font = dict(color = '#d486f0') ,legend_orientation='h', legend = dict(x = 0.1 , y = -0.05))
    fig_3.update_xaxes(showgrid = False , zeroline = False ,showline=False )
    fig_3.update_yaxes(showgrid = False , zeroline = False , showline = False )

    ################### creating fig 4 #####################################################

    fig_4 = go.Figure(
        data = go.Scatter(
            x = ts_recovery['Date'],
            y = ts_recovery['Recovery'],
            mode = 'lines',
            name = 'Recovery Cumulative',
            marker = dict(color='green')
        )
    )
    fig_4.update_layout(title="RECOVERY CUMULATIVE" ,paper_bgcolor ="#18191c" , plot_bgcolor="#18191c" , font = dict(color = '#d486f0') ,legend_orientation='h', legend = dict(x = 0.1 , y = -0.05))
    fig_4.update_xaxes(showgrid = False , zeroline = False ,showline=False )
    fig_4.update_yaxes(showgrid = False , zeroline = False , showline = False)

    ############################ creating fig 5 ####################################################
    fig_5 = go.Figure(
        data = go.Scatter(
            x = ts_deaths['Date'],
            y = ts_deaths['Deaths'],
            mode = 'lines',
            name = 'Deaths Cumulative',
            marker = dict(color = 'red')
        )
    )
    fig_5.update_layout(title="DEATHS CUMULATIVE" ,paper_bgcolor ="#18191c" , plot_bgcolor="#18191c" , font = dict(color = '#d486f0') ,legend_orientation='h', legend = dict(x = 0.1 , y = -0.05))
    fig_5.update_xaxes(showgrid = False , zeroline = False ,showline=False )
    fig_5.update_yaxes(showgrid = False , zeroline = False , showline = False)

    ########################## creating fig 6 #################################################
    d_r_1 = df_top10_cases.sort_values('Confirmed' , ascending=True , ignore_index=True)
    fig_6 = go.Figure(
        data =  go.Bar(
            x = d_r_1['Confirmed'],
            y = d_r_1['Country_Region'],
            orientation ='h',
            name = 'TOP 10 COUNTRIES - CASES',
        )
    )
    fig_6.update_layout(title = 'TOP 10 COUNTRIES - CASES' ,paper_bgcolor ="#18191c" , plot_bgcolor="#18191c" , font = dict(color = '#d486f0') ,legend_orientation='h', legend = dict(x = 0.1 , y = -0.05))
    fig_6.update_xaxes(showgrid = False , zeroline = False ,showline=False)
    fig_6.update_yaxes(showgrid = False , zeroline = False , showline = False)

    ################################## creating fig 7 ##########################################

    d_r_2 = df_top10_recovery.sort_values('Recovered' , ascending=True , ignore_index=True)
    fig_7 = go.Figure(
        data = go.Bar(
            x = d_r_2['Recovered'],
            y = d_r_2['Country_Region'],
            orientation = 'h',
            name = 'TOP 10 COUNTRIES - RECOVERY',
            marker = dict(color = 'LightGreen')
        )
    )
    fig_7.update_layout(title='TOP 10 COUNTRIES - RECOVERY' ,paper_bgcolor ="#18191c" , plot_bgcolor="#18191c" , font = dict(color = '#d486f0') ,legend_orientation='h', legend = dict(x = 0.1 , y = 0.05))
    fig_7.update_xaxes(showgrid = False , zeroline = False ,showline=False)
    fig_7.update_yaxes(showgrid = False , zeroline = False , showline = False)

    #################################### creating fig 8 ##########################################
    d_r_3 = df_top10_deaths.sort_values('Deaths' , ascending=True , ignore_index=True)
    fig_8 = go.Figure(
        data = go.Bar(
            x = d_r_3['Deaths'],
            y = d_r_3['Country_Region'],
            orientation = 'h',
            name = 'TOP 10 COUNTRIES - DEATHS',
            marker = dict(color = '#eb3131')
        )
    )
    fig_8.update_layout(title = 'TOP 10 COUNTRIES - DEATHS' ,paper_bgcolor ="#18191c" , plot_bgcolor="#18191c" , font = dict(color = '#d486f0') ,legend_orientation='h', legend = dict(x = 0.1 , y = -0.05))
    fig_8.update_xaxes(showgrid = False , zeroline = False ,showline=False)
    fig_8.update_yaxes(showgrid = False , zeroline = False , showline = False)

    ###################### updating table data ################################################

    def generate_table(dataframe, max_rows=10):
        return html.Table([
            html.Thead(
                html.Tr([html.Th(col) for col in dataframe.columns] , style = {'color':'#d486f0'})
            ),
            html.Tbody([
                html.Tr([
                    html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
                ] , style = {'color':'white'}) for i in range(min(len(dataframe), max_rows))
            ])
        ], style = {
            'backgroundColor':"#18191c"
        })
    df_table = data_total.sort_values('Confirmed' ,ascending=False, ignore_index = 3)
    table = generate_table(df_table , max_rows=20)

    return [fig_1 ,
            fig_2 ,
            fig_3 ,
            fig_4 ,
            fig_5 ,
            fig_6 ,
            fig_7 ,
            fig_8 ,
            table]

if __name__ == '__main__':
    app3.run_server(debug=True)
