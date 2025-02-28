import serial
import csv
import time
import datetime
import struct

import serial.serialutil
import serial.tools
import serial.tools.list_ports

# 引入window
import ALPwindow

# 检查 Serial 是否存在
if not hasattr(serial, 'Serial'):
    print("无法找到 Serial 类，请检查 pyserial 库是否正确安装。")
    exit(1)
    
try:
    serial_port = serial.Serial('COM9', 115200)  # 打开串口
except serial.serialutil.SerialException as e:
    print("无法打开串口，请检查串口是否存在...", e)
    # 读取存在的串口列表
    ports = serial.tools.list_ports.comports()
    if ports:
        print("存在的串口列表：", [port for port, desc, hwid in ports])
    else:
        print("没有找到串口，请检查串口连接。")
    exit(1)

with open('data.csv', 'w', newline='', encoding='utf-8') as raw_file, \
     open('datapc.csv', 'w', newline='', encoding='utf-8') as proc_file:

    writer_raw = csv.writer(raw_file)
    writer_proc = csv.writer(proc_file)

    writer_raw.writerow(["Time", "Value"])   # data.csv 表头
    writer_proc.writerow(["Time", "Value"])    # datapc.csv 表头

    buffer = bytearray()
    marker = b'\x00\x00\x80\x7f'  # 数据包结束标识

    while True:
        # 每次读取串口缓冲区中现有的数据
        bytes_to_read = serial_port.in_waiting or 1
        data = serial_port.read(bytes_to_read)
        if data:
            # 写入原始数据，每个字节记录一行
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S") + f".{now.microsecond//1000:03d}.{now.microsecond%1000:03d}"
            for byte in data:
                writer_raw.writerow([current_time, byte])
                print(current_time, "raw byte:", byte)

            # 将新读到的数据累加到缓冲区中
            buffer.extend(data)

        # 在缓冲区查找完整数据包
        while True:
            index = buffer.find(marker)
            if index == -1:
                break  # 缓冲区中没有完整数据包
            # 找到结束标识，将整个数据包提取出来（包含标识）
            packet = buffer[:index+len(marker)]
            # 从缓冲区清除已处理的数据包
            del buffer[:index+len(marker)]
            
            # 数据包内容（不含标识）
            packet_data = packet[:-len(marker)]
            # 检查数据长度是否为4的倍数
            if len(packet_data) % 4 == 0:
                # 每4个字节转换为一个 float（这里使用 little-endian 格式）
                for i in range(0, len(packet_data), 4):
                    float_bytes = packet_data[i:i+4]
                    value = struct.unpack('<f', float_bytes)[0]
                    writer_proc.writerow([current_time, value])
                    # print("Processed:", current_time, value)
            else:
                print(current_time, "数据长度不完整，忽略该数据包。")
                
