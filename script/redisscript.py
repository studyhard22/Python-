import requests
import redis
import time
import json

# Redis连接信息
redis_host = "192.168.199.101"
redis_port = 6379
redis_password = ""

# 监控平台信息
monitor_url = 'http://localhost:3000'  # 更新为你的监控平台URL

# 连接Redis
r = redis.Redis(host=redis_host, port=redis_port, password=redis_password)

# 获取Redis内存使用情况
def get_redis_memory_info():
    memory_info = r.info("memory")
    used_memory = memory_info["used_memory"]
    used_memory_human = memory_info["used_memory_human"]
    return {
        "Redis内存使用情况": "{} ({})".format(used_memory_human, used_memory)
    }

# 获取Redis命中率
def get_redis_hit_rate():
    info = r.info("stats")
    keyspace_hits = int(info["keyspace_hits"])
    keyspace_misses = int(info["keyspace_misses"])
    hit_rate = 0.0 if (keyspace_hits + keyspace_misses == 0) else keyspace_hits / (keyspace_hits + keyspace_misses)
    return {
        "Redis命中率": "{:.2%}".format(hit_rate)
    }

# 获取Redis连接数
def get_redis_connections():
    connections = r.client_list()
    return {
        "Redis连接数": str(len(connections))
    }

# 获取Redis运行时信息
def get_redis_runtime_info():
    info = r.info("server")
    uptime_in_seconds = int(info["uptime_in_seconds"])
    return {
        "Redis运行时间（秒）": uptime_in_seconds
    }

# 获取Redis最大内存使用情况
def get_redis_max_memory():
    info = r.info("memory")
    max_memory = info["maxmemory"]
    max_memory_human = info["maxmemory_human"]
    return {
        "Redis最大内存使用情况": "{} ({})".format(max_memory_human, max_memory)
    }

# 获取CPU使用率
def get_cpu_usage():
    # 添加获取CPU使用率的代码
    # 你可以使用系统工具或第三方库来获取CPU使用率
    # 并将其格式化为你的监控数据中的一个项

    # 例如：
    cpu_usage = 50  # 假设CPU使用率为50%
    return {
        "CPU使用率": "{}%".format(cpu_usage)
    }


# 提交监控数据
def submit_monitor_data(data):
    headers = {'Content-Type': 'application/json'}
    res = requests.post(url=monitor_url, data=json.dumps(data), headers=headers)
    print(res.text)

# 定时任务
def run_monitor():
    interval = 10  # 监控间隔时间（单位：秒）
    while True:
        memory_info = get_redis_memory_info()
        hit_rate = get_redis_hit_rate()
        connections = get_redis_connections()
        runtime_info = get_redis_runtime_info()
        max_memory = get_redis_max_memory()
        cpu_usage = get_cpu_usage()
        data = {**memory_info, **hit_rate, **connections, **runtime_info, **max_memory, **cpu_usage}
        submit_monitor_data(data)
        time.sleep(interval)

# 主函数
if __name__ == "__main__":
    run_monitor()
