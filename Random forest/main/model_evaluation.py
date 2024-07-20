import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import explained_variance_score,  r2_score, mean_squared_error, mean_absolute_error

# 加载数据
df = pd.DataFrame(pd.read_csv('../data/house_data_cleaning2.csv'))
data = np.array(df[['house_Price','house_Area','house_Region','house_Type','house_Lease']].values)

# 提取特征和标签
one = OneHotEncoder(drop='first')
stand = StandardScaler()
str_features = one.fit_transform(data[:, 2:]).toarray()# 特征：面积、地区、户型、朝向
num_features = stand.fit_transform(data[:, 1:2])# 特征：面积
X = np.hstack([str_features, num_features])
y = data[:,0]# 标签：价格

#划分训练集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# 随机森林
random_model = RandomForestRegressor(n_estimators=1500, random_state=42, n_jobs=-1) #n_jobs=-1调用所有内核
random_model.fit(X, y)

# 评估模型
y_pred = random_model.predict(X_test)
#可解释方差
exp_score = explained_variance_score(y_test, y_pred)
#平均绝对误差
mae_score = mean_absolute_error(y_test, y_pred)
#均方差
mse_score =  mean_squared_error(y_test, y_pred)
#均方根误差/均方根误差
rmse_score = math.sqrt(mse_score)
#拟合度
r2_score = r2_score(y_test, y_pred)
print('可解释方差：', exp_score)
print('平均绝对误差：', mae_score)
print('均方差：',mse_score)
print('均方根误差：', rmse_score)
print('拟合度：', r2_score)

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] =False

# 绘制预测值与实际值的散点图
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, color='blue', label='实际值对应的预测值')
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--', label='理想趋势')
plt.xlabel('实际值')
plt.ylabel('预测值')
plt.title('预测值与实际值的散点图')
plt.legend()
plt.show()

# 绘制残差图
residuals_test = y_test - y_pred
plt.figure(figsize=(8, 6))
plt.scatter(y_pred, residuals_test, color='red', label='残差值')
plt.hlines(y=0, xmin=y_pred.min(), xmax=y_pred.max(), color='blue', linestyles='--', label='零线')
plt.xlabel('预测值')
plt.ylabel('残差值')
plt.title('预测值与实际值的残差图')
plt.legend()
plt.show()
