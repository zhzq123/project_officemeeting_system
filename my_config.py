import socket

# configuration for flask
DEBUG = True
SECRET_KEY = 'ksdjkfjlskdj9848714key'
USERNAME = 'admin'
PASSWORD = '..'
port = "5000"

super_admin_name = 'admin'
super_admin_email = 'zhangziqi@minieye.cc'
super_admin_password = 'zhzq123'
clear_all_database = True


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


host_ip = get_host_ip()
Mail_user_name = 'm15071333813@163.com'
Mail_user_password = 'zhzq123'
pattern = 'all'
