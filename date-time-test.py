"""时间处理  """
__author__on__ = 'shaozhiqi  2019/9/25'

# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------datetime---------------------------------------
from datetime import datetime, timedelta

now = datetime.now()  # 获取当前datetime
print(now)  # 2019-09-25 14:43:15.124296
print(type(now))  # <class 'datetime.datetime'>

# 如果仅导入import datetime，则必须引用全名datetime.datetime。
# datetime.now()返回当前日期和时间，其类型是datetime。

# 要指定某个日期和时间，我们直接用参数构造一个datetime：
dt = datetime(2019, 4, 19, 12, 20)  # 用指定日期时间创建datetime
print(dt)  # 2019-04-19 12:20:00

# ------------------------------------------------datetime转换为timestamp------------------------------------------
# 在计算机中，时间实际上是用数字表示的。我们把1970年1月1日 00:00:00 UTC+00:00时区的时刻称为epoch time，
# 记为0（1970年以前的时间timestamp为负数），当前时间就是相对于epoch time的秒数，称为timestamp。
# 可见timestamp的值与时区毫无关系，因为timestamp一旦确定，其UTC时间就确定了，转换到任意时区的时间也是完全确定的，
# 这就是为什么计算机存储的当前时间是以timestamp表示的，因为全球各地的计算机在任意时刻的timestamp都是完全相同的（假定时间已校准）。
dt = datetime(2015, 4, 19, 12, 20)  # 用指定日期时间创建datetime
print(dt.timestamp())  # 把datetime转换为timestamp
# 1429417200.0
# 注意Python的timestamp是一个浮点数。如果有小数位，小数位表示毫秒数。
# 某些编程语言（如Java和JavaScript）的timestamp使用整数表示毫秒数，这种情况下只需要把timestamp除以1000就得到Python的浮点表示方法。

# --------------------------------------------------timestamp转换为datetime----------------------------------------
# 要把timestamp转换为datetime，使用datetime提供的fromtimestamp()方法：
t = 1429417200.0
print(datetime.fromtimestamp(t))  # 2015-04-19 12:20:00

# 注意到timestamp是一个浮点数，它没有时区的概念，而datetime是有时区的。上述转换是在timestamp和本地时间做转换。
# 本地时间是指当前操作系统设定的时区。例如北京时区是东8区，则本地时间：
#  2015-04-19 12:20:00

# --------------------------------------------------str转换为datetime-------------------------------------------------
# 很多时候，用户输入的日期和时间是字符串，要处理日期和时间，首先必须把str转换为datetime。
# 转换方法是通过datetime.strptime()实现，需要一个日期和时间的格式化字符串：

cday = datetime.strptime('2019-6-1 18:19:59', '%Y-%m-%d %H:%M:%S')
print(cday)  # 2019-06-01 18:19:59

# ----------------------------------------------------datetime转换为str------------------------------------------------
# 如果已经有了datetime对象，要把它格式化为字符串显示给用户，就需要转换为str，转换方法是通过strftime()实现的，同样需要一个日期和时间的格式化字符串：

now = datetime.now()
print(now.strftime('%a, %b %d %H:%M'))  # Wed, Sep 25 14:56# ------------------------------------------------datetime加减--------------------------------------------------------now = datetime.now()print('now1:', now)  # now1: 2019-09-25 18:40:57.979018now2=now + timedelta(hours=10)print('now2:', now2)  # now2: 2019-09-26 04:40:57.979018now3=now - timedelta(days=1)print('now3:', now3)  # now3: 2019-09-24 18:40:57.979018now4=now + timedelta(days=2, hours=12)print('now4:', now4)  # now4: 2019-09-28 06:40:57.979018