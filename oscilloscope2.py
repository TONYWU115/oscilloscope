import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# 設定串口參數
ser = serial.Serial('COM3', 115200, timeout=1)  # Windows 用 COM4, Linux/Mac 用 '/dev/ttyUSB0'

# 儲存 ADC 數據
data = []

# 設定圖表
fig, ax = plt.subplots()
ax.set_ylim(0, 5)  # 假設 Arduino 讀取 0V ~ 5V
ax.set_xlim(0, 100)  # 顯示最近 100 筆數據
line, = ax.plot([], [], 'r-')

def update(frame):
    global data

    # 讀取 Arduino 發送的數據
    if ser.in_waiting:
        try:
            raw_value = ser.readline().decode().strip()
            if raw_value.replace(".", "").isdigit():  # 檢查是否為有效數值
                value = float(raw_value)
                data.append(value)
                if len(data) > 100:  # 限制數據量
                    data.pop(0)
        except Exception as e:
            print(f"錯誤: {e}")  # 打印錯誤訊息

    # 更新圖表數據
    line.set_data(np.linspace(0, 100, len(data)), data)
    return line,

# 啟動動畫
ani = animation.FuncAnimation(fig, update, interval=100, blit=True, cache_frame_data=False)
plt.show()

# 關閉串口
ser.close()
