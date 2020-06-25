from dziban.mkiv import Chart
from vega_datasets import data
from vega import VegaLite
import pandas as pd
import json
import copy

df = pd.read_json('./web/static/data/movies.json')
base = Chart(df)

def get_vegalite_str_from_vegalite(chart_vegalite):

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

def get_vegalite_str_from_chart(chart):
    chart_vegalite = chart._get_vegalite()

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

def vegaliteStr2vegalite(vegalite_str):
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

# chart = base.field("Director", channel="y").field("Title", channel="x").field("Release_Date", channel="size")
# print (chart._get_vegalite())

read_vlsf = open('vegalite_selected_fields.json', 'r')
vlsf = json.load(read_vlsf)
# new_vlsf = copy.deepcopy(vlsf)

# print (len(new_vlsf.keys()))

# nominals = ["MPAA_Rating", "Source", "Creative_Type", "Director", "Distributor", "Major_Genre", "Title"]
# long_nominal = ["Director", "Distributor", "Title"]
# short_nominal = ["Creative_Type", "Major_Genre", "MPAA_Rating", "Source"]

# for field_comb in new_vlsf:
#     if "row" in new_vlsf[field_comb]["encoding"]:
#         new_vlsf[field_comb] = {}

# with open('new_vegalite_selected_fields.json', 'w') as out:
#     json.dump(new_vlsf, out, indent=2)

# for field_comb in new_vlsf:
#     if not new_vlsf[field_comb]:
#         fields = field_comb.split('+')
#         fields.sort()
#         comb = {}
#         vlstr = ""
#         for field in fields:
#             if field in nominals:
#                 if field in long_nominal:
#                     if "long" in comb:
#                         comb["long"].append(field)
#                     else:
#                         comb["long"] = [field]
#                 else:
#                     if "short" in comb:
#                         comb["short"].append(field)
#                     else:
#                         comb["short"] = [field]
#             else:
#                 if "quan" in comb:
#                     comb["quan"].append(field)
#                 else:
#                     comb["quan"] = [field]
#         if "long" in comb:
#             if len(comb["long"]) == 3:
#                 continue
#             elif len(comb["long"]) == 2:
#                 chart = base.field(comb["long"][0], channel="x").field(comb["long"][1], channel="y")
#                 if "short" in comb:
#                     chart = chart.field(comb["short"][0], channel="color")
#                 elif "quan" in comb:
#                     chart = chart.field(comb["quan"][0], channel="size")
#             elif len(comb["long"]) == 1:
#                 chart = base.field(comb["long"][0], channel="y")
#                 if "short" in comb:
#                     if len(comb["short"]) == 2:
#                         chart = chart.field(comb["short"][0], channel="x").field(comb["short"][1], channel="color")
#                     elif len(comb["short"]) == 1:
#                         chart = chart.field(comb["short"][0], channel="x")
#                         if "quan" in comb:
#                             if "Release_Date" in comb["quan"]:
#                                 chart = chart.field("Release_Date", channel="size")
#                             else:
#                                 chart = chart.field(comb["quan"][0])
#                 elif "quan" in comb:
#                     if len(comb["quan"]) == 2:
#                         if comb["quan"][0] == "Release_Date":
#                             chart = chart.field("Release_Date", channel="x").field(comb["quan"][1])
#                         elif comb["quan"][1] == "Release_Date":
#                             chart = chart.field("Release_Date", channel="x").field(comb["quan"][0])
#                         else:
#                             chart = chart.field(comb["quan"][0], comb["quan"][1])
#                     elif len(comb["quan"]) == 1:
#                         if comb["quan"][0] == "Release_Date":
#                             chart = chart.field("Release_Date", channel="x")
#                         else:
#                             chart = chart.field(comb["quan"][0])
#             try:
#                 vlstr = get_vegalite_str_from_chart(chart)
#             except:
#                 print ("except:")
#                 print (field_comb)
#                 break
#             if "-row" in vlstr:
#                 print ("long:")
#                 print (field_comb)
#                 print (vlstr)
#                 continue
#         elif "short" in comb:
#             if len(comb["short"]) == 3:
#                 chart = base.field(comb["short"][0], channel="x").field(comb["short"][1], channel="y").field(comb["short"][2], channel="color")
#             elif len(comb["short"]) == 2:
#                 chart = base.field(comb["short"][0], channel="x").field(comb["short"][1], channel="y")
#                 if "quan" in comb:
#                     chart = chart.field(comb["quan"][0], channel="size")
#             elif len(comb["short"]) == 1:
#                 chart = base.field(comb["short"][0], channel="y")
#                 if "quan" in comb:
#                     if len(comb["quan"]) == 2:
#                         chart = chart.field(comb["quan"][0], comb["quan"][1])
#                     elif len(comb["quan"]) == 1:
#                         chart = chart.field(comb["quan"][0])
#             #vlstr = get_vegalite_str_from_chart(chart)
#             try:
#                 vlstr = get_vegalite_str_from_chart(chart)
#             except:
#                 print ("except:")
#                 print (field_comb)
#                 break
#             if "-row" in vlstr:
#                 print ("short")
#                 print (field_comb)
#                 print (vlstr)
#                 continue
#         else:
#             print ("three quans:")
#             print (field_comb)
        
#         new_vlsf[field_comb] = vegaliteStr2vegalite(vlstr)
    

# with open('new_vegalite_selected_fields.json', 'w') as out:
#     json.dump(new_vlsf, out, indent=2)

read_combine_bfs_result = open("combine_bfs_result.json", 'r')
combine_bfs_result = json.load(read_combine_bfs_result)

fields2vegaliteStr = {}

for field_comb in vlsf:
    if not vlsf[field_comb]:
        fields2vegaliteStr[field_comb] = ""
        continue
    chart_vegalite = vlsf[field_comb]
    fields2vegaliteStr[field_comb] = get_vegalite_str_from_vegalite(chart_vegalite)

for field_comb in fields2vegaliteStr:
    vlstr = fields2vegaliteStr[field_comb]
    if vlstr != "":
        if vlstr not in combine_bfs_result:
            print (vlstr)

# with open('fields2vegaliteStr.json', 'w') as out:
#     json.dump(fields2vegaliteStr, out, indent=2)