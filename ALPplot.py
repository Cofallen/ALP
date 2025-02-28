import matplotlib.pyplot as plt
import numpy as np

# datalist = []
# dataplot = []
# j = 0
# with open('datapc.csv', 'r', newline='', encoding='utf-8') as datapc:
#     data = datapc.readlines()
#     # print(data)
#     for item in data:
#         index = item.find(',')
#         if index != -1:
#             dataraw = (float)(item[(index+1):-1])
#             datalist.append(dataraw)
#         print(dataraw)
#     # print(datalist)
# for i in range(0, len(datalist)):
#     while datalist[i] == 0 and datalist[i-1] == 0:
#         while datalist[j] < 0:
#             j += 1
#         dataplot.append(float(datalist[j]))
#         j = 0
#         print(dataplot)    

datalist = []
dataplot = []

with open('datapc.csv', 'r', newline='', encoding='utf-8') as datapc:
    lines = datapc.readlines()
    # 遍历每一行，提取逗号后的值并转换为 float
    for item in lines:
        parts = item.strip().split(',')
        if len(parts) >= 2:
            try:
                dataraw = parts[1].strip()
                value = float(dataraw)
                datalist.append(value)
            except ValueError as e:
                print("转换 float 时出错:", e)
                
# print("datalist =", datalist)

# 后续处理 datalist 的逻辑需注意避免索引错误
# 例如避免使用 datalist[i-1] 时 i 等于 0
for i in range(1, len(datalist)):
    if datalist[i] == 0 and datalist[i-1] == 0:
        # 找到大于等于 0 的下一个数据，并添加到 dataplot 中
        j = i
        while j < len(datalist) and datalist[j] <= 0:
            j += 1
        if j < len(datalist):
            dataplot.append(datalist[j])
            # print("dataplot =", dataplot)

plt.plot(dataplot) # 唯一一个大于等于 0 的数据列
plt.show()

length = []
error = 0
# 确定数据包长度
for i in range(1, len(datalist)):
    if datalist[i] == 0 and datalist[i-1] == 0:
        j = i + 1
        # 加入索引边界检查
        while j < len(datalist) and datalist[j] != 0:
            j += 1
        if j < len(datalist):
            length.append(j - i + 2)
        else:
            print(f"在索引 {i} 处，找不到数据包尾 (0)，忽略该数据包。")
for i in length:
    if i != 10:
        error += 1
plt.pie(np.array([len(length)-error, error]), labels=['Correct', 'Error'], colors=['red', 'green'], autopct='%1.1f%%', shadow=True)
plt.text(0.5, 1.0, f"errRate: {error/len(length):.2f}", ha='center', va='bottom', transform=plt.gca().transAxes)
plt.text(0.5, 0.9, f"aveLength: {sum(length)/len(length):.2f}", ha='center', va='bottom', transform=plt.gca().transAxes)
plt.show()
