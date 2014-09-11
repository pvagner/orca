#!/usr/bin/python

"""Test of Dojo tree presentation."""

from macaroon.playback import *
import utils

sequence = MacroSequence()

sequence.append(KeyComboAction("Tab"))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Tab"))
sequence.append(utils.AssertPresentationAction(
    "1. Tab to continents",
    ["BRAILLE LINE:  'before:  $l'",
     "     VISIBLE:  'before:  $l', cursor=0",
     "BRAILLE LINE:  'Continents expanded list item'",
     "     VISIBLE:  'Continents expanded list item', cursor=1",
     "BRAILLE LINE:  'Continents expanded list item'",
     "     VISIBLE:  'Continents expanded list item', cursor=1",
     "SPEECH OUTPUT: 'Continents'",
     "SPEECH OUTPUT: 'expanded tree level 1'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Down"))
sequence.append(utils.AssertPresentationAction(
    "2. Down arrow to Africa",
    ["KNOWN ISSUE: We shouldn't be speaking the panel here",
     "BRAILLE LINE:  'Africa collapsed list item'",
     "     VISIBLE:  'Africa collapsed list item', cursor=1",
     "BRAILLE LINE:  'Africa collapsed list item'",
     "     VISIBLE:  'Africa collapsed list item', cursor=1",
     "SPEECH OUTPUT: 'Continents'",
     "SPEECH OUTPUT: 'panel'",
     "SPEECH OUTPUT: 'Africa'",
     "SPEECH OUTPUT: 'collapsed tree level 2'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_Enter"))
sequence.append(utils.AssertPresentationAction(
    "3. Basic whereAmI",
    ["BRAILLE LINE:  'Africa collapsed list item'",
     "     VISIBLE:  'Africa collapsed list item', cursor=1",
     "SPEECH OUTPUT: 'list item'",
     "SPEECH OUTPUT: 'Africa'",
     "SPEECH OUTPUT: '1 of 6 collapsed tree level 2'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Right"))
sequence.append(utils.AssertPresentationAction(
    "4. Expand Africa",
    ["BRAILLE LINE:  'Africa expanded list item'",
     "     VISIBLE:  'Africa expanded list item', cursor=1",
     "SPEECH OUTPUT: 'expanded'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Down"))
sequence.append(utils.AssertPresentationAction(
    "5. Down arrow to Egypt",
    ["KNOWN ISSUE: We shouldn't be speaking the panel here",
     "BRAILLE LINE:  'Egypt list item'",
     "     VISIBLE:  'Egypt list item', cursor=1",
     "BRAILLE LINE:  'Egypt list item'",
     "     VISIBLE:  'Egypt list item', cursor=1",
     "SPEECH OUTPUT: 'Africa'",
     "SPEECH OUTPUT: 'panel'",
     "SPEECH OUTPUT: 'Egypt'",
     "SPEECH OUTPUT: 'tree level 3'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Down"))
sequence.append(utils.AssertPresentationAction(
    "6. Down arrow to Kenya",
    ["BRAILLE LINE:  'Kenya collapsed list item'",
     "     VISIBLE:  'Kenya collapsed list item', cursor=1",
     "BRAILLE LINE:  'Kenya collapsed list item'",
     "     VISIBLE:  'Kenya collapsed list item', cursor=1",
     "SPEECH OUTPUT: 'Kenya'",
     "SPEECH OUTPUT: 'collapsed'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Right"))
sequence.append(utils.AssertPresentationAction(
    "7. Expand Kenya",
    ["BRAILLE LINE:  'Kenya expanded list item'",
     "     VISIBLE:  'Kenya expanded list item', cursor=1",
     "SPEECH OUTPUT: 'expanded'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Left"))
sequence.append(utils.AssertPresentationAction(
    "8. Collapse Kenya",
    ["BRAILLE LINE:  'Kenya collapsed list item'",
     "     VISIBLE:  'Kenya collapsed list item', cursor=1",
     "SPEECH OUTPUT: 'collapsed'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Down"))
sequence.append(utils.AssertPresentationAction(
    "9. Down arrow to Sudan",
    ["BRAILLE LINE:  'Sudan collapsed list item'",
     "     VISIBLE:  'Sudan collapsed list item', cursor=1",
     "BRAILLE LINE:  'Sudan collapsed list item'",
     "     VISIBLE:  'Sudan collapsed list item', cursor=1",
     "SPEECH OUTPUT: 'Sudan'",
     "SPEECH OUTPUT: 'collapsed'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Down"))
sequence.append(utils.AssertPresentationAction(
    "10. Down arrow to Asia",
    ["BRAILLE LINE:  'Asia collapsed list item'",
     "     VISIBLE:  'Asia collapsed list item', cursor=1",
     "BRAILLE LINE:  'Asia collapsed list item'",
     "     VISIBLE:  'Asia collapsed list item', cursor=1",
     "SPEECH OUTPUT: 'Asia'",
     "SPEECH OUTPUT: 'collapsed tree level 2'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Right"))
sequence.append(utils.AssertPresentationAction(
    "11. Expand Asia",
    ["BRAILLE LINE:  'Asia expanded list item'",
     "     VISIBLE:  'Asia expanded list item', cursor=1",
     "SPEECH OUTPUT: 'expanded'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Down"))
sequence.append(utils.AssertPresentationAction(
    "12. Down arrow to China",
    ["KNOWN ISSUE: We shouldn't be speaking the panel here",
     "BRAILLE LINE:  'China list item'",
     "     VISIBLE:  'China list item', cursor=1",
     "BRAILLE LINE:  'China list item'",
     "     VISIBLE:  'China list item', cursor=1",
     "SPEECH OUTPUT: 'Asia'",
     "SPEECH OUTPUT: 'panel'",
     "SPEECH OUTPUT: 'China'",
     "SPEECH OUTPUT: 'tree level 3'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Down"))
sequence.append(utils.AssertPresentationAction(
    "13. Down arrow to India",
    ["BRAILLE LINE:  'India list item'",
     "     VISIBLE:  'India list item', cursor=1",
     "BRAILLE LINE:  'India list item'",
     "     VISIBLE:  'India list item', cursor=1",
     "SPEECH OUTPUT: 'India'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Down"))
sequence.append(utils.AssertPresentationAction(
    "14. Down arrow to Russia",
    ["BRAILLE LINE:  'Russia list item'",
     "     VISIBLE:  'Russia list item', cursor=1",
     "BRAILLE LINE:  'Russia list item'",
     "     VISIBLE:  'Russia list item', cursor=1",
     "SPEECH OUTPUT: 'Russia'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Down"))
sequence.append(utils.AssertPresentationAction(
    "15. Down arrow to Mongolia",
    ["BRAILLE LINE:  'Mongolia list item'",
     "     VISIBLE:  'Mongolia list item', cursor=1",
     "BRAILLE LINE:  'Mongolia list item'",
     "     VISIBLE:  'Mongolia list item', cursor=1",
     "SPEECH OUTPUT: 'Mongolia'"]))

sequence.append(utils.AssertionSummaryAction())
sequence.start()
