## 安裝需求

```bash
pip install opencv-python numpy pillow
```

### 依賴套件說明
- **opencv-python**: 電腦視覺處理
- **numpy**: 數值計算
- **pillow**: 中文字體支援（PIL）

## 使用方法

1. **準備環境**:
   - 確保您的電腦有攝影機
   - 將要播放的圖片放在 `images` 資料夾中
   - 將要播放的影片放在 `videos` 資料夾中

2. **執行程式**:
   ```bash
   python gesture_control.py
   ```

3. **操作說明**:
   - 程式啟動後會先進行背景偵測（3秒）
   - 將手移動到綠色指令區域並停留約 1.5 秒即可觸發
   - 觸發後會有 3 秒冷卻時間
   - 按 'q' 鍵可隨時退出程式

## 指令區域

程式會在畫面上顯示四個指令區域：

- **拍照**: 觸發拍照功能，照片會儲存在 `photos` 資料夾
- **播放圖片**: 播放 `images` 資料夾中的所有圖片
- **播放影片**: 播放 `videos` 資料夾中的所有影片
- **退出**: 退出程式

## 設定檔說明

您可以修改 `config.py` 來調整程式行為：

### 基本設定
- `COMMAND_ZONES`: 指令區域的位置和大小
- `THRESHOLD`: 手勢偵測敏感度（數值越小越敏感）
- `TRIGGER_DURATION`: 觸發所需時間（秒）
- `COOLDOWN_DURATION`: 冷卻時間（秒）

### 攝影機設定
- `CAMERA_INDEX`: 攝影機索引（通常 0 是內建攝影機）
- `FRAME_WIDTH`, `FRAME_HEIGHT`: 畫面解析度

### 檔案設定
- `PHOTOS_FOLDER`: 照片儲存資料夾
- `IMAGES_FOLDER`: 圖片播放資料夾
- `VIDEOS_FOLDER`: 影片播放資料夾

### 視覺設定
- `ZONE_COLOR`: 指令區域顏色
- `TEXT_COLOR`: 文字顏色
- `PROGRESS_COLOR`: 進度條顏色

## 支援的檔案格式

### 圖片格式
- JPG/JPEG
- PNG
- BMP
- TIFF

### 影片格式
- MP4
- AVI
- MOV
- MKV
- WMV

## 故障排除

1. **攝影機無法開啟**:
   - 檢查攝影機是否被其他程式佔用
   - 嘗試修改 `config.py` 中的 `CAMERA_INDEX`

2. **手勢偵測不準確**:
   - 調整 `config.py` 中的 `THRESHOLD` 參數
   - 確保光線充足且背景穩定

3. **觸發太敏感或太遲鈍**:
   - 調整 `TRIGGER_DURATION` 參數
   - 調整 `THRESHOLD` 參數