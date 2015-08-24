'''
Utilities for generating sound.  
'''

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__license__   = "LGPL"

from gi.repository import Gst
import time, _thread

class SoundUtils:

	def __init__(self):
		Gst.init_check()
		
	def createSimpePipeline(self):
		self._pipeline = Gst.Pipeline(name='orca-pipeline')
		self._source = Gst.ElementFactory.make('audiotestsrc', 'src')
		self._sink = Gst.ElementFactory.make('autoaudiosink', 'output')	
		self._pipeline.add(self._source)
		self._pipeline.add(self._sink)
		self._source.link(self._sink)
			
	def source_set_property(self,prop, value):
		self._source.set_property(prop, value)
		
	def play_sound(self,duration):

		self._pipeline.set_state(Gst.State.PLAYING)
		time.sleep(duration)
		self.pipeline_stop()
		
	def _threadSound(self, duration):
		_thread.start_new_thread( self.play_sound, (duration , ) )

	def pipeline_stop(self):
		self._pipeline.set_state(Gst.State.PAUSED)
		return
