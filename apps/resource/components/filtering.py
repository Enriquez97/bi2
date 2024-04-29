import dash_mantine_components as dmc
from dash_iconify import DashIconify

def accordion_ftr(type = ""):
    if type != None:
        return dmc.Accordion(
            children=[
                dmc.AccordionItem(
                    [
                        dmc.AccordionControl(
                            f"Filtros - {type}",
                            icon=DashIconify(
                                icon="tabler:settings-2",
                                color="blue",
                                width=20,
                                )
                        ),
                        dmc.AccordionPanel([
                            dmc.Grid([
                                dmc.Col([
                                    dmc.Select(
                                        label="Template",
                                        placeholder="Select",
                                        id="select-template",
                                        value="plotly",
                                        data=['plotly','ggplot2', 'seaborn', 'simple_white','plotly_white', 'plotly_dark', 
                                            'presentation', 'xgridoff','ygridoff', 'gridon', 'none'],
                                        clearable=False
                                    ),
                                
                                ],span = 2),
                                dmc.Col([
                                    dmc.Select(
                                        label="Tipo",
                                        placeholder="Select",
                                        id="select-type",
                                        value="relative",
                                        data=["relative","overlay","group","stack"],
                                        clearable=False
                                    ),
                                ],span = 2),
                                dmc.Col([
                                    dmc.Select(
                                        label="Orientacion",
                                        placeholder="Select",
                                        id="select-orientation",
                                        value="vertical",
                                        data=["vertical","horizontal"],
                                        clearable=False
                                    ),
                                ],span = 2),
                                dmc.Col([
                                    dmc.CheckboxGroup(
                                        id="checkbox-group",
                                        #label="Select your favorite framework/library",
                                        #description="This is anonymous",
                                        orientation="horizontal",
                                        withAsterisk=True,
                                        offset="md",
                                        mb=10,
                                        children=[
                                            dmc.Checkbox(label="Tick X", value=True),
                                            dmc.Checkbox(label="Tick Y", value=True),
                                            dmc.Checkbox(label="Leyenda", value=True),
                                            #dmc.Checkbox(label="Angular", value="angular"),
                                        ],
                                        value=[True,True,True],
                                    ),
                                ],span = 6),
                                
                            ],gutter ="xl"),
                            
                            dmc.TextInput(
                                id="input-name",
                                label="KPI Name",
                                placeholder = "Name"
                            ),
                        ]),
                    ],
                    value="customization",
                ),
                
            ],
        )