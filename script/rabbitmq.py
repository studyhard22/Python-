import time

import requests
import pika

# RabbitMQ连接信息
rabbitmq_host = "localhost"
rabbitmq_port = 5672
rabbitmq_username = "guest"
rabbitmq_password = "guest"

# 监控平台信息
monitor_url = "http://fstack-bmint.sfcloud.local/busimon/BusinessMlonitorSql/putCollectedPropertyData4outside"
monitor_data = {
    "key1": "",
    "key2": "",
    "key3": ""
}

# 连接RabbitMQ
credentials = pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
parameters = pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# 获取RabbitMQ队列数量
def get_rabbitmq_queue_count():
    queue_count = channel.queue_declare(queue="", passive=True).method.message_count
    monitor_data["RabbitMQ队列数量"] = str(queue_count)

# 获取RabbitMQ连接数
def get_rabbitmq_connections():
    connections = channel.connection.client_properties.get("connection_details", {}).get("connection_count", 0)
    monitor_data["RabbitMQ连接数"] = str(connections)

# 提交监控数据
def submit_monitor_data():
    res = requests.post(url=monitor_url, data=monitor_data)
    print(res.text)

# 定时任务
def run_monitor():
    interval = 10  # 监控间隔时间（单位：秒）
    while True:
        get_rabbitmq_queue_count()
        get_rabbitmq_connections()
        submit_monitor_data()
        time.sleep(interval)

# 主函数
if __name__ == "__main__":
    run_monitor()
