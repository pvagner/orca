'''
Utilities for generating sound.  
'''

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__license__   = "LGPL"

try:
    from gi.repository import Gst
    import time, _thread
    gstreamerAvailable = True
except:
    gstreamerAvailable = False

class SoundUtils:

    def __init__(self):
        if not gstreamerAvailable:
            return
        Gst.init_check()

    def createSimpePipeline(self):
        if not gstreamerAvailable:
            return
        self._pipeline = Gst.Pipeline(name='orca-pipeline')
        self._source = Gst.ElementFactory.make('audiotestsrc', 'src')
        self._sink = Gst.ElementFactory.make('autoaudiosink', 'output')	
        self._pipeline.add(self._source)
        self._pipeline.add(self._sink)
        self._source.link(self._sink)
	
    def source_set_property(self,prop, value):
        if not gstreamerAvailable:
            return
        self._source.set_property(prop, value)

    def play_sound(self,duration):
        if not gstreamerAvailable:
            return
        self._pipeline.set_state(Gst.State.PLAYING)
        time.sleep(duration)
        self.pipeline_stop()

    def _threadSound(self, duration):
        if not gstreamerAvailable:
            return
        _thread.start_new_thread( self.play_sound, (duration , ) )

    def pipeline_stop(self):
        if not gstreamerAvailable:
            return
        self._pipeline.set_state(Gst.State.PAUSED)
