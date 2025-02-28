import serial
import csv
import time


# Check if the Serial attribute exists
print(hasattr(serial, 'Serial'))  # This should print True if the import is correct


serial_port = serial.Serial('COM9', 115200) 

with open('data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Time", "Value"]) 

    while True:
       
        data = serial_port.readline().strip()
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')  
        # writer.writerow([current_time, data]) 
        # print(data) 

        for byte in data:
            writer.writerow([current_time, byte])
            print(current_time, byte)

# serial_port.close() 



