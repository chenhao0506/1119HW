import solara
import leafmap.maplibregl as leafmap
import os

MAPTILER_KEY = os.environ.get("MAPTILER_API_KEY", "") 

def create_3d_map():
    # 檢查 API Key 是否存在
    if not MAPTILER_KEY:
        # 如果沒有 Key，回傳一個基礎地圖，但不會有地形
        m = leafmap.Map(
            center=[121.424, 23.682], 
            zoom=13, 
            style="OpenStreetMap",
        )
        m.layout.height = "700px"
        return m
    
    # MapTiler Outdoor-v2 Style 內建支援地形資料
    style_url = f"https://api.maptiler.com/maps/outdoor-v2/style.json?key={MAPTILER_KEY}"
    
    m = leafmap.Map(
        style=style_url,
        center=[121.424, 23.682], 
        zoom=10,
        # 啟用地形：當使用 MapTiler Style 時，通常只需設定 style URL，
        # Leafmap 會自動處理 style.json 內定義的地形源。
        # 如果需要明確設定，通常是: terrain={"source": "mapbox-dem"}
        )
    m.layout.height = "700px"
    return m

@solara.component
def Page():
    # 2. 警示使用者如果金鑰未設定
    if not MAPTILER_KEY:
        solara.Warning(
            "MapTiler API Key 未設定。請在 Hugging Face Space Settings 中加入 'MAPTILER_API_KEY' Secret，否則 3D 地形無法載入。"
        )
    
    solara.Markdown("## 3D 地形展示 (MapLibre GL)")
    
    # 3. 使用 solara.use_memo 快取地圖物件
    # 依賴於 MAPTILER_KEY，當 Key 改變時地圖會重新生成
    map_object = solara.use_memo(create_3d_map, dependencies=[MAPTILER_KEY])

    # 4. 渲染地圖
    return map_object.to_solara()