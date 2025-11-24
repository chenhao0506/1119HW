import solara
import ee
import geemap.foliumap as geemap  
import os

# 1. 初始化 Earth Engine
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ee_service_account.json"
ee.Initialize()

def create_split_map():
    # 定義區域 (河段近似經緯)
    region = ee.Geometry.Point(121.38, 23.63).buffer(3000)  # 半徑約 3 km
    # 或更寬的 bbox: ee.Geometry.BBox(xmin, ymin, xmax, ymax)

    # 潰堤前影像：你要找合適時間點
    image_pre = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
                 .filterBounds(region)
                 .filterDate("2025-08-01", "2025-08-15")
                 .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 10))
                 .median()
                 .clip(region))

    # 潰堤後影像：事件發生後
    image_post = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
                  .filterBounds(region)
                  .filterDate("2025-09-20", "2025-10-05")
                  .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 10))
                  .median()
                  .clip(region))

    # 視覺化參數
    vis = {"bands": ["B4", "B3", "B2"], "min": 0, "max": 3000}

    # 建立地圖
    m = geemap.Map(center=[23.63, 121.38], zoom=14, height="650px")

    # 在地圖中添加兩影像圖層
    left_layer = geemap.ee_tile_layer(image_pre, vis, "潰堤前 (衛星)")
    right_layer = geemap.ee_tile_layer(image_post, vis, "潰堤後 (衛星)")

    # 建立分割比對控制
    m.split_map(left_layer=left_layer, right_layer=right_layer)

    return m

@solara.component
def Page():
    solara.Markdown("## 馬太鞍溪：潰堤前後衛星影像比對")
    solara.Markdown(
        "透過左側影像呈現潰堤前的河道與堰塞湖狀態，右側影像顯示潰堤後的淤積、改道與洪水影響範圍。使用滑動分割地圖進行直觀比對。"
    )

    # 使用 use_memo 快取地圖物件
    map_widget = solara.use_memo(create_split_map, dependencies=[])

    with solara.Column(style={"width": "100%", "height": "700px"}):
        solara.display(map_widget)
