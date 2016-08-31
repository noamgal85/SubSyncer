# FFMpeg.py
import os.path
import constants
import subprocess
import shutil


class clsFFMpeg(object):
	#--------------------------------------------------------------------------
	def __init__(self, isVideoPath, isAudioFormat):
		# Check if FFMpeg is installed
		try:
			subprocess.call([shutil.which("ffmpeg"), "-version"])
		except:
			e = sys.exc_info()
			raise ValueError ("FFMpeg is not installed correctly", e[0], e[1] )

		# Set local video params and check validation
		self.__sVideoPath 		= isVideoPath
		self.__sVideoFilename	= os.path.basename(self.__sVideoPath)
		self.__validate()

		# Set working directory
		self.__sWorkDir  		= os.path.dirname(self.__sVideoPath)
		os.chdir(self.__sWorkDir)

		# Set audio filename
		self.__sAudioFilename	= os.path.splitext(self.__sVideoFilename)[0] + \
								  isAudioFormat

	#--------------------------------------------------------------------------
	def __validate(self):
		# Check video path is legal
		if (os.path.isfile(self.__sVideoPath) != True):
			raise ValueError ("Not a file")

	#--------------------------------------------------------------------------
	def ConvertVideo2Audio(self):
		try:
			# Convert file
			subprocess.call([shutil.which("ffmpeg"), 		# Command to run
							"-y", 							# Overwrite existing file
							 "-i", self.__sVideoFilename,	# Input file
							 "-ac", "1", 					# Number of audio channels
							 "-acodec", "pcm_s16le",		# force audio codec
							 #"-ar", "4000",				# Audio sampling rate (in Hz)
							 self.__sAudioFilename			# Output file
							])
		except e:
			print("In Except")
			print(e.args)
			raise ValueError (e.args)

		print("After call")
		# return the new filename
		return self.__sWorkDir+"\\"+self.__sAudioFilename

	#--------------------------------------------------------------------------
	def GetAudioDir(self):
		return self.__sWorkDir

	#--------------------------------------------------------------------------
	def GetAudioFilname(self):
		return self.__sAudioFilename

'''
# Testing
if __name__ == "__main__":
	try: 
		var1 = clsFFMpeg("C:\\temp\\test.mp4")
		var2 = var1.ConvertVideo2Audio()
		print ("Result: " + var2)
	except ValueError as e:
		print(e.args)
'''