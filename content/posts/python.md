---
title: Python
date: 2026-04-03T00:00:00+08:00
draft: false
slug: python
tags: [Python, 编程语言]
source: 02-Knowledge/编程/Python.md
---
## 语言规范
python之禅
pythonic
### 命名
## 语法
### 数据
#### 变量定义
#### 作用域
#### 数据结构
### 运算
### 流程控制
#### 条件
#### 循环
### 函数
#### 定义
#### 调用
#### 常用函数
map
filter
range
enumerate
### 导包
```python
import util as u
from util.file_util import read_lines
from util.log_util import *
```
### 异常处理
### AOP
[python_aop](/posts/python-aop/)
### 多线程
### 多线程&多进程
由于**GIL（全局解释器锁）**，Python多线程无法真正并行（仅并发）。
多进程可绕过GIL，实现真正的并行（利用多核CPU）。
多进程：
```python
import os
from multiprocessing import Process
def process_task(name):
print(f"子进程 {name} PID: {os.getpid()}，父进程 PID: {os.getppid()}")
if __name__ == '__main__':
p = Process(target=process_task, args=('child',))
p.start()
p.join()
print(f"主进程 PID: {os.getpid()}")
```
进程池
`from mulitprocessing import Pool`
```python
from multiprocessing import Process, Lock
import time
def process_task(lock, filepath):
with lock:  # 进程间文件访问需要锁
with open(filepath, 'a') as f:
f.write(f"Process {os.getpid()} wrote at {time.time()}\n")
if __name__ == '__main__':
lock = Lock()  # 跨进程锁
filepath = 'shared.log'
processes = [Process(target=process_task, args=(lock, filepath)) for _ in range(3)]
for p in processes:
p.start()
for p in processes:
p.join()
```
多线程
```python
import threading
def thread_task(name):
print(f"线程 {name} 正在执行")
threads = []
for i in range(3):
t = threading.Thread(target=thread_task, args=(f'Thread-{i}',))
threads.append(t)
t.start()
for t in threads:
t.join()
```
线程池
```python
from concurrent.futures import ThreadPoolExecutor
import requests
def fetch_url(url):
response = requests.get(url)
return f"{url}: {len(response.content)} bytes"
urls = ["https://www.python.org", "https://www.google.com", "https://www.github.com"]
# 使用线程池（适合I/O阻塞操作）
with ThreadPoolExecutor(max_workers=3) as executor:
results = list(executor.map(fetch_url, urls))
print(results)
```
锁仅针对于多线程
```python
import threading
counter = 0
lock = threading.Lock()
def increment():
global counter
for _ in range(100000):
with lock:  # 自动获取和释放锁
counter += 1
threads = [threading.Thread(target=increment) for _ in range(5)]
for t in threads:
t.start()
for t in threads:
t.join()
print(f"最终计数器值: {counter}")  # 应该是500000
```
### 文件操作
```python
with open('.bashrc', 'r', encoding='utf-8') as f:
f.readlines()
f.wirtelines()
```
### 网络编程
### 数据库相关
#### redis
```python
import redis
# 连接
pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)
# 操作
r.set('visits', 0)
r.incr('visits')
print(f"Total visits: {r.get('visits').decode()}")
```
#### mysql
SQLAlchemy
```python
import pymysql
# 连接
conn = pymysql.connect(host='localhost', user='root', database='test_db')
try:
with conn.cursor() as cursor:
# 创建表
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(80),
age INT
)
""")
# 插入数据
cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", ('Bob', 30))
conn.commit()
# 查询
cursor.execute("SELECT * FROM users")
print(cursor.fetchall())
finally:
conn.close()
```
#### mongodb
```python
from pymongo import MongoClient
# 连接
client = MongoClient('mongodb://localhost:27017/')
db = client['test_db']
users = db['users']
# 操作
users.insert_one({"name": "Alice", "age": 25})
print(list(users.find({"age": {"$gt": 20}})))
client.close()
```
## 小技巧
[python使用requirements管理依赖](/posts/python-requirements/)
## 类库
[GitHub - Textualize/textual: The lean application framework for Python.  Build sophisticated user interfaces with a simple Python API. Run your apps in the terminal and a web browser.](https://github.com/Textualize/textual)
[GitHub - KimiNewt/pyshark: Python wrapper for tshark, allowing python packet parsing using wireshark dissectors](https://github.com/KimiNewt/pyshark)
bs4
re
lxml
selectsium