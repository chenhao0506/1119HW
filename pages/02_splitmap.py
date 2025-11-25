import solara
import leafmap.leafmap as leafmap

# 地圖基本設定集中管理，方便後續修改
MAP_CENTER = [23.632, 121.380]  # 花蓮馬太鞍溪
MAP_ZOOM = 14
MAP_HEIGHT = "70vh"  # 使用視窗高度比例，RWD 較佳

def create_split_map():
    split_map = leafmap.split_map(
        left_layer="Esri.WorldImagery",
        right_layer="OpenStreetMap",
        left_label="衛星影像",
        right_label="街道地圖",
        center=MAP_CENTER,
        zoom=MAP_ZOOM,
    )

    # 調整地圖樣式
    split_map.layout.height = MAP_HEIGHT
    split_map.layout.border = "1px solid #ccc"

    return split_map


@solara.component
def Page():
    solara.Markdown("## 馬太鞍溪捲簾比對 (Split Map)")
    solara.Markdown(
        "透過捲簾滑動方式，比對衛星影像與街道地圖，協助觀察馬太鞍溪河道位置與周邊地貌變化。"
    )

    # 地圖使用 memo，避免重複渲染造成效能下降
    split_widget = solara.use_memo(create_split_map, dependencies=[])

    # 外層容器排版
    with solara.Column(
        style={
            "width": "100%",
            "maxWidth": "1200px",
            "margin": "0 auto",
            "padding": "10px",
        }
    ):
        solara.display(split_widget)