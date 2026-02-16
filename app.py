from model import forecast_revenue
import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc
from insights import generate_insights

# Load Data
df = pd.read_csv("data/sales_data.csv")
insights = generate_insights()

# Initialize App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "AI Analytics Dashboard"

# Charts
revenue_fig = px.line(
    df,
    x="Date",
    y="Revenue",
    markers=True,
    template="plotly_dark",
    title="Revenue Trend"
)
forecast_df = forecast_revenue()

forecast_fig = px.line(
    forecast_df,
    x="DayIndex",
    y="Revenue",
    color="Type",
    template="plotly_dark",
    title="Revenue Forecast (Next 7 Days)"
)


region_fig = px.bar(
    df.groupby("Region")["Revenue"].sum().reset_index(),
    x="Region",
    y="Revenue",
    template="plotly_dark",
    title="Revenue by Region"
)

# Sidebar
sidebar = html.Div(
    [
        html.H2("SaaS Analytics", className="logo"),
        html.Hr(),
        html.P("Business Intelligence", className="menu-title"),
        dbc.Nav(
            [
                dbc.NavLink("Dashboard", active=True),
                dbc.NavLink("Revenue"),
                dbc.NavLink("Customers"),
                dbc.NavLink("Forecasting"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)

# KPI Cards
def kpi_card(title, value):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H6(title, className="card-title"),
                html.H3(value, className="card-value"),
            ]
        ),
        className="kpi-card"
    )

content = html.Div(
    [
        html.H2("Dashboard Overview", className="section-title"),

        dbc.Row(
            [
                dbc.Col(kpi_card("Average Revenue", f"${insights['avg_revenue']}"), md=4),
                dbc.Col(kpi_card("Best Day", insights["best_day"]), md=4),
                dbc.Col(kpi_card("Worst Day", insights["worst_day"]), md=4),
            ],
            className="mb-4"
        ),
        dbc.Row(
    [
        dbc.Col(dcc.Graph(figure=forecast_fig), md=12),
    ],
    className="mt-4"
),

        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=revenue_fig), md=8),
                dbc.Col(dcc.Graph(figure=region_fig), md=4),
            ]
        )
    ],
    className="content",
)

app.layout = html.Div([sidebar, content])

if __name__ == "__main__":
    app.run(debug=True)
