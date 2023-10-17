import psutil

# 获取CPU和内存使用情况
cpu_usage = psutil.cpu_percent(interval=1)
memory_info = psutil.virtual_memory()

print(f"CPU Usage: {cpu_usage}%")
print(f"Memory Usage: {memory_info.percent}%")
