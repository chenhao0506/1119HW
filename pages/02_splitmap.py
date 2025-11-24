import solara
import ee
import geemap.foliumap as geemap
import os
import json

# EE 初始化
ee_sa_json = os.environ.get("EE_SERVICE_ACCOUNT")
if ee_sa_json:
    credentials_dict = json.loads(ee_sa_json)
    credentials = ee.ServiceAccountCredentials(
        credentials_dict["client_email"],
        credentials_dict["private_key"]
    )
    ee.Initialize(credentials)
else:
    ee.Authenticate()
    ee.Initialize()

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

    # Folium Map + SplitMap
    m = geemap.Map(center=[23.63, 121.38], zoom=14, height="650px")
    m.split_map(
        left_layer=image_pre,
        right_layer=image_post,
        left_name="潰堤前",
        right_name="潰堤後",
        vis_params=vis
    )
    return m

@solara.component
def Page():
    solara.Markdown("## 馬太鞍溪：潰堤前後衛星影像比對")
    solara.Markdown(
        "左側影像呈現潰堤前的河道與堰塞湖狀態，右側影像顯示潰堤後的淤積與洪水影響範圍。"
    )

    map_widget = solara.use_memo(create_split_map, dependencies=[])

    with solara.Column(style={"width": "100%", "height": "700px"}):
        solara.display(map_widget)
