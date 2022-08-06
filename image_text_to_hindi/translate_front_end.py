# pip install --upgrade --user pyqt5 pyqt5-tools
# from PyQt5 import QtWidgets
# class Widget(QtWidgets):
#     def __init__(self):
#         pass
    
from translate import convert

try:
    import dash
except:
    import os, sys, subprocess
    subprocess.call(f'{sys.executable} -m pip install dash==1.12')
    os.system(f'{sys.executable} {__file__}')

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import socket

external_stylesheets = []
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.title = 'Translate'

app.layout = html.Div([
    html.Header([
        html.P('Translate English to Hindi', style={'width':'100%', 'display':'block', 'text-align':'center', 'font-weight':'bold', 'font-size':'1.5em'}), 
        html.Div(id='internet_check', style={'width': '100%', 'display': 'block', 'text-align': 'center', 'font-weight': 'bold', }), 
        html.Br()
    ], style={'width':'100%','display':'block','text-align':'center'}),
    html.Div([
        html.Label('Text to translate', style={'width': '10%', 'display': 'inline-table'}),
        dcc.Input(id='input_text', style={
            'width': '88%', 
            'display': 'inline-table', 
            'border-radius': '5px',
            'border': '2px solid #C0C0C0',
            'color': '#000000',
            'resize': 'vertical',
            'overflow': 'auto',
            }),
    ], id='input_div', style={}), html.Br(), html.Br(), html.Br(), 
    html.Div([
        html.Label('Hindi', style={'width': '10%', 'display': 'inline-table'}),
        html.Label(id='output_text_hindi', style={
            'width': '88%', 
            'display': 'inline-table',
            'border': '2px solid #C0C0C0',
            'border-radius': '7px solid #C0C0C0',
        }),
        html.Br(),
        html.Label('Possible Mistakes', style={'width': '10%', 'display': 'inline-table'}),
        html.Label(id='output_mistakes_hindi', style={
            'width': '88%', 
            'display': 'inline-table', 
            'border': '2px solid #C0C0C0', 
            'border-radius': '7px solid #C0C0C0',
        }),
        html.Br(),
        html.Label('Possible Translations', style={'width': '10%', 'display': 'inline-table'}),
        html.Label(id='output_tranlations_hindi', style={
            'width': '88%', 
            'display': 'inline-table', 
            'border': '2px solid #C0C0C0', 
            'border-radius': '7px solid #C0C0C0',
        }),
    ], id='hindi_div', style={'width': '100%', 'display': 'block', 'visibility': 'hidden'}), html.Br(),
    # html.Div([
    #     html.Label('Marathi', style={'width': '10%', 'display': 'inline-table'}),
    #     html.Label(id='output_text_marathi', style={
    #         'width': '88%', 
    #         'display': 'inline-table',
    #         'border': '2px solid #C0C0C0',
    #         'border-radius': '7px solid #C0C0C0',
    #     }),
    #     html.Br(),
    #     html.Label('Possible Mistakes', style={'width': '10%', 'display': 'inline-table'}),
    #     html.Label(id='output_mistakes_marathi', style={
    #         'width': '88%', 
    #         'display': 'inline-table', 
    #         'border': '2px solid #C0C0C0', 
    #         'border-radius': '7px solid #C0C0C0',
    #     }),
    #     html.Br(),
    #     html.Label('Possible Translations', style={'width': '10%', 'display': 'inline-table'}),
    #     html.Label(id='output_tranlations_marathi', style={
    #         'width': '88%', 
    #         'display': 'inline-table', 
    #         'border': '2px solid #C0C0C0', 
    #         'border-radius': '7px solid #C0C0C0',
    #     }),
    # ], id='marathi_div', style={'width': '100%', 'display': 'block', 'visibility': 'hidden'}), html.Br(),
    html.Div([
        html.Label('Original Text', style={'width': '10%', 'display': 'inline-table'}),
        html.Label(id='output_text_english', style={
            'width': '88%',
            'display': 'inline-table',
            'border': '2px solid #C0C0C0',
            'border-radius': '7px solid #C0C0C0',
        })
    ], id='original_text_div', style={'width': '100%', 'display': 'block', 'visibility': 'hidden'}),
], style={})

@app.callback(Output('output_text_hindi', 'children'), [Input('input_text', 'value'),])
def hindi(input_text):
    try:
        return convert(input_text)['hindi']['text'] if input_text != '' or input_text != None else ''
    except:
        pass
    
@app.callback(Output('output_mistakes_hindi', 'children'), [Input('input_text', 'value'),])
def hindi(input_text):
    try:
        return convert(input_text)['hindi']['possible_mistakes'] if input_text != '' or input_text != None else ''
    except:
        pass
    
@app.callback(Output('output_tranlations_hindi', 'children'), [Input('input_text', 'value'),])
def hindi(input_text):
    try:
        return convert(input_text)['hindi']['possible_translations'] if input_text != '' or input_text != None else ''
    except:
        pass
    
@app.callback(Output('hindi_div', 'style'), [Input('input_text', 'value'), ])
def hindi(input_text):
    if input_text == '' or socket.gethostbyname(socket.gethostname()) == '127.0.0.1' or input_text == None:
        return {'width': '100%', 'display': 'block', 'visibility': 'hidden'}
    else:
        return {'width': '100%', 'display': 'block'}

# @app.callback(Output('output_text_marathi', 'children'), [Input('input_text', 'value'), ])
# def marathi(input_text):
#     try:
#         return convert(input_text)['marathi']['text'] if input_text != '' or input_text != None else ''
#     except:
#         pass

# @app.callback(Output('output_mistakes_marathi', 'children'), [Input('input_text', 'value'),])
# def hindi(input_text):
#     try:
#         return convert(input_text)['marathi']['possible_mistakes'] if input_text != '' or input_text != None else ''
#     except:
#         pass
    
# @app.callback(Output('output_tranlations_marathi', 'children'), [Input('input_text', 'value'),])
# def hindi(input_text):
#     try:
#         return convert(input_text)['marathi']['possible_translations'] if input_text != '' or input_text != None else ''
#     except:
#         pass

# @app.callback(Output('marathi_div', 'style'), [Input('input_text', 'value'), ])
# def marathi(input_text):
#     if input_text == '' or socket.gethostbyname(socket.gethostname()) == '127.0.0.1' or input_text == None:
#         return {'width': '100%', 'display': 'block', 'visibility': 'hidden'}
#     else:
#         return {'width': '100%', 'display': 'block'}

@app.callback(Output('output_text_english', 'children'), [Input('input_text', 'value')])
def english(input_text):
    return input_text

@app.callback(Output('original_text_div', 'style'), [Input('input_text', 'value'), ])
def english(input_text):
    if input_text == '' or socket.gethostbyname(socket.gethostname()) == '127.0.0.1' or input_text == None:
        return {'width': '100%', 'display': 'block', 'visibility': 'hidden'}
    else:
        return {'width': '100%', 'display': 'block'}

@app.callback(Output('internet_check', 'children'), [Input('input_text', 'value'), ])
def check_internet(input_text):
    if socket.gethostbyname(socket.gethostname()) == '127.0.0.1':
        return 'No Internet Connection'
    else:
        return 'Internet Connection available'

@app.callback(Output('internet_check', 'style'), [Input('input_text', 'value'), ])
def check_internet(input_text):
    if socket.gethostbyname(socket.gethostname()) == '127.0.0.1':
        return {'width': '100%', 'display': 'block', 
                'text-align': 'center', 'font-weight': 'bold', 'color': 'red'}
    else:
        return {'width': '100%', 'display': 'block', 
                'text-align': 'center', 'font-weight': 'bold', 'color': 'green'}

if __name__ == '__main__':
    app.run_server(debug=True)