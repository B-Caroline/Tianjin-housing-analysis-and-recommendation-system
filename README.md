  以天津市租房市场为案例，使用 Python 爬虫采集链家网站挂牌的房屋租赁信息。再在三台 Linux 虚拟机上搭建 Spark 集群，运用 Scala 语言编写清洗任务提交到集群运行，以实现对采集的原始数据的清洗与预处理。构建基于 Flask 框架的屋租赁信息分析与可视化平台，运用 Echarts 库对选定的特征数据进行可视化分析和呈现。基于充足且精确的数据支持，训练随机森林预测模型，根据用户期望的租房条件预测租金价格，最后推荐相关房屋租赁信息。
  
liancheng.py是Python爬虫文件；

data_cleaning是清洗文件；

Flask_web文件夹下，app.py是启动入口，model.py是数据库连接模型，templates文件夹下的HTML文件都是页面；

Random forest文件夹下，house_price_predict.py是随机森林预测模型，model_evaluation.py是模型评估；

database文件夹下，house表是原始数据表，house_data_cleaning表是清洗后存储的表，user表是用户注册与登录的表。
