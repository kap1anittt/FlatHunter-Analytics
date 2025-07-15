import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor

# Загрузка модели и данных
model = pickle.load(open('model.pkl', 'rb'))  # Ваша сохраненная модель
df = pd.read_csv('data.csv')  # Ваши данные

# Инициализация Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Анализ цен на недвижимость", style={'textAlign': 'center'}),
    
    # Блок ввода параметров
    html.Div([
        html.H3("Параметры объекта"),
        html.Label("Тип автора:"),
        dcc.Dropdown(
            id='author_type',
            options=[{'label': i, 'value': i} for i in df['author_type'].unique()],
            value='realtor_based'
        ),
        
        html.Label("Локация:"),
        dcc.Dropdown(
            id='location',
            options=[{'label': i, 'value': i} for i in df['location'].unique()],
            value='Москва'
        ),
        
        html.Label("Тип сделки:"),
        dcc.Dropdown(
            id='deal_type',
            options=[{'label': i, 'value': i} for i in df['deal_type'].unique()],
            value='rent_long'
        ),
        
        html.Label("Площадь (м²):"),
        dcc.Input(id='living_meters', type='number', value=60.1),
        
        html.Button('Рассчитать', id='submit-val', n_clicks=0)
    ], style={'padding': 20, 'flex': 1}),
    
    # Блок результатов
    html.Div([
        html.H3("Результаты прогноза"),
        html.Div(id='prediction-output'),
        dcc.Graph(id='price-distribution'),
        dcc.Graph(id='feature-importance')
    ], style={'padding': 20, 'flex': 2})
], style={'display': 'flex', 'flexDirection': 'row'})

# Callback для прогноза
@app.callback(
    [Output('prediction-output', 'children'),
     Output('price-distribution', 'figure'),
     Output('feature-importance', 'figure')],
    [Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('author_type', 'value'),
     dash.dependencies.State('location', 'value'),
     dash.dependencies.State('deal_type', 'value'),
     dash.dependencies.State('living_meters', 'value')]
)
def update_output(n_clicks, author_type, location, deal_type, living_meters):
    # Создаем DataFrame для предсказания
    input_data = pd.DataFrame({
        'author_type': [author_type],
        'location': [location],
        'deal_type': [deal_type],
        'living_meters': [living_meters],
        # Добавьте остальные параметры по аналогии
    })
    
    # Делаем предсказание
    prediction = model.predict(input_data)[0]
    
    # График распределения цен
    hist_fig = px.histogram(df, x='price_per_m2', nbins=50, 
                           title='Распределение цен за м²')
    
    # График важности признаков
    importance_fig = px.bar(
        x=model.named_steps['regressor'].feature_importances_,
        y=model.feature_names_in_,
        orientation='h',
        title='Важность признаков'
    )
    
    return [
        html.Div([
            html.H4(f"Предсказанная цена: {prediction:.2f} руб/м²"),
            html.P(f"Параметры: {living_meters}м², {location}, {deal_type}")
        ]),
        hist_fig,
        importance_fig
    ]

if __name__ == '__main__':
    app.run_server(debug=True)