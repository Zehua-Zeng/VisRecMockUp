from flask import Flask, render_template, request, jsonify, send_from_directory, current_app
import os
import json

## dziban
from dziban.mkiv import Chart
from vega_datasets import data
from vega import VegaLite
import pandas as pd

df = pd.read_json('./web/static/data/movies.json')
base = Chart(df)
all_fields = base.get_fields()

read_vlsf = open('vegalite_selected_fields.json', 'r')
vlsf = json.load(read_vlsf)

read_bfs = open('temp_results_v2.json', 'r')
breadth_first_result = json.load(read_bfs)

read_dfs_last = open('temp_results_v3.json', 'r')
depth_first_last_node_result = json.load(read_dfs_last)

## flask
app = Flask(__name__, static_folder='web/static',
            template_folder='web/templates')

# render index at route /
@app.route('/')
def index():
    return render_template("index.html")

# NoRec at route /v1
@app.route('/v1')
def v1():
    return render_template("v1.html")

# Breadth-first at route /v2
@app.route('/v2')
def v2():
    return render_template("v2.html")

# Depth-first-last-node at route /v3
@app.route('/v3')
def v3():
    return render_template("v3.html")

@app.route('/test')
def test():
    return render_template('test.html')

# send static files from directory (data)
@app.route('/data/<path:filename>')
def send_data(filename):
    return send_from_directory('web/static/data', filename)

@app.route('/js/<path:filename>')
def send_js(filename):
    return send_from_directory('web/static/js', filename)

# send static files from directory (css)
@app.route('/css/<path:filename>')
def send_css(filename):
    return send_from_directory('web/static/css', filename)

@app.route('/js2pyFieldsv1', methods=['POST'])
def js2pyFieldsv1():
    receivedData = json.loads(request.form.get('data'))
    fields = receivedData["fields"]
    fields.sort()
    fields_str = "+".join(fields)
    vegaliteDictFinal = {}
    if not vlsf[fields_str]:
        return jsonify(status="empty", actualVegaLite=vegaliteDictFinal)
    vlstr = vl2vlStr(vlsf[fields_str])
    vegaliteDictFinal[vlstr] = vlsf[fields_str]
    return jsonify(status="success", actualVegaLite=vegaliteDictFinal)

@app.route('/js2pyFieldsv2', methods=['POST'])
def js2pyFieldsv2():
    receivedData = json.loads(request.form.get('data'))
    fields = receivedData["fields"]
    # print (fields)
    vegaliteDict = {}
    if len(fields) == 1:
        chart = base.field(fields[0])
        vegaliteDict = chart._get_vegalite()
    if len(fields) == 2:
        chart = base.field(fields[0], fields[1])
        vegaliteDict = chart._get_vegalite()
    if len(fields) == 3:
        chart = base.field(fields[0], fields[1], fields[2])
        vegaliteDict = chart._get_vegalite()
    vegaliteStr = json.dumps(vegaliteDict)
    vegaliteStr = vegaliteStr.replace('cars', 'movies')
    vegaliteStr = vegaliteStr.replace(', "scale": {"zero": true}', '')
    vegaliteDictFinal = json.loads(vegaliteStr)
    fields.sort()
    fieldStr = "+".join(fields)
    try:
        vegaliteUnordered = breadth_first_result[fieldStr]
    except:
        return jsonify(status="success", actualVegaLite=vegaliteDictFinal, recVegaLite="")
    vegaliteRanked = sorted(vegaliteUnordered, key=vegaliteUnordered.get)
    vegaliteRankedFinal = []
    for vgl in vegaliteRanked:
        if '"row":' in vgl:
            continue
        vgl = vgl.replace('cars', 'movies')
        vgl = vgl.replace(', "scale": {"zero": true}', '')
        vegaliteRankedFinal.append(json.loads(vgl))
    return jsonify(status="success", actualVegaLite=vegaliteDictFinal, recVegaLite=vegaliteRankedFinal)

@app.route('/js2pyFieldsv3', methods=['POST'])
def js2pyFieldsv3():
    receivedData = json.loads(request.form.get('data'))
    fields = receivedData["fields"]
    # print (fields)
    vegaliteDict = {}
    if len(fields) == 1:
        chart = base.field(fields[0])
        vegaliteDict = chart._get_vegalite()
    if len(fields) == 2:
        chart = base.field(fields[0], fields[1])
        vegaliteDict = chart._get_vegalite()
    if len(fields) == 3:
        chart = base.field(fields[0], fields[1], fields[2])
        vegaliteDict = chart._get_vegalite()
    vegaliteStr = json.dumps(vegaliteDict)
    vegaliteStr = vegaliteStr.replace('cars', 'movies')
    vegaliteStr = vegaliteStr.replace(', "scale": {"zero": true}', '')
    vegaliteDictFinal = json.loads(vegaliteStr)
    fields.sort()
    fieldStr = "+".join(fields)
    try:
        vegaliteUnordered = depth_first_last_node_result[fieldStr]
    except:
        return jsonify(status="success", actualVegaLite=vegaliteDictFinal, recVegaLite="")
    vegaliteRanked = sorted(vegaliteUnordered, key=vegaliteUnordered.get)
    vegaliteRankedFinal = []
    for vgl in vegaliteRanked:
        if '"row":' in vgl:
            continue
        vgl = vgl.replace('cars', 'movies')
        vgl = vgl.replace(', "scale": {"zero": true}', '')
        vegaliteRankedFinal.append(json.loads(vgl))
    return jsonify(status="success", actualVegaLite=vegaliteDictFinal, recVegaLite=vegaliteRankedFinal)

def vl2vlStr(chart_vegalite):
    vegalite_str = ""
    vegalite_str += "mark:" + chart_vegalite["mark"] + ';'
    encoding_arr = []
    for encoding in chart_vegalite["encoding"]:
        if encoding == "undefined":
            continue
        encoding_str = ""
        if "field" in chart_vegalite["encoding"][encoding]:
            encoding_str += chart_vegalite["encoding"][encoding]["field"] + "-"
        else:
            encoding_str += "-"
        encoding_str += chart_vegalite["encoding"][encoding]["type"] + "-"
        encoding_str += encoding
        if "aggregate" in chart_vegalite["encoding"][encoding]:
            encoding_str += "<" + "aggregate" + ">" + chart_vegalite["encoding"][encoding]["aggregate"]
        if "bin" in chart_vegalite["encoding"][encoding]:
            encoding_str += "<" + "bin" + ">"
        
        encoding_arr.append(encoding_str)
    
    encoding_arr.sort()
    vegalite_str += "encoding:" + ",".join(encoding_arr)

    return vegalite_str



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)