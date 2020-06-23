from dziban.mkiv import Chart
from vega_datasets import data
from vega import VegaLite
import pandas as pd

df = pd.read_json('./web/static/data/movies.json')
#cars = data('cars')

base = Chart(df)
all_fields = base.get_fields()



# fields = ['MPAA_Rating', 'IMDB_Votes']

# prior = base.field('MPAA_Rating')
# next_one = prior.field('IMDB_Votes')

# print (prior._get_stats(next_one))
# print (next_one._get_stats(prior))
# if len(fields) == 2:
#     chart = base.field(fields[0], fields[1])
#     print (chart._get_vegalite())
#chart = base.field(fields)


# print (prior.get_fields())
# print (prior._get_vegalite())
# next_one = prior.field('Major_Genre')
# print ("next one vegalite:")
# print (next_one._get_vegalite())

# next_cold = next_one.field('Running_Time_min')
# print ("next cold vegalte:")
# print (next_cold._get_vegalite())

# next_anchored = next_one.anchor().field('Running_Time_min')
# print ("next anchor vegalte:")
# print (next_anchored._get_vegalite())

# print ("next cold get stats:")
# print (next_cold._get_stats(next_one))

# print ("next anchor get stats:")
# print (next_anchored._get_stats())

#vegaliteUnordered = {'{"$schema": "https://vega.github.io/schema/vega-lite/v3.json", "data": {"url": "data/movies.json"}, "mark": "bar", "encoding": {"x": {"type": "quantitative", "aggregate": "count"}, "row": {"type": "nominal", "field": "Distributor"}, "y": {"type": "nominal", "field": "Major_Genre"}}}': 1.6276308553716943, '{"$schema": "https://vega.github.io/schema/vega-lite/v3.json", "data": {"url": "data/movies.json"}, "mark": "bar", "encoding": {"x": {"type": "quantitative", "aggregate": "count"}, "row": {"type": "nominal", "field": "Director"}, "y": {"type": "nominal", "field": "Major_Genre"}}}': 1.6276308553716943, '{"$schema": "https://vega.github.io/schema/vega-lite/v3.json", "data": {"url": "data/movies.json"}, "mark": "bar", "encoding": {"x": {"type": "quantitative", "aggregate": "count"}, "color": {"type": "nominal", "field": "Creative_Type"}, "y": {"type": "nominal", "field": "Major_Genre"}, "undefined": {"stack": true}}}': 1.629469122426869, '{"$schema": "https://vega.github.io/schema/vega-lite/v3.json", "data": {"url": "data/movies.json"}, "mark": "bar", "encoding": {"x": {"type": "quantitative", "aggregate": "count"}, "color": {"type": "nominal", "field": "MPAA_Rating"}, "y": {"type": "nominal", "field": "Major_Genre"}, "undefined": {"stack": true}}}': 1.629569012547736, '{"$schema": "https://vega.github.io/schema/vega-lite/v3.json", "data": {"url": "data/movies.json"}, "mark": "bar", "encoding": {"x": {"type": "quantitative", "aggregate": "count"}, "y": {"type": "nominal", "field": "Major_Genre"}, "row": {"type": "nominal", "field": "Title"}}}': 1.6334385171565584, '{"$schema": "https://vega.github.io/schema/vega-lite/v3.json", "data": {"url": "data/movies.json"}, "mark": "bar", "encoding": {"x": {"type": "quantitative", "aggregate": "count"}, "y": {"type": "nominal", "field": "Major_Genre"}, "row": {"type": "nominal", "field": "Release_Date"}}}': 1.6334385171565584, '{"$schema": "https://vega.github.io/schema/vega-lite/v3.json", "data": {"url": "data/movies.json"}, "mark": "bar", "encoding": {"x": {"type": "quantitative", "aggregate": "count"}, "y": {"type": "nominal", "field": "Major_Genre"}, "color": {"type": "nominal", "field": "Source"}, "undefined": {"stack": true}}}': 1.7349768875192604, '{"$schema": "https://vega.github.io/schema/vega-lite/v3.json", "data": {"url": "data/movies.json"}, "mark": "bar", "encoding": {"x": {"type": "quantitative", "aggregate": "count"}, "y": {"type": "nominal", "field": "Major_Genre"}, "color": {"type": "quantitative", "aggregate": "mean", "field": "US_Gross"}}}': 2.4522047943178458, '{"$schema": "https://vega.github.io/schema/vega-lite/v3.json", "data": {"url": "data/movies.json"}, "mark": "bar", "encoding": {"x": {"type": "quantitative", "aggregate": "count"}, "y": {"type": "nominal", "field": "Major_Genre"}, "color": {"type": "quantitative", "aggregate": "mean", "field": "Worldwide_Gross"}}}': 2.4522047943178458, '{"$schema": "https://vega.github.io/schema/vega-lite/v3.json", "data": {"url": "data/movies.json"}, "mark": "bar", "encoding": {"x": {"type": "quantitative", "aggregate": "count"}, "y": {"type": "nominal", "field": "Major_Genre"}, "color": {"type": "quantitative", "aggregate": "mean", "field": "US_DVD_Sales"}}}': 2.4522047943178458, '{"$schema": "https://vega.github.io/schema/vega-lite/v3.json", "data": {"url": "data/movies.json"}, "mark": "bar", "encoding": {"x": {"type": "quantitative", "aggregate": "count"}, "y": {"type": "nominal", "field": "Major_Genre"}, "color": {"type": "quantitative", "aggregate": "mean", "field": "Production_Budget"}}}': 2.4522047943178458, '{"$schema": "https://vega.github.io/schema/vega-lite/v3.json", "data": {"url": "data/movies.json"}, "mark": "bar", "encoding": {"x": {"type": "quantitative", "aggregate": "count"}, "color": {"type": "quantitative", "aggregate": "mean", "field": "IMDB_Rating"}, "y": {"type": "nominal", "field": "Major_Genre"}}}': 2.461329908675799, '{"$schema": "https://vega.github.io/schema/vega-lite/v3.json", "data": {"url": "data/movies.json"}, "mark": "bar", "encoding": {"x": {"type": "quantitative", "aggregate": "count"}, "color": {"type": "quantitative", "aggregate": "mean", "field": "IMDB_Votes"}, "y": {"type": "nominal", "field": "Major_Genre"}}}': 2.461329908675799, '{"$schema": "https://vega.github.io/schema/vega-lite/v3.json", "data": {"url": "data/movies.json"}, "mark": "bar", "encoding": {"x": {"type": "quantitative", "aggregate": "count"}, "y": {"type": "nominal", "field": "Major_Genre"}, "color": {"type": "quantitative", "aggregate": "mean", "field": "Running_Time_min"}}}': 2.6004471414883423, '{"$schema": "https://vega.github.io/schema/vega-lite/v3.json", "data": {"url": "data/movies.json"}, "mark": "bar", "encoding": {"x": {"type": "quantitative", "aggregate": "count"}, "y": {"type": "nominal", "field": "Major_Genre"}, "color": {"type": "quantitative", "aggregate": "mean", "field": "Rotten_Tomatoes_Rating"}}}': 2.6004471414883423}
