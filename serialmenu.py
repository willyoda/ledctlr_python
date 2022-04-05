import wx


class Ex2(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(Ex2, self).__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        ...
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fileMenu.Append(wx.ID_ANY, 'Open', 'open')
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)


class Example(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fileMenu.Append(wx.ID_ANY, 'serial', 'hello')
        menubar.Append(fileMenu, '&Port')
        self.SetMenuBar(menubar)

        self.SetSize((480, 320))
        self.Centre()

        self.Bind(wx.EVT_MENU, self.OnSerial)

    def OnSerial(self, e):
        print('serial')
        ex2 = Ex2(None, title='world')
        ex2.SetBackgroundColour('blue')
        ex2.Show()


def main():
    # app = wx.App()
    # ex = Example(None)
    # ex.Show()
    # app.MainLoop()

    app = wx.App()
    ex = Example(None,title='Hello')
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
