from dziban.mkiv import Chart
from vega_datasets import data
from vega import VegaLite
import pandas as pd
import json
import copy

read_vlsf = open('vegalite_selected_fields.json', 'r')
vlsf = json.load(read_vlsf)
new_vlsf = copy.deepcopy(vlsf)

for field_comb in new_vlsf:
    if "row" in new_vlsf[field_comb]["encoding"]:
        new_vlsf[field_comb] = {}

with open('new_vegalite_selected_fields.json', 'w') as out:
    json.dump(new_vlsf, out, indent=2)