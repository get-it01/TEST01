import pandas as pd
from  sqlalchemy import create_engine
import numpy as np
from pymysql import install_as_MySQLdb
# pandas 打开csv文件
dir = r'D:\windocu\desktop\bigdata\bigdata_analyse-main\tap4fun\tap_fun_test.csv'
data = pd.read_csv(dir,encoding='utf-8')
# print(data.head()) # 打印前五行
# data = data[['user_id', 'register_time', 'pvp_battle_count', 'pvp_lanch_count', 'pvp_win_count', 'pve_battle_count',
#          'pve_lanch_count', 'pve_win_count', 'avg_online_minutes', 'pay_price', 'pay_count']
#     ]
# print(data.head())
# print('info',data.info())
# print('descri',data.describe())
# print('colums',data.columns)
# print('isnull',data.isnull().sum())
# # print('duplicat',data.duplicated().sum())
# engine = create_engine('mysql://root:root@localhost:3306/dbtest')
# data.to_sql('tap_fun_test',con=engine,if_exists='replace',index=False)


# 数据写入到oracle中
def write_oracle(data):
    engine = create_engine('oracle://root:root@localhost:1521/orcl')
    data.to_sql('tap_fun_test',con=engine,if_exists='replace',index=False)

# 将数据写入mysql中
def write_mysql(data):
    engine = create_engine('mysql://root:root@localhost:3306/dbtest')
    data.to_sql('tap_fun_test',con=engine,if_exists='replace',index=False)
# 查询mysql数据
def read_mysql(data):
    engine = create_engine('mysql://root:root@localhost:3306/dbtest')
    data = pd.read_sql('select * from tap_fun_test',con=engine)
    print(data.head())
    print(data.info())
