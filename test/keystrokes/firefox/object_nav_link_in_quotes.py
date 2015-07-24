#!/usr/bin/python

"""Test of line navigation output of Firefox."""

from macaroon.playback import *
import utils

sequence = MacroSequence()

# Work around some new quirk in Gecko that causes this test to fail if
# run via the test harness rather than manually.
sequence.append(KeyComboAction("<Control>r"))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("<Control>Home"))
sequence.append(utils.AssertPresentationAction(
    "1. Top of file",
    ["BRAILLE LINE:  'line 1'",
     "     VISIBLE:  'line 1', cursor=1",
     "SPEECH OUTPUT: 'line 1'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Down"))
sequence.append(utils.AssertPresentationAction(
    "2. Line Down",
    ["BRAILLE LINE:  '\"'",
     "     VISIBLE:  '\"', cursor=1",
     "SPEECH OUTPUT: '\"'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Down"))
sequence.append(utils.AssertPresentationAction(
    "3. Line Down",
    ["BRAILLE LINE:  'line 2 \".'",
     "     VISIBLE:  'line 2 \".', cursor=1",
     "SPEECH OUTPUT: 'line 2 link'",
     "SPEECH OUTPUT: '\".'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Down"))
sequence.append(utils.AssertPresentationAction(
    "4. Line Down",
    ["BRAILLE LINE:  'line 3'",
     "     VISIBLE:  'line 3', cursor=1",
     "SPEECH OUTPUT: 'line 3'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "5. Line Up",
    ["BRAILLE LINE:  'line 2 \".'",
     "     VISIBLE:  'line 2 \".', cursor=1",
     "SPEECH OUTPUT: 'line 2 link'",
     "SPEECH OUTPUT: '\".'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "6. Line Up",
    ["BRAILLE LINE:  '\"'",
     "     VISIBLE:  '\"', cursor=1",
     "SPEECH OUTPUT: '\"'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "7. Line Up",
    ["BRAILLE LINE:  'line 1'",
     "     VISIBLE:  'line 1', cursor=1",
     "SPEECH OUTPUT: 'line 1'"]))

sequence.append(utils.AssertionSummaryAction())
sequence.start()
