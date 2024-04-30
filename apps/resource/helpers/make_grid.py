import plotly.express as px
import dash_ag_grid as dag
import dash_mantine_components as dmc

def Grid(content = [],g = "xs"):
    return \
    dmc.Grid(
        children = content,
        gutter= g
    )

def Col(content = [], size = 12):
    return \
    dmc.Col(  
        children = content,
        xs = 12,
        sm = 12,
        md = size,
        lg = size,
        xl = size
    )