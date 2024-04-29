from dash import Dash, dcc, html, Input, Output,State,dash_table,no_update,clientside_callback
import plotly.express as px
import dash_ag_grid as dag

def dataframe_group(type_operation = "", dataframe = None, var_cate = [], var_num = []):
    if type_operation == "sum":
        return dataframe.groupby(var_cate)[var_num].sum().reset_index()
    elif type_operation == "mean":
        return dataframe.groupby(var_cate)[var_num].mean().reset_index()
    elif type_operation == "count":
        return dataframe.groupby(var_cate)[var_num].count().reset_index()
    else :
        return dataframe[var_cate+var_num]


def layout_create(type_l = "", dataframe = None, cate = [], num = []):
    if type_l == "Bar px":
        fig = px.bar(dataframe, x=cate[0], y=num[0])
        return dcc.Graph(figure= fig,style={"height":350}),fig.to_dict()
    elif type_l == "Pie px":
        fig = px.pie(dataframe, names=cate[0], values=num[0])
        return dcc.Graph(figure=fig,style={"height":350}),fig.to_dict()
    elif type_l == "Line px":
        fig = px.line(dataframe,x=cate[0],y = num[0])
        return dcc.Graph(figure = fig,style={"height":350}),fig.to_dict()
    elif type_l == "Table dag":
        table =  dag.AgGrid(
            id='table-data',
            columnDefs=[{"field": i, "type": "rightAligned"} for i in dataframe.columns],
            rowData=dataframe.to_dict("records"),
            columnSize = "responsiveSizeToFit",
            defaultColDef={"resizable": True, "sortable": True, "filter": True, "minWidth":100},
            className = 'ag-theme-quartz',
            style={'font-size':8},
        )
        return table,table