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

# read_f2vlstr = open('fields2vegaliteStr.json', 'r')
# f2vlstr = json.load(read_f2vlstr)

read_bsf_results = open('combine_bfs_result.json', 'r')
bsf_results = json.load(read_bsf_results)

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
@app.route('/NoRecommendations')
def v1():
    return render_template("v1.html")

# Breadth-first at route /v2
@app.route('/BreadthFirst')
def v2():
    return render_template("v2.html")

# Depth-first-last-node at route /v3
@app.route('/DepthFirstLastNode')
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

# communication with front end:
@app.route('/js2pyFieldsV1', methods=['POST'])
def js2pyFieldsV1():
    receivedData = json.loads(request.form.get('data'))
    fields = receivedData["fields"]
    fields.sort()
    fields_str = "+".join(fields)
    vegaliteDictFinal = {}
    if not vlsf[fields_str]:
        return jsonify(status="empty", actualVegalite=vegaliteDictFinal)
    vlstr = get_vlStr_from_vl(vlsf[fields_str])
    vegaliteDictFinal[vlstr] = vlsf[fields_str]
    return jsonify(status="success", actualVegalite=vegaliteDictFinal)

@app.route('/js2pyFieldsV2', methods=['POST'])
def js2pyFieldsV2():
    receivedData = json.loads(request.form.get('data'))
    fields = receivedData["fields"]
    fields.sort()
    fields_str = "+".join(fields)
    vegaliteDictFinal = {}
    if not vlsf[fields_str]:
        return jsonify(status="empty", actualVegalite=vegaliteDictFinal, recVegalite="")
    vlstr = get_vlStr_from_vl(vlsf[fields_str])
    vegaliteDictFinal[vlstr] = vlsf[fields_str]

    # get recomendation:
    bfs_vl = bsf_results[vlstr]
    # print (bfs_vl)
    bfsRanked = sorted(bfs_vl, key=bfs_vl.get)
    # print (bfsRanked)
    bfsRankedFinal = []
    for vgl in bfsRanked:
        temp = {}
        vljson = json.loads(vgl)
        vglstr = get_vlStr_from_vl(vljson)
        temp[vglstr] = vljson
        bfsRankedFinal.append(temp)
    return jsonify(status="success", actualVegalite=vegaliteDictFinal, recVegalite=bfsRankedFinal)

@app.route('/js2pySpecV2', methods=['POST'])
def js2pySpecV2():
    receivedData = json.loads(request.form.get('data'))
    vl = receivedData["vljson"]
    # vl = json.loads(vljson_str)
    vlstr = get_vlStr_from_vl(vl)
    fields = get_fields_from_vlstr(vlstr)
    fields_str = "+".join(fields)

    new_vlstr = get_vlStr_from_vl(vlsf[fields_str])

    # get recomendation:
    bfs_vl = bsf_results[new_vlstr]
    # print (bfs_vl)
    bfsRanked = sorted(bfs_vl, key=bfs_vl.get)
    # print (bfsRanked)
    bfsRankedFinal = []
    for vgl in bfsRanked:
        temp = {}
        vljson = json.loads(vgl)
        vglstr = get_vlStr_from_vl(vljson)
        temp[vglstr] = vljson
        bfsRankedFinal.append(temp)

    return jsonify(status="success", recVegalite=bfsRankedFinal)

@app.route('/js2pyFieldsV3', methods=['POST'])
def js2pyFieldsV3():
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


# helper methods:
def get_vlStr_from_vl(chart_vegalite):
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


def get_vl_from_vlStr(vegalite_str):
    vegalite_json = {}
    vegalite_json["$schema"] = "https://vega.github.io/schema/vega-lite/v3.json"
    vegalite_json["data"] = {"url": "data/movies.json"}
    mark = vegalite_str.split(';')[0]
    encoding = vegalite_str.split(';')[1]
    vegalite_json["mark"] = mark.split(':')[1]
    encodings = {}
    fields = []
    encoding = encoding.split(':')[1]
    encoding_arr = encoding.split(',')
    for encode in encoding_arr:
        one_encoding = {}
        if '<' in encode:
            regular = encode.split('<')[0]
            transform = encode.split('<')[1]

            regular_split = regular.split('-')
            if len(regular_split) != 3:
                print ("something wrong with regular string.")
            field = regular_split[0]
            attr_type = regular_split[1]
            encoding_type = regular_split[2]

            one_encoding["type"] = attr_type
            if field != '':
                one_encoding["field"] = field
                fields.append(field)

            transform_split = transform.split('>')
            transform_type = transform_split[0]
            transform_val = transform_split[1]

            if transform_type == "bin":
                one_encoding["bin"] = True
            else:
                one_encoding[transform_type] = transform_val
            
            encodings[encoding_type] = one_encoding

        else:
            encode_split = encode.split('-')
            if len(encode_split) != 3:
                print ("something wrong with encode string.")
            
            field = encode_split[0]
            attr_type = encode_split[1]
            encoding_type = encode_split[2]

            one_encoding["type"] = attr_type
            if field != '':
                one_encoding["field"] = field
                fields.append(field)
            else:
                print ("something wrong:")
                print (vegalite_str)
            
            encodings[encoding_type] = one_encoding
    
    vegalite_json["encoding"] = encodings
    return vegalite_json

def get_fields_from_vlstr(vlstr):
    encoding_str = vlstr.split(';')[1]
    encoding_str = encoding_str.split(':')[1]
    encodings = encoding_str.split(',')
    fields = []
    for encode in encodings:
        field = encode.split('-')[0]
        if field == '':
            continue
        fields.append(field)
    fields.sort()
    return fields

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)