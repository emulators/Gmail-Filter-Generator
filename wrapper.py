# -*- coding: utf-8 -*
from gmail_filter_generator import CustomGmail_filter_generator
from gmail_filter_generator_ui import Gmail_filter_generator
from Tkinter import *
import tkFileDialog
import tkMessageBox
import Tkinter
from filterProcessor import FilterProcessor


class UIEvent(CustomGmail_filter_generator):
        #self._txt_email['textvariable']= StringVar( value="123456   test") #設定 textbox範例
        #self._lbl_status['text'] = self._txt_email.get() #讀取 textbox範例
    fp = FilterProcessor([])

    def setTextBox(self, TextToSet):
        self._txt_email['textvariable']= StringVar( value=TextToSet )
    
    def setStatus(self, statusText):
        self._lbl_status['text'] = statusText
        
    def txt_email_getText(self):
        return self._txt_email.get()

    def _btn_add_command(self, *args):
        em = self._txt_email.get()
        res = self.fp.AddToSet(em)
        #
        if (res == -1):
            self.setStatus(u"輸入的郵件信箱不符格式。")
        elif (res == 0):
            self.setStatus(u"%s 已存在。" % self._txt_email.get())
        else:
            self.setStatus(u"%s 已加入清單。" % self._txt_email.get())
        #
        # 清空清單, 把集合內東西顯示到清單中 (即更新清單)
        self._listbox_email.delete(0, Tkinter.END)
        for x in self.fp.getFilter():
            self._listbox_email.insert(0, x)
        #
        # 清空文字內容
        self.setTextBox("")
            
    def _btn_export_command(self, *args):
        saveFilePath = tkFileDialog.asksaveasfilename(\
            initialdir = "./",
            title = "Select file",
            filetypes = (("txt files","*.txt"),("all files","*.*")))
        
        if (saveFilePath):
            if not saveFilePath.endswith(".txt"):
                saveFilePath = saveFilePath + ".txt"
            stat = self.fp.exportFilter(saveFilePath)
            if (stat == "ok"):
                self.setStatus(u"匯出完成:\n%s" % saveFilePath)
            else:
                self.setStatus(u"訊息: %s" % stat)
        
    def _btn_load_command(self, *args):
        openedFilePath = tkFileDialog.askopenfilename(\
            initialdir = "./",\
            title = "Select file",\
            filetypes = (("txt files","*.txt"),("all files","*.*")))
        if (openedFilePath): 
            stat = self.fp.loadFilter(openedFilePath)
            if (isinstance(stat, set)):
                # 把集合內東西顯示到清單中
                for x in stat:
                    self._listbox_email.insert(0, x)
                self.setStatus(u"已讀取檔案:\n%s" % openedFilePath)
            else:
                self.setStatus(u"訊息:\n%s" % stat)
    
    def _btn_help_command(self, *args):
        infoMsg = ""
        try:
            with open("_versionInfo", "r") as ff:
                msgList = ff.readlines()
                infoMsg = "".join(msgList)
        except:
            infoMsg = u"無法讀取 _versionInfo檔案。"
        tkMessageBox.showinfo("About this program", infoMsg)

def main():
    # Standalone Code Initialization
    # DO NOT EDIT
    try: userinit()
    except NameError: pass
    root = Tk()

    demo2 = UIEvent(root)
    demo2._listbox_email.config(yscrollcommand=demo2._scrollbar_1.set, height=10, width=10)
    demo2._scrollbar_1.config(command=demo2._listbox_email.yview)
    root.title('Gmail filter generator')
    try: run()
    except NameError: pass
    root.protocol('WM_DELETE_WINDOW', root.quit)
    root.mainloop()

if __name__ == '__main__': main()