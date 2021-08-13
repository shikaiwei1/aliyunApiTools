# 用于Web调用测试
from wsgiref.simple_server import make_server
# 导入我们自己编写的web函数,用于调试:
from cdn.dir_flush import handler

# 创建一个服务器，IP地址为空，端口是8000，处理函数是application:
httpd = make_server('', 8000, handler)
print('Serving HTTP on port 8000...')
# 开始监听HTTP请求:
httpd.serve_forever()