       self.serial.timeout = 0.5   # make sure that the alive event can be checked from time to time
        self.settings = TerminalSetup()  # placeholder for the settings
        self.thread = None
        self.alive = threading.Event()
        # begin wxGlade: TerminalFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        # Menu Bar
        self.frame_terminal_menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(ID_CLEAR, "&Clear", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(ID_SAVEAS, "&Save Text As...", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendSeparator()
        wxglade_tmp_menu.Append(ID_TERM, "&Terminal Settings...", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendSeparator()
        wxglade_tmp_menu.Append(ID_EXIT, "&Exit", "", wx.ITEM_NORMAL)
        self.frame_terminal_menubar.Append(wxglade_tmp_menu, "&File")
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(ID_RTS, "RTS", "", wx.ITEM_CHECK)
        wxglade_tmp_menu.Append(ID_DTR, "&DTR", "", wx.ITEM_CHECK)
        wxglade_tmp_menu.Append(ID_SETTINGS, "&Port Settings...", "", wx.ITEM_NORMAL)
        self.frame_terminal_menubar.Append(wxglade_tmp_menu, "Serial Port")
        self.SetMenuBar(self.frame_terminal_menubar)
        # Menu Bar end
        self.text_ctrl_output = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE | wx.TE_READONLY)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_MENU, self.OnClear, id=ID_CLEAR)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, id=ID_SAVEAS)
        self.Bind(wx.EVT_MENU, self.OnTermSettings, id=ID_TERM)
        self.Bind(wx.EVT_MENU, self.OnExit, id=ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnRTS, id=ID_RTS)
        self.Bind(wx.EVT_MENU, self.OnDTR, id=ID_DTR)
        self.Bind(wx.EVT_MENU, self.OnPortSettings, id=ID_SETTINGS)
        # end wxGlade
        self.__attach_events()          # register events
        self.OnPortSettings(None)       # call setup dialog on startup, opens port
        if not self.alive.isSet():
            self.Close()

    def StartThread(self):
        """Start the receiver thread"""
        self.thread = threading.Thread(target=self.ComPortThread)
        self.thread.setDaemon(1)
        self.alive.set()
        self.thread.start()
        self.serial.rts = True
        self.serial.dtr = True
        self.frame_terminal_menubar.Check(ID_RTS, self.serial.rts)
        self.frame_terminal_menubar.Check(ID_DTR, self.serial.dtr)

    def StopThread(self):
        """Stop the receiver thread, wait until it's finished."""
        if self.thread is not None:
            self.alive.clear()          # clear alive event for thread
            self.thread.join()          # wait until thread has finished
            self.thread = None

    def __set_properties(self):
        # begin wxGlade: TerminalFrame.__set_properties
        self.SetTitle("Serial Terminal")
        self.SetSize((546, 383))
        self.text_ctrl_output.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, ""))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: TerminalFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.text_ctrl_output, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def __attach_events(self):
        # register events at the controls
        self.Bind(wx.EVT_MENU, self.OnClear, id=ID_CLEAR)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, id=ID_SAVEAS)
        self.Bind(wx.EVT_MENU, self.OnExit, id=ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnPortSettings, id=ID_SETTINGS)
        self.Bind(wx.EVT_MENU, self.OnTermSettings, id=ID_TERM)
        self.text_ctrl_output.Bind(wx.EVT_CHAR, self.OnKey)
        self.Bind(wx.EVT_CHAR_HOOK, self.OnKey)
        self.Bind(EVT_SERIALRX, self.OnSerialRead)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnExit(self, event):  # wxGlade: TerminalFrame.<event_handler>
        """Menu point Exit"""
        self.Close()

    def OnClose(self, event):
        """Called on application shutdown."""
        self.StopThread()               # stop reader thread
        self.serial.close()             # cleanup
        self.Destroy()                  # close windows, exit app

    def OnSaveAs(self, event):  # wxGlade: TerminalFrame.<event_handler>
        """Save contents of output window."""
        with wx.FileDialog(
                None,
                "Save Text As...",
                ".",
                "",
                "Text File|*.txt|All Files|*",
                wx.SAVE) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                filename = dlg.GetPath()
                with codecs.open(filename, 'w', encoding='utf-8') as f:
                    text = self.text_ctrl_output.GetValue().encode("utf-8")
                    f.write(text)

    def OnClear(self, event):  # wxGlade: TerminalFrame.<event_handler>
        """Clear contents of output window."""
        self.text_ctrl_output.Clear()

    def OnPortSettings(self, event):  # wxGlade: TerminalFrame.<event_handler>
        """
        Show the port settings dialog. The reader thread is stopped for the
        settings change.
        """
        if event is not None:           # will be none when called on startup
            self.StopThread()
            self.serial.close()
        ok = False
        while not ok:
            with wxSerialConfigDialog.SerialConfigDialog(
                    self,
                    -1,
                    "",
                    show=wxSerialConfigDialog.SHOW_BAUDRATE | wxSerialConfigDialog.SHOW_FORMAT | wxSerialConfigDialog.SHOW_FLOW,
                    serial=self.serial) as dialog_serial_cfg:
                dialog_serial_cfg.CenterOnParent()
                result = dialog_serial_cfg.ShowModal()
            # open port if not called on startup, open it on startup and OK too
            if result == wx.ID_OK or event is not None:
                try:
                    self.serial.open()
                except serial.SerialException as e:
                    with wx.MessageDialog(self, str(e), "Serial Port Error", wx.OK | wx.ICON_ERROR)as dlg:
                        dlg.ShowModal()
                else:
                    self.StartThread()
                    self.SetTitle("Serial Terminal on {} [{},{},{},{}{}{}]".format(
                        self.serial.portstr,
                        self.serial.baudrate,
                        self.serial.bytesize,
                        self.serial.parity,
                        self.serial.stopbits,
                        ' RTS/CTS' if self.serial.rtscts else '',
                        ' Xon/Xoff' if self.serial.xonxoff else '',
                        ))
                    ok = True
            else:
                # on startup, dialog aborted
                self.alive.clear()
                ok = True

    def OnTermSettings(self, event):  # wxGlade: TerminalFrame.<event_handler>
        """\
        Menu point Terminal Settings. Show the settings dialog
        with the current terminal settings.
        """
        with TerminalSettingsDialog(self, -1, "", settings=self.settings) as dialog:
            dialog.CenterOnParent()
            dialog.ShowModal()

    def OnKey(self, event):
        """\
        Key event handler. If the key is in the ASCII range, write it to the
        serial port. Newline handling and local echo is also done here.
        """
        code = event.GetUnicodeKey()
        # if code < 256:   # XXX bug in some versions of wx returning only capital letters
        #     code = event.GetKeyCode()
        if code == 13:                      # is it a newline? (check for CR which is the RETURN key)
            if self.settings.echo:          # do echo if needed
                self.text_ctrl_output.AppendText('\n')
            if self.settings.newline == NEWLINE_CR:
                self.serial.write(b'\r')     # send CR
            elif self.settings.newline == NEWLINE_LF:
                self.serial.write(b'\n')     # send LF
            elif self.settings.newline == NEWLINE_CRLF:
                self.serial.write(b'\r\n')   # send CR+LF
        else:
            char = unichr(code)
            if self.settings.echo:          # do echo if needed
                self.WriteText(char)
            self.serial.write(char.encode('UTF-8', 'replace'))         # send the character
        event.StopPropagation()

    def WriteText(self, text):
        if self.settings.unprintable:
            text = ''.join([c if (c >= ' ' and c != '\x7f') else unichr(0x2400 + ord(c)) for c in text])
        self.text_ctrl_output.AppendText(text)

    def OnSerialRead(self, event):
        """Handle input from the serial port."""
        self.WriteText(event.data.decode('UTF-8', 'replace'))

    def ComPortThread(self):
        """\
        Thread that handles the incoming traffic. Does the basic input
        transformation (newlines) and generates an SerialRxEvent
        """
        while self.alive.isSet():
            b = self.serial.read(self.serial.in_waiting or 1)
            if b:
                # newline transformation
                if self.settings.newline == NEWLINE_CR:
                    b = b.replace(b'\r', b'\n')
                elif self.settings.newline == NEWLINE_LF:
                    pass
                elif self.settings.newline == NEWLINE_CRLF:
                    b = b.replace(b'\r\n', b'\n')
                wx.PostEvent(self, SerialRxEvent(data=b))

    def OnRTS(self, event):  # wxGlade: TerminalFrame.<event_handler>
        self.serial.rts = event.IsChecked()

    def OnDTR(self, event):  # wxGlade: TerminalFrame.<event_handler>
        self.serial.dtr = event.IsChecked()