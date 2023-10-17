import psutil
from http.server import BaseHTTPRequestHandler, HTTPServer


# 创建一个自定义的请求处理类
class RequestHandler(BaseHTTPRequestHandler):
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
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # 发送响应内容
        self.wfile.write(html.encode('utf-8'))


# 启动HTTP服务
def start_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print('正在监听 http://localhost:8000')
    httpd.serve_forever()


start_server()
