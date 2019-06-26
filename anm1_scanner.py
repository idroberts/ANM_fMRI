#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ANM1_scanner
author: Ian Roberts

with eye tracker
allows for restarting
"""

# load modules
import pandas as pd
import numpy as np
import random, os, time, sys, pylink
from psychopy.preferences import prefs
prefs.general['shutdownKey'] = 'escape' # set experiment escape key
from psychopy import visual, core, event, data, gui, logging, info, monitors
import itertools

# load experiment functions
import generalFunctions as gf
import questionnaires as qs
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy


class EyeLinkNoOutput(pylink.EyeLink):

    def __init__(self, ipaddr=None):
        pylink.EyeLink.__init__(self, ipaddr)

    def progressUpdate(self, arg1, arg2):
        pass


# general experiment settings
expName = 'ANM1_scanner'  # experiment name
edfName = 'ANM'
expVersion = 2.5  # experiment version
DEBUG = False  # set debug mode (if True: not fullscreen and subject number is 9999)
dummyMode = False  # whether to run eye tracker in dummy mode (don't collect) or not
dispMonitor = 'testMonitor'  # display name
screenToUse = 1
overallTrialNum = 0  # initialize overall trial number to be 0
textFont = 'Arial'
scannerTrigger = '5'


# set up counterbalances
partnerColors = list(itertools.permutations([(1,1,-1),  # yellow
                                             (-1,-1,1),  # blue
                                             (1,-1,-1)]))  # red
partnerShapes = list(itertools.permutations([3, 4, 32]))  # number of edges
respOrders = ['LtoR', 'RtoL']
blockSets = list(itertools.permutations([0, 1, 2]))
selfSide = ['left', 'right']

conds = [respOrders, blockSets, selfSide]
condCombos = list(itertools.product(*conds))  # generate all possible combinations
nCondCombos = len(condCombos)  # number of counterbalanced condition combinations


# create window for task and run refresh rate test
if DEBUG:
    fullscreen = False
elif not DEBUG:
    fullscreen = True


# present dialogue box for subject info
expInfo = gf.subject_info(entries=['subject', 'fileNumber', 'runNumber', 'saveFile'], debug=DEBUG,
                          debugValues=[999, 1, 1, ''], expName=expName, expVersion=expVersion,
                          counterbalance=nCondCombos)

if expInfo['fileNumber'] is None or expInfo['fileNumber'] == '':
    expInfo['fileNumber'] = 1

if expInfo['runNumber'] is None or expInfo['runNumber'] == '':
    expInfo['runNumber'] = 1
elif 0 < int(expInfo['runNumber']) < 6:
    expInfo['runNumber'] = int(expInfo['runNumber'])
else:
    raise Exception('The run number must be between 1 and 5. The number entered was: %d' %(int(expInfo['runNumber'])))
    win.close()
    core.quit()
# elif expInfo['fileNumber'] < 1 or 9 < expInfo['fileNumber']:
#     raise Exception('File number must be between 1 and 9, inclusive.')
#     win.close()
#     core.quit()

saveDir = os.path.join(os.getcwd(), 'data', 'subject_' + str(expInfo['subject']))
if not os.path.exists(saveDir):
    os.makedirs(saveDir)

if expInfo['saveFile'] is None or expInfo['saveFile'] == '':
    saveFilename = os.path.join(saveDir, "%04d_%s_%s.csv") %(int(expInfo['subject']), expInfo['startTime'], expInfo['expName'])
    saveFilename_practice = os.path.join(saveDir, "%04d_%s_%s_%s.csv") %(int(expInfo['subject']), expInfo['startTime'], expInfo['expName'], 'practice')
    # lastRunNumber = 0
else:
    if expInfo['saveFile'][-4:] == '.csv':
        saveFilename = os.path.join(saveDir, expInfo['saveFile'])
    elif '.' not in expInfo['saveFile'][-4:]:
        saveFilename = os.path.join(saveDir, expInfo['saveFile'] + '.csv')
    else:
        raise Exception("Looks like you've entered the wrong file: saveFile should be a .csv. You entered: %s" %(expInfo['saveFile']))
        win.close()
        core.quit()

    saveFilename_practice = os.path.join(saveDir, "%04d_%s_%s_%s.csv") %(int(expInfo['subject']), expInfo['startTime'], expInfo['expName'], 'practice')
    # prevData = pd.read_csv(saveFilename)
    # lastRunNumber = max(prevData['runNumber'])


###### SETUP EYELINK ######

# setup triggers
pos_instructs = 139
neu_instructs = 129
neg_instructs = 119

pos_fix = 138
neu_fix = 128
neg_fix = 118

pos_loNeed = 130
neu_loNeed = 120
neg_loNeed = 110

pos_hiNeed = 230
neu_hiNeed = 220
neg_hiNeed = 210

pos_prop = 137
neu_prop = 127
neg_prop = 117

pos_resps = [131,132,133,134]
neu_resps = [121,122,123,124]
neg_resps = [111,112,113,114]
no_resp = 99


if not dummyMode:
    tk = EyeLinkNoOutput('100.1.1.1')
else:
    tk = EyeLinkNoOutput(None)

# STEP III: Open an EDF data file EARLY
# Note that the file name cannot exceeds 8 characters
# please open eyelink data files early to record as much info as possible
edfFolder = os.path.join(os.getcwd(), 'edfData')
if not os.path.exists(edfFolder):
    os.makedirs(edfFolder)

edfFileName = edfName + str(expInfo['subject']) + '_' + str(expInfo['fileNumber']) + '.EDF'
tk.openDataFile(edfFileName)
# add personalized data file header (preamble text)
tk.sendCommand("add_file_preamble_text '%s'" %(expName + " v" + str(expVersion) + " file_" + str(expInfo['fileNumber'])))

if DEBUG:
    scnWidth, scnHeight = (1200, 700)
else:
    scnWidth, scnHeight = (1400, 1050)
mon = monitors.Monitor(dispMonitor, width=47.0, distance=100.0)
mon.setSizePix((scnWidth, scnHeight))
win = visual.Window(size=(scnWidth, scnHeight), fullscr=fullscreen, units='pix', monitor=mon, colorSpace='rgb', color=(-1, -1, -1), screen=screenToUse)

# call the custom calibration routine "EyeLinkCoreGraphicsPsychopy.py", instead of the default
# routines that were implemented in SDL
genv = EyeLinkCoreGraphicsPsychoPy(tk, win)
pylink.openGraphicsEx(genv)

# STEP V: Set up the tracker
# we need to put the tracker in offline mode before we change its configrations
tk.setOfflineMode()

# sampling rate, 250, 500, 1000, or 2000; this command won't work for EyeLInk II/I
tk.sendCommand('sample_rate 500')

# inform the tracker the resolution of the subject display
# [see Eyelink Installation Guide, Section 8.4: Customizing Your PHYSICAL.INI Settings ]
tk.sendCommand("screen_pixel_coords = 0 0 %d %d" % (scnWidth-1, scnHeight-1))

# save display resolution in EDF data file for Data Viewer integration purposes
# [see Data Viewer User Manual, Section 7: Protocol for EyeLink Data to Viewer Integration]
tk.sendMessage("DISPLAY_COORDS = 0 0 %d %d" % (scnWidth-1, scnHeight-1))

# specify the calibration type, H3, HV3, HV5, HV13 (HV = horiztonal/vertical),
tk.sendCommand("calibration_type = HV5") # tk.setCalibrationType('HV9') also works, see the Pylink manual

# the model of the tracker, 1-EyeLink I, 2-EyeLink II, 3-Newer models (100/1000Plus/DUO)
eyelinkVer = tk.getTrackerVersion()

#turn off scenelink camera stuff (EyeLink II/I only)
if eyelinkVer == 2: tk.sendCommand("scene_camera_gazemap = NO")

# Set the tracker to parse Events using "GAZE" (or "HREF") data
tk.sendCommand("recording_parse_type = GAZE")

# Online parser configuration: 0-> standard/coginitve, 1-> sensitive/psychophysiological
# the Parser for EyeLink I is more conservative, see below
# [see Eyelink User Manual, Section 4.3: EyeLink Parser Configuration]
if eyelinkVer>=2: tk.sendCommand('select_parser_configuration 0')

# get Host tracking software version
hostVer = 0
if eyelinkVer == 3:
    tvstr  = tk.getTrackerVersionString()
    vindex = tvstr.find("EYELINK CL")
    hostVer = int(float(tvstr[(vindex + len("EYELINK CL")):].strip()))

# specify the EVENT and SAMPLE data that are stored in EDF or retrievable from the Link
# See Section 4 Data Files of the EyeLink user manual
tk.sendCommand("file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT")
tk.sendCommand("link_event_filter = LEFT,RIGHT,FIXATION,FIXUPDATE,SACCADE,BLINK,BUTTON,INPUT")
if hostVer>=4:
    tk.sendCommand("file_sample_data = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS,HTARGET,INPUT")
    tk.sendCommand("link_sample_data = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,HTARGET,INPUT")
else:
    tk.sendCommand("file_sample_data = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS,INPUT")
    tk.sendCommand("link_sample_data = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,INPUT")



# get partner cue combo
partnerConds = [partnerColors, partnerShapes]
partnerCombos = list(itertools.product(*partnerConds))
random.seed(1928)
random.shuffle(partnerCombos)
partnerCounterbalance = expInfo['subject'] % len(partnerCombos)

runTimeTest = info.RunTimeInfo(win=win, refreshTest=True)
currRefreshRate = runTimeTest['windowRefreshTimeAvg_ms'] / 1000
print currRefreshRate


payFile = os.path.join(os.getcwd(), 'data', 'payFile.csv')
dgQuizFile = os.path.join(os.getcwd(), 'stim', 'anm1_dgQuiz.csv')
pdQuizFile = os.path.join(os.getcwd(), 'stim', 'anm1_pdQuiz.csv')


# generate names for data and session log files
payInfo = os.path.join(saveDir, "%04d_payInfo.txt") %(int(expInfo['subject']))
logFilename = os.path.join(saveDir, "%04d_%s_%s.log") %(int(expInfo['subject']), expInfo['startTime'], expInfo['expName'])
logfile = logging.LogFile(logFilename, filemode = 'w', level = logging.EXP) #set logging information (core.quit() is required at the end of experiment to store logging info!!!)

# create clocks for timing
globalClock = core.Clock()
blockClock = core.Clock()
rtClock = core.Clock()


### settings for experimental tasks
# file paths for images
respOptsImageFile = os.path.join("stim", "respOpts.png")

subjectConds = condCombos[expInfo['counterbalance']]
subjectPartners = partnerCombos[partnerCounterbalance]

### partner cue settings

# partner colors (colors stored in 0th element)
posColor = subjectPartners[0][0]
neuColor = subjectPartners[0][1]
negColor = subjectPartners[0][2]

# partner shapes (shapes stored in 1st element)
posShape = visual.Polygon(win=win, edges=subjectPartners[1][0], radius=100, units="pix")
neuShape = visual.Polygon(win=win, edges=subjectPartners[1][1], radius=100, units="pix")
negShape = visual.Polygon(win=win, edges=subjectPartners[1][2], radius=100, units="pix")

posShape.lineColor = posColor
posShape.fillColor = posColor
neuShape.lineColor = neuColor
neuShape.fillColor = neuColor
negShape.lineColor = negColor
negShape.fillColor = negColor

# resp options ordering (ordering stored in 2nd element)
respOrder = subjectConds[0]

partnerSymbols = pd.DataFrame({"partner": ["pos", "neu", "neg"],
                               "color": [posColor, neuColor, negColor],
                               "shape": [posShape.edges, neuShape.edges, negShape.edges],
                               "subject": expInfo['subject'],
                               "counterbalance": expInfo['counterbalance']})
partnerSymbols.to_csv(os.path.join(saveDir, "%04d_%s_%s_%s.csv") %(int(expInfo['subject']), expInfo['startTime'], expInfo['expName'], 'partnerSymbols'), header = True, mode = 'w', index = False)


# counterbalance partner block sets
blockSets = ('anm1_partner1_trials.csv', 'anm1_partner2_trials.csv', 'anm1_partner3_trials.csv')

posBlocks = pd.read_csv(os.path.join(os.getcwd(), 'stim', blockSets[subjectConds[1][0]]))
neuBlocks = pd.read_csv(os.path.join(os.getcwd(), 'stim', blockSets[subjectConds[1][1]]))
negBlocks = pd.read_csv(os.path.join(os.getcwd(), 'stim', blockSets[subjectConds[1][2]]))

posBlocks['partner'] = 'pos'
neuBlocks['partner'] = 'neu'
negBlocks['partner'] = 'neg'

posBlocks['blockSet'] = blockSets[subjectConds[1][0]]
neuBlocks['blockSet'] = blockSets[subjectConds[1][1]]
negBlocks['blockSet'] = blockSets[subjectConds[1][2]]


# load practice block
pracBlock = pd.read_csv(os.path.join(os.getcwd(), 'stim', 'anm1_practice2_trials.csv'))
pracBlock = pracBlock.loc[range(18),:]  # trim to just 18 trials (even 3-way split)
pracPartnerOrder = ['pos', 'neu', 'neg']
random.shuffle(pracPartnerOrder)  # randomly order partners
pracBlock.loc[range(0,6), 'partner'] = pracPartnerOrder[0]  # label partners
pracBlock.loc[range(6,12), 'partner'] = pracPartnerOrder[1]
pracBlock.loc[range(12,18), 'partner'] = pracPartnerOrder[2]
pracBlock['blockSet'] = 'anm1_practice2_trials.csv'
pracBlock['instructsDur'] = 0
pracBlock['instructsJitterDur'] = 0
pracBlock.loc[[0,6,12], 'instructsDur'] = 10.0
pracBlock.loc[[0,6,12], 'instructsJitterDur'] = random.sample([1.5, 2.5, 3.5], 3)
pracBlock['partnerBlockTrialNum'] = [1,2,3,4,5,6] * 3
pracBlock['partnerBlockNum'] = 0
pracBlock['overallPartnerTrialNum'] = 0
pracBlock = pracBlock.reindex_axis(sorted(pracBlock.columns), axis=1)  # sort columns alphabetically

## settings for dictator game
dflt = 20  # default outcome amount

posRect = visual.Rect(win=win, width=1300, height=850, lineWidth=10, lineColor=posColor, units="pix")
neuRect = visual.Rect(win=win, width=1300, height=850, lineWidth=10, lineColor=neuColor, units="pix")
negRect = visual.Rect(win=win, width=1300, height=850, lineWidth=10, lineColor=negColor, units="pix")
pracRect = visual.Rect(win=win, width=1300, height=850, lineWidth=10, lineColor=(1,1,1), units="pix")
respRect = visual.Rect(win=win, pos=(0,20), width=850, height=350, lineWidth=10, lineColor=(-0.1, -0.1, -0.1), units="pix")

partnerBlockText = visual.TextStim(win=win, text='For the following trials, your partner will be:', pos=(0,250), color=(1,1,1), font=textFont, height=50, units="pix", wrapWidth=1000)
pauseText = visual.TextStim(win=win, text='Please take a moment to rest', pos=(0,0), color=(1,1,1), font=textFont, height=50, units="pix", wrapWidth=1200)
preparingScannerText = visual.TextStim(win=win, text='Preparing scanner...', pos=(0,0), color=(1,1,1), font=textFont, height=50, units="pix")
waitingForScannerText = visual.TextStim(win=win, text='Waiting for scanner...', pos=(0,0), color=(1,1,1), font=textFont, height=50, units="pix")
initialScansText = visual.TextStim(win=win, text='Taking initial scans...', pos=(0,0), color=(1,1,1), font=textFont, height=50, units="pix")

fixation = visual.TextStim(win=win, text='+', pos=(0,0), color=(1,1,1), font=textFont, units="pix", height=70)
probText = visual.TextStim(win=win, text='', pos=(0,0), color=(1,1,1), font=textFont, height=120, units="pix")

# counterbalance self other sides
if subjectConds[2] == 'left':
    selfLabel = visual.TextStim(win=win, text='You', pos=(-300,70), color=(1,1,1), font=textFont, height=60, units="pix")
    otherLabel = visual.TextStim(win=win, text='Partner', pos=(300,70), color=(1,1,1), font=textFont, height=60, units="pix")
    selfAmount = visual.TextStim(win=win, text='00', pos=(-300, -70), color=(1,1,1), font=textFont, height=120, units="pix")
    otherAmount = visual.TextStim(win=win, text='00', pos=(300, -70), color=(1,1,1), font=textFont, height=120, units="pix")
elif subjectConds[2] == 'right':
    selfLabel = visual.TextStim(win=win, text='You', pos=(300,70), color=(1,1,1), font=textFont, height=60, units="pix")
    otherLabel = visual.TextStim(win=win, text='Partner', pos=(-300,70), color=(1,1,1), font=textFont, height=60, units="pix")
    selfAmount = visual.TextStim(win=win, text='00', pos=(300, -70), color=(1,1,1), font=textFont, height=120, units="pix")
    otherAmount = visual.TextStim(win=win, text='00', pos=(-300, -70), color=(1,1,1), font=textFont, height=120, units="pix")


# create response keys
respKeys = ['1', '2', '3', '4']  # list of response keys that subjects can use
if respOrder == 'LtoR':
    respHandImageFile = os.path.join("stim", "hand_LtoR.png")
    respLabels = ['strong\n  no', 'no', 'yes', 'strong\n  yes']  # initialize list of response labels to be displayed on screen
    acceptKeys = ['3', '4']
    rejectKeys = ['1', '2']
    respDecode = {'1': 1, '2': 2, '3': 3, '4': 4}
else:
    respHandImageFile = os.path.join("stim", "hand_RtoL.png")
    respLabels = ['strong\n  yes', 'yes', 'no', 'strong\n  no']  # initialize list of response labels to be displayed on screen
    acceptKeys = ['1', '2']
    rejectKeys = ['3', '4']
    respDecode = {'1': 4, '2': 3, '3': 2, '4': 1}
# generate TextStim for response options
respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=respLabels,
                                     scaleWidth=400, primaryPos=-300, primaryHeight=40, win=win, bold=True, units='pix')


# Load instruction images

# get neutral partner shape and color
neuColorText = 'yellow'
if neuColor == (1,1,-1):
    neuColorText = 'yellow'
elif neuColor == (-1,-1,1):
    neuColorText = 'blue'
elif neuColor == (1,-1,-1):
    neuColorText = 'red'

instructSummaryFile = os.path.join(os.getcwd(), 'taskInstructs', 'instructSummary_%s_%d_%s.png' %(neuColorText, neuShape.edges, subjectConds[2]))

instructSummary = visual.ImageStim(win=win, pos=(0,0),
    image=os.path.join(os.getcwd(), 'taskInstructs', 'instructSummary_%s_%d_%s.png' %(neuColorText, neuShape.edges, subjectConds[2])),
    size=(720, 405), units="pix")

respOptsImage = visual.ImageStim(win=win, pos=(0,-0.3), image=respOptsImageFile, size=(560, 269), units="pix")

respHandImage = visual.ImageStim(win=win, pos=(0,-270), image=respHandImageFile, size=(400,404), units="pix")

mouse = event.Mouse(visible=False, win=win)  # create mouse

# ============================================================================ #
# CUSTOM FUNCTIONS FOR TASKS

def initial_scans():

    event.clearEvents()

    initialScansText.setAutoDraw(True)

    while not event.getKeys(keyList = ['space']):
        win.flip()

    initialScansText.setAutoDraw(False)
    event.clearEvents()


def generate_runs(posBlocks=None, neuBlocks=None, negBlocks=None):
    ''' Function to generate runs for presentation

    Args:
        posBlocks (data frame): pandas data frame of positive partner blocks
        neuBlocks (data frame): pandas data frame of neutral partner blocks
        negBlocks (data frame): pandas data frame of negative partner blocks
    '''

    posBlocks = posBlocks.copy()
    neuBlocks = neuBlocks.copy()
    negBlocks = negBlocks.copy()

    posBlockOrder = [1, 2, 3, 4, 5]
    neuBlockOrder = [1, 2, 3, 4, 5]
    negBlockOrder = [1, 2, 3, 4, 5]

    random.seed(expInfo['subject'])
    random.shuffle(posBlockOrder)
    random.shuffle(neuBlockOrder)
    random.shuffle(negBlockOrder)

    runs = {}

    for run in range(5):
        posBlock = posBlocks[posBlocks['partnerBlockNum'] == posBlockOrder[run]].copy()
        neuBlock = neuBlocks[neuBlocks['partnerBlockNum'] == neuBlockOrder[run]].copy()
        negBlock = negBlocks[negBlocks['partnerBlockNum'] == negBlockOrder[run]].copy()

        posBlock.reset_index(drop=True, inplace=True)
        neuBlock.reset_index(drop=True, inplace=True)
        negBlock.reset_index(drop=True, inplace=True)

        posBlock['instructsDur'] = 0
        neuBlock['instructsDur'] = 0
        negBlock['instructsDur'] = 0

        posBlock['instructsJitterDur'] = 0
        neuBlock['instructsJitterDur'] = 0
        negBlock['instructsJitterDur'] = 0

        instructsJitters = [1.5, 2.5, 3.5]
        random.shuffle(instructsJitters)
        posBlock.loc[0, 'instructsDur'] = 10.0
        neuBlock.loc[0, 'instructsDur'] = 10.0
        negBlock.loc[0, 'instructsDur'] = 10.0

        posBlock.loc[0, 'instructsJitterDur'] = instructsJitters[0]
        neuBlock.loc[0, 'instructsJitterDur'] = instructsJitters[1]
        negBlock.loc[0, 'instructsJitterDur'] = instructsJitters[2]

        blocks = [posBlock, neuBlock, negBlock]
        random.shuffle(blocks)

        runs[run] = pd.concat(blocks, ignore_index=True)

        # sort columns alphabetically
        runs[run] = runs[run].reindex_axis(sorted(runs[run].columns), axis=1)

    return runs


def run_decision_run(trialsDf=None, saveFile=None):

    # write header to csv or not? Default is not to write header. Try to read csv file from working directory. If fail to read csv (it hasn't been created yet), then the csv has to be created for the study and the header has to be written.
    writeHeader = False
    try:  # try reading csv file dimensions (rows = no. of trials)
        pd.read_csv(saveFile)
    except:  # if fail to read csv, then it's trial 1
        writeHeader = True

    # store additional info in data frame
    trialsDf['accept'] = np.nan
    trialsDf['subject'] = expInfo['subject']
    trialsDf['expName'] = expInfo['expName']
    trialsDf['expVersion'] = expInfo['expVersion']
    trialsDf['startTime'] = str(time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime()))
    trialsDf['endTime'] = np.nan
    trialsDf['windowRefreshTimeAvg_ms'] = runTimeTest['windowRefreshTimeAvg_ms']
    trialsDf['windowRefreshTimeSD_ms'] = runTimeTest['windowRefreshTimeSD_ms']
    trialsDf['runNumber'] = 0
    # trialsDf['blockTime'] = np.nan
    trialsDf['globalTime'] = np.nan
    trialsDf['fileNumber'] = expInfo['fileNumber']
    trialsDf['resp'] = None
    trialsDf['respNum'] = None
    trialsDf['rt'] = np.nan
    trialsDf['overallTrialNumber'] = 0
    trialsDf['selfSide'] = subjectConds[2]
    trialsDf['respOrder'] = respOrder
    trialsDf['instructs_onset'] = np.nan
    trialsDf['instructsJitter_onset'] = np.nan
    trialsDf['need_onset'] = np.nan
    trialsDf['jitter_onset'] = np.nan
    trialsDf['prop_onset'] = np.nan
    trialsDf['iti_onset'] = np.nan
    trialsDf['resp_onset'] = np.nan
    trialsDf['instructsTTL'] = np.nan
    trialsDf['fixTTL'] = np.nan
    trialsDf['needTTL'] = np.nan
    trialsDf['propTTL'] = np.nan
    trialsDf['respTTL'] = np.nan
    # trialsDf['implementPain'] = np.nan


    # DISPLAY PAUSE SCREEN
    pauseText.setAutoDraw(True)
    event.clearEvents()
    timer = core.CountdownTimer(5.0)
    noPauseResp = True
    while noPauseResp:
        if timer.getTime() < 0:
            keysPressed = event.getKeys(keyList=['space'])
            if len(keysPressed) > 0:
                noPauseResp = False
        else:
            event.clearEvents()
        win.flip()
    event.clearEvents()
    pauseText.setAutoDraw(False)
    win.flip()

    # RUN CALIBRATION
    tk.doTrackerSetup()

    # BUTTON REMINDER
    # gf.show_instructs(win=win,
    #     text=["A quick reminder:"],
    #     timeAutoAdvance=0, timeRequired=0, advanceKey=['1','2','3','4'], image=respHandImageFile, imageDim=(400,404),
    #     imagePos=(0,-50), scaleImage=1.0,
    #     saveFile=os.path.join(saveDir, "instructs21_.png"), units='pix')

    # PAUSE FOR EXPERIMENTER
    preparingScannerText.setAutoDraw(True)
    event.clearEvents()
    notReady = True
    while notReady:
        keysPressed = event.getKeys(keyList = ['space', 'q'])
        if len(keysPressed) > 0:
            if keysPressed[0] == 'space':
                notReady =  False
            elif keysPressed[0] == 'q':
                # QUIT PROGRAM

                # close the EDF data file
                tk.setOfflineMode()
                tk.closeDataFile()
                pylink.pumpDelay(50)

                # Get the EDF data and say goodbye
                tk.receiveDataFile(edfFileName, os.path.join(edfFolder, edfFileName))

                # close the link to the tracker
                tk.close()

                # close the graphics
                pylink.closeGraphics()

                win.close()
                core.quit()

        win.flip()
    event.clearEvents()
    preparingScannerText.setAutoDraw(False)

    # Assign runNumber based on existing csv file. Read the csv file and find the largest block number and add 1 to it to reflect this block's number.
    # try:
    #     runNumber = max(pd.read_csv(saveFile)['runNumber']) + 1
    #     trialsDf['runNumber'] = runNumber
    # except:  # if fail to read csv, then it's block 1
    #     runNumber = 1
    #     trialsDf['runNumber'] = runNumber

    # Assign runNumber
    runNumber = expInfo['runNumber']
    trialsDf['runNumber'] = runNumber

    # start eye tracker recording
    error = tk.startRecording(1,1,1,1)
    pylink.pumpDelay(100) # wait for 100 ms to make sure data of interest is recorded

    # WAIT FOR SCANNER START
    respHandImage.setAutoDraw(True)
    waitingForScannerText.setAutoDraw(True)
    event.clearEvents()
    while not event.getKeys(keyList = ['5']):
        win.flip()
    event.clearEvents()
    respHandImage.setAutoDraw(False)
    waitingForScannerText.setAutoDraw(False)

    blockClock.reset()

    # initialize variable for storing partner on previous trial
    prevPartner = []

    # run block trials
    for i, thisTrial in trialsDf.iterrows():

        # send the standard "TRIALID" message to mark the start of a trial
        # [see Data Viewer User Manual, Section 7: Protocol for EyeLink Data to Viewer Integration]
        tk.sendMessage('TRIALID')

        # if new partner on this trial, give task instructions
        if trialsDf.loc[i, 'partner'] != prevPartner:

            # change partner rect cue and shape
            instructsTTL = 0
            if trialsDf.loc[i, 'partner'] == 'pos':
                partnerCue = posRect
                partnerShape = posShape
                instructsTTL = pos_instructs
                fixTTL = pos_fix
                loNeedTTL = pos_loNeed
                hiNeedTTL = pos_hiNeed
                propTTL = pos_prop
                respTTLs = pos_resps
            elif trialsDf.loc[i, 'partner'] == 'neu':
                partnerCue = neuRect
                partnerShape = neuShape
                instructsTTL = neu_instructs
                fixTTL = neu_fix
                loNeedTTL = neu_loNeed
                hiNeedTTL = neu_hiNeed
                propTTL = neu_prop
                respTTLs = neu_resps
            elif trialsDf.loc[i, 'partner'] == 'neg':
                partnerCue = negRect
                partnerShape = negShape
                instructsTTL = neg_instructs
                fixTTL = neg_fix
                loNeedTTL = neg_loNeed
                hiNeedTTL = neg_hiNeed
                propTTL = neg_prop
                respTTLs = neg_resps
            elif trialsDf.loc[i, 'partner'] == 'practice':
                partnerCue = pracRect

            # set pos and size
            if trialsDf.loc[i, 'partner'] != 'practice':
                partnerShape.pos = (0,0)
                partnerShape.radius = 100
                partnerCue.setAutoDraw(True)
                partnerShape.setAutoDraw(True)
            elif trialsDf.loc[i, 'partner'] == 'practice':
                partnerCue.setAutoDraw(True)
                otherLabel.pos = (0,0)
                otherLabel.setAutoDraw(True)

            # DISPLAY INSTRUCTIONS
            tk.sendMessage('instructs_onset %d' %(instructsTTL))  # send fixation onset to EyeLink
            partnerBlockText.setAutoDraw(True)
            trialsDf.loc[i, 'instructs_onset'] = blockClock.getTime()
            timer = core.CountdownTimer(10.0)  # display for 10 secs
            while timer.getTime() > 0:
                win.flip()
            partnerBlockText.setAutoDraw(False)

            # set for trials
            if trialsDf.loc[i, 'partner'] != 'practice':
                partnerShape.setAutoDraw(False)
                if subjectConds[2] == 'left':
                    partnerShape.pos = (300,70)
                elif subjectConds[2] == 'right':
                    partnerShape.pos = (-300,70)
                partnerShape.radius = 80
            elif trialsDf.loc[i, 'partner'] == 'practice':
                otherLabel.setAutoDraw(False)
                if subjectConds[2] == 'left':
                    otherLabel.pos = (300,70)
                elif subjectConds[2] == 'right':
                    otherLabel.pos = (-300,70)

            # INSTRUCTIONS JITTER
            tk.sendMessage('fixation_onset %d' %(fixTTL))  # send fixation onset to EyeLink
            fixation.setAutoDraw(True)
            trialsDf.loc[i, 'instructsJitter_onset'] = blockClock.getTime()
            timer = core.CountdownTimer(trialsDf.loc[i, 'instructsJitterDur'])
            while timer.getTime() > 0:
                win.flip()
            fixation.setAutoDraw(False)


        global overallTrialNum
        trialsDf.loc[i, 'overallTrialNumber'] = overallTrialNum + 1
        overallTrialNum += 1

        trialsDf.loc[i, 'blockTrialNum'] = i + 1

        keysPressed = []  # initialize list of keys pressed
        keyResp = None  # initialize key response as None
        RT = None  # initialize RT as None
        # RTfromClock = None

        # set trial values
        selfAmount.setText(str(trialsDf.loc[i, 'selfProp']))
        otherAmount.setText(str(trialsDf.loc[i, 'otherProp']))
        probText.setText(str(trialsDf.loc[i, 'prob']) + '%')

        # get times at beginning of trial
        trialsDf.loc[i, 'globalTime'] = globalClock.getTime()
        # trialsDf.loc[i, 'blockTime'] = blockClock.getTime()

        # NEED
        if trialsDf.loc[i, 'prob'] > 50:
            tk.sendMessage('hiNeed_onset %d' %(hiNeedTTL))  # send high need onset to EyeLink
        else:
            tk.sendMessage('loNeed_onset %d' %(loNeedTTL))  # send low need onset to EyeLink
        probText.setAutoDraw(True)
        trialsDf.loc[i, 'need_onset'] = blockClock.getTime()
        timer = core.CountdownTimer(trialsDf.loc[i, 'needDur'])
        while timer.getTime() > 0:
            win.flip()
        probText.setAutoDraw(False)

        # JITTER
        tk.sendMessage('fixation_onset %d' %(fixTTL))  # send fixation onset to EyeLink
        fixation.setAutoDraw(True)
        trialsDf.loc[i, 'jitter_onset'] = blockClock.getTime()
        timer = core.CountdownTimer(trialsDf.loc[i, 'jitterDur'])
        while timer.getTime() > 0:
            win.flip()
        fixation.setAutoDraw(False)

        # CHOICE
        selfLabel.setAutoDraw(True)
        selfAmount.setAutoDraw(True)
        otherAmount.setAutoDraw(True)

        if trialsDf.loc[i, 'partner'] != 'practice':
            partnerShape.setAutoDraw(True)
        elif trialsDf.loc[i, 'partner'] == 'practice':
            otherLabel.setAutoDraw(True)

        if trialsDf.loc[i, 'blockType'] == 'practice':
            for j in respKeys:
                respOptions[j].setAutoDraw(True)

        win.callOnFlip(rtClock.reset)  # reset rtClock on next window flip
        event.clearEvents()  # clear events

        # display proposal and collect response
        tk.sendMessage('proposal_onset %d' %(propTTL))  # send proposal onset to EyeLink
        trialsDf.loc[i, 'prop_onset'] = blockClock.getTime()
        timer = core.CountdownTimer(trialsDf.loc[i, 'propDur'])
        while timer.getTime() > 0:
            keysPressed = event.getKeys(keyList=respKeys + ['q'], timeStamped=rtClock)  # load keys that have been pressed

            if len(keysPressed) > 0:  # check if a key has been pressed yet
                if keyResp is None:  # check if another key response has already been recorded
                    trialsDf.loc[i, 'resp_onset'] = blockClock.getTime()
                    keyResp, RT = keysPressed[0]  # access first key response and corresponding RT
                    # RTfromClock = rtClock.getTime()  # record RT from rtClock

                    if keyResp == 'q':
                        # QUIT RUN AND PROGRAM

                        # close the EDF data file
                        tk.setOfflineMode()
                        tk.closeDataFile()
                        pylink.pumpDelay(50)

                        # Get the EDF data and say goodbye
                        tk.receiveDataFile(edfFileName, os.path.join(edfFolder, edfFileName))

                        # close the link to the tracker
                        tk.close()

                        # close the graphics
                        pylink.closeGraphics()

                        v = 1
                        abortFile = os.path.join(saveDir, "%04d_abortRun%d_%d.csv") %(int(expInfo['subject']), runNumber, v)
                        while os.path.isfile(abortFile):
                            v += 1
                            abortFile = os.path.join(saveDir, "%04d_abortRun%d_%d.csv") %(int(expInfo['subject']), runNumber, v)
                        
                        trialsDf.to_csv(abortFile, header = True, mode = 'a', index = False)

                        win.close()
                        core.quit()

                    # send response onset to EyeLink
                    tk.sendMessage('response_onset %d' %(respTTLs[respDecode[keyResp] - 1]))  # subtract 1 for indexing

                    respRect.setAutoDraw(True)
                    if trialsDf.loc[i, 'blockType'] == 'practice':
                        # change color of option selected
                        selectedOption = respOptions[keyResp]
                        selectedOption.color = (-1, 1, -1)

            win.flip()

        # TRIAL CLEAN UP
        selfLabel.setAutoDraw(False)
        selfAmount.setAutoDraw(False)
        otherAmount.setAutoDraw(False)
        respRect.setAutoDraw(False)

        if trialsDf.loc[i, 'partner'] != 'practice':
            partnerShape.setAutoDraw(False)
        elif trialsDf.loc[i, 'partner'] == 'practice':
            otherLabel.setAutoDraw(False)

        if trialsDf.loc[i, 'blockType'] == 'practice':
            for j in respKeys:
                respOptions[j].setAutoDraw(False)
            # change back color of selected option
            if keyResp is not None:
                selectedOption.color = (1,1,1)

        if trialsDf.loc[i, 'partner'] != prevPartner:
            trialsDf.loc[i, 'instructsTTL'] = instructsTTL

        # set current partner as previous partner
        prevPartner = trialsDf.loc[i, 'partner']

        # RECORD DATA
        # code response as accept or reject
        if keyResp in acceptKeys:
            trialsDf.loc[i, 'accept'] = 1
        elif keyResp in rejectKeys:
            trialsDf.loc[i, 'accept'] = 0
        else:
            trialsDf.loc[i, 'accept'] = np.nan

        trialsDf.loc[i, 'fixTTL'] = fixTTL
        trialsDf.loc[i, 'propTTL'] = propTTL
        if trialsDf.loc[i, 'prob'] > 50:
            trialsDf.loc[i, 'needTTL'] = hiNeedTTL  # send high need onset to EyeLink
        else:
            trialsDf.loc[i, 'needTTL'] = loNeedTTL  # send high need onset to EyeLink

        # append data to data frame
        trialsDf.loc[i, 'resp'] = keyResp
        if keyResp is not None:
            trialsDf.loc[i, 'respNum'] = respDecode[keyResp]
            trialsDf.loc[i, 'respTTL'] = respTTLs[respDecode[keyResp] - 1]
        else:
            trialsDf.loc[i, 'respTTL'] = no_resp
            tk.sendMessage('response_onset %d' %(no_resp))  # send no response TTL
        trialsDf.loc[i, 'rt'] = RT

        # ITI
        tk.sendMessage('fixation_onset %d' %(fixTTL))  # send fixation onset to EyeLink
        fixation.setAutoDraw(True)
        trialsDf.loc[i, 'iti_onset'] = blockClock.getTime()
        timer = core.CountdownTimer(trialsDf.loc[i, 'itiDur'])
        while timer.getTime() > 0:
            win.flip()
        fixation.setAutoDraw(False)

    # ADD EXTRA FIXATION TIME AT END OF RUN
    fixation.setAutoDraw(True)
    timer = core.CountdownTimer(10)
    while timer.getTime() > 0:
        win.flip()
    fixation.setAutoDraw(False)
    trialsDf.loc[i, 'itiDur'] += 10  # add the extra 10 seconds to the last iti duration

    posRect.setAutoDraw(False)
    neuRect.setAutoDraw(False)
    negRect.setAutoDraw(False)
    pracRect.setAutoDraw(False)

    trialsDf['endTime'] = str(time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime()))
    tk.stopRecording() # stop recording

    # append block data to save file
    trialsDf.to_csv(saveFile, header = writeHeader, mode = 'a', index = False)

    return trialsDf



def select_dictator_decision():
    allDecisions = pd.read_csv(saveFilename)
    allDecisions = allDecisions[allDecisions['blockType'] != 'practice']
    selectedTrial = allDecisions.sample(1)

    if pd.notnull(selectedTrial['accept']).values[0]:
        if selectedTrial['accept'].values == 1:
            selfOut = np.asscalar(selectedTrial['selfProp'])
            otherOut = np.asscalar(selectedTrial['otherProp'])
        else:
            selfOut = dflt
            otherOut = dflt
    else:
        randAccept = random.randint(0, 1)
        selectedTrial['accept'] = randAccept
        if randAccept == 1:
            selfOut = np.asscalar(selectedTrial['selfProp'])
            otherOut = np.asscalar(selectedTrial['otherProp'])
        else:
            selfOut = dflt
            otherOut = dflt

    painProb = float(selectedTrial['prob']) / 100.0
    subjectRole = 'dictator'

    decisionResult = pd.DataFrame({'dictator': [selfOut],
    'receiver': [otherOut],
    'dictator_proposed': np.asscalar(selectedTrial['selfProp']),
    'receiver_proposed': np.asscalar(selectedTrial['otherProp']),
    'accept': selectedTrial['accept'].values,
    'painProb': [painProb]})
    # 'painImplement': [""],
    # 'subjectRole': [subjectRole],
    # 'finalProb': [np.nan],
    # 'finalPay': [np.nan],
    # 'amountSpent': [np.nan]})

    return decisionResult


# ============================================================================ #
# RUN EXPERIMENT

gf.show_instructs(win=win, text=["Welcome to the experiment!"],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], saveFile=os.path.join(saveDir, "instructs0.png"), units='pix')

### Dictator Game --------------------------------------------------------------

# generate runs
runs = generate_runs(posBlocks=posBlocks, neuBlocks=neuBlocks, negBlocks=negBlocks)

# pause for initial scans
initial_scans()

# run practice if haven't done any runs yet
if expInfo['runNumber'] < 2:
    # review task instructions
    gf.show_instructs(win=win,
        text=["Before beginning the actual task, you're going to complete one block of practice trials so that you can get familiar with how the task will go in the scanner.\n\nWe'll quickly review the task before starting."],
        timeAutoAdvance=0, timeRequired=0, advanceKey=['1','2','3','4'], saveFile=os.path.join(saveDir, "instructs20_.png"), units='pix')

    gf.show_instructs(win=win,
        text=["First, recall that you will be using the buttons on the buttonbox to provide the following responses:"],
        timeAutoAdvance=0, timeRequired=0, advanceKey=['1','2','3','4'], image=respHandImageFile, imageDim=(400,404),
        imagePos=(0,-50), scaleImage=1.0,
        saveFile=os.path.join(saveDir, "instructs21_.png"), units='pix')

    gf.show_instructs(win=win,
        text=["Here are what each of the responses mean:"],
        timeAutoAdvance=0, timeRequired=0, advanceKey=['1','2','3','4'], image=respOptsImageFile,
        imageDim=(659,381), imagePos=(0,-50),
        saveFile=os.path.join(saveDir, "instructs22_.png"), units='pix')

    gf.show_instructs(win=win,
        text=[""],
        timeAutoAdvance=0, timeRequired=0, advanceKey=['1','2','3','4'], image=instructSummaryFile,
        imageDim=(1200,675), imagePos=(0,0),
        saveFile=os.path.join(saveDir, "instructs23_.png"), units='pix')

    gf.show_instructs(win=win,
        text=["You will now complete a brief practice block. Let the experimenter know if you have any questions before beginning.\n\nDuring the practice block you will have a key at the bottom of the screen letting you know what button you pressed.\n\nThis key will be removed for the actual task. Please use the practice trials to make sure that you are responding as you intend."],
        timeAutoAdvance=0, timeRequired=0, advanceKey=['1','2','3','4'],
        saveFile=os.path.join(saveDir, "instructs24_.png"), units='pix', textPos=(0,0))

    # run practice
    # pracBlock = pracBlock.loc[range(3),:]
    run_decision_run(trialsDf=pracBlock, saveFile=saveFilename_practice)

    gf.show_instructs(win=win,
        text=["You have completed the practice trials. Let the experimenter know if you have any questions."],
        timeAutoAdvance=0, timeRequired=0, advanceKey=['1','2','3','4'], saveFile=os.path.join(saveDir, "instructs25_.png"), units='pix')

# run task
# runs[0] = runs[0].loc[range(3),:]
# runs[1] = runs[1].loc[range(3),:]
# runs[2] = runs[2].loc[range(3),:]

if expInfo['runNumber'] < 2:
    overallTrialNum = 0
    run_decision_run(trialsDf=runs[0], saveFile=saveFilename)

if expInfo['runNumber'] < 3:
    overallTrialNum = 60
    run_decision_run(trialsDf=runs[1], saveFile=saveFilename)

if expInfo['runNumber'] < 4:
    overallTrialNum = 120
    run_decision_run(trialsDf=runs[2], saveFile=saveFilename)

if expInfo['runNumber'] < 5:
    overallTrialNum = 180
    run_decision_run(trialsDf=runs[3], saveFile=saveFilename)

if expInfo['runNumber'] < 6:
    overallTrialNum = 240
    run_decision_run(trialsDf=runs[4], saveFile=saveFilename)


# randomly select one trial for outcome
selTrial = select_dictator_decision()
print "Ice water probability: %.2f\nDictator proposed: %d\nReceiver proposed: %d\nChoice: %d\nDictator paid: %d\nReceiver paid: %d" %(selTrial['painProb'], selTrial['dictator_proposed'], selTrial['receiver_proposed'], selTrial['accept'], selTrial['dictator'], selTrial['receiver'])
f1=open(payInfo, 'w+')
f1.write("Ice water probability: %.2f\nDictator proposed: %d\nReceiver proposed: %d\nChoice: %d\nDictator paid: %d\nReceiver paid: %d" %(selTrial['painProb'], selTrial['dictator_proposed'], selTrial['receiver_proposed'], selTrial['accept'], selTrial['dictator'], selTrial['receiver']))
f1.close()


# end
gf.show_instructs(win=win,
    text=["You have completed the task."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], saveFile=os.path.join(saveDir, "instructs26_.png"), units='pix')

# close the EDF data file
tk.setOfflineMode()
tk.closeDataFile()
pylink.pumpDelay(50)

# Get the EDF data and say goodbye
tk.receiveDataFile(edfFileName, os.path.join(edfFolder, edfFileName))

# close the link to the tracker
tk.close()

# close the graphics
pylink.closeGraphics()


win.close()
core.quit()
