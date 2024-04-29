import dash_mantine_components as dmc
from dash import html

def accordion_show_layout(list_sp = []):
    return \
    html.Div(
    dmc.Accordion(
        value=list_sp[0],
        children=[
            dmc.AccordionItem(
                [
                    dmc.AccordionControl(i),
                    dmc.AccordionPanel(
                        children=i
                    ),
                ],
                value=list_sp
                #value="customization",
            )for i in list_sp
        ],
        
    )
    
)