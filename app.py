import pandas as pd
import plotly.graph_objs as go
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import datetime
import warnings
warnings.filterwarnings('ignore')

# external CSS stylesheets
external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk',
        'crossorigin': 'anonymous'
    }
]

patients = pd.read_csv('data/AgeGroupDetails.csv')
age = pd.read_csv("data/AgeGroupDetails.csv")
covid = pd.read_csv("data/covid_19_india.csv")
patients['diagnosed_date'] = pd.to_datetime(patients['diagnosed_date'], dayfirst=False)
covid['Date'] = pd.to_datetime(covid['Date'], dayfirst=True)

confirmed = covid.groupby([covid['Date'].dt.month, 'State/UnionTerritory'])['Confirmed'].sum().reset_index()
cured = covid.groupby([covid['Date'].dt.month, 'State/UnionTerritory'])['Cured'].sum().reset_index()
death = covid.groupby([covid['Date'].dt.month, 'State/UnionTerritory'])['Deaths'].sum().reset_index()
group = pd.merge(confirmed, cured, on=['Date', 'State/UnionTerritory']).merge(death, on=['Date', 'State/UnionTerritory']).sort_values('Date')

again1 = group.groupby('Date')[['Confirmed', 'Cured', 'Deaths']].sum().reset_index()
again1['Date'] = again1['Date'].map(lambda x: datetime.datetime.strptime(str(x), '%m')).dt.month_name()
again2 = group.groupby(['State/UnionTerritory'])[['Confirmed', 'Cured', 'Deaths']].sum().reset_index()

temp3 = patients['diagnosed_date'].dt.month.value_counts().reset_index().sort_values('index')
temp3['index'] = temp3['index'].apply(lambda x: datetime.datetime.strptime(str(x), '%m')).dt.month_name()

temp1 = patients['current_status'].value_counts()
total = temp1.sum()
active = temp1.to_dict()['Hospitalized']
recovered = temp1.to_dict()['Recovered']
deaths  = temp1.to_dict()['Deceased']

options1 = [
    {'label': 'All', 'value': 'All'},
    {'label': 'Hospitalized', 'value': 'Hospitalized'},
    {'label': 'Recovered', 'value': 'Recovered'},
    {'label': 'Deceased', 'value': 'Deceased'},
]

options2 = [
    {'label': 'State wise', 'value': 'detected_state'},
    {'label': 'City wise', 'value': 'detected_city'},
    {'label': 'District wise', 'value': 'detected_district'}
]

# app.py
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1(id="title", children="Covid-19 Dashboard - India (2020)", 
                     style={"color": "#b24e25",
                            'textAlign':'center',
                            'fontSize': 45,
                            'backgroundColor': '#004a77',
                            'display': 'block',
                            'margin': 'auto'}),
    html.Br(),

    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total Cases", className='text-light'),
                    html.H4(f"{total}", className='text-light')
                ], className='card-body',),
            ], className='card bg-danger text-center'),

# bg-danger, bg-primary, bg-secondary, bg-success, bg-warning, bg-info, bg-light, bg-dark
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Active", style={'color': 'black'}),
                    html.H4(f"{active}", style={'color': 'black'})
                ], className='card-body'),
            ], className='card',
                style={'backgroundColor': '#17a2b8', 'color': 'black', 'textAlign': 'center'}),
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Recovered"),
                    html.H4(f"{recovered}")
                ], className='card-body'),
            ], className='card',
                style={'backgroundColor': '#ffc107', 'color': 'black', 'textAlign': 'center'}),
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Deaths"),
                    html.H4(f"{deaths}")
                ], className='card-body'),
            ], className='card',
                style={'backgroundColor': '#28a745','color': 'white' ,'textAlign': 'center'}),
        ], className='col-md-3'),
    ], className='row'),

    html.Br(),

    html.Div([
        html.Div([
            dcc.Graph(id='pie1',
                      figure={'data': [go.Pie(labels=['Active', 'Recovered', 'Deaths'], 
                                              hovertext=['Active', 'Recovered', 'Deaths'], 
                                              values=[active, recovered, deaths],
                                              marker=dict(colors=['#17a2b8', '#ffc107', '#dc3545']))],

                              'layout': go.Layout(title='Covid-19 India Status', 
                                                  font={'color': 'black'},
                                                  height=400, width=536)})
        ], className='col-md-6'),
        html.Div([
            dcc.Graph(id='pie2',
                      figure={'data': [go.Pie(labels=age['AgeGroup'], 
                                              hovertext=['AgeGroup', 'TotalCases'], 
                                              values=age['TotalCases'],
                                              marker=dict(colors=age['AgeGroup']))],

                              'layout': go.Layout(title='Age distribution of patients in India',
                                                  title_x=0.5,  # Title position 
                                                  xaxis={'title': 'AgeGroup'},
                                                  yaxis={'title': 'TotalCases'},
                                                  font=dict(family='Arial', size=14, color='black'),  # Font style
                                                  legend=dict(orientation='v'),  # Legend position
                                                  annotations=[dict(text='Total Cases', x=0.5, y=0.5, font_size=15, showarrow=False)],  # Annotation
                                                  height=400, width=536)})
        ], className='col-md-6'),
    ], className='row'),

    html.Br(),

    html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(id='state-dropdown', options=options1, value='All', placeholder='All' ),
            ], className='col-md-6', style={'color': 'black' ,'textAlign': 'center'}),
            html.Div([
                dcc.Dropdown(id='special-dropdown', options=options2, value='State wise', placeholder='State wise'),
            ], className='col-md-6', style={'color': 'black' ,'textAlign': 'center'}),
        ], className='row')]),


    html.Div([dcc.Graph(id='bar')], 
             style = {'left': '0', 'right': '0', 'margin-left': 'auto', 'margin-right': 'auto', 'width': '100%'}),

    html.Br(),

    html.Div(
        [
            html.Div([
                dcc.Graph(id='cases-graph')
            ], className='col-md-6'),

            html.Div([dcc.Graph(id='cases-graph2')], className='col-md-6'),
        ]
    , className='row')

], className='container')

@app.callback(Output('bar', 'figure'), [Input('state-dropdown', 'value') , Input('special-dropdown', 'value')])
def updated_graph(status, special):
    if status == 'All' and special == 'State wise':
        data = patients['detected_state'].value_counts().reset_index()
        return {'data': [go.Bar(x = data['index'], 
                                y = data['detected_state'], 
                                text = data['detected_state'],
                                textposition = 'auto',
                                marker= {'color': data['detected_state']},
                                name='All')],

                'layout': go.Layout(title = 'States with number of cases', 
                                    xaxis = {'title': 'States', 'tickangle': 45}, 
                                    yaxis = {'title': 'Number of cases'},
                                    titlefont={'color': 'purple'},
                                    margin={"l": 70, "b": 160, "t": 70, "r": 90},
                                    font=dict(family='Arial', size=14, color='black'),
                                    hovermode="closest"),}
    elif status != 'All' and special == 'State wise':
        data = patients[patients['current_status'] == status]['detected_state'].value_counts().reset_index()
        
        return {'data': [go.Bar(x = data['index'], 
                                y = data['detected_state'], 
                                text = data['detected_state'], 
                                textposition = 'auto',
                                marker= {'color': data['detected_state']},
                                name='All')],

                'layout': go.Layout(title = 'States with number of cases', 
                                    xaxis = {'title': 'States', 'tickangle': 45}, 
                                    yaxis = {'title': 'Number of cases'},
                                    titlefont={'color': 'blue'},
                                    margin={"l": 70, "b": 160, "t": 70, "r": 90},
                                    font=dict(family='Arial', size=14, color='black'),
                                    hovermode="closest"),}
    
    elif status == 'All' and special != 'State wise':
        name = special.split('_')[1]
        temp2 = patients[special].value_counts().reset_index()
        return {'data': [go.Bar(x = temp2['index'], 
                                y = temp2[special], 
                                text = temp2[special], 
                                textposition = 'auto',
                                marker= {'color': temp2[special]},
                                name = name.title())],

                'layout': go.Layout(title = f'{name.title()} with number of cases', 
                                    xaxis = {'title': f'{name.title()}', 'tickangle': 45}, 
                                    yaxis = {'title': 'Number of cases'}
                                    ,titlefont={'color': 'blue'},
                                    margin={"l": 70, "b": 160, "t": 70, "r": 90},
                                    font=dict(family='Arial', size=14, color='black'),
                                    hovermode="closest"),
                                }
    else:
        data = patients[patients['current_status'] == status]
        temp2 = data[special].value_counts().reset_index()
        name = special.split('_')[1]
        return {'data': [go.Bar(x = temp2['index'], 
                                y = temp2[special], 
                                text = temp2[special], 
                                textposition = 'auto',
                                marker= {'color': temp2[special]},
                                name = name.title())],

                'layout': go.Layout(title = f'{name.title()} with number of cases', 
                                    xaxis = {'title': f'{name.title()}', 'tickangle': 45}, 
                                    yaxis = {'title': 'Number of cases'},
                                    titlefont={'color': 'red'},
                                    margin={"l": 70, "b": 160, "t": 70, "r": 90},
                                    font=dict(family='Arial', size=14, color='black'),
                                    hovermode="closest")}

# Define callback to update the graph
@app.callback(Output('cases-graph', 'figure'), Input('state-dropdown', 'value'))
def update_graph1(value):
    # Create traces
    trace1 = go.Bar(x=again1['Date'], y=again1['Confirmed'],
                    text=again1['Confirmed'],
                    textposition='auto',
                    name='Confirmed')

    trace2 = go.Bar(x=again1['Date'], y=again1['Cured'],
                    text=again1['Cured'],
                    textposition='auto',
                    name='Cured')

    trace3 = go.Bar(x=again1['Date'], y=again1['Deaths'],
                    text=again1['Deaths'],
                    textposition='auto',
                    name='Deaths')

    data = [trace1, trace2, trace3]
    layout = go.Layout(
        title='Number of cases in India',
        title_x = 0.5,
        xaxis=dict(title='Months', tickangle= 45),
        yaxis=dict(title='Number of cases', type='log'),
        font=dict(family='Arial', size=14, color='black'),
        barmode='group'
    )
    fig = go.Figure(data=data, layout=layout)
    return fig

@app.callback(Output('cases-graph2', 'figure'), Input('state-dropdown', 'value'))
def update_graph2(value):
    # Create traces
    trace = go.Scatter(x = temp3['index'], 
                   y = temp3['diagnosed_date'],
                   mode = 'lines+markers',)

    # create line plot using plotly
    trace = go.Scatter(x = temp3['index'], 
                    y = temp3['diagnosed_date'],
                    mode = 'lines+markers',)
    data = [trace]
    layout = go.Layout(
        title='State wise Number of cases in India',
        title_x = 0.5,
        xaxis=dict(title='Months', tickangle= 45),
        yaxis=dict(title='Number of cases', type='log'),
        font=dict(family='Arial', size=14, color='black'),
    )
    fig = go.Figure(data=data, layout=layout)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port = 5000) # by default port is 8520
