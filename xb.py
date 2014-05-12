#!/usr/bin/python
# coding=utf8

import re
import string

# read html file
html = open('./html')
html_context = html.read()

# full
r_full = re.compile(r">满班率<.*?>(\d{1,3}\.\d{2})%<.*?<!--原老师续报率计算-->", re.S)
full_rate = re.findall(r_full, html_context)
#print full_rate

# quit
r_quit = re.compile(r">开课后退费率<.*?>(\d{1,3}\.\d{2})%<.*?<!--学而思续报率计算-->", re.S)
quit_rate = re.findall(r_quit, html_context)
#print quit_rate

# spring
r_spring = re.compile(r"春续暑续报率.*?>\(学而思\)<.*?>(\d{1,3}\.\d{2})%<", re.S)
spring_rate = re.findall(r_spring, html_context)
#print spring_rate

# autumn
r_autumn = re.compile(r">\(学而思\)<.*?春续秋续报率.*?>\(学而思\)<.*?>(\d{1,3}\.\d{2})%<", re.S)
autumn_rate = re.findall(r_autumn, html_context)
#print autumn_rate

# class num
class_num = len(full_rate)

# get average value
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

print "满班率 : %0.2f" % (ave_full * 100) + "%"
print "退费率 : %0.2f" % (ave_quit * 100) + "%"
print "春季续报率 : %0.2f" % (ave_spring * 100) + "%"
print "秋季续报率 : %0.2f" % (ave_autumn * 100) + "%"

score = ((ave_spring + ave_autumn) / 2 * 1.6  + ave_full * 0.4 - ave_quit * 2.0) * 50
print "总分 : " + str(score)

# close html file
html.close();
