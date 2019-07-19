#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request
import sys
import os
import time
import csv
import traceback

def makedirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def download():
    yearDict = {"A":"2015","B":"2016","C":"2017","D":"2018"}
    pdfAmountDict = {"A":310,"B":620,"C":452,"D":1000}
    csvHeader = ['YEAR', 'SYNBOL','NUMBER','RESULT']
    csvBody = []
    failureNum = 0
    proxy = urllib.request.ProxyHandler({'http': '127.0.0.1'})
    print(proxy)
    opener = urllib.request.build_opener(proxy)
    urllib.request.install_opener(opener)
    for symbol, year in yearDict.items():
        makedirs(year)
        for x in range(1,pdfAmountDict[symbol]+1):
            if failureNum >= 10:
                break
            url = "https://www.fld.caa.go.jp/caaks/cssc06/youshiki5?yousiki5216File={0}{1}%255C{0}{1}_youshiki5.pdf".format(symbol, x)
            title = "{0}/{1}{2}-V.pdf".format(year, symbol, x)
            row = [year,symbol,x]
            try:
                print("{0}：".format(title), end="")
                urllib.request.urlretrieve(url,"{0}".format(title))
                print("SUCCESS!")
                row.append("○")
                if symbol == "D" :
                    failureNum = 0
            except:
                print("FAILURE!!!!!")
                traceback.print_exc()
                row.append("×")
                if symbol == "D" :
                    failureNum+=1
            csvBody.append(row)
            time.sleep(1)
    print(csvHeader)
    print(csvBody)
    with open('result.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(csvHeader)
        writer.writerows(csvBody)
                
if __name__ == "__main__":
    download()
