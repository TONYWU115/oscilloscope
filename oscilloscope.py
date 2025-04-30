import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 設定串口參數
ser = serial.Serial('COM3', 115200, timeout=1)  # Windows 用 COM3, Linux/Mac 用 '/dev/ttyUSB0'

# 儲存 ADC 數據
data = []

# 設定圖表
fig, ax = plt.subplots()
ax.set_ylim(-5, 5)  # ADC 解析度範圍 (0~1023)
ax.set_xlim(0, 100)  # 顯示最近 100 筆數據
line, = ax.plot([], [], 'r-')

def update(frame):
    global data

    # 讀取 Arduino 發送的數據
    if ser.in_waiting:
        try:
            value = float(ser.readline().decode().strip())  # 讀取並解析數據
            data.append(value)
            if len(data) > 100:  # 限制數據量
                data.pop(0)
        except:
            pass

    # 更新圖表數據
    line.set_data(range(len(data)), data)
    return line,

# 啟動動畫
ani = animation.FuncAnimation(fig, update, interval=100, blit=True)
plt.show()

# 關閉串口
ser.close()
