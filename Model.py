# Model.py
import os
import constants
from wx.lib.pubsub import pub
from FFMpeg import clsFFMpeg

#------------------------------------------------------------------------------
class Model():
	def __init__(self):
		self.__sCurrDir 		= os.getcwd()
		self.__nVideoType 		= constants.MOVIE
		self.__sVideoPath 		= ""
		self.__sSubPath 		= ""
		self.__sAudioPath		= ""
		self.__sAudioDir  		= ""
		self.__sAudioFilename 	= ""

	#----------------------------------------------------------------------
	def InitializeVideoTypes(self):
		return ([constants.TXT_MOVIE, constants.TXT_TV_SERIES])

	def GetDefaultVideoType(self):
		return constants.TXT_MOVIE

	#----------------------------------------------------------------------
	def GetMovieWildcard(self):
		return 	"Videos (*.avi, *.mov, *.mkv, *.mp4, ...)|*.avi;*.mov;*.mp4;*.mkv;*.flv;*.wmv;*.mpg;*.mpeg;*.mts|" \
				"All files (*.*)|*.*"

	def GetSubWildcard(self):
		return 	"Subtitles (*.srt)|*.srt"

	#----------------------------------------------------------------------
	def GetCurrentDirectory(self):
		return self.__sCurrDir

	def SetCurrentDirectory(self, value):
		self.__sCurrDir = value
		# Tell anyone who cares that the value has been changed
		pub.sendMessage("DIR CHANGED", value=self.__sCurrDir)

	#----------------------------------------------------------------------
	def GetVideoType(self):
		return self.__nVideoType

	def SetVideoType(self, value):
		self.__nVideoType = value
		# Tell anyone who cares that the value has been changed
		pub.sendMessage("RDB CHANGED", value=self.__nVideoType)

	#----------------------------------------------------------------------
	def GetVideoPath(self):
		return self.__sVideoPath

	def SetVideoPath(self, isPath):
		self.__sVideoPath = isPath
		self.__sCurrDir = os.path.dirname(self.__sVideoPath)
		# Tell anyone who cares that the value has been changed
		pub.sendMessage("VDO CHANGED", value=os.path.basename(self.__sVideoPath))

	#----------------------------------------------------------------------
	def GetSubPath(self):
		return self.__sSubPath

	def SetSubPath(self, isPath):
		self.__sSubPath = isPath
		self.__sCurrDir = os.path.dirname(self.__sSubPath)
		# Tell anyone who cares that the value has been changed
		pub.sendMessage("SUB CHANGED", value=os.path.basename(self.__sSubPath))

	#--------------------------------------------------------------------------
	def Sync(self):
		# Validations
		print("Video path: " + self.__sVideoPath + ", Sub path: " + self.__sSubPath)

		if (not self.__sVideoPath) or (not self.__sSubPath):
			print("IN IF")
			pub.sendMessage("INVALID", value="All fields required")
			return

		# 1. Convert the video file to a sound file
		self.__ConvertVideo2Audio()
		print("Conversion complete")

		#"TODO": sadf2. Create .scc file by executing local dll file using Audio file & Sub
		# 2.a Delete WAV file
		os.remove(self.__sAudioPath)
		print ("File removed")

		# 3. Call remote dll using .scc file that will create the final subs
		# 3.a Remember to pass software's version to the server

		# 4. Open URL to download the file

		


	#--------------------------------------------------------------------------
	def __ConvertVideo2Audio(self):
		# Convert video file to audio file
		try:
			# Create instance of FFMpeg
			fmpConverter = clsFFMpeg(self.GetVideoPath(), constants.AUDIO_FORMAT)

			# Convert video to audio and set audio params
			print("before convert")
			self.__sAudioPath 		= fmpConverter.ConvertVideo2Audio()
			self.__sAudioDir  		= fmpConverter.GetAudioDir()
			self.__sAudioFilename	= fmpConverter.GetAudioFilname()
			print ( "Audio path: " + self.__sAudioPath + "\n" + \
					"Audio Dir:  " + self.__sAudioDir  + "\n" + \
					"Audio File: " + self.__sAudioFilename)
		
		except e:
			print(e.args)
			pub.sendMessage("INVALID", value=e.args)
			return
