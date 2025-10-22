import cv2
import numpy as np
import time
import os
import glob
from datetime import datetime
from config import *
from PIL import Image, ImageDraw, ImageFont

# 用來儲存每個熱區的觸發計時器
zone_timers = {name: 0 for name in COMMAND_ZONES.keys()}

# 用來儲存每個熱區的冷卻計時器
zone_cooldowns = {name: 0 for name in COMMAND_ZONES.keys()}

# 建立必要的資料夾
os.makedirs(PHOTOS_FOLDER, exist_ok=True)
os.makedirs(VIDEOS_FOLDER, exist_ok=True)
os.makedirs(IMAGES_FOLDER, exist_ok=True)

# --- 中文字體支援函數 ---
def get_chinese_font(size=CHINESE_FONT_SIZE):
    """獲取中文字體"""
    try:
        # 使用設定檔中的字體路徑
        for font_path in CHINESE_FONT_PATHS:
            if os.path.exists(font_path):
                return ImageFont.truetype(font_path, size)
        
        # 如果都找不到，使用預設字體
        return ImageFont.load_default()
    except:
        return ImageFont.load_default()

def draw_chinese_text(img, text, position, font_size=20, color=(255, 255, 255)):
    """在 OpenCV 圖片上繪製中文文字"""
    try:
        # 將 OpenCV 圖片轉換為 PIL 圖片
        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)
        
        # 獲取中文字體
        font = get_chinese_font(font_size)
        
        # 繪製文字
        draw.text(position, text, font=font, fill=color)
        
        # 轉換回 OpenCV 格式
        img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        return img_cv
    except Exception as e:
        print(f"中文字體繪製失敗: {e}")
        # 如果失敗，使用 OpenCV 的英文顯示
        cv2.putText(img, "Text Error", position, cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        return img

# --- 功能函數 ---
def take_photo(frame):
    """拍照功能"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{PHOTOS_FOLDER}/photo_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"✓ 照片已儲存為 {filename}")
        return True
    except Exception as e:
        print(f"✗ 拍照失敗: {e}")
        return False

def play_images():
    """播放圖片功能"""
    try:
        # 使用設定檔中的副檔名
        image_files = []
        for ext in IMAGE_EXTENSIONS:
            image_files.extend(glob.glob(f"{IMAGES_FOLDER}/*{ext}"))
            image_files.extend(glob.glob(f"{IMAGES_FOLDER}/*{ext.upper()}"))
        
        if not image_files:
            print(f"✗ 沒有找到圖片檔案，請將圖片放在 {IMAGES_FOLDER} 資料夾中")
            return False
        
        print(f"✓ 找到 {len(image_files)} 張圖片，開始播放...")
        for img_path in image_files:
            img = cv2.imread(img_path)
            if img is not None:
                # 調整圖片大小以適應視窗
                height, width = img.shape[:2]
                if width > MAX_IMAGE_WIDTH:
                    ratio = MAX_IMAGE_WIDTH / width
                    new_width = MAX_IMAGE_WIDTH
                    new_height = int(height * ratio)
                    img = cv2.resize(img, (new_width, new_height))
                
                cv2.imshow('Image Viewer', img)
                print(f"正在顯示: {os.path.basename(img_path)}")
                print("按任意鍵繼續下一張，按 'q' 退出圖片播放")
                
                key = cv2.waitKey(0) & 0xFF
                if key == ord('q'):
                    break
        
        cv2.destroyWindow('Image Viewer')
        print("✓ 圖片播放完成")
        return True
    except Exception as e:
        print(f"✗ 播放圖片失敗: {e}")
        return False

def play_videos():
    """播放影片功能"""
    try:
        # 使用設定檔中的副檔名
        video_files = []
        for ext in VIDEO_EXTENSIONS:
            video_files.extend(glob.glob(f"{VIDEOS_FOLDER}/*{ext}"))
            video_files.extend(glob.glob(f"{VIDEOS_FOLDER}/*{ext.upper()}"))
        
        if not video_files:
            print(f"✗ 沒有找到影片檔案，請將影片放在 {VIDEOS_FOLDER} 資料夾中")
            return False
        
        print(f"✓ 找到 {len(video_files)} 個影片檔案，開始播放...")
        for video_path in video_files:
            cap_video = cv2.VideoCapture(video_path)
            if not cap_video.isOpened():
                print(f"✗ 無法開啟影片: {video_path}")
                continue
            
            print(f"正在播放: {os.path.basename(video_path)}")
            print("按 'q' 停止播放，按 's' 跳到下一個影片")
            
            while True:
                ret, frame = cap_video.read()
                if not ret:
                    break
                
                cv2.imshow('Video Player', frame)
                key = cv2.waitKey(VIDEO_FRAME_DELAY) & 0xFF
                if key == ord('q'):
                    cap_video.release()
                    cv2.destroyWindow('Video Player')
                    return True
                elif key == ord('s'):
                    break
            
            cap_video.release()
        
        cv2.destroyWindow('Video Player')
        print("✓ 影片播放完成")
        return True
    except Exception as e:
        print(f"✗ 播放影片失敗: {e}")
        return False

def is_in_cooldown(zone_name):
    """檢查是否在冷卻時間內"""
    if zone_cooldowns[zone_name] == 0:
        return False
    return time.time() - zone_cooldowns[zone_name] < COOLDOWN_DURATION

def start_cooldown(zone_name):
    """開始冷卻計時"""
    zone_cooldowns[zone_name] = time.time()

# --- 初始化 ---
cap = cv2.VideoCapture(CAMERA_INDEX)
if not cap.isOpened():
    print(f"✗ 無法開啟攝影機 {CAMERA_INDEX}")
    exit(1)

# 設定攝影機解析度
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

# 使用 MOG2 演算法，對光線變化有較好的適應性
fgbg = cv2.createBackgroundSubtractorMOG2(
    history=MOG2_HISTORY,
    varThreshold=MOG2_VAR_THRESHOLD,
    detectShadows=MOG2_DETECT_SHADOWS
)

print("程式已啟動。請保持穩定，準備偵測背景。")
time.sleep(3) # 給予使用者幾秒鐘時間準備

print("背景偵測完成，手勢控制已啟用！")
print("請將手移動至任一指令熱區，並停留約 1.5 秒以觸發。")
print("按 'q' 鍵可隨時退出程式。")

# 記錄開始時間
start_time = time.time()

# --- 主迴圈 ---
frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        print("✗ 無法讀取攝影機畫面")
        break

    frame_count += 1
    
    # 鏡像翻轉，讓手勢與畫面更直覺
    frame = cv2.flip(frame, 1)

    # 應用背景相減，得到一個前景遮罩
    fgmask = fgbg.apply(frame)
    
    # 對前景遮罩進行形態學操作，減少雜訊
    kernel = np.ones((MORPH_KERNEL_SIZE, MORPH_KERNEL_SIZE), np.uint8)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    # 處理每個熱區
    for name, (x, y, w, h) in COMMAND_ZONES.items():
        # 檢查是否在冷卻時間內
        if is_in_cooldown(name):
            # 顯示冷卻狀態
            remaining_time = COOLDOWN_DURATION - (time.time() - zone_cooldowns[name])
            cv2.rectangle(frame, (x, y), (x + w, y + h), ZONE_COOLDOWN_COLOR, 2)
            frame = draw_chinese_text(frame, f"冷卻中 {remaining_time:.1f}s", (x + 10, y + 70), 16, ZONE_COOLDOWN_COLOR)
            continue
        
        # 在畫面上繪製熱區矩形
        cv2.rectangle(frame, (x, y), (x + w, y + h), ZONE_COLOR, 2)
        
        # 繪製指令文字（使用中文字體）
        frame = draw_chinese_text(frame, name, (x + 10, y + 30), 20, TEXT_COLOR)
        
        # 裁剪出前景遮罩中對應熱區的部分
        roi = fgmask[y:y+h, x:x+w]
        
        # 計算熱區內白色像素的總數（代表變化量）
        motion_pixels = cv2.countNonZero(roi)
        
        # 顯示偵測到的變化量（除錯用）
        if SHOW_MOTION_PIXELS:
            cv2.putText(frame, f"變化: {motion_pixels}", (x + 10, y + 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, STATUS_COLOR, 1)

        # 判斷是否超過觸發閥值
        if motion_pixels > THRESHOLD:
            # 如果是第一次偵測到，就開始計時
            if zone_timers[name] == 0:
                zone_timers[name] = time.time()
                print(f"🔍 偵測到 {name} 區域的手勢動作")
            
            # 檢查是否已達到觸發時間
            elapsed_time = time.time() - zone_timers[name]
            progress = min(elapsed_time / TRIGGER_DURATION, 1.0)
            
            # 繪製進度條
            bar_width = int(w * progress)
            cv2.rectangle(frame, (x, y + h - 10), (x + bar_width, y + h), PROGRESS_COLOR, -1)
            
            # 顯示觸發進度
            frame = draw_chinese_text(frame, f"觸發中... {elapsed_time:.1f}s", (x + 10, y + 70), 16, (0, 0, 255))

            if elapsed_time >= TRIGGER_DURATION:
                # 執行指令
                print(f"🎯 觸發指令: {name}！")
                
                # 開始冷卻計時
                start_cooldown(name)
                
                # 執行對應的功能
                success = False
                if name == "拍照":
                    success = take_photo(frame)
                elif name == "播放圖片":
                    success = play_images()
                elif name == "播放影片":
                    success = play_videos()
                elif name == "退出":
                    print("正在退出程式...")
                    cap.release()
                    cv2.destroyAllWindows()
                    exit()
                
                if success:
                    print(f"✅ {name} 指令執行成功")
                else:
                    print(f"❌ {name} 指令執行失敗")
                    
                # 觸發後重設計時器
                zone_timers[name] = 0
                
        else:
            # 如果變化量低於閥值，重設計時器
            if zone_timers[name] != 0:
                zone_timers[name] = 0

    # 顯示狀態資訊
    if SHOW_FPS:
        fps = frame_count // max(1, int(time.time() - start_time))
        frame = draw_chinese_text(frame, f"FPS: {fps}", (10, 30), 18, STATUS_COLOR)
    frame = draw_chinese_text(frame, "按 'q' 退出程式", (10, frame.shape[0] - 20), 18, STATUS_COLOR)

    # 顯示主畫面
    cv2.imshow('Hand Gesture Control', frame)

    # 按下 'q' 鍵可隨時退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("使用者手動退出程式。")
        break

# 釋放資源並關閉視窗
cap.release()
cv2.destroyAllWindows()
