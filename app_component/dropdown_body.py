import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import data_query.data_query_handler as data_handler

def return_oi_dropdown_body():
    exchange_df = data_handler.get_oi_exchange()
    return [html.H6("Select exchange"),dcc.Dropdown(
            id='oi-contract-dropdown',
            options=[{"label":item,"value":item}for item in exchange_df[0].values],
            placeholder="Select a exchange"
            ),html.H6("Select future"),
            dcc.Dropdown(
                id='oi-future-dropdown',
                options=[],
                placeholder="Select a future"
            )]

def return_funding_rate_dropdown_body():
    exchange_df = data_handler.get_funding_exchange()
    return [ html.H6("Select exchange"),dcc.Dropdown(
            id='funding-contract-dropdown',
            options=[{"label":item,"value":item}for item in exchange_df[0].values],
            placeholder="Select a exchange"
            ),html.H6("Select future"),dcc.Dropdown(
                id='funding-future-dropdown',
                options=[],
                placeholder="Select a future"
            )]