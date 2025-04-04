import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Chargement des données
df = pd.read_csv("supermarket_sales.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Week"] = df["Date"].dt.isocalendar().week

# Initialiser l'app Dash
app = dash.Dash(__name__)
server = app.server

# Nouvelle police
font_family = 'Poppins, sans-serif'

# Style des cartes
card_style = {
    'boxShadow': '0 4px 12px rgba(0,0,0,0.1)',
    'padding': '30px',
    'borderRadius': '15px',
    'backgroundColor': '#ffffffcc',
    'backdropFilter': 'blur(10px)',
    'margin': '10px',
    'flex': '1',
    'textAlign': 'center',
    'display': 'flex',
    'flexDirection': 'column',
    'justifyContent': 'center',
    'fontFamily': font_family
}

# Mise en page
app.layout = html.Div(style={
    'fontFamily': font_family,
    'background': 'linear-gradient(to right, #001f3f, #0074D9)',
    'minHeight': '100vh',
    'padding': '0',
    'margin': '0'
}, children=[

    html.Div([
        html.H1("Analyse des ventes d’un supermarché", style={
            'textAlign': 'center',
            'color': 'white',
            'padding': '30px 0',
            'fontWeight': 'bold',
            'fontSize': '38px',
            'fontFamily': font_family
        })
    ]),

    html.Div([
        html.Div([
            html.Label("Sexe :", style={'color': 'white', 'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='sex-filter',
                options=[
                    {'label': 'Homme', 'value': 'Male'},
                    {'label': 'Femme', 'value': 'Female'},
                    {'label': 'Les deux', 'value': 'All'}
                ],
                value='All',
                clearable=False,
                style={'color': 'black'}
            ),
            html.Label("Ville :", style={'marginTop': '10px', 'color': 'white', 'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='city-filter',
                options=[{'label': 'Toutes les villes', 'value': 'All'}] +
                        [{'label': c, 'value': c} for c in df['City'].unique()],
                value='All',
                clearable=False,
                style={'color': 'black'}
            )
        ], style={
            'width': '20%',
            'padding': '20px',
            'borderRadius': '15px',
            'backgroundColor': '#004080cc',
            'margin': '20px'
        }),

        html.Div(id='indicators', style={
            'display': 'flex',
            'flexDirection': 'row',
            'justifyContent': 'center',
            'alignItems': 'center',
            'width': '75%',
            'margin': '20px'
        })
    ], style={
        'display': 'flex',
        'justifyContent': 'space-between'
    }),

    html.Div([
        html.Div([dcc.Graph(id='histogram-total')], style=card_style),
        html.Div([dcc.Graph(id='bar-total-invoice')], style=card_style),
        html.Div([dcc.Graph(id='pie-product-line')], style=card_style),
    ], style={
        'display': 'flex',
        'flexDirection': 'row',
        'justifyContent': 'space-between',
        'padding': '20px'
    })
])

@app.callback(
    [Output('indicators', 'children'),
     Output('histogram-total', 'figure'),
     Output('bar-total-invoice', 'figure'),
     Output('pie-product-line', 'figure')],
    [Input('sex-filter', 'value'),
     Input('city-filter', 'value')]
)
def update_dashboard(selected_sex, selected_city):
    dff = df.copy()
    if selected_sex != 'All':
        dff = dff[dff['Gender'] == selected_sex]
    if selected_city != 'All':
        dff = dff[dff['City'] == selected_city]

    total_amount = dff['Total'].sum()
    total_invoices = dff['Invoice ID'].nunique()

    indicators = [
        html.Div([
            html.H3("Total Achats", style={'color': '#003366', 'fontSize': '24px'}),
            html.H2(f"{total_amount:.2f} $", style={'fontSize': '30px', 'color': '#001f3f'})
        ], style=card_style),

        html.Div([
            html.H3("Nombre Achats", style={'color': '#003366', 'fontSize': '24px'}),
            html.H2(f"{total_invoices}", style={'fontSize': '30px', 'color': '#001f3f'})
        ], style=card_style),
    ]

    fig1 = px.histogram(dff, x='Total')
    fig1.update_traces(marker_color='#004080')
    fig1.update_layout(
        title='Répartition des montants',
        xaxis_title="Montant total de l'achat (en $)",
        yaxis_title="Nombre d'achats",
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family=font_family, color='#333'),
        title_font=dict(size=20)
        
    )

    fig2 = px.bar(
    dff.groupby(['Gender', 'City'])['Invoice ID'].count().reset_index(),
    x='Gender',
    y='Invoice ID',
    color='City',
    barmode='group',
    labels={'Invoice ID': 'Nombre d\'achats', 'Gender': 'Sexe', 'City': 'Ville'},
    color_discrete_sequence=['#003f5c', '#0074D9', '#6699cc']  # Nuances de bleu
    )

    fig2.update_layout(
    title='Nombre total d\'achats par sexe et par ville',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family=font_family, color='#333'),
    title_font=dict(size=20)
    )   



    fig3 = px.pie(dff, names='Product line', color_discrete_sequence=[
        '#0074D9', '#005288', '#003f5c', '#0066cc', '#6699cc', '#99c2e6'
    ])
    fig3.update_layout(
        title='Répartition des produits',
        font=dict(family=font_family, color='#333'),
        title_font=dict(size=20)
    )

    return indicators, fig1, fig2, fig3

if __name__ == '__main__':
    app.run_server(debug=True)
