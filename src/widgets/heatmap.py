import os
import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc

from src.Dataset import Dataset

def create_heatmap(data_selected=None): 
    heatmap_figure = draw_heatmap(data_selected)
    return html.Div([
        dcc.Graph(figure=heatmap_figure, 
                config={
                    'displaylogo': False,
                    'modeBarButtonsToRemove': ['zoom', 'pan', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale']
                }, 
                id='heatmap', 
                clear_on_unhover=True),
        dcc.Tooltip(id="heatmap-tooltip", 
                    loading_text="LOADING"),
    ], className='border-widget stretchy-widget', id='heatmap-container')

def draw_heatmap(data_selected):
    if data_selected is None or len(data_selected) == 0:
        fig = go.Figure()

        # Add only layout information
        fig.update_layout(
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            annotations=[
                dict(
                    text="Select data on the scatterplot",
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(size=28, color="gray")
                )
            ],
            margin=dict(b=0, l=0, r=0, t=40)  # Adjust margins to ensure the text is visible
        )

        return fig

    data_selected = data_selected.sort_values('image_path')  # sort by image_path
    attr_data = Dataset.get_attr_data().loc[data_selected.index]
    attr_data = attr_data.loc[:, attr_data.any()]  # filter attributes with all zeros

    image_path = data_selected['image_path'].to_list()
    image_names = [os.path.splitext(os.path.basename(item))[0] for item in image_path]
    max_len_name = max(len(name) for name in image_names)

    fig = px.imshow(attr_data.to_numpy().tolist(), 
                    x=attr_data.columns.tolist(), 
                    y=image_path,
                    width=attr_data.shape[1]*20+8*max_len_name+200, height=attr_data.shape[0]*20+250+150)
    
    fig.update_traces(dict(showscale=False, 
                           coloraxis=None, 
                           colorscale='blues'), 
                           hoverinfo='none', 
                           hovertemplate=None)

    fig.update_layout(
        xaxis=dict(
            side='top', 
            tickangle=280, 
            automargin=False, 
            fixedrange=True
        ),
        yaxis=dict(
            # visible=False, 
            side='left',
            automargin=False, 
            fixedrange=True, 
            tickvals=list(range(len(image_names))),
            ticktext=image_names,
        ), 
        margin=dict(l=8*max_len_name, r=200, t=250, b=150), 
    )
    
    return fig