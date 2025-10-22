# 手勢控制程式設定檔
# 您可以修改這些參數來調整程式的行為

# 指令熱區設定 (x, y, 寬度, 高度)
# 請根據您的螢幕解析度和攝影機位置調整這些座標
COMMAND_ZONES = {
    "拍照": (50, 50, 200, 80),
    "播放圖片": (50, 150, 200, 80),
    "播放影片": (50, 250, 200, 80),
    "退出": (50, 350, 200, 80)
}

# 手勢偵測參數
THRESHOLD = 3000          # 觸發閥值，數值越小越敏感
TRIGGER_DURATION = 1.5    # 觸發所需持續時間（秒）
COOLDOWN_DURATION = 3.0   # 冷卻時間（秒）

# 攝影機設定
CAMERA_INDEX = 0          # 攝影機索引，通常 0 是內建攝影機
FRAME_WIDTH = 640         # 畫面寬度
FRAME_HEIGHT = 480        # 畫面高度

# 檔案路徑設定
PHOTOS_FOLDER = "photos"  # 照片儲存資料夾
IMAGES_FOLDER = "images"  # 圖片播放資料夾
VIDEOS_FOLDER = "videos"  # 影片播放資料夾

# 圖片播放設定
MAX_IMAGE_WIDTH = 800     # 圖片最大顯示寬度
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']

# 影片播放設定
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']
VIDEO_FRAME_DELAY = 30    # 影片播放延遲（毫秒）

# 背景相減設定
MOG2_HISTORY = 500        # MOG2 歷史幀數
MOG2_VAR_THRESHOLD = 16   # MOG2 變異閾值
MOG2_DETECT_SHADOWS = True # 是否偵測陰影

# 形態學操作設定
MORPH_KERNEL_SIZE = 5     # 形態學核心大小

# 視覺設定
ZONE_COLOR = (0, 255, 0)      # 熱區顏色 (B, G, R)
ZONE_COOLDOWN_COLOR = (100, 100, 100)  # 冷卻中熱區顏色
TEXT_COLOR = (0, 255, 0)       # 文字顏色
PROGRESS_COLOR = (0, 255, 0)   # 進度條顏色
STATUS_COLOR = (255, 255, 255) # 狀態文字顏色

# 除錯設定
SHOW_MOTION_PIXELS = True  # 是否顯示偵測到的變化量
SHOW_FPS = True           # 是否顯示 FPS

# 中文字體設定
CHINESE_FONT_SIZE = 20    # 中文字體大小
CHINESE_FONT_PATHS = [    # 中文字體路徑（按優先順序）
    "C:/Windows/Fonts/msyh.ttc",    # 微軟雅黑
    "C:/Windows/Fonts/simhei.ttf",  # 黑體
    "C:/Windows/Fonts/simsun.ttc",  # 宋體
    "C:/Windows/Fonts/arial.ttf"    # Arial (備用)
]
