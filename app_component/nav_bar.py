import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

def get_navbar():
    return dbc.NavbarSimple(
                                children=[
                                    #dbc.NavItem(dbc.NavLink("Page 1", href="#")),
                                    dbc.DropdownMenu(
                                        children=[
                                            dbc.DropdownMenuItem("Data Type", header=True),
                                            dbc.DropdownMenuItem("Open Interest", href="openInterest"),
                                            dbc.DropdownMenuItem("Funding Rate", href="fundingRate", disabled=False),
                                            dbc.DropdownMenuItem("Volume", href="Volume",disabled=True)

                                        ],
                                        nav=True,
                                        in_navbar=True,
                                        label="Data Type",
                                        id="type-dropdown"
                                    ),
                                ],
                                brand="AC Analytics",
                                brand_href="#",
                                color="secondary",
                                id="navbar",
                                dark=True,
                            )