#!/usr/bin/python
# coding=utf8

import re
import string
import time

DEBUG = 0

# open & read source html file
html = open('./html')
html_context = html.read()

# open target result file
result = open('./result', 'a+')

# full_rate
r_full = re.compile(r">满班率<.*?>(\d{1,3}\.\d{2})%<.*?<!--原老师续报率计算-->", re.S)
full_rate = re.findall(r_full, html_context)
if DEBUG == 1 :
	print "full_rate :\n" + str(full_rate)

# quit_rate
r_quit = re.compile(r">开课后退费率<.*?>(\d{1,3}\.\d{2})%<.*?<!--学而思续报率计算-->", re.S)
quit_rate = re.findall(r_quit, html_context)
if DEBUG == 1 :
	print "quit_rate :\n" + str(quit_rate)
	
# spring_rate
r_spring = re.compile(r"春续暑续报率.*?>\(学而思\)<.*?>(\d{1,3}\.\d{2})%<", re.S)
spring_rate = re.findall(r_spring, html_context)
if DEBUG == 1 :
	print "spring_rate :\n" + str(spring_rate)

# autumn_rate
r_autumn = re.compile(r">\(学而思\)<.*?春续秋续报率.*?>\(学而思\)<.*?>(\d{1,3}\.\d{2})%<", re.S)
autumn_rate = re.findall(r_autumn, html_context)
if DEBUG == 1 :
	print "autumn rate :\n" + str(autumn_rate)

# get class number
class_num = len(full_rate)

# get four average values
sum_full = 0.0
sum_quit = 0.0
sum_spring = 0.0
sum_autumn = 0.0

for class_i in range(class_num) :
	sum_full = sum_full + string.atof(full_rate[class_i])
	sum_quit = sum_quit + string.atof(quit_rate[class_i])
	sum_spring = sum_spring + string.atof(spring_rate[class_i])
	sum_autumn = sum_autumn + string.atof(autumn_rate[class_i])

ave_full = sum_full / class_num / 100
ave_quit = sum_quit / class_num / 100 
ave_spring = sum_spring / class_num / 100
ave_autumn = sum_autumn / class_num / 100

# calculate final score and level
score = ((ave_spring + ave_autumn) / 2 * 1.6  + ave_full * 0.4 - ave_quit * 2.0) * 50

if score >= 90 :
	level = 'S'
elif score >= 85 :
	level = 'A'
elif score >= 80 :
	level = 'B'
else : 
	level = 'NOT defined'

# output results to result file
local_time = time.localtime(time.time())
current_time = time.strftime('%Y-%m-%d %H:%M:%S\n', local_time) 
result.writelines(current_time)
result.writelines("--------------------\n")
result.writelines("满班率\t: %0.2f" % (ave_full * 100) + " %\n")
result.writelines("退费率\t: %0.2f" % (ave_quit * 100) + " %\n")
result.writelines("春续报\t: %0.2f" % (ave_spring * 100) + " %\n")
result.writelines("秋续报\t: %0.2f" % (ave_autumn * 100) + " %\n")
result.writelines("--------------------\n")
result.writelines("总分\t: %0.2f" % (score) + "\n")
result.writelines("等级\t: " + level + "\n\n\n")

# close source html file & result file
html.close();
result.close();
