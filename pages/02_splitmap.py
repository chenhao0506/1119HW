import solara
import leafmap.leafmap as leafmap
import leafmap.maplibregl as maplibregl
import os

# MapTiler 金鑰 (Hugging Face Secret)
MAPTILER_KEY = os.environ.get("MAPTILER_API_KEY", "")

def create_split_map():
    """建立左右滑動分割地圖"""
    split_control = leafmap.split_map(
        left_layer="Esri.WorldImagery",
        right_layer="OpenStreetMap",
        left_label="衛星影像",
        right_label="街道地圖",
        center=[23.632, 121.380],
        zoom=14,
    )
    split_control.layout.height = "650px"
    return split_control

def create_3d_map():
    """建立 3D MapLibre 地圖"""
    if not MAPTILER_KEY:
        m = maplibregl.Map(
            center=[120.9, 23.7],
            zoom=7,
            style="OpenStreetMap",
        )
        m.layout.height = "700px"
        return m

    style_url = f"https://api.maptiler.com/maps/outdoor-v2/style.json?key={MAPTILER_KEY}"
    m = maplibregl.Map(
        style=style_url,
        center=[121.4296,23.6832],
        zoom=12,
        pitch=45,
        bearing=15,
    )
    m.layout.height = "700px"
    return m

@solara.component
def Page():
    solara.Markdown("## 馬太鞍溪捲簾比對 (Split Map)")
    solara.Markdown("使用滑動分割視窗比較衛星影像與街道地圖。")
    split_widget = solara.use_memo(create_split_map, dependencies=[])
    solara.display(split_widget)

    solara.Markdown("## 馬太鞍溪 3D 地形")
    if not MAPTILER_KEY:
        solara.Warning(
            "MapTiler API Key 未設定，3D 地形將顯示基本地圖。"
        )
    map3d = solara.use_memo(create_3d_map, dependencies=[MAPTILER_KEY])
    solara.display(map3d.to_solara())

    solara.Markdown("### 災害說明")
    solara.Markdown(
        "在樺加沙颱風後，馬太鞍溪堰塞湖潰堤，洪水挾帶泥沙沖向下游，"
        "導致馬太鞍溪橋被沖毀，下游堤防受損，政府將民眾疏散至光復糖廠。"
    )
    repo_url = "https://raw.githubusercontent.com/s1243001/solara1119/main/"
    solara.Image(image=f"{repo_url}pic_03.jpg", width="100%")
