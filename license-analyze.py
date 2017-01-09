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
    tmpReverse  = {}
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
                if result[0] in tmpReverse:
                    print('>>> aliases ' + result[0] + ' Alias also target')
                if result[1] in tmpData:
                    print('>>> aliases ' + result[0] + ' Target also alias')
                if result[0].lower() != result[0]:
                    print('>>> aliases ' + result[0] + ' Alias contains capital letters')
                if result[1].lower() != result[1]:
                    print('>>> aliases ' + result[1] + ' Target contains capital letters')
                tmpData[result[0]] = result[1]
                tmpReverse[result[1]] = result[0]
        oldTarget = ''
        doSort = False
        for entry in tmpData:
            if tmpData[entry] < oldTarget:
                doSort = True
                break
            oldTarget = tmpData[entry]
        if doSort:
            for i in sorted(tmpReverse):
                rawData[tmpReverse[i]] = i
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
    try:
        with open(fileName, 'r') as fp:
            for line in fp:
                line = line[:-1]
                if line.startswith('#') or line.startswith(' ') or len(line) == 0:
                    continue
                mail = line[:line.index(';')]
                if mail.lower() != mail:
                    print('>>> personalLicense.csv ' + mail + ' mail contains capital letters')
                rawData.append(mail)
    except Exception as e:
      print('Error load file ' + fileName + ' due to ' + str(e))
      rawData = None
    return rawData



def load_wiki(homeDir):
    rawData = []
    fileName = homeDir + 'wiki.txt'
    try:
      fp = open(fileName, encoding='utf-8')
      inx = 0
      for line in fp:
        line = line[:-1]
        inx += 1
        if inx == 1:
          eName = line
        elif inx == 2:
          eMail = line
        elif inx == 3:
          eLicense = line
        elif inx == 4:
          if not line.startswith('>-'):
            raise Exception('convert problem')
          if eMail in rawData['licensedWiki']:
            raise Exception('already there')
          if '@' not in eMail or not eLicense.startswith('http'):
            print('illegal license email(' + eMail + ') license(' + eLicense + ')')
          else:
            rawData['licensedWiki'][eMail] = {'name': eName, 'license': eLicense}
          inx = 0
      fp.close()
    except Exception as e:
      print('Error load file ' + fileName + ' due to ' + str(e))
      rawData = None

    fileName = homeDir + 'gitdm-config/known-licensee.csv'
    try:
      fp = open(fileName, encoding='utf-8')
      for line in fp:
        if len(line) == 1 or line.startswith('#'):
          continue
        line = line[:-1]
        arr = line.split(',')
        eName = arr[0]
        eMail = arr[1]
        eLic = arr[3]
        if eMail.startswith('{{nospam'):
          arr = eMail[:-2].split('|')
          eMail = arr[1] + '@' + arr[2]
          for i in range(3,len(arr)):
            eMail += '.' + arr[i]
        if eMail.startswith('@'):
          rawData['corporate'][eMail] = {'name': eName, 'license': eLic}
        elif eMail not in rawData['licensedFile']:
          rawData['licensedFile'][eMail] = {'name': eName, 'license': eLic}
      fp.close()
    except Exception as e:
      print('Error load file ' + fileName + ' due to ' + str(e))
      rawData = None
    return rawData






def runCompare(homedir):
    dataAliases = load_alias(homedir)
    dataDomainMail = load_domainmap(homedir)
    dataLicenseMail = load_licensePersonal(homedir)
    dataWiki = load_wiki(homedir)


if __name__ == '__main__':
    runCompare('./')
