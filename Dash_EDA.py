# Import packages
from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.io as pio

pio.templates.default = 'plotly_dark'
load_figure_template('LUX')

# Incorporate data
df = pd.read_csv(r"C:\Users\Asus\Downloads\processed_data.csv")

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col(
            html.Div('Advanced Data Analytics: Income Distribution and Demographic Profiling', className="text-dark text-center fs-2 fw-bold"),
            width=50
        )
    ], style={'backgroundColor': '#2D2D2D', 'padding': '10px'}),  # Padding for the header

    # Graphs section
    dbc.Row([
# Box Plot with Dropdown
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H4("Select Feature for Box Plot", className="card-title text-dark"),
                    dcc.Dropdown(
                        options=[{"label": col, "value": col} for col in df.columns],
                        value='education', id='x-axis-dropdown',
                        className="mb-3"  # Margin below the dropdown
                    ),
                    dcc.Graph(id='box-plot')
                ]),
                className="mb-4",  # Margin below the card
                color="dark",  # Card color
                outline=True
            )
        ], width=6),

 # Pie Chart for "race"
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H4("Distribution of Race", className="card-title text-dark"),
                    dcc.Graph(id='pie-chart')
                ]),
                className="mb-4",  # Margin below the card
                color="dark",  # Card color
                outline=True
            )
        ], width=6),
    ], className="mb-4"),

    # Horizontal Histogram
    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H4("Income Distribution by Selected Feature", className="card-title text-dark"),
                    dcc.Graph(id='horizontal-histogram')
                ]),
                className="mb-4",  # Margin below the card
                color="dark",  # Card color
                outline=True
            )
        ], width=12),
    ]),
    # Footer section to add my name: 
dbc.Row([
    dbc.Col([
        html.Div('©Created by Rana Hamed', className="text-dark text-center")
    ], width=12)
], style={'marginTop': '30px', 'marginBottom': '10px', 'backgroundColor': '#2D2D2D'})

], fluid=True)

# Callbacks for updating graphs based on selected features
@callback(
    Output('box-plot', 'figure'),
    Output('pie-chart', 'figure'),
    Output('horizontal-histogram', 'figure'),
    Input('x-axis-dropdown', 'value')
)
##################### style bacgournd

def update_graphs(x_feature):
    box_plot = px.box(df, x='income', y=x_feature,
                      title=f'Box Plot of {x_feature} by Income')
    # Pie Chart for "race" field with modern colors
    race_dis = df['race'].value_counts()
    pie_chart = px.pie(values=race_dis, names=race_dis.index,
                       color_discrete_sequence=px.colors.sequential.Jet,
                       title='Distribution of Race')
    # pie chart comment :   
    observation_text = (
        "An important point to notice here is that except Whites, there are very few people <br>"
        "of different races. Due to this, one may fail to notice the exact <br>"
        "percentage and relationship of people earning more than 50K dollars a year."
    )

    horizontal_histogram = px.histogram(df, y=x_feature, color='income',
                                        color_discrete_sequence=['#E69F00', '#56B4E9'],  # Clear and distinct colors
                                        orientation='h',
                                        title=f'Horizontal Histogram of {x_feature} by Income')

####### now the color styling of all three graphs :
    pie_chart.update_layout(
            title={
        'text': f'Distribution of Race',
        'font': {'size': 24, 'family': 'Arial', 'color': 'white'},  # Title font settings
        'x': 0.5,  # Center the title
        'xanchor': 'center'
    },
        annotations=[
            dict(
                text=observation_text,
                showarrow=False,  # Remove the arrow to keep it simple
                font=dict(size=20, family='Arial', color='#ffffff'),  # Font size, family, and color
                x=0.5,  # X-coordinate (centered)
                y=-0.2,  # Adjusted Y-coordinate to position the text better
                xanchor='center',  # Center the text horizontally
                yanchor='top',  # Anchor the text to the top
                align="center",  # Center the text
                bgcolor='#333333',  # Background color for readability
                borderpad=4,  # Padding between the border and text
                bordercolor='#ffffff'  # Border color around the text
            )
        ],
        margin=dict(b=150),  # Increase bottom margin to accommodate the annotation
        plot_bgcolor='#ffffff',
        paper_bgcolor='#000000',
        font=dict(color='white')
    )
    box_plot.update_layout(
    title={
        'text': f'Box Plot of {x_feature} by Income',
        'font': {'size': 24, 'family': 'Arial', 'color': 'white'},  # Title font settings
        'x': 0.5,  # Center the title
        'xanchor': 'center'
    },
    plot_bgcolor='#ffffff',  # Dark background for the plot area
    paper_bgcolor='#000000', # Darker background color for the paper area
    font=dict(color='white')  # Font color for the text
)
    horizontal_histogram.update_layout(
            title={
        'text': f'Horizontal Histogram of {x_feature} by Income',
        'font': {'size': 24, 'family': 'Arial', 'color': 'white'},  # Title font settings
        'x': 0.5,  # Center the title
        'xanchor': 'center'
    },
        
    plot_bgcolor='#1E1E1E',
    paper_bgcolor='#2D2D2D',
    font=dict(color='white')
)
    return box_plot, pie_chart, horizontal_histogram

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8055)
