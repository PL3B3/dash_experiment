"""
Running
  `python app.py`
  'pipenv run python app.py'

See http://127.0.0.1:8050/ in your web browser.
"""

from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px

app = Dash(__name__)

colors = {
  'background': '#111111',
  'text': '#fc6c85'
}

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fruit_fig = px.bar(df, x="City", y="Amount", color="Fruit", barmode="group")

fruit_fig.update_layout(
  plot_bgcolor=colors['background'],
  paper_bgcolor=colors['background'],
  font_color=colors['text']
)


markdown_text = '''
### First Dash App

We can do the text writing in markdown yay

click on [this link](https://dash.plotly.com/layout). do it. do it now
'''

app.layout = html.Div(children=[
  dcc.Markdown(
    children=markdown_text,
    style={
      'color': colors['text']
    }
  ),

  html.Br(),
  html.Label("Slider"),
  dcc.Slider(
    min=1,
    max=5,
    marks={i : f'Day {i}' for i in range(1, 6)},
    value=5
  ),

  html.Br(),
  dcc.Graph(
    id='fruit-graph',
    figure=fruit_fig
  )
])

if __name__ == '__main__':
  app.run_server(debug=True)