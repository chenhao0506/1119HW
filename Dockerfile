# --- 基礎映像 ---
FROM python:3.11-slim

# --- 系統套件（GDAL, PROJ 等 GIS 必備） ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gdal-bin \
    libgdal-dev \
    libproj-dev \
    && rm -rf /var/lib/apt/lists/*

# --- 設定 GDAL 環境變數 ---
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# --- 設定工作目錄 ---
WORKDIR /app

# --- 複製 requirements.txt 並安裝套件 ---
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# --- 複製整個 repo ---
COPY . .

# --- 暴露 Solara 預設埠 ---
EXPOSE 7860

# --- 啟動 Solara App ---
CMD ["solara", "run", "pages", "--host", "0.0.0.0", "--port", "7860"]
