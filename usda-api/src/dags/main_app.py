from main_ml import MachineLearning
from main_weather import WeatherAnalysis
from dash import Dash, Input, Output,State, dcc, no_update, html

class App:
    def __init__(self):
        self.app = Dash(__name__)
        self.setup_app_layout()
        self.setup_callbacks()
        
    def setup_app_layout(self):
        self.app.layout = html.Div([
            html.Div([
                html.H1('Weather Analysis Report'),
                dcc.Tabs(id='tabs0', value = 'tab0-1', children= [
                    dcc.Tab(label='Precipitation Analysis', value='tab0-1'),
                    dcc.Tab(label= 'Temperature Analysis', value = 'tab0-2')
                ]),
                html.Div(id='tabs0-content')
            ]),
            html.Div([
                html.H1('Machine Learning with LSTM'),
                dcc.Tabs(id="tabs", value='tab-1', children=[
                    dcc.Tab(label='Analyze Corn Chart', value='tab-1'),
                    dcc.Tab(label='Training LSTM', value='tab-2'),
                    dcc.Tab(label='Forecasting LSTM', value='tab-3'),
                ]),
                html.Div(id='tabs-content'),
            ]),
        ])
        
        
    def setup_callbacks(self):
        @self.app.callback(
            Output('tabs0-content', 'children'),
            Input('tabs0', 'value')
         )
        def render_content_zero(tab):
            if tab == 'tab0-1':
                fig = WeatherAnalysis('./Weather_quote/weather_quote.csv').create_precipitation_plot()
                return  dcc.Graph(figure = fig)

            else:
                fig = WeatherAnalysis('./Weather_quote/weather_quote.csv').create_temperature_plot()
                return dcc.Graph(figure = fig)


        
        @self.app.callback(
            Output('tabs-content', 'children'),
            Input('tabs', 'value')
        )
        def render_content(tab):
            if tab == 'tab-1':
                return html.Div([
                    html.Label('Period:'),
                    dcc.RadioItems(
                        id='toggle-rangeslider',
                        options=[{ 'label': "All time", 'value': "All" },
                                { 'label': "5y", 'value': "5y" },
                                { 'label': "1y", 'value': "1y" },
                                { 'label': "6m", 'value': "6m" },
                                { 'label': "1m", 'value': "1m" },
                                { 'label': "last 5 prices", 'value': "5 days" },],
                        value = "All",
                        inline=True                  
                    ),
                    dcc.Graph(id='corn-chart')
                ])
                
            elif tab == 'tab-2':
                return html.Div([
                    html.Label('Optimizer:'),
                    dcc.RadioItems(
                        id='toggle-optimizer',
                        options=[
                            {'label' : 'SGD', 'value': 'SGD'},
                            {'label' : 'Adam', 'value': 'Adam'}
                        ],
                        value = 'SGD',
                        inline=True
                    ),
                    html.Label('Epoch:'),
                    html.Div(
                    dcc.Slider(
                        id = 'toggle-epoch',
                        min=0, max=50, step=5, value = 1,
                        marks={
                            0:'default weights',
                            5: '5 epochs',
                            10: '10 epochs',
                            15: '15 epochs',
                            20: '20 epochs',
                            25: '25 epochs',
                            30: '30 epochs',
                            35: '35 epochs',
                            40: '40 epochs',
                            45: '45 epochs',
                            50: '50 epochs',
                        }),
                        style= {
                            'width' :'80%',
                            'margin' : '1%'}),
                    
                    html.Button('Train', id = 'train',style={
                                'background-color': '#007bff',
                                'color': 'white',
                                'border': 'none',
                                'border-radius': '5px',
                                'padding': '5px 10px',
                                'text-align': 'center',
                                'text-decoration': 'none',
                                'display': 'inline-block',
                                'font-size': '16px',
                                'margin': '4px 2px',
                                'cursor': 'pointer',
                            }),
                    
                    dcc.Graph(id='eval-chart'),
                    
                ])
            else:
                return html.Div([
                        html.Label('Forecast Number of Days:'),
                        dcc.Slider(
                            id = 'toggle-days',
                            min = 0, max =30, value = 0, step = 1,
                            marks={
                                0:'0', 5:'5', 10:'10', 15: '15', 20: '20', 25:'25', 30:'30 days'
                            }
                        ),
                        html.Label('Weights:'),
                        dcc.RadioItems(
                            id = 'toggle-weights',
                            options = [
                                {'label' : 'Default weights', 'value' : True},
                                {'label' : 'Train weights', 'value': False}
                            ],
                            value= False,
                            inline = True,
                        ),
                        html.Button('Forecast', id = 'forecast',style={
                                'background-color': '#007bff',
                                'color': 'white',
                                'border': 'none',
                                'border-radius': '5px',
                                'padding': '5px 10px',
                                'text-align': 'center',
                                'text-decoration': 'none',
                                'display': 'inline-block',
                                'font-size': '16px',
                                'margin': '4px 2px',
                                'cursor': 'pointer',
                                }),
                        
                        dcc.Graph(id='forecast-chart'),
                    ])
        
        @self.app.callback(
            Output('corn-chart', 'figure'),
            Input("toggle-rangeslider", "value"),
        )
        def display_corn_chart(value):
            fig = MachineLearning('./Corn_quote/corn_quote.csv').analyze_stock_prices(value)
            return fig
        @self.app.callback(
            Output('eval-chart', 'figure'),
            Input('train', 'n_clicks'),
            [State('toggle-epoch', 'value'),
            State('toggle-optimizer', 'value')]
        )
        def evaluate(n_clicks, num_epoch, optimizer):
            if n_clicks is None:
                return no_update
            else :
                fig = MachineLearning('./Corn_quote/corn_quote.csv').train_model(num_epoch, optimizer)
            return fig
    
        @self.app.callback(
            Output('forecast-chart', 'figure'),
            Input('forecast', 'n_clicks'),
            [State('toggle-days', 'value'),
             State('toggle-weights', 'value')]
        )
        def forecast(n_clicks, days, weight):
            if n_clicks is None:
                return no_update
            else:
                fig = MachineLearning('./Corn_quote/corn_quote.csv').forecast_stock_prices(days, weight)
                return fig
        
    def run(self, debug = False):
        self.app.run_server(debug = debug)
    
    


if __name__ == '__main__':
    app = App()
    app.run(debug = True)