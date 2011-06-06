#!/usr/bin/python
# -*- coding: UTF -8 -*-

# NAME:
#   genesis_get_annual_tc_frequency_pdf
#
# AUTHOR:
#   zhengguangyuan, Peking University
#   guanxiaoyuan@gmail.com
#
# PURPOSE:
#   Derive probability density function of typhoon annual occurrence (TAO) by historical data, using Poisson distribution and Negtive Binomial distribution.
#
# INPUTS:
#   An N-elements vector containing historical annual typhoon occurrence.
#
# OPTIONAL INPUTS:
#
# KEYWORD PARAMETERS:
#
# OUTPUTS:
#   A 3 by 2 array. 
#
#   For the first row, the first element is theta of Poisson distribution, 
#   the second element is -9999, and the third element is the P-value of Chi-square test.
#
#   For the second row, the first element is p of Negtive Binomial distribution, 
#   the second element is r of Negtive Binomial distribution, and the third element is the P-value of Chi-square test.
#
# OPTIONAL OUTPUTS:
#
# EXAMPLE:  
#   HIS_TAO = [21,27,23,21,28,23,22,31,23,27,29,30,24,34,32,35,39,27,19,26,36,31,21,32,21,25,21,30,24,24,29,25,23,27,27,29,23,31,32,29,29,31,28,36,23,
#               26,28,16,22,23,26,26,21,29,23,23,24,22,22]
#
#   RESULT = TAO_PDF_get(HIS_TAO)
#   PRINT, RESULT
#    
#   26.4237     -9999.00     0.305581
#   1.20070     -158.000     0.000000

from math import *
from numpy import *
from imsl.stat.poissonCdf import poissonCdf
from scipy.stats.stats import *

#阶乘的计算
def factorial(NUM):
    factorial = long(1)
    for i in range(1, NUM + 1):
        factorial = factorial * i
    return factorial

#台风年发生频次概率密度算法
def genesis_get_annual_tc_frequency_pdf(db, annual_tracknum):

    cur = db.cursor()
    sql = 'SELECT AVG("public"."frequency"."Count") FROM "public"."frequency"'
    cur.execute(sql)
    rows = cur.fetchall()

    print 'occurrence_mean:', rows[0][0]
    occurrence_mean = rows[0][0]    #台风年发生频次的均值

    #sql = 'SELECT STDDEV_POP("public"."frequency"."Count") FROM "public"."frequency"'
    #cur.execute(sql)
    #rows = cur.fetchall()
	
    #print 'occurrence_stdd:', rows[0][0]
    #print 'occurrence_vari through occurrence_stdd:', rows[0][0]**2
    #occurrence_vari = pow(rows[0][0], 2)
    #print 'ssss', occurrence_vari

    sql = 'SELECT VAR_POP("public"."frequency"."Count") FROM "public"."frequency"'
    cur.execute(sql)
    rows = cur.fetchall()
    print 'occurrence_vari:', rows[0][0]
    occurrence_vari = rows[0][0]     #台风年发生频次的方差

    sql = 'SELECT MAX("public"."frequency"."Count") FROM "public"."frequency"'
    cur.execute(sql)
    rows = cur.fetchall()

    print 'occurrence_max:', rows[0][0]
    occurrence_max = rows[0][0]      #台风年发生频次的最大值

    sql = 'SELECT COUNT(*) FROM "public"."frequency"'
    cur.execute(sql)
    rows = cur.fetchall()
    n_year = rows[0][0]
    print "n_year", n_year

    TAO_PDF = [[0, 0, 0], [0, 0, 0]]

    TAO_PDF[0][0] = occurrence_mean
    TAO_PDF[0][1] = -9999.

    TAO_PDF[1][0] = occurrence_mean/occurrence_vari

    print 'p:', TAO_PDF[1][0]

    #print occurrence_vari**2
    TAO_PDF[1][1] = int(round(occurrence_mean * TAO_PDF[1][0] / (1 - TAO_PDF[1][0])))

    Occurrence_Freq = []
    for j in range(occurrence_max + 1):
        Occurrence_Freq.append([])
        for i in range(4):
            Occurrence_Freq[j].append(0.)

    for i in range(occurrence_max+1):
        Occurrence_Freq[i][0] = i

    count_temp = 0
    for i in range(n_year):
        if annual_tracknum[i][1] == 0:
            count_temp = count_temp + 1
    #"the 0th dat:"
    Occurrence_Freq[0][1] = count_temp
    #print Occurrence_Freq[0][1]
    Occurrence_Freq[0][2] = round(poissonCdf(0, occurrence_mean) * n_year)
    #print Occurrence_Freq[0][1]

    #泊松分布
    for i in range(1, occurrence_max + 1):
        count_temp = 0
        for j in range(n_year):
            if annual_tracknum[j][1] == i:
                count_temp = count_temp + 1

        #print "the ", i, "ith data:"
        Occurrence_Freq[i][1] = float(count_temp)
        #print Occurrence_Freq[i][1]
        Occurrence_Freq[i][2] = float((poissonCdf(Occurrence_Freq[i][0], occurrence_mean) - poissonCdf(Occurrence_Freq[i][0] - 1, occurrence_mean))* n_year)
        #print Occurrence_Freq[i][2]
        
    test_obs = []
    test_poi = []

    #
    m = []
    m1 = []
    m2 = []
    
    for i in range(occurrence_max + 1):
        m.append(round(Occurrence_Freq[i][1]) )
        m1.append(round(Occurrence_Freq[i][2]) )
    print 'm'
    for i in range(len(m)):
        print m[i]
    print'm1'
    for i in range(len(m1)):
        print m1[i]
    print 'Xi'
    for i in range(occurrence_max + 1):
        print Occurrence_Freq[i][0]
    print 'Oi'
    for i in range(occurrence_max + 1):
        print Occurrence_Freq[i][1]
    print 'EPi'
    for i in range(occurrence_max + 1):
        print Occurrence_Freq[i][2]

    #

    #泊松分布的卡方检验
    
    for i in range(occurrence_max + 1):
        test_obs.append(Occurrence_Freq[i][1] + 0.04 )
        test_poi.append(Occurrence_Freq[i][2] + 0.04 )
        #print "test_obs", i, test_obs[i], "test_poi", i, test_poi[i]
    #result_xsq = chisquare(Occurrence_Freq[0:occurrence_max + 1][1],Occurrence_Freq[0:occurrence_max + 1][2])

    obs = array(test_obs)
    print 'obs:'
    print obs
    poisson = array(test_poi)
    print 'poisson:'
    print poisson
    
    result_xsq = chisquare(obs, poisson)
    print 'xsq:', result_xsq
    TAO_PDF[0][2] = result_xsq[1]
    print 'p-value:', TAO_PDF[0][2]

    #负二项分布及卡方检验
    if TAO_PDF[1][0] < 1:
        for i in range(0, occurrence_max + 1):
            Occurrence_Freq[i][3] = float(((TAO_PDF[1][0]**TAO_PDF[1][1]) * ((1-TAO_PDF[1][0])**Occurrence_Freq[i][0]) * factorial(TAO_PDF[1][1]+Occurrence_Freq[i][0]-1)/(factorial(Occurrence_Freq[i][0])*factorial(TAO_PDF[1][1]-1)))*n_year)

        test_neg = []
        for i in range(occurrence_max + 1):
            test_neg.append(Occurrence_Freq[i][3] + 0.04 )
            #print "test_obs", i, test_obs[i], "test_neg", i, test_neg[i]

        neg = array(test_neg)
        print 'obs:'
        print obs
        print 'neg:'
        print neg
        result_xsq = chisquare(obs, neg)
        #result_xsq = chisquare(Occurrence_Freq[0:occurrence_max + 1][1],Occurrence_Freq[0:occurrence_max + 1][3])

        print 'xsp:', result_xsq
        TAO_PDF[1][2] = result_xsq[1]
        
    else:
        TAO_PDF[1][2] = 0

    print 'p-value:', TAO_PDF[1][2]

    #

    print 'ENi'
    for i in range(occurrence_max + 1):
        print Occurrence_Freq[i][3]
    print 'm2'
    for i in range(occurrence_max + 1):
        m2.append(round(Occurrence_Freq[i][3]) )
    for i in range(len(m2)):
        print m2[i]
    print 'TAO_PDF'
    print TAO_PDF
    #
    
    return TAO_PDF
