# View.py
try:
	import wx
except ImportError:
	raise ImportError("The wxPython module is required to run this program.")

#------------------------------------------------------------------------------
class View(wx.Frame):
	def __init__(self,parent,title,lblList, rdbDefault):
		wx.Frame.__init__(self,parent,title=title) 
		self.parent = parent
		self.initialize(lblList, rdbDefault)

	# -------------------------------------------------------------------------
	def initialize(self, lblList, rdbDefault):
		# Create sizer
		self.__szr = wx.GridBagSizer()

		# Create a radioBox to decide the video type
		self.rdbVdoType = wx.RadioBox(self, label = "Vidoe type", 
										choices = lblList, majorDimension = 1, 
										style = wx.RA_SPECIFY_ROWS)
		self.rdbVdoType.SetStringSelection(rdbDefault)

		# create video browse button
		self.btnBrwsVideo = wx.Button(self, label="Browse a video")
		
		# create video path text
		self.__txtVideoPath = wx.StaticText(self,-1,style=wx.BORDER_SIMPLE)
		self.__txtVideoPath.SetBackgroundColour("light gray")

		# create subtitle browse button
		self.btnBrwsSub = wx.Button(self, label="Browse subtitle")

		# create subtitle path text
		self.__txtSubPath = wx.StaticText(self,-1,style=wx.BORDER_SIMPLE)
		self.__txtSubPath.SetBackgroundColour("light gray")
		
		# create sync button
		self.btnSync = wx.Button(self, label="Sync me!")

		# create message text
		self.__txtMessage = wx.StaticText(self,-1,style=wx.ALIGN_CENTER)
		self.__txtMessage.SetBackgroundColour("light blue")

		# Add object to sizer
		self.__szr.Add(self.rdbVdoType,		(0,0))
		self.__szr.Add(self.btnBrwsVideo, 	(2,0))
		self.__szr.Add(self.btnBrwsSub, 	(3,0))
		self.__szr.Add(self.__txtVideoPath,	(2,1),(0,50),wx.EXPAND)
		self.__szr.Add(self.__txtSubPath,	(3,1),(0,50),wx.EXPAND)
		self.__szr.Add(self.btnSync, 		(4,1))
		self.__szr.Add(self.__txtMessage,	(5,0),(0,50),wx.EXPAND)

		# Set size properties & fix screen size
		self.__szr.AddGrowableCol(0)
		self.SetSizerAndFit(self.__szr)
		self.SetSizeHints(self.GetSize().x,self.GetSize().y,self.GetSize().x,self.GetSize().y);

		self.Show(True)

	# -------------------------------------------------------------------------
	def GetSelectedVideoType(self):
		return self.rdbVdoType.GetStringSelection()

	# -------------------------------------------------------------------------
	def SetVideoPath(self, value):
		self.__txtVideoPath.SetLabel(label = value)
		self.__szr.Layout()

	def SetSubPath(self, value):
		self.__txtSubPath.SetLabel(label = value)
		self.__szr.Layout()

	def SetMessage(self, value):
		self.__txtMessage.SetLabel(label = value)
		self.__szr.Layout()


#------------------------------------------------------------------------------
class FileDialog():
	def __init__(self,parent, sTitle, sDirectory, sWildcard):
		self.dlg = wx.FileDialog(
			parent,
			message=sTitle,
			defaultDir=sDirectory,
			defaultFile="",
			wildcard=sWildcard,
			style=wx.FD_OPEN | wx.FD_CHANGE_DIR
			)

	def ShowModal(self):
		return self.dlg.ShowModal()

	def GetPath(self):
		return self.dlg.GetPath()

	def Destroy(self):
		self.dlg.Destroy()
