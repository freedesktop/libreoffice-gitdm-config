#!/usr/bin/env python3
#
# This file is part of the LibreOffice project.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#



### DESCRIPTION
#
# This program controls the license files:
# 1) loads aliases, license*, domain-map
# 2) write sorted versions of aliases (special handling due to ' ' seperator) and license*
# 3) look for and load wiki.txt
# 4) check consistency
# 5) write newwiki.txt with wiki updates
# 6) write warnings about inconsistences
#



import sys
import csv
import io
import os
import operator
import datetime
import collections



def load_alias(homeDir):
    rawData = collections.OrderedDict()
    tmpData = collections.OrderedDict()
    fileName = homeDir + 'aliases'

    try:
        with open(fileName, 'r') as fp:
            for line in fp:
                line = line[:-1]
                if line.startswith('#') or line.startswith(' ') or len(line) == 0:
                    continue
                if line.startswith('"'):
                    x = line.index('"', 1)
                    result = [line[1:x], line[x+2:]]
                else:
                    result = line.split(' ')
                if result[0] in tmpData:
                    print('>>> aliases ' + result[0] + ' DUPLICATED')
                if result[1] in tmpData:
                    print('>>> aliases ' + result[0] + ' Target also alias')
                if result[0].lower() != result[0]:
                    print('>>> aliases ' + result[0] + ' Alias contains capital letters')
                if result[1].lower() != result[1]:
                    print('>>> aliases ' + result[1] + ' Target contains capital letters')
                if result[0] == result[1]:
                    print('>>> aliases ' + result[0] + ' Target == Alias')
                for i in tmpData:
                    if result[0] == tmpData[i]:
                        print('>>> aliases ' + result[0] + ' Alias also target')
                        break
                tmpData[result[0]] = result[1]
        oldTarget = ''
        doSort = False
        for entry in tmpData:
            if tmpData[entry] < oldTarget:
                doSort = True
                break
            oldTarget = tmpData[entry]
        if doSort:
            s = [(k, tmpData[k]) for k in sorted(tmpData, key=tmpData.get)]
            for i in s:
                rawData[i[0]] = i[1]
            with open(fileName, 'w') as fp:
                for entry in rawData:
                    if ' ' in entry:
                        print('"' + entry + '" ' + rawData[entry], file=fp)
                    else:
                        print(entry + ' ' + rawData[entry], file=fp)
        else:
            rawData = tmpData
    except Exception as e:
      print('>>> Error load file ' + fileName + ' due to ' + str(e))
      rawData = None
    return rawData



def load_domainmap(homeDir):
    rawData = []
    fileName = homeDir + 'domain-map'
    try:
        with open(fileName, 'r') as fp:
            for line in fp:
                line = line[:-1]
                if line.startswith('#') or line.startswith(' ') or len(line) == 0:
                    continue
                if '\t' in line:
                    mail = line[:line.index('\t')]
                else:
                    mail = line[:line.index(' ')]
                if '@' in mail and mail not in rawData:
                    if mail.lower() != mail:
                        print('>>> domain-map ' + mail + ' mail contains capital letters')
                    rawData.append(mail)
    except Exception as e:
      print('Error load file ' + fileName + ' due to ' + str(e))
      rawData = None
    return rawData



def load_licensePersonal(homeDir):
    rawData = []
    fileName = homeDir + 'licensePersonal.csv'
    orgText = []
    try:
        with open(fileName, 'r') as fp:
            for line in fp:
                line = line[:-1]
                orgText.append(line)
                if line.startswith('#') or line.startswith(' ') or len(line) == 0:
                    continue
                mail = line[:line.index(';')]
                if mail.lower() != mail:
                    print('>>> personalLicense.csv ' + mail + ' mail contains capital letters')
                if mail in rawData:
                    print('>>> personalLicense.csv ' + mail + ' duplicate')
                rawData.append(mail)
        newText = sorted(orgText)
        if newText != orgText:
            with open(fileName, 'w') as fp:
                for line in newText:
                   print(line, file=fp)
    except Exception as e:
      print('Error load file ' + fileName + ' due to ' + str(e))
      rawData = None
    return rawData



def load_wiki(homeDir):
    rawData = []
    fileName = homeDir + 'wiki.txt'
    try:
        with open(fileName, 'r') as fp:
            doCollect = 0
            for line in fp:
                line = line[:-1]
                if line.startswith('{|'):
                    doCollect = 1
    except Exception as e:
      print('Error load file ' + fileName + ' due to ' + str(e))
      rawData = None

    return rawData



def checkConsistency(aliases, domain, license):
    for dMail in domain:
        if not dMail in license:
            print('>>> domain-map ' + dMail + ' not in licensePersonal !')
        if dMail in aliases:
            print('>>> domain-map ' + dMail + ' used as aliaes in aliases !')
    for entry in aliases:
        if entry in license:
            print('>>> aliases ' + entry + ' alias is licensed !')
        if not aliases[entry] in license:
            print('>>> aliases ' + aliases[entry] + ' target is not licensed !')



def runCompare(homedir):
    dataAliases = load_alias(homedir)
    dataDomainMail = load_domainmap(homedir)
    dataLicenseMail = load_licensePersonal(homedir)
#    dataWiki = load_wiki(homedir)

    checkConsistency(dataAliases, dataDomainMail, dataLicenseMail)


if __name__ == '__main__':
    runCompare('./')
