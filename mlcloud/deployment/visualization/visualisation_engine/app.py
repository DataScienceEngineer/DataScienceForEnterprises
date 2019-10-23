from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import importlib
from app_config import app
import json
from flask import request
from threading import Lock
import os

DATA_FILENAME=str(os.getcwd())+'/static/root.json'
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    html.Div(dash_table.DataTable(), style={'display': 'none'})
])

error_page = html.Div([
    html.H2('404 Error', style={'text-align': 'center'}),
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    print(DATA_FILENAME)
    with open(DATA_FILENAME) as f:
        data = json.load(f)
        for node in data:
            if 'a_attr' not in node.keys() and 'href' not in node.keys():
                continue
            node_attr=node['a_attr']['href']
            if pathname==node_attr:
                node_attr=node_attr.replace("/",".")
                module = importlib.import_module(node_attr[1:])
                return module.layout
        return error_page

@app.server.route('/html/<path:path>')
def static_file(path):
    return app.server.send_static_file(path)

@app.server.route('/createNode/', methods=['POST'])
def createNode():
    newNode=request.json
    with Lock():
        with open(DATA_FILENAME, 'r') as json_data:
            data = json.load(json_data)
        data.append(newNode)
        with open(DATA_FILENAME, 'w') as json_data:
            json.dump(data, json_data)
    return json.dumps({'status': 'OK', 'newNode': newNode})
    #nodeText =  request.args['nodeText'];
    #nodeAddress = request.args['nodeAddress'];
    #return json.dumps({'status':'OK','nodeText':nodeText,'nodeAddress':nodeAddress});

@app.server.route('/deleteNode/', methods=['GET'])
def deleteNode():
    nodeDelete=request.args['deleteNode']
    with Lock():
        with open(DATA_FILENAME, 'r') as json_data:
            data = json.load(json_data)
        for entry in data:
            if nodeDelete==entry['id']:
                data.remove(entry)
        with open(DATA_FILENAME, 'w') as json_data:
            json.dump(data, json_data)
    return json.dumps({'status': 'OK', 'DeleteNode': nodeDelete})

@app.server.route('/editNode/', methods=['POST'])
def editNode():
    editNode=request.json
    with Lock():
        with open(DATA_FILENAME, 'r') as json_data:
            data = json.load(json_data)

        for entry in data:
            if editNode['id']==entry['id']:
                data.remove(entry)
                data.append(editNode)

        with open(DATA_FILENAME, 'w') as json_data:
            json.dump(data, json_data)
    return json.dumps({'status': 'OK', 'editNode': editNode})

if __name__ == '__main__':
    app.run_server(port=8050,host="0.0.0.0",debug=True)