import pandas as pd
import plotly.express as px


def document_topics_pie(topics):
    df = pd.Series(topics, name="score").to_frame()
    df = df[df.score > 0.02]
    fig = px.pie(df, values="score", names=df.index, title="Document Topics")
    fig.update_layout(showlegend=False)
    return fig
