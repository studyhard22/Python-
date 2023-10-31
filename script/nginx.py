import requests
import subprocess

# 使用 curl 命令获取 Nginx 当前的状态信息
nginx_status = subprocess.check_output(['curl', 'http://192.168.199.101:90/nginx_status']).decode('utf-8')

# 解析 Nginx 状态信息
status_lines = nginx_status.split('\n')

# 提取连接数、请求数、处理请求数、等待连接数、共享内存区使用情况等指标
connections = status_lines[0].split()[-1]
requests_count = status_lines[2].split()[2]
reading = status_lines[3].split()[1]
writing = status_lines[3].split()[3]
waiting = status_lines[3].split()[5]
# shm_zone_usage = status_lines[4].split()[3]

# 构造需要提交的数据
data = {
    'connections': connections,
    'requests': requests_count,
    'reading': reading,
    'writing': writing,
    'waiting': waiting,
    # 'shm_zone_usage': shm_zone_usage
}

# 提交数据到监控平台
# url = 'http://fstack-bmint.sfcloud.local/busimon/BusinessMlonitorSql/putCollectedPropertyData4outside'
url = 'http://localhost:3000'
response = requests.post(url, json=data)

# 输出响应结果
print(response.text)
