import time
now = int(round(time.time() * 1000))
now_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now / 1000))
print(type(now_str))
print(now_str)
