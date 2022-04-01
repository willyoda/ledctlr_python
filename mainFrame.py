import wx
from labelbook_tst import MyLabelBook
import wx.lib.agw.labelbook as LB
import wx.lib.agw.aui as aui

_pageTexts = ["控制策略", "远程本地", "场景控制", "参数设置", "实时告警"]
_pageIcons = ["roll.png", "charge.png", "add.png", "decrypted.png", "news.png"]

# Show how to derive a custom wxLog class
class MyLog(wx.Log):
    def __init__(self,tc,logTime=0) -> None:
        super().__init__()
        self.tc = tc
        self.logTime= logTime

    def DoLogText(self,message):
        if self.tc >0:
            self.tc.AppendText(message +'\n')

class SamplePane(wx.Panel):
    def __init__(self, parent ,label,*args, **kw):
        super().__init__(parent ,*args, **kw)
        self.SetBackgroundColour('#DB7093')
        
        label += ' test'
        stx= wx.StaticText(self,-1,label,pos=(10,10))


class MyLabelBook(LB.LabelBook):
    ...

    def __init__(self, parent):
        style = LB.INB_FIT_BUTTON |LB.INB_FIT_LABELTEXT|LB.INB_LEFT | \
            LB.INB_DRAW_SHADOW | LB.INB_BORDER|LB.INB_BOLD_TAB_SELECTION
        super().__init__(parent, agwStyle = style)
        self.initUI()

        imagesList = wx.ImageList(32,32)
        self.AssignImageList(imagesList)

    def initUI(self):
        print('MyLabelBook')


        for indx,txts in enumerate(_pageTexts):
            label = "This is panel number %d"%(indx+1)
            self.AddPage(SamplePane(self,label),txts,True,indx)

        #demo is  ok 
        # pane1 = wx.Panel(self)
        # pane2 = wx.Panel(self)
        # self.AddPage(pane1, "Tab1", 1, 0)
        # self.AddPage(pane2, "Tab2", 1, 0)


class MainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.InitUI()

        self.SetPosition((30,30))
        # self.SetSize((1344,756))
        self.SetSize((1024,576))

    def InitUI(self):

        pnlTop  = wx.Panel(self)
        pnlTop.SetBackgroundColour('#6495ED')
        self.mgr=aui.AuiManager()

        self.mgr.SetManagedWindow(pnlTop)

        vTopSzr = wx.BoxSizer(wx.VERTICAL)    

        menubar = wx.MenuBar()
        tlbar = wx.ToolBar(self)
        stubar = wx.StatusBar(self)

        #add menu
        filemenu = wx.Menu()
        filemenu.Append(wx.ID_ANY,'itme1','itme1 help')
        menubar.Append(filemenu,'&File')

        #add labelbook
        notebook = MyLabelBook(pnlTop)
        # vTopSzr.Add(notebook,proportion =1,flag = wx.EXPAND|wx.ALL,border = 5)

        

        #add Log window
        self.log = wx.TextCtrl(pnlTop,id=wx.ID_ANY,value='Log',name='Log', 
                    style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        wx.Log.SetActiveTarget(MyLog(self.log))

        
        # vTopSzr.Add(self.log,proportion =1,flag = wx.EXPAND|wx.ALL ,border=5)

        self.mgr.AddPane(notebook,
                        aui.AuiPaneInfo().
                        CenterPane().Layer(2).BestSize((240, -1)).
                        MinSize((240, -1)).
                        Floatable(0).FloatingSize((240, 700)).
                        Caption("wxPython Demos").
                        CloseButton(False).
                        Name("DemoTree"))
                        
        self.mgr.AddPane(self.log,
                        aui.AuiPaneInfo().
                        # Left().Layer(2).BestSize((240, -1)).
                        Bottom().Caption("wxPython Demos"))

        text3 = wx.TextCtrl(pnlTop, -1, "Main content window",
                            wx.DefaultPosition, wx.Size(200,150),
                            wx.NO_BORDER | wx.TE_MULTILINE)

        # text4 = wx.TextCtrl(pnlTop, -1, "4 window",
        #                     wx.DefaultPosition, wx.Size(200,150),
        #                     wx.NO_BORDER | wx.TE_MULTILINE)

        text4 = wx.Panel(pnlTop, -1, 
                            wx.DefaultPosition, wx.Size(200,150),
                            )
        wx.Dialog(text4,title='hello ')                
        # text4.SetBackgroundColour('red')




        self.mgr.AddPane(text3, aui.AuiPaneInfo().Right())
        self.mgr.AddPane(text4, aui.AuiPaneInfo().Bottom())


        # pnlTop.SetSizer(vTopSzr)
        # self.SetSizer(vTopSzr)

        # tell the manager to "commit" all the changes just made
        self.mgr.Update()
        
        self.SetToolBar(tlbar)
        self.SetStatusBar(stubar)
        self.SetMenuBar(menubar)








def main():
    app =wx.App()
    w = MainFrame(None ,title = 'LedCtrl_v1.0.0')  
    w.Show()  
    app.MainLoop()

if __name__ == '__main__':
    main()