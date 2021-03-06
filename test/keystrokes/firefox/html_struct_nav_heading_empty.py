#!/usr/bin/python

"""Test of structural navigation by heading."""

from macaroon.playback import *
import utils

sequence = MacroSequence()

sequence.append(KeyComboAction("<Control>Home"))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("1"))
sequence.append(utils.AssertPresentationAction(
    "1. 1 for next heading at level 1",
    ["BRAILLE LINE:  'line 2 h1'",
     "     VISIBLE:  'line 2 h1', cursor=1",
     "SPEECH OUTPUT: 'line 2 heading level 1'"]))

sequence.append(utils.AssertionSummaryAction())
sequence.start()
