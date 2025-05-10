# 台灣天氣查詢網站

這是一個使用 Flask 框架開發的天氣查詢網站，透過中央氣象署的開放資料 API 提供台灣各縣市的即時天氣資訊。

## 功能特點

- 支援台灣各大縣市天氣查詢
- 顯示即時天氣狀況
- 提供溫度範圍（最高溫/最低溫）
- 顯示降雨機率
- 提供舒適度指數
- 支援 Docker 部署

## 技術堆疊

- Python 3
- Flask Web 框架
- HTML/CSS
- Docker
- Docker Compose
- GitHub Actions（CI/CD）
- AWS EC2 部署


### 部署所需的環境變數

在 GitHub Secrets 中需設定以下變數：
- `DOCKER_USERNAME`: Docker Hub 使用者名稱
- `DOCKER_PASSWORD`: Docker Hub 密碼
- `EC2_HOST`: AWS EC2 主機位址
- `EC2_USER`: EC2 SSH 使用者名稱
- `EC2_KEY`: EC2 SSH 私鑰

## 安裝與執行

1. 複製專案
```bash
git clone [你的專案網址]
cd weather-web-app
```

2. 安裝相依套件
```bash
pip install -r requirements.txt
```

3. 設定環境變數
在專案根目錄建立 `.env` 檔案並加入：
```
API_KEY=中央氣象署API金鑰
```

4. 執行應用程式
```bash
python app.py
```





