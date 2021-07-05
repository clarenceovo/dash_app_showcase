import dash_table
import dash_html_components as html
import plotly.express as px
import dash_core_components as dcc
import data_query.data_query_handler as data_handler

def return_oi_body():
    return [dcc.Graph(
            id='oi_fig',
            figure=px.line([],x=[0],y=[0],render_mode=['webgl'])),
            dash_table.DataTable(
                id='oi_table',
                columns=[{"name": i, "id": i} for i in ['Date', 'Price', 'OI', 'USD Value']],
                page_size=10,
                style_table={'height': '300px', 'overflowY': 'auto'}

            )

    ]


def return_funding_rate_body():
    return [dcc.Graph(
        id='funding_fig',
        figure=px.line([], x=[0], y=[0], render_mode=['webgl'])),
        dash_table.DataTable(
            id='funding_table',
            columns=[{"name": i, "id": i} for i in ['Date','percentage_rate','annual_percentage_rate']],
            page_size=10,
            style_table={'height': '300px', 'overflowY': 'auto'}

        )

    ]
