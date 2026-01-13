import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read data
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Initialize app
app = dash.Dash(__name__)

# Custom Styling
COLORS = {
    'background': '#f4f7f6',
    'card_bg': '#ffffff',
    'header': '#1a1a1a',
    'accent': '#005288', # SpaceX Blue
    'success': '#28a745',
    'text': '#333333'
}

app.layout = html.Div(style={'backgroundColor': COLORS['background'], 'padding': '20px', 'fontFamily': 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif'}, children=[
    
    # HEADER
    html.Div([
        html.H1('SpaceX Launch Records Dashboard',
                style={'textAlign': 'center', 'color': COLORS['header'], 'fontWeight': 'bold', 'margin': '0'}),
        html.Hr(style={'width': '50px', 'borderColor': COLORS['accent'], 'borderWidth': '3px', 'margin': '10px auto'}),
    ], style={'marginBottom': '30px'}),

    # SUMMARY STATS ROW
    html.Div(id='stats-container', style={'display': 'flex', 'justifyContent': 'space-around', 'marginBottom': '25px', 'gap': '20px'}, children=[
        # Stats will be populated by callback based on dropdown/slider selection
    ]),

    # MIDDLE ROW: Controls & Pie Chart
    html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '20px', 'justifyContent': 'center'}, children=[
        
        # Control Panel Card
        html.Div(style={'flex': '1', 'minWidth': '300px', 'backgroundColor': COLORS['card_bg'], 'padding': '25px', 'borderRadius': '12px', 'boxShadow': '0 4px 15px rgba(0,0,0,0.05)'}, children=[
            html.Label("1. Select Launch Site:", style={'fontWeight': 'bold', 'color': COLORS['accent']}),
            dcc.Dropdown(
                id='site-dropdown',
                options=[{'label': 'All Sites', 'value': 'ALL'}] +
                        [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                value='ALL',
                placeholder='Select a Launch Site here',
                searchable=True,
                style={'marginTop': '10px'}
            ),
            html.Div(style={'marginTop': '50px'}, children=[
                html.Label("2. Filter by Payload (Kg):", style={'fontWeight': 'bold', 'color': COLORS['accent']}),
                dcc.RangeSlider(
                    id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={0: '0', 5000: '5000', 10000: '10000'},
                    value=[min_payload, max_payload]
                ),
            ])
        ]),

        # Pie Chart Card
        html.Div(style={'flex': '1.5', 'minWidth': '450px', 'backgroundColor': COLORS['card_bg'], 'padding': '15px', 'borderRadius': '12px', 'boxShadow': '0 4px 15px rgba(0,0,0,0.05)'}, children=[
            dcc.Graph(id='success-pie-chart')
        ]),
    ]),

    # BOTTOM ROW: Scatter Plot
    html.Div(style={'marginTop': '25px', 'backgroundColor': COLORS['card_bg'], 'padding': '20px', 'borderRadius': '12px', 'boxShadow': '0 4px 15px rgba(0,0,0,0.05)'}, children=[
        dcc.Graph(id='success-payload-scatter-chart')
    ])
])

# CALLBACK 1: Dynamic Summary Stats
@app.callback(
    Output('stats-container', 'children'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_stats(site, payload):
    low, high = payload
    df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
    if site != 'ALL':
        df = df[df['Launch Site'] == site]
    
    total_launches = len(df)
    successes = df['class'].sum()
    rate = (successes / total_launches * 100) if total_launches > 0 else 0
    avg_payload = df['Payload Mass (kg)'].mean() if total_launches > 0 else 0

    stats_cards = [
        ("TOTAL LAUNCHES", f"{total_launches}"),
        ("SUCCESS RATE", f"{rate:.1f}%"),
        ("AVG PAYLOAD", f"{avg_payload:,.0f} kg")
    ]

    return [
        html.Div(style={'flex': '1', 'backgroundColor': COLORS['card_bg'], 'padding': '20px', 'borderRadius': '12px', 'textAlign': 'center', 'boxShadow': '0 4px 15px rgba(0,0,0,0.05)'}, children=[
            html.H3(val, style={'color': COLORS['accent'], 'margin': '0', 'fontSize': '28px'}),
            html.P(label, style={'color': '#888', 'margin': '5px 0 0 0', 'fontSize': '12px', 'fontWeight': 'bold'})
        ]) for label, val in stats_cards
    ]

# CALLBACK 2: Pie Chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def get_pie_chart(entered_site, payload):
    low, high = payload
    df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
    
    if entered_site == 'ALL':
        df_all = df.groupby('Launch Site', as_index=False)['class'].sum()
        fig = px.pie(df_all, values='class', names='Launch Site', 
                     title='Distribution of Successful Launches',
                     hole=.4, color_discrete_sequence=px.colors.qualitative.Bold)
    else:
        df_site = df[df['Launch Site'] == entered_site]
        outcome_counts = df_site['class'].value_counts().reset_index()
        outcome_counts.columns = ['class', 'count']
        outcome_counts['Outcome'] = outcome_counts['class'].map({1: 'Success', 0: 'Failure'})
        fig = px.pie(outcome_counts, values='count', names='Outcome', 
                     title=f'Success Rate: {entered_site}',
                     hole=.4, color_discrete_map={'Success': '#28a745', 'Failure': '#dc3545'})
    
    fig.update_layout(margin=dict(t=50, b=20, l=20, r=20), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    return fig

# CALLBACK 3: Scatter Plot
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter(selected_site, payload_range):
    low, high = payload_range
    df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
    
    if selected_site != 'ALL':
        df = df[df['Launch Site'] == selected_site]
        title = f'Payload vs. Outcome for {selected_site}'
    else:
        title = 'Payload vs. Outcome for All Sites'

    fig = px.scatter(df, x='Payload Mass (kg)', y='class', 
                     color='Booster Version Category', 
                     hover_data=['Launch Site'], title=title,
                     category_orders={"class": [0, 1]})
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='#f0f0f0', title='Payload Mass (kg)'),
        yaxis=dict(gridcolor='#f0f0f0', title='Outcome (0=Fail, 1=Success)', tickmode='array', tickvals=[0, 1]),
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
