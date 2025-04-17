# import os
# import pandas as pd
# import numpy as np
# import sqlalchemy
# import pymysql
# from sqlalchemy import create_engine
# import pyecharts

# # 从mysql中读取数据
# def read_mysql(data):
#     engine = create_engine('mysql://root:root@localhost:3306/dbtest')
#     data = pd.read_sql('select * from tap_fun_test',con=engine)
#     print(data.head())
#     print(data.info())
# # 使用echarts生成柱状图
import os
import pandas as pd
import numpy as np
import sqlalchemy
import pymysql
from sqlalchemy import create_engine, text
from pyecharts.charts import Bar, Pie
from pyecharts import options as opts

# 注册 PyMySQL 为 MySQL 的驱动
pymysql.install_as_MySQLdb()

# sql读取充值和未充值人的比例
sql = '''
    select
        sum(case when pay_count > 0 then 1 else 0 end) as `pay_role`,
        sum(case when pay_price > 0 then 0 else 1 end) as `free_role`
    from
        tap_fun_test;
'''
# 从mysql中读取数据
def read_mysql():
    engine = create_engine('mysql+pymysql://root:mysql@localhost:3306/dbtest')
    with engine.connect() as con:
        result = con.execute(text(sql))
        return result.fetchone()
# echarts生成饼图，显示充值人数和未充值人数

def generate_pie_chart(data):
    pie = (
        Pie()
            .add("充值与未充值的人数", [list(z) for z in zip(['充值', '未充值'], data)])
            .set_global_opts(title_opts=opts.TitleOpts(title="充值与未充值的人数"))
    )
    pie.render_notebook()# 生成饼图
    # 保存到本地
    pie.render("pie_pay.html")




def generate_bar_chart(data):
    bar = (
        Bar()
            .add_xaxis(['充值', '未充值'])
            .add_yaxis("人数", [data[0], data[1]], label_opts=opts.LabelOpts(position="inside"))
            .set_global_opts(title_opts=opts.TitleOpts(title="充值与未充值的人数"))
    )
    bar.render_notebook()# 生成柱状图
    # 保存到本地
    bar.render("bar_pay.html") 





def read_mysql_newuser():
    #sql语句 从register_time字段提取日期，并统计每日新注册用户数量
    sql = '''
        select
            date(register_time) as date,
            count(user_id) as new_user
        from
            tap_fun_test
        group by
            date(register_time)
        order by
            date(register_time) desc
    '''
    engine = create_engine('mysql+pymysql://root:mysql@localhost:3306/dbtest')
    with engine.connect() as con:
        result = con.execute(text(sql))
        return pd.DataFrame(result.fetchall(), columns=result.keys())

# 写一个函数，根据传入的数据，register_time和new_user数量，生成柱状图，表示每日新增用户数
def generate_bar_chart_newuser(data):
    bar = (
        Bar()
            .add_xaxis(data['date'].tolist())
            .add_yaxis("人数", data['new_user'].tolist(), label_opts=opts.LabelOpts(position="inside"))
            .set_global_opts(title_opts=opts.TitleOpts(title="每日新注册用户数量"))
    )
    bar.render_notebook()# 生成柱状图
    # 保存到本地
    bar.render("bar_newuser.html")



def generate_bar_chart_newuser(data):
    bar = (
        Bar()
            .add_xaxis(data['date'].tolist())
            .add_yaxis("人数", data['new_user'].tolist(), label_opts=opts.LabelOpts(position="inside"))
            .set_global_opts(title_opts=opts.TitleOpts(title="每日新注册用户数量"))
    )
    bar.render_notebook()# 生成柱状图
    # 保存到本地
    bar.render("bar_newuser.html")


if __name__ == "__main__":
    data = read_mysql_newuser()
    generate_bar_chart_newuser(data)
    data = read_mysql()
    generate_pie_chart(data)