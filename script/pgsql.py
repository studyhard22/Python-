import psycopg2
import requests
from datetime import datetime

# 连接 PostgreSQL 数据库
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="your_database",
    user="your_username",
    password="your_password"
)

# 创建一个游标对象
cursor = conn.cursor()

# 获取当前时间
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 查询数据库性能统计信息
cursor.execute("SELECT * FROM pg_stat_bgwriter")
bgwriter_stats = cursor.fetchone()

cursor.execute("SELECT * FROM pg_stat_database WHERE datname = current_database()")
database_stats = cursor.fetchone()

cursor.execute("SELECT * FROM pg_stat_user_tables")
table_stats = cursor.fetchall()

# 将结果转换为字典格式
result = {
    "时间": str(current_time),
    "背景写入器统计信息": {
        "后台写入请求数量": int(bgwriter_stats[0]),
        "后台写入完成数量": int(bgwriter_stats[1]),
        "后台写入最大延迟 (毫秒)": int(bgwriter_stats[2])
    },
    "数据库统计信息": {
        "数据库名称": str(database_stats[0]),
        "后台进程 ID": int(database_stats[1]),
        "连接数量": int(database_stats[2]),
        "慢查询数量": int(database_stats[3])
    },
    "用户表统计信息": []
}

for stat in table_stats:
    table_stat = {
        "表名": str(stat[0]),
        "更新数量": int(stat[1]),
        "插入数量": int(stat[2]),
        "删除数量": int(stat[3]),
        "扫描数量": int(stat[4]),
        "慢查询数量": int(stat[5])
    }
    result["用户表统计信息"].append(table_stat)

# 关闭游标和数据库连接
cursor.close()
conn.close()

# 发送 POST 请求将数据提交到监控平台
api_endpoint = "http://fstack-bmint.sfcloud.local/busimon/BusinessMlonitorSql/putCollectedPropertyData4outside"
data = {"data": result}
response = requests.post(api_endpoint, json=data)

# 打印响应结果
print(response.text)
