
import os
import pandas as pd
import numpy as np
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




# data = data[['user_id', 'register_time', 'pvp_battle_count', 'pvp_lanch_count', 'pvp_win_count', 'pve_battle_count',
#          'pve_lanch_count', 'pve_win_count', 'avg_online_minutes', 'pay_price', 'pay_count']
#     ]

# 数据库获取胜率相关的数据
def read_mysql_winrate():
    sql = '''
select
    'PVP' as `GAME_TYPE`,
    SUM(pvp_win_count)/SUM(pvp_battle_count) as `PVE_WIN`,
    SUM(CASE when pay_price > 0 then pvp_win_count else 0 end )/SUM(CASE when pay_price > 0 then pvp_battle_count else 0 end) as `PVE_WIN_PRICE`,
    SUM(CASE when pay_price = 0 then pvp_win_count else 0 end )/SUM(CASE when pay_price = 0 then pvp_battle_count else 0 end) as `PVE_WIN_NOPRICE`
from
    tap_fun_test
union all
select
    'PVE' AS `GAME_TYPE`,
    SUM(pve_win_count)/SUM(pve_battle_count) as `PVE_WIN`,
    SUM(CASE when pay_price > 0 then pve_win_count else 0 end )/SUM(CASE when pay_price > 0 then pve_battle_count else 0 end) as `PVE_WIN_PRICE`,
    SUM(CASE when pay_price = 0 then pve_win_count else 0 end )/SUM(CASE when pay_price = 0 then pve_battle_count else 0 end) as `PVE_WIN_NOPRICE`
from
    tap_fun_test
    '''
    engine = create_engine('mysql+pymysql://root:mysql@localhost:3306/dbtest')
    with engine.connect() as con:
        result = con.execute(text(sql))
        return pd.DataFrame(result.fetchall(), columns=result.keys())

# 写一个函数，根据传入的数据，生成柱状图，表示游戏类型和付费用户的胜率
def generate_bar_chart_winrate(data):
    bar = (
        Bar()
            .add_xaxis(data['GAME_TYPE'].tolist())
            .add_yaxis("PVE_WIN", data['PVE_WIN'].tolist(), label_opts=opts.LabelOpts(position="inside"))
            .add_yaxis("PVE_WIN_PRICE", data['PVE_WIN_PRICE'].tolist(), label_opts=opts.LabelOpts(position="inside"))
            .add_yaxis("PVE_WIN_NOPRICE", data['PVE_WIN_NOPRICE'].tolist(), label_opts=opts.LabelOpts(position="inside"))
            .set_global_opts(title_opts=opts.TitleOpts(title="游戏类型和付费用户的胜率"))
    )
    bar.render_notebook()# 生成柱状图
    # 保存到本地
    bar.render("bar_winrate.html")
    # 打开html文件
    




if __name__ == "__main__":
    # data = read_mysql_newuser()
    # generate_bar_chart_newuser(data)
    # data = read_mysql()
    # generate_pie_chart(data)
    # data = read_mysql_winrate()
    # generate_bar_chart_winrate(data)
    os.system("bar_winrate.html")