import wx
import wx.lib.agw.aui as aui


class MyLog(wx.Log):
    def __init__(self, textCtrl, logTime=0):
        wx.Log.__init__(self)
        self.tc = textCtrl
        self.logTime= logTime

    def DoLogText(self,message):
        if self.tc >0:
            self.tc.AppendText(message +'\n')

class MyFrame(wx.Frame):

    def __init__(self, parent, id=-1, title="AUI Test", pos=wx.DefaultPosition,
                 size=(800, 600), style=wx.DEFAULT_FRAME_STYLE):

        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        self.SetBackgroundColour('#6495ED')
        self._mgr = aui.AuiManager()

        # notify AUI which frame to use
        self._mgr.SetManagedWindow(self)

        # create several text controls
        text1 = wx.TextCtrl(self, -1, "Pane 1 - sample text",
                            wx.DefaultPosition, wx.Size(200,150),
                            wx.NO_BORDER | wx.TE_MULTILINE)

        self.tc = wx.TextCtrl(self, -1, "Pane 2 - sample text",
                            wx.DefaultPosition, wx.Size(200,150),
                            wx.NO_BORDER | wx.TE_MULTILINE)
        self.log = MyLog(self.tc)
        wx.Log.SetActiveTarget(self.log)   

        text3 = wx.TextCtrl(self, -1, "Main content window",
                            wx.DefaultPosition, wx.Size(200,150),
                            wx.NO_BORDER | wx.TE_MULTILINE)



        # add the panes to the manager
        self._mgr.AddPane(text1, aui.AuiPaneInfo().Left().Caption("Pane Number One"))
        self._mgr.AddPane(self.tc, aui.AuiPaneInfo().Bottom().Caption("LOG"))
        self._mgr.AddPane(text3, aui.AuiPaneInfo().CenterPane())

        # tell the manager to "commit" all the changes just made
        self._mgr.Update()

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # self.log.DoLogText('hello')
        self.tc.write('hello')

    def OnClose(self, event):
        # deinitialize the frame manager
        self._mgr.UnInit()
        event.Skip()


# our normal wxApp-derived class, as usual

app = wx.App(0)

frame = MyFrame(None)
app.SetTopWindow(frame)
frame.Show()

app.MainLoop()