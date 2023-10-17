# Python-
随便写写python脚本
<h1>开启一个本地的8000服务器</h1>
<p>调用http.server模块：from http.server import BaseHTTPRequestHandler, HTTPServer</p>
<p>调用psutil模块：import psutil</p>
import psutil  # 导入 psutil 模块，用于获取系统信息，这里用于获取 CPU 使用率
from http.server import BaseHTTPRequestHandler, HTTPServer  # 导入 http.server 模块，用于创建 HTTP 服务器
# 创建一个自定义的请求处理类
class RequestHandler(BaseHTTPRequestHandler):
    # 定义一个方法处理 HTTP GET 请求
    def do_GET(self):
        # 获取当前CPU的使用率
        cpu_percent = psutil.cpu_percent(interval=1)

        # 构建要返回的HTML响应内容
        html = f"""
        <html>
        <head>
            <title>CPU use:</title>
        </head>
        <body>
            <h1>CPU use: {cpu_percent}%</h1>
        </body>
        </html>
        """
        # 设置响应头
        self.send_response(200)  # 设置响应状态码为 200，表示成功
        self.send_header('Content-type', 'text/html')  # 设置响应头中的 Content-type 为 text/html
        self.end_headers()  # 结束响应头的设置

        # 发送响应内容
        self.wfile.write(html.encode('utf-8'))  # 将 HTML 内容以 UTF-8 编码发送给客户端

# 启动HTTP服务
def start_server():
    server_address = ('', 8000)  # 定义服务器地址为本地计算机的端口 8000
    httpd = HTTPServer(server_address, RequestHandler)  # 创建 HTTP 服务器实例，将自定义的请求处理类传递给它
    print('正在监听 http://localhost:8000')  # 输出服务器监听信息
    httpd.serve_forever()  # 启动服务器并持续监听请求

start_server()  # 启动服务器
