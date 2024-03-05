import requests
import bs4
import csv
import pandas as pd

# 打开CSV文件，以UTF-8编码和换行符写入
with open('C:/李宇斌/Python/test/houseprice_yuexiu_dongshankou.csv', 'w', encoding='utf-8', newline='') as file:
    file.write('\ufeff')
    writer = csv.writer(file)

    # 写入表头
    header = ["标题", "位置", "总价", "房屋信息", "单价"]
    writer.writerow(header)

    # 遍历页面
    for k in range(100):
        url = f"https://gz.lianjia.com/ershoufang/pg{k}rs越秀东山口/"

        payload = {
            'type': '1',
            'query': 'https://gz.lianjia.com/ershoufang/yuexiu/?sug=越秀',
            'Cookie': 'lianjia_uuid=67b662d6-c131-4b55-b76a-529f22fd6ca8; select_city=440100; lianjia_ssid=c04d2d4f-20bb-4b03-94d7-f67b0923ead0'
        }
        headers = {
            'Referer': requests.utils.quote('https://gz.lianjia.com/ershoufang/yuexiu/?sug=越秀'),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        content = response.text
        soup = bs4.BeautifulSoup(content, 'lxml')

        titles = soup.select('.info.clear .title')
        position = soup.select('.positionInfo')
        total_price = soup.select('.totalPrice')
        uniprice = soup.select('.unitPrice')
        house_info = soup.select('.houseInfo')

        item_num = len(titles)
        for i in range(item_num):
            content_list = [titles[i].getText(), position[i].getText(), total_price[i].getText(),
                            house_info[i].getText(), uniprice[i].getText()]
            writer.writerow(content_list)

# Load the CSV file into a DataFrame
df = pd.read_csv('C:/李宇斌/Python/test/houseprice_yuexiu_dongshankou.csv')

# Split the "房屋信息" column by "|" and create a new DataFrame
split_df = df['房屋信息'].str.split('|', expand=True)

# Add the new columns to the original DataFrame
for i in range(split_df.shape[1]):
    df[f'房屋信息_{i+1}'] = split_df[i]

# Drop the original "房屋信息" column
df = df.drop('房屋信息', axis=1)
# 删除最后一列
df = df.drop(df.columns[-1], axis=1)

#文件“位置”列，按照“—"符号分列
df[['街道', '区域']] = df['位置'].str.split('-', expand=True)
df = df.drop('位置', axis=1)
#
# Iterate over each row in "房屋信息_6" column
for index, row in df.iterrows():
    row['房屋信息_6'] = str(row['房屋信息_6'])
    # If there is '年' in the data of this row
    if '年' in row['房屋信息_6']:
        # Keep the data in this row
        pass
    # If there is no '年'
    else:
        # Move this row's data to the corresponding position in "房屋信息7" column
        if pd.notnull(row['房屋信息_6']):
            df.at[index, '房屋信息_7'] = row['房屋信息_6']
        # Delete this row's data
        df.at[index, '房屋信息_6'] = ''

#把表头的几个替换一下“房屋信息_1”替换为“房型”,‘房屋信息_2'替换为"面积（平方）",'房屋信息_3'替换为"朝向",'房屋信息_4'替换为"装修",'房屋信息_5'替换为"楼层",’房屋信息_6‘替换为"建筑时间",’房屋信息_7‘替换为"建筑类型"
df.rename(columns={'单价': '单价(元/平米）', '总价': '总价（万）', '房屋信息_1': '房型', '房屋信息_2': '面积（平方）', '房屋信息_3': '朝向', '房屋信息_4': '装修', '房屋信息_5': '楼层', '房屋信息_6': '建筑时间', '房屋信息_7': '建筑类型'}, inplace=True)

#文件“楼层”列，把每一行的“楼层”去掉
df['楼层'] = df['楼层'].str.replace('楼层', '')
#文件“房型”列分列，按照“室”和“厅”为分割符分列，按照“室”分割的做左边的列列头改名字为“房”，右边的列列头改名字为“厅”
df[['房', '厅']] = df['房型'].str.split('室', expand=True)
df = df.drop('房型', axis=1)
# 移出“房”列里面带有“车位”的行
df = df[~df['房'].str.contains('车位')]
# 移出“房”列里面带有“车位”的行
df = df[~df['房'].str.contains('车位')]
#生成的“厅”列每一行的“厅”字去掉
df['厅'] = df['厅'].str.replace('厅', '')
#文件’面积”列，把每一行的“平米”字去掉
df['面积（平方）'] = df['面积（平方）'].str.replace('平米', '')
df['单价(元/平米）'] = df['单价(元/平米）'].str.replace('元/平', '')
df['总价（万）'] = df['总价（万）'].str.replace('万', '')

#文件’朝向”列，把每一行包含的空格全部去掉
df['朝向'] = df['朝向'].str.strip()
# 清理“单价(元/平米）”列的数据
df['单价(元/平米）'] = df['单价(元/平米）'].str.replace(',', '').astype(float)

# Save the modified DataFrame to a new CSV file with UTF-8 encoding
output_file_path = 'C:\李宇斌\Python/test/链家越秀东山口房屋资料（数据清洗后）.csv'
df.to_csv(output_file_path, index=True, encoding='gbk')

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import time
now = time.localtime()
# 将时间格式化为指定格式的字符串
formatted_date = time.strftime("%Y-%m-%d", now)
print(formatted_date)
# 加载支持中文的字体
font = FontProperties(fname=r"C:\Windows\Fonts\SimHei.ttf", size=14)  # 路径根据你的系统环境修改

# Load the CSV file into a DataFrame
df = pd.read_csv('C:\李宇斌\Python/test/链家越秀东山口房屋资料（数据清洗后）.csv',encoding='gbk')
data = df
# 计算总数
tq = len(data)

# 计算房和厅的组合数量
combination_count = data.groupby(['房', '厅']).size()

# 获取组合数量
combination_count
print(combination_count)

# # 清理“单价(元/平米）”列的数据
# data['单价(元/平米)'] = data['单价(元/平米)'].astype(str).str.replace(',', '').astype(float)
# data['单价(元/平米）'] = data['单价(元/平米）'].str.replace('元/平米', '').str.replace('以上', '').str.replace('以下', '').str.replace('-', '').str.replace('万', '').str.replace('元', '').str.replace(' ', '')


#把“单价(元/平米）”列的数据都变成数值数据
data['单价(元/平米）'] = pd.to_numeric(data['单价(元/平米）'], errors='coerce')

# 再次计算3房1厅组合的平均价格
average_price_311 = data[(data['房'] == 3) & (data['厅'] == 1)]['单价(元/平米）'].mean()

# 计算所有价格组合的“单价(元/平米）”列的平均价格
price_averages = df.groupby(['房', '厅']).mean(numeric_only=True).round(0)

# 把price_averages做表格导出
price_averages.to_csv('房厅的平均价格图.csv')
plt.rcParams['font.family'] = 'SimHei'  # 或者使用 'Arial Unicode MS'
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# Filter the data for houses with 3 rooms and 1 living room
three_rooms_one_living_room = data[(data['房'] == 3) & (data['厅'] == 1)]

# 1. Calculate the average total price, average unit price, and average area of these houses
average_total_price = three_rooms_one_living_room['总价（万）'].mean().round(0)
average_unit_price = three_rooms_one_living_room['单价(元/平米）'].mean().round(0)
average_area = three_rooms_one_living_room['面积（平方）'].mean().round(0)

# 2. Analyze the distribution of orientations
orientation_distribution = three_rooms_one_living_room['朝向'].value_counts().head(10)

# 3. Analyze the distribution of decoration conditions
decoration_distribution = three_rooms_one_living_room['装修'].value_counts().head(10)

# 4. Analyze the distribution of floor levels
floor_distribution = three_rooms_one_living_room['楼层'].value_counts().head(10)

total = average_total_price, average_unit_price, average_area, orientation_distribution, decoration_distribution, floor_distribution

#打印文字描述上面total的内容
print('1. 总价平均值：', average_total_price)
print('2. 单价平均值：', average_unit_price)
print('3. 面积平均值：', average_area)
print('4. 前十位主要朝向分布：', orientation_distribution)
print('5. 装修分布：', decoration_distribution)
print('6. 前十位楼层分布：', floor_distribution)


# 设置图形的大小
plt.figure(figsize=(50, 30))
font = FontProperties(fname=r"C:\Windows\Fonts\msyh.ttc", size=14)
# plt.xticks(rotation=20, fontproperties=font)
# plt.yticks(fontproperties=font)

# 对每个房间和客厅的组合进行循环，并为每个组合绘制一个条形图
for combination, price in price_averages['单价(元/平米）'].items():
    # 横坐标的标签用使用SimHei字体，字体调整与柱形同宽
    plt.gca().xaxis.set_tick_params(labelsize=14, rotation=270)
    plt.gca().xaxis.set_major_locator(plt.MultipleLocator(1))
    plt.text(f"{combination[0]}房{combination[1]}厅", price, f"{price}", ha='center', va='bottom', fontproperties=font)
    plt.bar(f"{combination[0]}房{combination[1]}厅", price, color='skyblue')
    # 横坐标上的文字用使用SimHei字体
    plt.xticks(rotation=0, fontproperties=font)
    print(combination,price)

# 设置标题和标签
plt.title(f"（日期：{formatted_date}）"+'链家网越秀区东山口二手房数据统计图'+f"（共：{tq}）套", fontproperties=font)
plt.xlabel('房间和客厅组合', fontproperties=font)
plt.ylabel('平均单价 (元/平米)', fontproperties=font)

# 显示图例（如果需要）
plt.legend(title='房厅组合与平均单价', prop=font)

# 显示图形
plt.show()

#图片另存为JPG格式图片
plt.savefig('C:\李宇斌\Python/test/price_averages.jpg',dpi=300, bbox_inches='tight')


#把上述8张图纸都汇聚一张大的图纸并另存到文件夹
plt.figure(figsize=(50, 20))
#给图纸添加标题加入formatted_date的数值
# 把formatted_date数值加入标题
plt.suptitle(f"（日期：{formatted_date}）"+'链家网越秀区东山口三房一厅二手房数据统计图'+f"（共：{tq}）套", fontsize=16)
font = FontProperties(fname=r"C:\Windows\Fonts\msyh.ttc", size=14)

plt.subplot(2, 3, 1)
three_rooms_one_living_room['总价（万）'].hist(bins=30)
plt.xticks(rotation=0, fontproperties=font)
plt.title('总价分布图', fontproperties=font)
plt.xlabel('总价（万）', fontproperties=font)
plt.ylabel('数量', fontproperties=font)

# # 绘制单价分布图
plt.subplot(2, 3, 2)
three_rooms_one_living_room['单价(元/平米）'].hist(bins=30)
plt.xticks(rotation=0, fontproperties=font)
plt.title('单价分布图', fontproperties=font)
plt.xlabel('单价（元/平米）', fontproperties=font)
plt.ylabel('数量', fontproperties=font)

# # 绘制面积分布图
plt.subplot(2, 3, 3)
three_rooms_one_living_room['面积（平方）'].hist(bins=30)
plt.title('面积分布图', fontproperties=font)
plt.xlabel('面积（平方）', fontproperties=font)
plt.ylabel('数量', fontproperties=font)

plt.subplot(2, 3, 4)
plt.pie(orientation_distribution, labels=orientation_distribution.index,
        textprops={'fontsize': 12},autopct='%1.1f%%', startangle=140)
plt.axis('equal')
plt.title('朝向分布图', fontproperties=font)

plt.subplot(2, 3, 5)
plt.pie(decoration_distribution, labels=decoration_distribution.index,
        textprops={'fontsize': 12},autopct='%1.1f%%', startangle=140)
plt.axis('equal')
plt.title('装修情况分布图', fontproperties=font)

plt.subplot(2, 3, 6)
plt.pie(floor_distribution, labels=floor_distribution.index,
        textprops={'fontsize': 12},autopct='%1.1f%%', startangle=140)
plt.axis('equal')
plt.title('楼层分布图', fontproperties=font)

# #图片另存为
plt.savefig('C:\李宇斌\Python/test/链家网越秀区东山口三房一厅二手房数据统计图.jpg', dpi=300, bbox_inches='tight')
plt.show()

# #把上述资料生成图表形式展示
# import matplotlib.pyplot as plt
#
# # 绘制总价分布图
# three_rooms_one_living_room['总价（万）'].hist(bins=30)
# plt.xticks(rotation=0, fontproperties=font)
# plt.title('链家网越秀区三房一厅前3000套房总价分布图', fontproperties=font)
# plt.xlabel('总价（万）', fontproperties=font)
# plt.ylabel('数量', fontproperties=font)
# plt.show()
#
# # 绘制单价分布图
# three_rooms_one_living_room['单价(元/平米）'].hist(bins=30)
# plt.xticks(rotation=0, fontproperties=font)
# plt.title('链家网越秀区三房一厅前3000套房单价分布图', fontproperties=font)
# plt.xlabel('单价（元/平米）', fontproperties=font)
# plt.ylabel('数量', fontproperties=font)
# plt.show()
#
# # 绘制面积分布图
# three_rooms_one_living_room['面积（平方）'].hist(bins=30)
# plt.title('链家网越秀区三房一厅前3000套房面积分布图', fontproperties=font)
# plt.xlabel('面积（平方）', fontproperties=font)
# plt.ylabel('数量', fontproperties=font)
# plt.show()
#
# # 绘制朝向分布图
# plt.pie(orientation_distribution, labels=orientation_distribution.index,
#         textprops={'fontsize': 12}, autopct='%1.1f%%', startangle=80
#         )
# plt.axis('equal')
# plt.title('链家网越秀区三房一厅前3000套房朝向分布图', fontproperties=font)
# plt.show()
#
# # 绘制装修分布图
# plt.pie(decoration_distribution, labels=decoration_distribution.index,
#         textprops={'fontsize': 12},autopct='%1.1f%%', startangle=140)
# plt.axis('equal')
# plt.title('链家网越秀区三房一厅前3000套房装修分布图', fontproperties=font)
# plt.show()
#
# # 绘制楼层分布图
# plt.pie(floor_distribution, labels=floor_distribution.index,
#         textprops={'fontsize': 12},autopct='%1.1f%%', startangle=140)
# plt.axis('equal')
# plt.title('链家网越秀区三房一厅前3000套房楼层分布图', fontproperties=font)
# plt.show()
#
# # 绘制总价与面积关系图
# plt.scatter(three_rooms_one_living_room['面积（平方）'], three_rooms_one_living_room['总价（万）'])
# plt.xlabel('面积（平方）', fontproperties=font)
# plt.ylabel('总价（万）', fontproperties=font)
# plt.title('链家网越秀区三房一厅前3000套房总价与面积关系图', fontproperties=font)
# plt.show()
#
# # 绘制单价与面积关系图
# plt.scatter(three_rooms_one_living_room['面积（平方）'], three_rooms_one_living_room['单价(元/平米）'])
# plt.xlabel('面积（平方）', fontproperties=font)
# plt.ylabel('单价（元/平米）', fontproperties=font)
# plt.title('链家网越秀区三房一厅前3000套房单价与面积关系图', fontproperties=font)
# plt.show()
