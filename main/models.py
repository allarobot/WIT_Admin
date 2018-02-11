# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from functools import reduce
import datetime
import pandas as pd
import os
import re
"""
Created on Tue Dec 19 13:18:54 2017

@author: COMAC
"""

class FindFiles(object):
    def __init__(self, folder_in = None, fileExt = '.txt'):
        self._rawfiles = []        
        try:
            for rt, dirs, files in os.walk(folder_in, topdown=False):
                for fl in files:
                    
                    fl = os.path.join(rt, fl)
                    fl = os.path.abspath(fl)
                    f = os.path.splitext(fl)
                    if f[1] == fileExt:
                        self._rawfiles.append(fl)

        except:
            print("Error Happen! ")

    def path(self):
        return self._rawfiles


class Jsw:
    '''
    info=[connector1,pin1,connector2,pin2,chapter,testType]
    '''
    columns = ['connector1','pin1','connector2','pin2','chapter','pin1Type','pin2Type']
    test_type = ['continuity','insulation']
    sheet_in = [u'连续性测试表', u'接地线导通测试表']
    pin_type = ['auto','tb','nap']

    def __init__(self, fin):
        self._fin = fin
        self.info_pv, self.info_g = None, None
        self._process()
        
    def _process(self):
        data_in = pd.read_excel(self._fin, sheet_name=Jsw.sheet_in[0])
        data_in = self._strcleanning(data_in)
        data_in2 = pd.read_excel(self._fin, sheet_name=Jsw.sheet_in[1])
        data_in2 = self._strcleanning(data_in2)
        # print(data_in)
        # print(data_in2)
        self.info_pv = self._pinType(data_in)
        self.info_pv.columns = Jsw.columns
        self.info_g = self._pinType(data_in2)
        self.info_g.columns = Jsw.columns

    def _strcleanning(self,pd):
        '''
        get useful information from pd at column of [0, 1, 3, 4, 6]
        :param pd:
        :return:
        '''
        pd = pd.fillna('')
        row, col = pd.shape
        # print("before", pd.loc[0][0])

        unicode = str ##python3
        for i in range(row):
            pd.loc[i] = [unicode(x).replace(' ','') for x in pd.loc[i]]
        # print("after", pd.loc[0][0])
        column = [0, 1, 3, 4, 6]
        pd = pd.iloc[:, column]
        return pd

    def _hasTB(self,row_data):
        '''
        whether 'TB' in row elements.upper()
        :param row_data:
        :return:
        '''
        for data in row_data:
            if u"TB" in data.upper():
                return True
        return False
    
    def _valid(self, data):
        '''
        cnt1,cnt2 must be a combination of 0-9,a-z,A-Z,'-'
        '''
        mat1 = re.match("[\w-]+", data)
        if mat1 and data == mat1.group():
            return True
        return False


    def _pinType(self,df):
        row, col = df.shape
        pin1Type = []
        pin2Type = []
        for r in range(row):
            cnt1,index1,cnt2,index2,chapter = df.iloc[r]
            pin1Type.append('auto')
            pin2Type.append('auto')
            if self._hasTB((cnt1,index1)):
                pin1Type[r] = 'tb'
            elif not self._valid(cnt1):
                pin1Type[r] = 'nap'
            if self._hasTB((cnt2,index2)):
                pin2Type[r] = 'tb'
            elif not self._valid(cnt2):
                pin2Type[r] = 'nap'
        df['pin1Type'] = pin1Type
        df['pin2Type'] = pin2Type
        return df


class Pgv:
    '''
    info=[connector1,pin1,connector2,pin2,chapter,\
    testType,status,value,unit,addr1,addr2]
    '''
    columns = ["connector1", "pin1", "connector2", "pin2", "testType", "status", "value", "unit", "pin1_addr", "pin2_addr"]
    typedic = {'FC': 'insulation', 'CC': 'continuity'}
    info_pattern = r"(?<=:)\s+([A-Z]{2})\s+([0-9]+)\s+([\S]+)\s*:\s+([0-9]+)\s+([A-Z]+)\s+([<>0-9.MK]+)\s+([A-Z]+)\s+([\S]+)"
    time_pattern = r"(?<=测试中止)\s+([0-9]+[\s\S]+[0-9]+)\s*分析仪停止"

    def __init__(self, file_in):
        '''
        '''
        self._file_in = file_in
        self.pdTestLists = None
        self.strDateTime = ""
        self._process()

    def _process(self):
        '''
        In -- TXT file of testing report
        Return -- [[ ],...]        
        '''
        fp = open(self._file_in, U'r')
        txt = fp.read()
        lists = []
        time = ""
        re1 = re.compile(Pgv.info_pattern+"|"+Pgv.time_pattern)
        for mat in re1.finditer(txt):
            # print(mat.groups())
            line = mat.groups() #["command","addr1","pin1","addr2","status","value","unit","pin2"]
            if reduce(lambda x,y: x and y,line[:8] ):
                # print("line[:8]",line[:8])
                pin1_addr, pin2_addr, status, value, unit = line[1], line[3], line[4], line[5], line[6]
                connector1, pin1 = self._connector_index(line[2])
                connector2, pin2 = self._connector_index(line[7])
                test_type = Pgv.typedic.get(line[0], 'NULL')
                line = [connector1, pin1, connector2, pin2, test_type, status, value, unit, pin1_addr, pin2_addr]
                lists.append(line)
            elif line[8]:
                time = line[8]
        fp.close()
        self.pdTestLists = pd.DataFrame(lists, columns=Pgv.columns)
        self.strDateTime = time
        print(self.info_lists.shape)

    def _connector_index(self, pin_name):
        '''
        Can be omitted!
        In -- pin name
        Return -- Connector name
        this is hardcoding method, don't fit every case
        '''
        # print("pin_name",pin_name)
        re1 = re.compile("[0-9A-Z]+-*[0-9A-Z]*-*[0-9A-Z]*")
        mt = re1.search(pin_name)
        if mt:
            cnt = mt.group(0)
            return cnt, pin_name[len(cnt)+1:]
        else:
            return pin_name, ''


class Format(object):
    def __init__(self, data):
        self._data = data

    def jsons_to_DF(self):

        return pd.DataFrame(self._data)

    # def continuty_test(self, df, start):
    #     row, col = df.shape
    #     data_out = pd.DataFrame(np.zeros((row * 2, 4)), dtype=str, columns=txt_out._col_name)
    #     for r_n in range(row):
    #         data_out.iloc[r_n * 2, 0:] = start, u'X-' + df.iloc[r_n, 0] + '-' + str(df.iloc[r_n, 1]), u'ATA-' + \
    #                                      df.iloc[r_n, 6].split('-')[0] + '-B1', u''
    #         data_out.iloc[r_n * 2 + 1, 0:] = u'', u'C-' + df.iloc[r_n, 3] + '-' + str(
    #             df.iloc[r_n, 4]), u'ATA-' + df.iloc[r_n, 6].split('-')[0] + '-B1', u''
    #         start += 1
    #     return data_out, start
    #
    # def _gnd_test(self, df, start):
    #     row, col = df.shape
    #     data_out = pd.DataFrame(np.zeros((row * 2, 4)), dtype=str, columns=txt_out._col_name)
    #     for r_n in range(row):
    #         data_out.iloc[r_n * 2, 0:] = start, u'X-' + df.iloc[r_n, 0] + '-' + str(df.iloc[r_n, 1]), u'ATA-' + \
    #                                      df.iloc[r_n, 6].split('-')[0] + '-B2', u''
    #         data_out.iloc[r_n * 2 + 1, 0:] = u'', u'C-' + df.iloc[r_n, 3], u'ATA-' + df.iloc[r_n, 6].split('-')[
    #             0] + '-B2', u''
    #         start += 1
    #     return data_out, start
    #
    # def _ratio(self):
    #     '''
    #     calculate the ratio of HIGH result
    #     In -- {Node:(PASS number,HIGH number)}
    #     Return -- {Node: HIGH ratio}
    #     '''
    #     for key in self._stats:
    #         n_pass, n_high, _t = self._stats[key]
    #         self._stats[key] = n_pass, n_high, float(n_pass) / (n_pass + n_high)
    #
    # def _stats_sort(self, threshold=0.5):
    #     '''
    #     In -- {Connector: PASS Number,HIGH Number,PASS ratio,...}
    #     Return -- [(Node,ratio),...] with decrease order ,and > threshold
    #     '''
    #     lst = sorted(self._stats.items(), key=lambda d: sum(d[1]), reverse=True)
    #     lst = sorted(lst, key=lambda d: d[1][2], reverse=False)
    #     lst = filter(lambda d: d[1][2] > threshold, lst)
    #     return lst
    #
    # def _count(self):
    #     '''
    #     {'Connector Name':(PASS number,HIGH number,PASS ratio)}
    #     '''
    #     result = dict()
    #     row, col = self._lists.shape
    #     for i in range(row):
    #         info = self._lists.iloc[i]
    #         #            print(info)
    #         status, pin_a, pin_b = info[4], info[2], info[7]
    #         connector_a, connector_b = self._connector(pin_a), self._connector(pin_b)
    #         valueA = result.get(connector_a, (0, 0, 0))
    #         valueB = result.get(connector_b, (0, 0, 0))
    #         if status == 'PASS':
    #             result[connector_a] = (valueA[0] + 1, valueA[1], 0)
    #             result[connector_b] = (valueB[0] + 1, valueB[1], 0)
    #         elif status == 'HIGH':
    #             result[connector_a] = (valueA[0], valueA[1] + 1, 0)
    #             result[connector_b] = (valueB[0], valueB[1] + 1, 0)
    #     #        print(result)
    #     self._stats = result
    #
    # def analysis(self):
    #     '''
    #     '''
    #     self._lists_from_log()
    #     self._count()
    #     self._ratio()

    def jsons_to_testprog(self, start=0):
        '''
        '''
        col_data = [u"PIN1", u"PIN2", u"CHAPTER"]
        col_prog = [u"No", u"测试程序", u"章节号", u"备注"]
        No, pins, chapter = [], [], []
        high_line = self.jsons_DF()
        row, col = high_line.shape
        for i in range(row):
            No.append(str(start + i))
            pins.append(u"X-"+high_line[col_data[0]].iloc[i])
            chapter.append(high_line[col_data[2]].iloc[i])
            No.append("")
            pins.append(u"C-"+high_line[col_data[1]].iloc[i])
            chapter.append(high_line[col_data[2]].iloc[i])
        pd_prog = pd.DataFrame([], columns=col_prog)
        pd_prog[col_prog[0]] = No
        pd_prog[col_prog[1]] = pins
        pd_prog[col_prog[2]] = chapter

        return pd_prog

    # def to_txt_report(self, thr=0.5):
    #     '''
    #     Print out
    #     '''
    #     lst = self._stats_sort(threshold=thr)
    #     str_line = "===Node Name===PASS Ratio===\n"
    #     for item in lst:
    #         connector, passratio = item[0], item[1][2]
    #         str_line += "%12s%10.2f%%\n" % (connector, passratio * 100)
    #
    #     with open(self._report_out, 'w') as fp:
    #         fp.write(str_line)

class Save(object):
    keys = (u'chapter', u'pin1', u'pin2')
    col_name = (u'No', u'测试程序', u'章节号', u'备注')

    def __init__(self, data):
        self.pdData = data
        pass

    def to_txt(self, path, fmt=None):
        column = self.pdData.columns
        n_row, n_col = self.pdData.shape
        header = ''
        for item in column:
            header += "{0:=^20}".format(item)
        header += "\n"
        lines = header
        for r in range(n_row):
            line = ''
            for item in self.pdData.iloc[r]:
                line += "{0:20}".format(item)
            line += '\n'
            lines += line
        with open(path, 'w') as fp:
            fp.write(lines)

    def to_csv(self, path, fmt=None):
        '''
        Print out
        '''
        self.pdData.to_csv(path, encoding='utf-8')

    def to_excel(self, path, sheet_name="sheet_1", fmt='noindex'):
        idx = True
        if fmt == "noindex":
            idx = False

        self.pdData.to_excel(path, sheet_name=sheet_name, encoding='utf-8',index=idx)

    def to_html(self, path, fmt=None):
        with open(path, 'wb') as fp:
            str_out = self.pdData.to_html()
            fp.write(str_out.encode('utf-8'))


class DTime(object):
    def __init__(self,strDTime):
        self._datetime = datetime.datetime.strptime(strDTime,"%y %b %d  %X")
        self.year = self._datetime.year
        self.month = self._datetime.month
        self.day = self._datetime.day
        self.hour = self._datetime.hour
        self.minute = self._datetime.minute
        self.second = self._datetime.second

