# Orca
#
# Copyright 2015 Peter Vágner <pvdeejay@gmail.com>
# Copyright 2006, 2007, 2008, 2009 Brailcom, o.p.s.
#
# Author: Tomas Cerha <cerha@brailcom.org>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., Franklin Street, Fifth Floor,
# Boston MA  02110-1301 USA.


"""Provides an Orca speech server for eSpeak backend."""

__id__ = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__license__   = "LGPL"

from gi.repository import GLib
import re
import time
import os.path

from . import chnames
from . import debug
from . import guilabels
from . import messages
from . import speechserver
from . import settings
from . import orca_state
from . import punctuation_settings
from .acss import ACSS

try:
    from espeak import espeak
except:
    _espeak_available = False
else:    
    _espeak_available = True

PUNCTUATION = re.compile('[^\w\s]', re.UNICODE)
ELLIPSIS = re.compile('(\342\200\246|\.\.\.\s*)')

#Parameter bounds
minRate=80
maxRate=450
minPitch=0
maxPitch=99

class SpeechServer(speechserver.SpeechServer):
    # See the parent class for documentation.

    _active_servers = {}
    
    DEFAULT_SERVER_ID = 'default'
    _SERVER_NAMES = {DEFAULT_SERVER_ID: guilabels.DEFAULT_SYNTHESIZER}

    def getFactoryName():
        return guilabels.ESPEAK
    getFactoryName = staticmethod(getFactoryName)

    def getSpeechServers():
        servers = []
        default = SpeechServer._getSpeechServer(SpeechServer.DEFAULT_SERVER_ID)
        if default is not None:
            servers.append(default)
        return servers
    getSpeechServers = staticmethod(getSpeechServers)

    def _getSpeechServer(cls, serverId):
        """Return an active server for given id.

        Attempt to create the server if it doesn't exist yet.  Returns None
        when it is not possible to create the server.
        
        """
        if serverId not in cls._active_servers:
            cls(serverId)
        # Don't return the instance, unless it is succesfully added
        # to `_active_Servers'.
        return cls._active_servers.get(serverId)
    _getSpeechServer = classmethod(_getSpeechServer)

    def getSpeechServer(info=None):
        if info is not None:
            thisId = info[1]
        else:
            thisId = SpeechServer.DEFAULT_SERVER_ID
        return SpeechServer._getSpeechServer(thisId)
    getSpeechServer = staticmethod(getSpeechServer)

    def shutdownActiveServers():
        for server in list(SpeechServer._active_servers.values()):
            server.shutdown()
    shutdownActiveServers = staticmethod(shutdownActiveServers)

    # *** Instance methods ***

    def __init__(self, serverId):
        super(SpeechServer, self).__init__()
        self._id = serverId
        self._client = None
        self._current_voice_properties = {}
        self._acss_manipulators = (
            (ACSS.RATE, self._set_rate),
            (ACSS.AVERAGE_PITCH, self._set_pitch),
            (ACSS.GAIN, self._set_volume),
            (ACSS.FAMILY, self._set_family),
            )
        if not _espeak_available:
            debug.println(debug.LEVEL_WARNING,
                          "eSpeak interface not installed.")
            return
        self._PUNCTUATION_MODE_MAP = {
            settings.PUNCTUATION_STYLE_ALL:  espeak.Punctuation.All,
            settings.PUNCTUATION_STYLE_MOST: espeak.Punctuation.Custom,
            settings.PUNCTUATION_STYLE_SOME: espeak.Punctuation.Custom,
            settings.PUNCTUATION_STYLE_NONE: espeak.Punctuation.Any,
            }
        self._CALLBACK_TYPE_MAP = {
            espeak.event_SENTENCE: speechserver.SayAllContext.PROGRESS,
            #espeak.event_END: speechserver.SayAllContext.INTERRUPTED,
            espeak.event_MSG_TERMINATED: speechserver.SayAllContext.COMPLETED,
           #espeak.event_MARK:speechserver.SayAllContext.PROGRESS,
            }

        self._default_voice_name = guilabels.SPEECH_DEFAULT_VOICE % serverId
        
        try:
            self._init()
        except:
            debug.println(debug.LEVEL_WARNING,
                          "eSpeak failed to initialize:")
            debug.printException(debug.LEVEL_WARNING)
        else:
            SpeechServer._active_servers[serverId] = self

        self._lastKeyEchoTime = None

    def _init(self):
        self._current_voice_properties = {}
        mode = self._PUNCTUATION_MODE_MAP[settings.verbalizePunctuationStyle]
        espeak.set_parameter(espeak.Parameter.Punctuation,mode,0)

    def updateCapitalizationStyle(self):
        """Updates the capitalization style used by the speech server."""
        pass

    def updatePunctuationLevel(self):
        """ Punctuation level changed, inform this speechServer. """
        mode = self._PUNCTUATION_MODE_MAP[settings.verbalizePunctuationStyle]
        espeak.set_parameter(espeak.Parameter.Punctuation,mode,0)

    def _paramToPercent(self, current, min, max):
        """Convert a raw parameter value to a percentage given the current, minimum and maximum raw values.
        @param current: The current value.
        @type current: int
        @param min: The minimum value.
        @type current: int
        @param max: The maximum value.
        @type max: int
        """
        return int(round(float(current - min) / (max - min) * 100))

    def _percentToParam(self, percent, min, max):
        """Convert a percentage to a raw parameter value given the current percentage and the minimum and maximum raw parameter values.
        @param percent: The current percentage.
        @type percent: int
        @param min: The minimum raw parameter value.
        @type min: int
        @param max: The maximum raw parameter value.
        @type max: int
        """
        return int(round(float(percent) / 100 * (max - min) + min))

    def _set_rate(self, acss_rate):
        rate = self._percentToParam(acss_rate, minRate, maxRate)
        espeak.set_parameter(espeak.Parameter.Rate, rate, 0)

    def _set_pitch(self, acss_pitch):
        pitch = self._percentToParam((acss_pitch *10), minPitch, maxPitch)
        espeak.set_parameter(espeak.Parameter.Pitch, pitch, 0)

    def _set_volume(self, acss_volume):
        volume = int(acss_volume *10)
        espeak.set_parameter(espeak.Parameter.Volume, volume, 0)

    def _set_family(self, acss_family):
        familyLocale = acss_family.get(speechserver.VoiceFamily.LOCALE)
        if not familyLocale:
            import locale
            familyLocale, encoding = locale.getdefaultlocale()
        if familyLocale:
            lang = familyLocale.split('_')[0]
            if lang:
                espeak.set_voice(lang)
        else:
            name = acss_family.get(speechserver.VoiceFamily.NAME)
            if name != self._default_voice_name:
                espeak.set_voice(name)

    def _apply_acss(self, acss):
        if acss is None:
            acss = settings.voices[settings.DEFAULT_VOICE]
        current = self._current_voice_properties
        for acss_property, method in self._acss_manipulators:
            value = acss.get(acss_property)
            if value is not None:
                if current.get(acss_property) != value:
                    method(value)
                    current[acss_property] = value
            elif acss_property == ACSS.AVERAGE_PITCH:
                method(5.0)
                current[acss_property] = 5.0
            elif acss_property == ACSS.FAMILY \
                    and acss == settings.voices[settings.DEFAULT_VOICE]:
                # We need to explicitly reset (at least) the family.
                # See bgo#626072.
                #
                method({})
                current[acss_property] = {}

    def __addVerbalizedPunctuation(self, oldText):
        """Depending upon the users verbalized punctuation setting,
        adjust punctuation symbols in the given text to their pronounced
        equivalents. The pronounced text will either replace the
        punctuation symbol or be inserted before it. In the latter case,
        this is to retain spoken prosity.

        Arguments:
        - oldText: text to be parsed for punctuation.

        Returns a text string with the punctuation symbols adjusted accordingly.
        """

        spokenEllipsis = messages.SPOKEN_ELLIPSIS + " "
        newText = re.sub(ELLIPSIS, spokenEllipsis, oldText)
        symbols = set(re.findall(PUNCTUATION, newText))
        for symbol in symbols:
            try:
                level, action = punctuation_settings.getPunctuationInfo(symbol)
            except:
                continue

            if level != punctuation_settings.LEVEL_NONE:
                # eSpeak should handle it.
                #
                continue

            charName = " %s " % chnames.getCharacterName(symbol)
            if action == punctuation_settings.PUNCTUATION_INSERT:
                charName += symbol
            newText = re.sub(symbol, charName, newText)

        if orca_state.activeScript:
            newText = orca_state.activeScript.utilities.adjustForDigits(newText)

        return newText

    def _speak(self, text, acss, callback=None):
        if isinstance(text, ACSS):
            text = ''
        text = self.__addVerbalizedPunctuation(text)
        if orca_state.activeScript:
            text = orca_state.activeScript.\
                utilities.adjustForPronunciation(text)

        # We need to make several replacements.
        text = text.translate({
            0x1: None, # used for embedded commands
            0x5B: u" [", # [: [[ indicates phonemes
        })

        self._apply_acss(acss)
        espeak.set_SynthCallback(callback)
        espeak.synth(text)

    def _say_all(self, iterator, orca_callback):
        """Process another sayAll chunk.

        Called by the gidle thread.

        """
        try:
            context, acss = next(iterator)
        except StopIteration:
            pass
        else:
            def callback(event, pos, len):
                t = self._CALLBACK_TYPE_MAP[event]
                if t == speechserver.SayAllContext.PROGRESS:
                    if pos >1:
                        context.currentOffset = (context.startOffset +pos -1)
                    else:
                        context.currentOffset = context.startOffset
                elif t == speechserver.SayAllContext.COMPLETED:
                    context.currentOffset = context.endOffset
                GLib.idle_add(orca_callback, context, t)
                if t == speechserver.SayAllContext.COMPLETED:
                    GLib.idle_add(self._say_all, iterator, orca_callback)
            self._speak(context.utterance, acss, callback=callback)
        return False # to indicate, that we don't want to be called again.

    def _cancel(self):
        espeak.cancel()

    def _change_default_speech_rate(self, step, decrease=False):
        acss = settings.voices[settings.DEFAULT_VOICE]
        delta = step * (decrease and -1 or +1)
        try:
            rate = acss[ACSS.RATE]
        except KeyError:
            rate = 50
        acss[ACSS.RATE] = max(0, min(99, rate + delta))
        debug.println(debug.LEVEL_CONFIGURATION,
                      "Speech rate is now %d" % rate)

        self.speak(decrease and messages.SPEECH_SLOWER \
                   or messages.SPEECH_FASTER, acss=acss)

    def _change_default_speech_pitch(self, step, decrease=False):
        acss = settings.voices[settings.DEFAULT_VOICE]
        delta = step * (decrease and -1 or +1)
        try:
            pitch = acss[ACSS.AVERAGE_PITCH]
        except KeyError:
            pitch = 5
        acss[ACSS.AVERAGE_PITCH] = max(0, min(9, pitch + delta))
        debug.println(debug.LEVEL_CONFIGURATION,
                      "Speech pitch is now %d" % pitch)

        self.speak(decrease and messages.SPEECH_LOWER \
                   or messages.SPEECH_HIGHER, acss=acss)

    def _change_default_speech_volume(self, step, decrease=False):
        acss = settings.voices[settings.DEFAULT_VOICE]
        delta = step * (decrease and -1 or +1)
        try:
            volume = acss[ACSS.GAIN]
        except KeyError:
            volume = 5
        acss[ACSS.GAIN] = max(0, min(9, volume + delta))
        debug.println(debug.LEVEL_CONFIGURATION,
                      "Speech volume is now %d" % volume)

        self.speak(decrease and messages.SPEECH_SOFTER \
                   or messages.SPEECH_LOUDER, acss=acss)

    def getInfo(self):
        return [self._SERVER_NAMES.get(self._id, self._id), self._id]

    def getVoiceFamilies(self):
        # Always offer the configured default voice with a language
        # set according to the current locale.
        from locale import getlocale, LC_MESSAGES
        locale = getlocale(LC_MESSAGES)[0]
        if locale is None or locale == 'C':
            lang = None
            dialect = None
        else:
            lang, dialect = locale.split('_')
        list_synthesis_voices = espeak.list_voices()
        families = [speechserver.VoiceFamily({ \
              speechserver.VoiceFamily.NAME: self._default_voice_name,
              #speechserver.VoiceFamily.GENDER: speechserver.VoiceFamily.MALE,
              speechserver.VoiceFamily.DIALECT: dialect,
              speechserver.VoiceFamily.LOCALE: lang})]
        for voice in list_synthesis_voices:
            families.append(speechserver.VoiceFamily({ \
                speechserver.VoiceFamily.NAME: voice.name,
                speechserver.VoiceFamily.DIALECT: voice.variant,
                speechserver.VoiceFamily.LOCALE: voice.identifier.split("/")[-1]}))
        return families

    def speak(self, text=None, acss=None, interrupt=True):
        #if interrupt:
        #    self._cancel()

        # "We will not interrupt a key echo in progress." (Said the comment in
        # speech.py where these next two lines used to live. But the code here
        # suggests we haven't been doing anything with the lastKeyEchoTime in
        # years. TODO - JD: Dig into this and if it's truly useless, kill it.)
        if self._lastKeyEchoTime:
            interrupt = interrupt and (time.time() - self._lastKeyEchoTime) > 0.5

        if text:
            self._speak(text, acss)

    def speakUtterances(self, utteranceList, acss=None, interrupt=True):
        #if interrupt:
        #    self._cancel()
        for utterance in utteranceList:
            if utterance:
                self._speak(utterance, acss)

    def sayAll(self, utteranceIterator, progressCallback):
        GLib.idle_add(self._say_all, utteranceIterator, progressCallback)

    def speakCharacter(self, character, acss=None):
        #self._apply_acss(acss)

        name = chnames.getCharacterName(character)
        if not name:
            self.speak(character, acss)
            return

        if orca_state.activeScript:
            name = orca_state.activeScript.\
                utilities.adjustForPronunciation(name)
        self.speak(name, acss)

    def speakKeyEvent(self, event):
        if event.isPrintableKey() and event.event_string.isupper():
            acss = settings.voices[settings.UPPERCASE_VOICE]
        else:
            acss = ACSS(settings.voices[settings.DEFAULT_VOICE])

        event_string = event.getKeyName()
        if orca_state.activeScript:
            event_string = orca_state.activeScript.\
                utilities.adjustForPronunciation(event_string)

        lockingStateString = event.getLockingStateString()
        event_string = "%s %s" % (event_string, lockingStateString)
        self.speak(event_string, acss=acss)
        self._lastKeyEchoTime = time.time()

    def increaseSpeechRate(self, step=5):
        self._change_default_speech_rate(step)

    def decreaseSpeechRate(self, step=5):
        self._change_default_speech_rate(step, decrease=True)

    def increaseSpeechPitch(self, step=0.5):
        self._change_default_speech_pitch(step)

    def decreaseSpeechPitch(self, step=0.5):
        self._change_default_speech_pitch(step, decrease=True)

    def increaseSpeechVolume(self, step=0.5):
        self._change_default_speech_volume(step)

    def decreaseSpeechVolume(self, step=0.5):
        self._change_default_speech_volume(step, decrease=True)

    def stop(self):
        self._cancel()

    def shutdown(self):
        pass

    def reset(self, text=None, acss=None):
        pass

