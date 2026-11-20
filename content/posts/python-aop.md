---
title: python_aop
date: 2026-04-03T00:00:00+08:00
draft: false
slug: python-aop
tags: [Python, 编程语言]
source: 02-Knowledge/编程/python_aop.md
---
## 前置知识
**切面(Aspect)**: 封装横切关注点的模块
**连接点(Join Point)**: 程序执行过程中的特定点(如方法调用)
**通知(Advice)**: 在连接点执行的动作(如方法执行前后)
**切入点(Pointcut)**: 定义哪些连接点会被通知影响
## 一般写法
### 装饰器
```python
def log_aspect(func):
def wrapper(*args, **kwargs):
print(f"开始执行: {func.__name__}")
result = func(*args, **kwargs)
print(f"结束执行: {func.__name__}")
return result
return wrapper
@log_aspect
def business_method():
print("执行业务逻辑...")
business_method()
```
### 使用类装饰器
```python
class TransactionAspect:
def __init__(self, func):
self.func = func
def __call__(self, *args, **kwargs):
print("开启事务")
try:
result = self.func(*args, **kwargs)
print("提交事务")
return result
except Exception as e:
print("回滚事务")
raise e
@TransactionAspect
def process_order():
print("处理订单业务...")
process_order()
```
### 使用上下文管理器
```python
class PerformanceAspect:
def __enter__(self):
self.start = time.time()
def __exit__(self, exc_type, exc_val, exc_tb):
print(f"耗时: {time.time() - self.start:.4f}秒")
def business_logic():
with PerformanceAspect():
print("执行业务逻辑...")
time.sleep(1)
business_logic()
```