import solara
import ee
import geemap.foliumap as geemap
import os
import json

# -----------------------------
# 1. 初始化 Earth Engine
# -----------------------------
ee_sa_json = os.environ.get("EE_SERVICE_ACCOUNT")

if ee_sa_json:
    # 將 Hugging Face secret 解析成 dict
    credentials_dict = json.loads(ee_sa_json)
    
    # 用 client_email + private_key 初始化
    credentials = ee.ServiceAccountCredentials(
        credentials_dict["client_email"],
        key_file=None,
        private_key=credentials_dict["private_key"]
    )
    ee.Initialize(credentials)
else:
    # 本地或手動授權模式
    ee.Authenticate()
    ee.Initialize()

# -----------------------------
# 2. 建立 Split Map
# -----------------------------
def create_split_map():
    # 定義河段範圍
    region = ee.Geometry.Point(121.38, 23.63).buffer(3000)

    # 潰堤前影像
    image_pre = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(region)
        .filterDate("2025-08-01", "2025-08-15")
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 10))
        .median()
        .clip(region)
    )

    # 潰堤後影像
    image_post = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(region)
        .filterDate("2025-09-20", "2025-10-05")
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 10))
        .median()
        .clip(region)
    )

    # 視覺化參數
    vis = {"bands": ["B4", "B3", "B2"], "min": 0, "max": 3000}

    # 建立地圖
    m = geemap.Map(center=[23.63, 121.38], zoom=14, height="650px")

    # 加入兩影像圖層
    left_layer = geemap.ee_tile_layer(image_pre, vis, "潰堤前 (衛星)")
    right_layer = geemap.ee_tile_layer(image_post, vis, "潰堤後 (衛星)")

    # 建立分割比對控制
    m.split_map(left_layer=left_layer, right_layer=right_layer)

    return m

# -----------------------------
# 3. Solara 元件
# -----------------------------
@solara.component
def Page():
    solara.Markdown("## 馬太鞍溪：潰堤前後衛星影像比對")
    solara.Markdown(
        "透過左側影像呈現潰堤前的河道與堰塞湖狀態，右側影像顯示潰堤後的淤積、改道與洪水影響範圍。"
        "使用滑動分割地圖進行直觀比對。"
    )

    # 快取地圖物件
    map_widget = solara.use_memo(create_split_map, dependencies=[])

    with solara.Column(style={"width": "100%", "height": "700px"}):
        solara.display(map_widget)
