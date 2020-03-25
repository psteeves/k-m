import pandas as pd
import plotly.express as px
import streamlit as st


@st.cache(show_spinner=False)
def document_topics_pie(topics):
    df = pd.Series(topics, name="score").to_frame()
    fig = px.pie(df, values="score", names=df.index)
    fig.update_layout({"legend_orientation": "h"})
    fig.update_traces(textposition="inside", textinfo="percent")
    return fig
