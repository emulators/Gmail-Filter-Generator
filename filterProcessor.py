# -*- coding: utf-8 -*
'''
預定: 

產出格式: 
*@ foo.bar OR 
*@ bbo.foo OR
…

用 set 保存
每次輸入, 先檢查是否符合 email 格式 (用 reg exp 檢查 )
再把前面改成星號
確認舊集合個數
再放入 set裡面
確認新集合個數
比較新舊 (放入前與放入後) 集合個數有沒有變
有變 => 
    把集合內容寫入文字檔 (記得要加 OR )
    讀取文字檔
沒變 => 
    不用動

讀取文字檔的步驟:
每一行分別讀進 list
再把每個 entry 去掉 OR和空白
再把 list 轉成集合
再把集合中每個 entry填到 GUI的清單內
'''
import re
import sys

class FilterProcessor:
    filterSet = None
    
    def __init__(self, setObject):
        fs = setObject
        #
        if not isinstance(setObject, set):
            fs = set(setObject) # convert to set
        self.filterSet = fs
    
    def AddToSet(self, email):
        fltr = self.stripLeftPart(email)
        # add email to set
        if not (self.filterSet is None) and fltr:
            setLenBefore = len(self.filterSet)
            self.filterSet.add(fltr)
            setLenAfter = len(self.filterSet)
            if setLenAfter == setLenBefore:
                return 0
            else:
                return 1
            #print self.filterSet # for debug
        else:
            return -1
            
    def stripLeftPart(self, emailaddr):
        # check if email matches the email format
        if not bool(re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", emailaddr)):
            return ""
            
        # get substring from '@' character.
        restPartList = re.search(r"(@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",emailaddr)
        if restPartList:
            return "*%s" % restPartList.group()
        else:
            return ""
            
    def getFilter(self):
        return self.filterSet
        
    def exportFilter(self, exportPath):
        if (self.filterSet):
            # 把每個集合內元素後面加上 OR
            ListToExport = [(x+" OR \n") for x in self.filterSet]
            ListToExport[-1] = ListToExport[-1].replace(" OR \n", "") # 最尾端不用加 OR
            
            # 把清單內容匯出(存檔)
            try:
                totalText = "".join(ListToExport)
                with open(exportPath, "w") as f:
                    f.write(totalText)
                return "ok"
            except:
                exm = sys.exc_info()[0]
                return exm
        else:
            return "清單為空，不用匯出。"
            
    def loadFilter(self, loadPath):
        # 讀入
        try:
            with open(loadPath, "r") as f:
                ContList = f.readlines()
                ContList = [x.rstrip(" OR \n") for x in ContList]
                self.filterSet = set(ContList)
                return self.filterSet
        except:
            exm = sys.exc_info()[0]
            return exm
        