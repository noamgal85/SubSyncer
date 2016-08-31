# Controller.py
import Model
from View import View
from View import FileDialog
from wx.lib.pubsub import pub

try:
	import wx
except ImportError:
	raise ImportError("The wxPython module is required to run this program.")

class Controller:
	def __init__(self, app):
		self.model = Model.Model()

		#set up the frame which displays the screen
		self.vGui = View(None, "SubSyncer", 
						 self.model.InitializeVideoTypes(), 
						 self.model.GetDefaultVideoType())

		# Bind actions from the Gui to the controller
		self.vGui.rdbVdoType.Bind(wx.EVT_RADIOBOX, self.onVideoType)
		self.vGui.btnBrwsVideo.Bind(wx.EVT_BUTTON, self.onBrwsVideo)
		self.vGui.btnBrwsSub.Bind(wx.EVT_BUTTON, self.onBrwsSub)
		self.vGui.btnSync.Bind(wx.EVT_BUTTON, self.onSyncMe)

		# Subscribe to button clicks
		pub.subscribe(self.VideoTypeChanged,"RDB CHANGED")
		pub.subscribe(self.BrwsVideoChanged,"VDO CHANGED")
		pub.subscribe(self.BrwsSubChanged, 	"SUB CHANGED")
		pub.subscribe(self.Invalid, 	 	"INVALID")

		self.vGui.Show()

    #----------------------------------------------------------------------
	def onVideoType(self,event):
		self.model.SetVideoType(self.vGui.GetSelectedVideoType())

	def VideoTypeChanged(self, value):
		pass

	#----------------------------------------------------------------------
	def onBrwsVideo(self, event):
		# Delete current message
		self.vGui.SetMessage("")

		# Show FileDialog
		dlg = FileDialog(parent=self.vGui,
						 sTitle="Choose video file",
						 sDirectory=self.model.GetCurrentDirectory(),
						 sWildcard=self.model.GetMovieWildcard())

		if dlg.ShowModal() == wx.ID_OK:
			self.model.SetVideoPath(dlg.GetPath())

		dlg.Destroy()

	# Listener on VideoFile change
	def BrwsVideoChanged(self, value):
		self.vGui.SetVideoPath(value)

	#----------------------------------------------------------------------
	def onBrwsSub(self, event):
		# Delete current message
		self.vGui.SetMessage("")

		# Show FileDialog
		dlg = FileDialog(parent=self.vGui,
						 sTitle="Choose subtitle file",
						 sDirectory=self.model.GetCurrentDirectory(),
						 sWildcard=self.model.GetSubWildcard())

		if dlg.ShowModal() == wx.ID_OK:
			self.model.SetSubPath(dlg.GetPath())

		dlg.Destroy()

	# Listener on SubtitleFile change
	def BrwsSubChanged(self, value):
		self.vGui.SetSubPath(value)

    #------------------------------------------------------------------------
	def onSyncMe(self, event):
		self.model.Sync()

	# Listener on Message raise
	def Invalid(self, value):
		print("IN INVALID")
		self.vGui.SetMessage(value)


#----------------------------------------------------------------------------
if __name__ == "__main__":
	app = wx.App(False)
	controller = Controller(app)
	app.MainLoop()
