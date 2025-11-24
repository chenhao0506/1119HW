import solara
import ee
import geemap.foliumap as geemap
import os
import json
from google.oauth2 import service_account

# -----------------------------
# 1. 初始化 Earth Engine
# -----------------------------
ee_sa_json = os.environ.get("EE_SERVICE_ACCOUNT")
if ee_sa_json:
    info = json.loads(ee_sa_json)
    credentials = service_account.Credentials.from_service_account_info(info)
    ee.Initialize(credentials)
else:
    ee.Authenticate()
    ee.Initialize()

# -----------------------------
# 2. 建立 Split Map
# -----------------------------
def create_split_map():
    region = ee.Geometry.Point(121.38, 23.63).buffer(3000)
    image_pre = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
                 .filterBounds(region)
                 .filterDate("2025-08-01", "2025-08-15")
                 .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 10))
                 .median()
                 .clip(region))
    image_post = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
                  .filterBounds(region)
                  .filterDate("2025-09-20", "2025-10-05")
                  .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 10))
                  .median()
                  .clip(region))
    vis = {"bands": ["B4", "B3", "B2"], "min": 0, "max": 3000}

    m = geemap.Map(center=[23.63, 121.38], zoom=14, height="650px")
    left_layer = geemap.ee_tile_layer(image_pre, vis, "潰堤前 (衛星)")
    right_layer = geemap.ee_tile_layer(image_post, vis, "潰堤後 (衛星)")
    m.split_map(left_layer=left_layer, right_layer=right_layer)
    return m

@solara.component
def Page():
    solara.Markdown("## 馬太鞍溪：潰堤前後衛星影像比對")
    solara.Markdown("左邊是潰堤前，右邊是潰堤後。滑動分割比對影像。")
    map_widget = solara.use_memo(create_split_map, dependencies=[])
    with solara.Column(style={"width": "100%", "height": "700px"}):
        solara.display(map_widget)