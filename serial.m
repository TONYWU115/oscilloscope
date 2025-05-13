clc;
clear;

% 設置串口參數
serialPort = "COM3"; % 修改為實際的 COM 端口
baudRate = 115200;    

s = serialport(serialPort, baudRate);
configureTerminator(s, "LF");
flush(s);

% 數據顯示設定
sampleRate = 100;   % 數據接收頻率 (100 Hz)
dataLength = sampleRate * 1; % 保持顯示 1 秒數據 (100 個數據點)

voltage_data = zeros(1, dataLength);
time_data = linspace(-1, 0, dataLength); % x 軸範圍設置為 -1 秒到 0 秒

% 繪圖設定
figure;
h = plot(time_data, voltage_data, 'b', 'DisplayName', 'Voltage (V)');
ylim([0, 5]); % 設置電壓範圍 (0 ~ 5V)
xlabel('Time (s)');
ylabel('Voltage (V)');
legend;

while true
    if s.NumBytesAvailable > 0
        data = readline(s);
        voltage = str2double(data);
        
        if ~isnan(voltage)
            % 更新數據
            voltage_data = [voltage_data(2:end), voltage];
            
            % 繪圖更新
            set(h, 'YData', voltage_data);
            drawnow;
        end
    end
end

clear s;
