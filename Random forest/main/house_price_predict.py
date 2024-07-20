import re
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

# 加载数据
df = pd.DataFrame(pd.read_csv('../data/house_data_cleaning2.csv'))
data = np.array(df[['house_Price','house_Area','house_Region','house_Type','house_Lease']].values)

#用户期望
def expectation():
    #期望面积
    while True:
        try:
            user_area = int(input("请输入期望面积（m²）： "))
            break
        except ValueError:
            print("输入格式不正确，请重新输入。")

    #期望地区
    while True:
        hanzi_pattern = re.compile(r'^[\u4e00-\u9fa5]+$')  # 定义汉字匹配的正则表达式模式
        user_region = input("请输入期望地区（区）：")
        if hanzi_pattern.match(user_region):
            break
        else:
            print("输入不是汉字，请重新输入。")

    #期望户型
    while True:
        house_pattern = re.compile(r'^(\d+)室(\d+)厅(\d+)卫$')  # 定义房屋信息匹配的正则表达式模式
        user_type = input("请输入期望户型（如1室2厅1卫）： ")
        if house_pattern.match(user_type):
            break
        else:
            print("输入格式不正确，请重新输入（如1室2厅1卫）。")

    #期望租赁方式
    while True:
        user_lease = input("请输入期望租赁方式（整租/合租）： ")
        if user_lease == "整租" or user_lease == "合租":
            break
        else:
            print("输入格式不正确，请重新输入（整租/合租）。")

    expectation_data = np.array([2000, user_area, user_region, user_type, user_lease])

    new_data = np.append(data, [expectation_data], axis=0)

    return new_data, user_area, user_region, user_type, user_lease

#特征工程
def feature_engineering(new_data):
    # 提取特征和标签
    one = OneHotEncoder(drop='first')
    stand = StandardScaler()
    str_features = one.fit_transform(new_data[:, 2:]).toarray()  # 特征：地区、户型、朝向
    num_features = stand.fit_transform(new_data[:, 1:2])  # 特征：面积

    feature = np.hstack([str_features, num_features])
    label = new_data[:, 0]  # 标签：价格

    X = feature[0:-1, :]#取出除最后一行的所有
    y = label[:-1]#取出除最后一个元素的所有

    x_except = feature[-1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7)

    return X_train, X_test, y_train, y_test, X, y, x_except

#训练随机森林模型，预测租金
def random_forest_model(X_train, X_test, y_train, y_test, X, y, user_except):
    random_model = RandomForestRegressor(n_estimators=1500, random_state=42, n_jobs=-1)
    random_model.fit(X, y)

    sc1 = random_model.score(X_test, y_test)
    sc2 = random_model.score(X_train, y_train)
    print('===========================')
    print('随机森林准确率01：', sc1)
    print('随机森林准确率02：', sc2)

    #预测用户期望
    pre = random_model.predict([user_except])

    return round(pre[0])

#推荐房屋
def recommend(pre_price, user_area, user_region, user_type, user_lease):
    # 筛选符合要求的 house_Region
    filtered_data = df[df['house_Region'] == user_region].copy()
    # 计算每一行的 house_Price 列与目标值 2000 的差值的绝对值
    filtered_data['price_difference'] = abs(filtered_data['house_Price'] - pre_price)
    # 按照差值升序排列，并选择前 5 行
    selected_data = filtered_data.nsmallest(5, 'price_difference')

    pd.set_option('display.max_columns', None)  # 显示所有列
    pd.set_option('display.width', 1000)
    selected_data2 = selected_data.rename(columns={
        'house_Introduce': '房屋简介',
        'house_Region': '地区',
        'house_Address': '详细地址',
        'house_floor': '楼层',
        'house_Direction': '朝向',
        'house_Price': '租金',
        'house_Area': '房屋面积',
        'house_Heating': '供暖情况',
        'house_Type': '房屋户型',
        'house_Lease': '租赁方式',
        'price_difference': '价格差'
    })

    #输出结果
    print('==================================================================================')
    print('用户期望：','房屋面积：', user_area,'m²，', '房屋地址：',user_region,'区，', '房屋户型：',user_type, '，租赁方式：', user_lease)
    print('==================================================================================')
    print('预计租金为：' + str(pre_price) + '元')
    print('===================================推荐房屋======================================')
    print(selected_data2[['房屋简介', '详细地址', '房屋户型', '房屋面积', '楼层', '租赁方式','朝向', '租金', '价格差']])

if __name__ == '__main__':
    new_data, user_area, user_region, user_type, user_lease = expectation()
    X_train, X_test, y_train, y_test, X, y, user_except = feature_engineering(new_data)
    price = random_forest_model(X_train, X_test, y_train, y_test, X, y, user_except)
    recommend(price, user_area, user_region, user_type, user_lease)
