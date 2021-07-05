import dash
import dash_core_components as dcc
import dash_html_components as html
from flask import Flask
import dash_bootstrap_components as dbc
import pandas as pd
from app_component.nav_bar import *
from app_component.body import *
from app_component.dropdown_body import *
from dash.exceptions import PreventUpdate
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import logging
#from pandas.tseries.frequencies import *
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

server = Flask(__name__)
app = dash.Dash(__name__, suppress_callback_exceptions=True,server=server,url_base_pathname='/'
                ,external_stylesheets=[dbc.themes.BOOTSTRAP]
                ,meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

app.layout = html.Div([dcc.Location(id='url', refresh=False),html.Div(id='page-content')])
app.title = "AC Analytics"

@server.route("/")
def my_dash_app():
    return app.index()

def get_oi_layout():

    return dbc.Container(dbc.Tab([get_navbar(),]+
                    return_oi_dropdown_body()+
                    return_oi_body(),className = "mb-3"))


def get_funding_rate_layout():
    return dbc.Container(dbc.Tab([get_navbar(),]+
                    return_funding_rate_dropdown_body()+
                    return_funding_rate_body(),className = "mb-3"))


@app.callback(
    dash.dependencies.Output("oi-future-dropdown", 'options'),
    [dash.dependencies.Input('oi-contract-dropdown', 'value')]
)
def oi_update_future_dropdown(name):
    if not name:
        raise PreventUpdate
    contract = name
    future_df = data_handler.get_contract_pair(exchange=contract)
    return [{"label": item, "value": name + "@" + item} for item in future_df[0].values]


@app.callback(
    dash.dependencies.Output("oi_fig", 'figure'),
    [dash.dependencies.Input('oi-future-dropdown', 'value')]
)
def oi_update_chart(label):
    if not label:
        raise PreventUpdate
    logger.info(label)
    data_df = data_handler.get_oi_data(label)
    data_df.columns = ['time', 'price', 'open_interest']

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # fig = px.line(data_df,x='time',y=['open_interest'],render_mode=['webgl'])
    fig.add_trace(
        go.Scatter(x=data_df['time'], y=data_df['open_interest'], name="Open Interest Data"),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=data_df['time'], y=data_df['price'], name="Price Data"),
        secondary_y=True,
    )
    fig.update_xaxes(title_text="OI and Price Chart")
    fig.update_yaxes(title_text="Open Interest", secondary_y=False)
    fig.update_yaxes(title_text="Price", secondary_y=True)
    fig.update_xaxes(rangeslider_visible=True)
    return fig


@app.callback(
    dash.dependencies.Output("oi_table", 'data'),
    [dash.dependencies.Input('oi-future-dropdown', 'value')]
)
def oi_update_chart(label):
    if not label:
        raise PreventUpdate
    data_df = data_handler.get_oi_data(label)
    data_df.columns = ['Date', 'Price', 'OI']
    data_df['USD Value'] = data_df.apply(lambda x: "${:,}".format(round(x.Price * x.OI, 3)), axis=1)
    df = data_df.sort_values(by=['Date'], ascending=False)
    return df.to_dict("records")


@app.callback(
    dash.dependencies.Output("funding-future-dropdown", 'options'),
    [dash.dependencies.Input('funding-contract-dropdown', 'value')]
)
def update_future_dropdown(name):
    if not name:
        raise PreventUpdate
    contract = name
    future_df = data_handler.get_funding_contract(exchange=contract)
    return [{"label": item, "value": name + "@" + item} for item in future_df[0].values]

@app.callback(
    dash.dependencies.Output("funding_fig", 'figure'),
    [dash.dependencies.Input('funding-future-dropdown', 'value')]
)
def funding_update_chart(label):
    if not label:
        raise PreventUpdate
    data_df = data_handler.get_funding(label)
    data_df.columns = ['time', 'contract', 'percentage_rate']
    daily_df = data_df.copy()
    daily_df['time'] = pd.to_datetime(daily_df['time'])
    daily_df['time_index'] = daily_df['time']
    daily_df = daily_df.set_index('time')
    daily_df = daily_df.groupby("contract").resample('D').sum() #set resample strategy
    daily_df = daily_df.reset_index()
    daily_df['annual_percentage_rate'] = daily_df.apply(lambda x: float(x.percentage_rate) *365*100,axis=1)
    daily_df['time_index'] = daily_df['time']
    daily_df = daily_df.set_index("time_index")
    data_df['percentage_rate'] = data_df.apply(lambda x: x["percentage_rate"] * 100, axis=1)
    data_df['annual_percentage_rate'] = data_df.apply(lambda x: round(float(x["percentage_rate"]) * 24 * 365, 3),axis=1)
    fig = make_subplots(rows=2, subplot_titles=("Daily Rate", "Annualised Rate"),specs=[[{"secondary_y": True}],[{"secondary_y": True}]])
    fig.append_trace(go.Scatter(x=daily_df['time'], y=daily_df['annual_percentage_rate'], name="Annualized Rate", line_color="blue"), row=1,col=1)
    fig.add_trace(go.Scatter(x=daily_df['time'], y=daily_df['percentage_rate'], name="Daily Percentage Funding Rate", line_color="blue"), row=1,col=1,secondary_y=True
    )
    fig.append_trace(
        go.Scatter(x=data_df['time'], y=data_df['annual_percentage_rate'], name="Annualized Rate", line_color="black"), row=2,
        col=1
    )
    fig.add_trace(
        go.Scatter(x=data_df['time'], y=data_df['percentage_rate'], name="Percentage Rate", line_color="black"), row=2,
        col=1 , secondary_y=True
    )
    fig.update_xaxes(title_text="Daily Annualised Funding Rate", row=1, col=1)
    fig.update_xaxes(title_text="Hourly Annualised Funding Rate", row=2, col=1)
    fig.update_yaxes(title_text="Daily Funding Rate", row=1, col=1)
    fig.update_yaxes(title_text="Hourly Funding Rate", row=2, col=1)
    #SAVE CSV to check sum
    #daily_df.to_csv(r"C:\Users\Clarence Fung - ACDX\PycharmProjects\dash_oi_dashboard\daily.csv")
    #data_df.to_csv(r"C:\Users\Clarence Fung - ACDX\PycharmProjects\dash_oi_dashboard\hourly.csv")
    fig.add_hline(y=0, line_color="red")
    fig.update_layout(height=800, title_text="Funding Rate")
    return fig

@app.callback(dash.dependencies.Output("funding_table", 'data'),
            [dash.dependencies.Input('funding-future-dropdown', 'value')])
def update_chart(label):
    if not label:
        raise PreventUpdate
    data_df = data_handler.get_funding_table(label)
    data_df.columns=['Date','contract','percentage_rate']
    data_df['percentage_rate'] = data_df.apply(lambda x: f'{round(x["percentage_rate"]*100, 8)}',axis=1)
    data_df['annual_percentage_rate'] = data_df.apply(lambda x:f'{round(float(x["percentage_rate"])*24*365,3)}%',axis=1)
    data_df['percentage_rate'] = data_df.apply(lambda x: f'{x["percentage_rate"]}%', axis=1)
    df = data_df.sort_values(by=['Date'],ascending=False)
    return df.to_dict("records")

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):

    if pathname == '/openInterest':
        return get_oi_layout()

    elif pathname == '/fundingRate':
        return get_funding_rate_layout()

    else: # return open interest page as default
        return get_oi_layout()



if __name__ == '__main__':
    server.run(port=9888, host='0.0.0.0', debug=False)
