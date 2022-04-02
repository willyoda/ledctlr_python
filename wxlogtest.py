import wx


class LogFormatterWithThread(wx.LogFormatter):
	def __init__(self):
		super().__init__()

	# def Format(level=0, msg='', info=0):
	# # return "[%d] %s(%d) : %s" % \
	# #        (info.threadId, info.filename, info.line, msg)
	# # return "[%d] %s(%d) : %s" %(info.threadId, info.filename, info.line, msg)
		# return "myLog: %s" %(msg)

class MyLog(wx.Log):
	def __init__(self,tc,logTime=0):
		super().__init__()
		self.tc = tc
		self.logTime = logTime


	def DoLogText(self,message):
		if self.tc is not None:
			self.tc.AppendText(message +'\n') 	


# class MyLog(wx.LogGui):
# 	def __init__(self,tc):
# 		super().__init__()
# 		self.tc = tc
 
# 	def AppendLog(self, text, color):
# 		self.tc.SetDefaultStyle(wx.TextAttr(color))
# 		self.tc.AppendText(text+'\n')
 
# 	def DoLogTextAtLevel(self, level, msg):
# 		if level == wx.LOG_Error:
# 			color = wx.RED
# 		elif level == wx.LOG_Warning:
# 			color = wx.Colour(255, 127, 0)
# 		elif level == wx.LOG_Message:
# 			color = wx.BLUE
# 		elif level == wx.LOG_Info:
# 			color = wx.Colour(127, 127, 127)
# 		elif level == wx.LOG_Status:
# 			color = wx.Colour(0, 127, 0)
# 		else:
# 			color = wx.BLACK
# 		self.AppendLog(msg, color)
 
class TabPage(wx.Panel):
	def __init__(self, parent,pgnum,*args, **kw):
		super().__init__(parent,*args, **kw)

		if pgnum==1:
			self.SetBackgroundColour('#FFC0CB')
		elif pgnum ==2:
			self.SetBackgroundColour('#7B68EE')	
	sizer = wx.BoxSizer(wx.VERTICAL)






class Frame(wx.Frame):
	def __init__(self, *args, **kw):
		super().__init__(*args, **kw)

		self.initUI()

		
		self.Center()
		self.SetSize(480,480)

	def initUI(self):
		panel = wx.Panel(self)
		vSzr = wx.BoxSizer(wx.VERTICAL)

		self.stabar = wx.StatusBar(self)


		notebook = wx.Notebook(panel, style=wx.NB_MULTILINE)
		tabP1 = TabPage(notebook,1)
		notebook.AddPage(tabP1, "Page1")
		
		tabP2 = TabPage(notebook,2)
		notebook.AddPage(tabP2, "Page2")
		vSzr.Add(notebook, 1, wx.EXPAND)
		#notebook event
		notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED,self.OnPageChange)


		self.tc = wx.TextCtrl(panel, style=wx.BORDER_SUNKEN|wx.TE_MULTILINE|
					wx.TE_READONLY|wx.TE_RICH2|wx.HSCROLL)
		# # self.tc.SetFont(wx.Font(10, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		self.log = MyLog(self.tc)
		wx.Log.SetActiveTarget(self.log)
		wx.Log.SetVerbose(True)
		self.log.SetFormatter(LogFormatterWithThread())

		vSzr.Add(self.tc,1,wx.EXPAND|wx.ALL ,5)
		panel.SetSizer(vSzr)
		self.stabar.SetBackgroundColour('#F5DEB3')
		self.SetStatusBar(self.stabar)
 
	def OnPageChange(self,e):
		sl=e.GetSelection()+1
		msg = 'page change %d'%sl
		print(msg)
		# wx.LogMessage(msg)
		wx.LogMessage(msg)
		# wx.LogVerbose(msg)
		# # wx.LogStatus(self,msg)
		# wx.LogError(msg) #正常显示
		# wx.LogWarning(msg) #正常显示


	
 
if __name__ == "__main__":
	app = wx.App()
	ex=Frame(None,title = "Log Test")
	ex.Show()
	app.MainLoop()