import plotly.express as px


def create_empty(text):
    layout = dict(
        autosize=True,
        annotations=[dict(text=text, showarrow=False)],
        paper_bgcolor="#1c2022",
        plot_bgcolor="#1c2022",
        font_color="#A3AAB7",
        font=dict(color="FFFF", size=20),
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
    )
    return {"data": [], "layout": layout}

def graph_empty(text=''):
    layout = dict(
        autosize=True,
        annotations=[dict(text=text, showarrow=False)],
        #paper_bgcolor="#1c2022",
        #plot_bgcolor="#1c2022",
        #font_color="#A3AAB7",
        font=dict(color="FFFF", size=20),
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
    )
    return {"data": [], "layout": layout}

class Bar:
    def __init__(self, data,template):
        self.data = data
        self.template = template
        
    def bar_px(self,parametros : dict):
        figure = px.bar(
            dataframe = self.data, x=parametros["x"], y=parametros["y"],height = parametros["height"], template = parametros["template"],title = f"<b>{parametros["title"]}</b>",#
            color_discrete_sequence=parametros["color_discrete_sequence"]
        )
        figure.update_layout(legend=dict(orientation=parametros["orientation"],yanchor="bottom",y=1.02,xanchor="right",x=1),legend_title_text='',height = 380,bargroupgap=0.4)