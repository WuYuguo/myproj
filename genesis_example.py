#!/usr/bin/python
# -*- coding: UTF -8 -*-

import pgdb
import numpy
import random
#from osgeo import ogr
from math import asin,sin,cos,acos,radians,degrees,pow,sqrt,hypot,pi
from genesis_sim import *
from genesis_read_his import *
from genesis_read_all import *
from genesis_read_end import *

global n_years_sim   #模拟台风的年数
global x0            #研究区域经度左侧边缘
global y0            #研究区域纬度下侧边缘
global n_cols        #经度栅格数
global n_rows        #纬度栅格数
global grid_size     #栅格大小
global R             #设定的相关圆的半径
#global n_years     

n_years_sim = 60
x0          = 100
y0          = 0
n_cols      = 160
n_rows      = 70
grid_size   = 0.5
R           = 200
#n_years     = 60

#连接数据库
dbh = pgdb.connect(host = '162.105.17.236', database = 'typhoon', user = 'postgres', password = 'pg123')
#cur = db.cursor()

#import psycopg2
#dbh = psycopg2.connect("dbname = 'typhoon' user = 'postgres' password = 'pg123'")

global db
db = dbh

#读取起始点数据
genesis_his_dat = genesis_read_his(db)
#print genesis_his_dat[0]
#读取所有点数据
genesis_all_dat = genesis_read_all(db)
#print genesis_all_dat[0]
#读取终止点数据
genesis_end_dat = genesis_read_end(db)

#f = file("C:\VERSION FOR GENESIS_SIM\genesis_sim 5.28 afternoon\dat\history_typhoon_end_data.txt", "a +")
#f.write("Lon\tLat\n")
#for i in range(len(genesis_end_dat)):
#    f.write( str(genesis_end_dat[i][0]) + '\t' + str(genesis_end_dat[i][1]) + '\n')
#f.close()

#print "Lon\tLat"
#for i in range(len(genesis_end_dat)):
    #print	genesis_end_dat[i][0],	genesis_end_dat[i][1]
#print genesis_end_dat[0]
#路径模拟
genesis_sim(db, genesis_his_dat, n_years_sim, x0, y0, n_cols, n_rows, grid_size, R, genesis_all_dat, genesis_end_dat)












