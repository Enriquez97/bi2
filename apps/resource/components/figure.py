

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