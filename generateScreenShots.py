#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ANM1_scanner
author: Ian Roberts

"""

# load modules
import pandas as pd
import numpy as np
import random, os, time, sys
from psychopy.preferences import prefs
prefs.general['shutdownKey'] = 'escape' # set experiment escape key
from psychopy import visual, core, event, data, gui, logging, info
import itertools

# load experiment functions
import generalFunctions as gf
import questionnaires as qs

# general experiment settings
expName = 'ANM1_scanner'  # experiment name
expVersion = 1.0  # experiment version
DEBUG = False  # set debug mode (if True: not fullscreen and subject number is 9999)
monitor = 'testMonitor'  # display name
screenToUse = 0
overallTrialNum = 0  # initialize overall trial number to be 0
textFont = 'Arial'
scannerTrigger = '5'


# set up counterbalances
partnerColors = [(1,1,-1), (-1,-1,1), (1,-1,-1)]  # red
partnerShapes = [3, 4, 32]  # number of edges
selfSide = ['left', 'right']

# create window for task and run refresh rate test
if DEBUG:
    fullscreen = False
elif not DEBUG:
    fullscreen = True

# present dialogue box for subject info
expInfo = gf.subject_info(entries=['subject'], debug=DEBUG,
                          debugValues=[9999], expName=expName, expVersion=expVersion,
                          counterbalance=1)


# get partner cue combo
partnerConds = [partnerColors, partnerShapes, selfSide]
partnerCombos = list(itertools.product(*partnerConds))

win = visual.Window(size=(1200, 700), fullscr=fullscreen, units='pix', monitor=monitor, colorSpace='rgb', color=(-1,-1,-1), screen=screenToUse)
runTimeTest = info.RunTimeInfo(win=win, refreshTest=True)
currRefreshRate = runTimeTest['windowRefreshTimeAvg_ms'] / 1000
print currRefreshRate


saveDir = os.path.join(os.getcwd(), 'data', 'subject_' + str(expInfo['subject']))
if not os.path.exists(saveDir):
    os.makedirs(saveDir)

payFile = os.path.join(os.getcwd(), 'data', 'payFile.csv')
dgQuizFile = os.path.join(os.getcwd(), 'stim', 'anm1_dgQuiz.csv')
pdQuizFile = os.path.join(os.getcwd(), 'stim', 'anm1_pdQuiz.csv')


# generate names for data and session log files
saveFilename = os.path.join(saveDir, "%04d_%s_%s.csv") %(int(expInfo['subject']), expInfo['startTime'], expInfo['expName'])
logFilename = os.path.join(saveDir, "%04d_%s_%s.log") %(int(expInfo['subject']), expInfo['startTime'], expInfo['expName'])
logfile = logging.LogFile(logFilename, filemode = 'w', level = logging.EXP) #set logging information (core.quit() is required at the end of experiment to store logging info!!!)

# create clocks for timing
globalClock = core.Clock()
blockClock = core.Clock()
rtClock = core.Clock()


### settings for experimental tasks
# file paths for images
respOptsImage = os.path.join("stim", "respOpts.png")

# subjectConds = condCombos[expInfo['counterbalance']]
# subjectPartners = partnerCombos[partnerCounterbalance]

### partner cue settings

# partner colors (colors stored in 0th element)
# posColor = subjectPartners[0][0]
# neuColor = subjectPartners[0][1]
# negColor = subjectPartners[0][2]

# partner shapes (shapes stored in 1st element)
partnerShape = visual.Polygon(win=win, edges=3, radius=0.5, units="norm")
# neuShape = visual.Polygon(win=win, edges=subjectPartners[1][1], radius=0.5, units="norm")
# negShape = visual.Polygon(win=win, edges=subjectPartners[1][2], radius=0.5, units="norm")

# posShape.lineColor = posColor
# posShape.fillColor = posColor
# neuShape.lineColor = neuColor
# neuShape.fillColor = neuColor
# negShape.lineColor = negColor
# negShape.fillColor = negColor

# resp options ordering (ordering stored in 2nd element)
respOrder = 'LtoR'

# partnerSymbols = pd.DataFrame({"partner": ["pos", "neu", "neg"],
#                                "color": [posColor, neuColor, negColor],
#                                "shape": [posShape.edges, neuShape.edges, negShape.edges],
#                                "subject": expInfo['subject'],
#                                "counterbalance": expInfo['counterbalance']})
# partnerSymbols.to_csv(os.path.join(saveDir, "%04d_%s_%s_%s.csv") %(int(expInfo['subject']), expInfo['startTime'], expInfo['expName'], 'partnerSymbols'), header = True, mode = 'w', index = False)

# counterbalance partner block sets
# blockSets = ('anm1_partner1_trials.csv', 'anm1_partner2_trials.csv', 'anm1_partner3_trials.csv')

# posBlocks = pd.read_csv(os.path.join(os.getcwd(), 'stim', blockSets[subjectConds[1][0]]))
# neuBlocks = pd.read_csv(os.path.join(os.getcwd(), 'stim', blockSets[subjectConds[1][1]]))
# negBlocks = pd.read_csv(os.path.join(os.getcwd(), 'stim', blockSets[subjectConds[1][2]]))
#
# posBlocks['partner'] = 'pos'
# neuBlocks['partner'] = 'neu'
# negBlocks['partner'] = 'neg'
#
# posBlocks['blockSet'] = blockSets[subjectConds[1][0]]
# neuBlocks['blockSet'] = blockSets[subjectConds[1][1]]
# negBlocks['blockSet'] = blockSets[subjectConds[1][2]]


# load practice block
pracBlock = pd.read_csv(os.path.join(os.getcwd(), 'stim', 'anm1_practice_trials.csv'))
pracBlock = pracBlock.loc[range(len(partnerCombos)),:]

pracBlock['partner'] = range(len(partnerCombos))
pracBlock['color'] = 's'
pracBlock['selfSide'] = ''
pracBlock['shape'] = np.nan
pracBlock['prob'] = 78
pracBlock['selfProp'] = 23
pracBlock['otherProp'] = 15
pracBlock['needDur'] = 1.0
pracBlock['propDur'] = 1.0
pracBlock['jitterDur'] = 1.0
pracBlock['itiDur'] = 1.0

for i in range(len(partnerCombos)):
    pracBlock.at[i, 'color'] = partnerCombos[i][0]
    pracBlock.loc[i, 'shape'] = partnerCombos[i][1]
    pracBlock.loc[i, 'selfSide'] = partnerCombos[i][2]
pracBlock['blockSet'] = 'anm1_practice_trials.csv'
pracBlock['instructsDur'] = 0
pracBlock['instructsJitterDur'] = 2.5
pracBlock = pracBlock.reindex_axis(sorted(pracBlock.columns), axis=1)  # sort columns alphabetically




## settings for dictator game
dflt = 20  # default outcome amount

pracRect = visual.Rect(win=win, width=1.9, height=1.9, lineWidth=200, lineColor=(1,1,1), units="norm")
respRect = visual.Rect(win=win, pos=(0,-0.05), width=1.7, height=1.3, lineWidth=200, lineColor=(-0.1, -0.1, -0.1), units="norm")

partnerBlockText = visual.TextStim(win=win, text='For the following trials,\nyour partner will be:', pos=(0,0.5), color=(1,1,1), font=textFont, height=0.2, units="norm", wrapWidth=1.9)
pauseText = visual.TextStim(win=win, text='Please take a moment to rest', pos=(0,0), color=(1,1,1), font=textFont, height=0.1, units="norm", wrapWidth=1.0)
preparingScannerText = visual.TextStim(win=win, text='Preparing scanner...', pos=(0,0), color=(1,1,1), font=textFont, height=0.1, units="norm")
waitingForScannerText = visual.TextStim(win=win, text='Waiting for scanner...', pos=(0,0), color=(1,1,1), font=textFont, height=0.1, units="norm")
initialScansText = visual.TextStim(win=win, text='Taking initial scans...', pos=(0,0), color=(1,1,1), font=textFont, height=0.1, units="norm")

fixation = visual.TextStim(win=win, text='+', pos=(0,0), color=(1,1,1), font=textFont, units="norm", height=0.5)
selfLabel = visual.TextStim(win=win, text='You', pos=(-0.5,0.25), color=(1,1,1), font=textFont, units="norm", height=0.3)
otherLabel = visual.TextStim(win=win, text='Partner', pos=(0.5,0.25), color=(1,1,1), font=textFont, units="norm")
selfAmount = visual.TextStim(win=win, text='00', pos=(-0.5, -0.25), color=(1,1,1), font=textFont, height=0.5, units="norm")
otherAmount = visual.TextStim(win=win, text='00', pos=(0.5, -0.25), color=(1,1,1), font=textFont, height=0.5, units="norm")
probText = visual.TextStim(win=win, text='', pos=(0,0), color=(1,1,1), font=textFont, height=0.5, units="norm")

# create response keys
respKeys = ['1', '2', '3', '4']  # list of response keys that subjects can use
if respOrder == 'LtoR':
    keyboardImage_dg = os.path.join("stim", "hand_LtoR.png")
    respLabels = ['strong\n  no', 'no', 'yes', 'strong\n  yes']  # initialize list of response labels to be displayed on screen
    acceptKeys = ['3', '4']
    rejectKeys = ['1', '2']
    respDecode = {'1': 1, '2': 2, '3': 3, '4': 4}
else:
    keyboardImage_dg = os.path.join("stim", "hand_RtoL.png")
    respLabels = ['strong\n  yes', 'yes', 'no', 'strong\n  no']  # initialize list of response labels to be displayed on screen
    acceptKeys = ['1', '2']
    rejectKeys = ['3', '4']
    respDecode = {'1': 4, '2': 3, '3': 2, '4': 1}
# generate TextStim for response options
respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=respLabels,
                                     scaleWidth=0.6, primaryPos=-0.8, primaryHeight=0.08, win=win, bold=True)

instructsImage = visual.ImageStim(win=win, pos=(0,-0.3), image=respOptsImage, size=(1.0, 0.75), units="norm")

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
    trialsDf['blockTime'] = np.nan
    trialsDf['globalTime'] = np.nan
    trialsDf['resp'] = None
    trialsDf['respNum'] = None
    trialsDf['rt'] = np.nan
    trialsDf['overallTrialNumber'] = 0
    # trialsDf['implementPain'] = np.nan


    # DISPLAY PAUSE SCREEN
    # pauseText.setAutoDraw(True)
    # event.clearEvents()
    # timer = core.CountdownTimer(5.0)
    # noPauseResp = True
    # while noPauseResp:
    #     if timer.getTime() < 0:
    #         keysPressed = event.getKeys(keyList=['1','2','3','4'])
    #         if len(keysPressed) > 0:
    #             noPauseResp = False
    #     else:
    #         event.clearEvents()
    #     win.flip()
    # event.clearEvents()
    # pauseText.setAutoDraw(False)

    # PAUSE FOR EXPERIMENTER
    # preparingScannerText.setAutoDraw(True)
    # event.clearEvents()
    # while not event.getKeys(keyList = ['space']):
    #     win.flip()
    # event.clearEvents()
    # preparingScannerText.setAutoDraw(False)

    # WAIT FOR SCANNER START
    waitingForScannerText.setAutoDraw(True)
    event.clearEvents()
    while not event.getKeys(keyList = ['5']):
        win.flip()
    event.clearEvents()
    waitingForScannerText.setAutoDraw(False)


    # Assign runNumber based on existing csv file. Read the csv file and find the largest block number and add 1 to it to reflect this block's number.
    try:
        runNumber = max(pd.read_csv(saveFile)['runNumber']) + 1
        trialsDf['runNumber'] = runNumber
    except:  # if fail to read csv, then it's block 1
        runNumber = 1
        trialsDf['runNumber'] = runNumber

    blockClock.reset()

    # initialize variable for storing partner on previous trial
    prevPartner = 999
    prevColor = 'magenta'

    # run block trials
    for i, thisTrial in trialsDf.iterrows():

        if trialsDf.loc[i, 'color'] == (1,1,-1):
            colorText = "yellow"
        elif trialsDf.loc[i, 'color'] == (-1,-1,1):
            colorText = "blue"
        elif trialsDf.loc[i, 'color'] == (1,-1,-1):
            colorText = "red"

        # if new partner on this trial, give task instructions
        if trialsDf.loc[i, 'partner'] != prevPartner:

            # change partner rect cue and shape
            partnerShape.setEdges(trialsDf.loc[i, 'shape'])
            partnerShape.setFillColor(trialsDf.loc[i, 'color'])
            partnerShape.setLineColor(trialsDf.loc[i, 'color'])
            partnerCue = pracRect
            partnerCue.setLineColor(trialsDf.loc[i, 'color'])
            partnerShape.pos = (0,-0.2)
            partnerShape.radius = 0.4
            partnerShape.setAutoDraw(True)
            partnerCue.setAutoDraw(True)

            # DISPLAY INSTRUCTIONS
            partnerBlockText.setAutoDraw(True)
            # timer = core.CountdownTimer(1.0)  # display for 10 secs
            # while timer.getTime() > 0:
            win.flip()
            win.getMovieFrame()
            partnerBlockText.setAutoDraw(False)

            partnerShape.setAutoDraw(False)
            if trialsDf.loc[i, 'selfSide'] == 'left':
                partnerShape.pos = (0.5,0.25)
                selfLabel.pos = (-0.5,0.25)
                selfAmount.pos = (-0.5,-0.25)
                otherAmount.pos = (0.5,-0.25)
            elif trialsDf.loc[i, 'selfSide'] == 'right':
                partnerShape.pos = (-0.5,0.25)
                selfLabel.pos = (0.5,0.25)
                selfAmount.pos = (0.5,-0.25)
                otherAmount.pos = (-0.5,-0.25)
            partnerShape.radius = 0.3

            # INSTRUCTIONS JITTER
            # fixation.setAutoDraw(True)
            # timer = core.CountdownTimer(trialsDf.loc[i, 'instructsJitterDur'])
            # while timer.getTime() > 0:
            #     win.flip()
            # fixation.setAutoDraw(False)


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
        trialsDf.loc[i, 'blockTime'] = blockClock.getTime()

        # NEED
        if colorText != prevColor:
            probText.setAutoDraw(True)
            # timer = core.CountdownTimer(trialsDf.loc[i, 'needDur'])
            # while timer.getTime() > 0:
            win.flip()
            win.getMovieFrame()
            probText.setAutoDraw(False)

        # JITTER
        if colorText != prevColor:
            fixation.setAutoDraw(True)
            # timer = core.CountdownTimer(trialsDf.loc[i, 'jitterDur'])
            # while timer.getTime() > 0:
            win.flip()
            win.getMovieFrame()
            fixation.setAutoDraw(False)
        prevColor = colorText

        # CHOICE
        selfLabel.setAutoDraw(True)
        selfAmount.setAutoDraw(True)
        otherAmount.setAutoDraw(True)

        if trialsDf.loc[i, 'partner'] != 'practice':
            partnerShape.setAutoDraw(True)
        elif trialsDf.loc[i, 'partner'] == 'practice':
            otherLabel.setAutoDraw(True)
            for j in respKeys:
                respOptions[j].setAutoDraw(True)

        win.callOnFlip(rtClock.reset)  # reset rtClock on next window flip
        event.clearEvents()  # clear events

        # display proposal and collect response
        timer = core.CountdownTimer(trialsDf.loc[i, 'propDur'])
        win.flip()
        win.getMovieFrame()
        respRect.setAutoDraw(True)
        win.flip()
        win.getMovieFrame()
        keyResp = '1'
        # while timer.getTime() > 0:
        #     keysPressed = event.getKeys(keyList=respKeys, timeStamped=rtClock)  # load keys that have been pressed
        #
        #     if timer.getTime() < 0.5:  # check if a key has been pressed yet
        #         if keyResp is None:  # check if another key response has already been recorded
        #             # keyResp, RT = keysPressed[0]  # access first key response and corresponding RT
        #             # RTfromClock = rtClock.getTime()  # record RT from rtClock
        #
        #             respRect.setAutoDraw(True)
        #             win.flip()
        #             keyResp = '1'
        #             win.getMovieFrame()
        #             if trialsDf.loc[i, 'partner'] == 'practice':
        #                 # change color of option selected
        #                 selectedOption = respOptions[keyResp]
        #                 selectedOption.color = (-1, 1, -1)
        #
        #     win.flip()

        # TRIAL CLEAN UP
        selfLabel.setAutoDraw(False)
        selfAmount.setAutoDraw(False)
        otherAmount.setAutoDraw(False)
        respRect.setAutoDraw(False)

        partnerShape.setAutoDraw(False)

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

        # append data to data frame
        trialsDf.loc[i, 'resp'] = keyResp
        if keyResp is not None:
            trialsDf.loc[i, 'respNum'] = respDecode[keyResp]
        trialsDf.loc[i, 'rt'] = RT

        # ITI
        # fixation.setAutoDraw(True)
        # timer = core.CountdownTimer(trialsDf.loc[i, 'itiDur'])
        # while timer.getTime() > 0:
        #     win.flip()
        # fixation.setAutoDraw(False)

        win.saveMovieFrames(os.path.join(os.getcwd(), 'screenShots', 'screenshots_%s_%d_%s_.png' %(colorText, trialsDf.loc[i, 'shape'], trialsDf.loc[i, 'selfSide'])))

    partnerCue.setAutoDraw(False)

    trialsDf['endTime'] = str(time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime()))

    # append block data to save file
    # trialsDf.to_csv(saveFilename, header = writeHeader, mode = 'a', index = False)

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

    painProb = float(selectedTrial['prob']) / 100
    subjectRole = 'dictator'

    decisionResult = pd.DataFrame({'subject': expInfo['subject'],
    'dictator': [selfOut],
    'receiver': [otherOut],
    'dictator_proposed': np.asscalar(selectedTrial['selfProp']),
    'receiver_proposed': np.asscalar(selectedTrial['otherProp']),
    'accept': selectedTrial['accept'].values,
    'painProb': [painProb],
    'painImplement': [""],
    'subjectRole': [subjectRole],
    'finalProb': [np.nan],
    'finalPay': [np.nan],
    'amountSpent': [np.nan]})

    return decisionResult



def spend_money(win=win, startProb=None, startPay=None):

    # "Continue" text displayed at the bottom of each screen
    continueInstruct = 'Press RETURN to submit your decision'
    continueText = visual.TextStim(win=win, units='norm', colorSpace='rgb', color=(1,1,1), font='Arial', text=continueInstruct, height=0.08, wrapWidth=1.4, pos=(0.0, -0.85))

    optPositions = gf.spacer(items=11, space=0.9, anchor=-0.4)
    marker = visual.Rect(win=win, width=0.15, height=0.25, lineColor=(1,-1,-1), lineWidth=25, pos=optPositions[0])

    spendText = visual.TextStim(win=win, units='norm', colorSpace='rgb', color=(1,1,1), font='Arial', text="How much would you like to spend?", height=0.1, wrapWidth=1.4, pos=(0.0, -0.17))

    probLabel = visual.TextStim(win=win, units='norm', colorSpace='rgb', color=(1,1,1), font='Arial', text="Chance of ice:", height=0.1, pos=(0.4,0.6))
    probDisp = visual.TextStim(win=win, units='norm', colorSpace='rgb', color=(1,1,1), font='Arial', text=str(startProb) + "%", height=0.2, pos=(0.4,0.4), bold=True)
    payLabel  = visual.TextStim(win=win, units='norm', colorSpace='rgb', color=(1,1,1), font='Arial', text="Final payment:", height=0.1, pos=(-0.4,0.6))
    payDisp = visual.TextStim(win=win, units='norm', colorSpace='rgb', color=(1,1,1), font='Arial', text="$" + str(startPay), height=0.2, pos=(-0.4,0.4), bold=True)

    respKeys = ['return', 'left', 'right']

    spendOpts = {}
    for i in range(11):
        spendOpts[i] = visual.TextStim(win=win, text='$' + str(i), font="Arial", pos=optPositions[i], colorSpace='rgb', color=(1,1,1), bold=True, height=0.1)

    for j in spendOpts:
        spendOpts[j].setAutoDraw(True)
    marker.setAutoDraw(True)
    probLabel.setAutoDraw(True)
    probDisp.setAutoDraw(True)
    payLabel.setAutoDraw(True)
    payDisp.setAutoDraw(True)
    continueText.setAutoDraw(True)
    spendText.setAutoDraw(True)

    noChoice = True
    currSpend = 0
    currPay = startPay
    currProb = startProb
    keysPressed = []
    event.clearEvents()

    while noChoice:

        keysPressed = event.getKeys(keyList=respKeys)

        if len(keysPressed) > 0:
            keyResp = keysPressed[0]

            if keyResp == 'return':
                noChoice = False
                marker.lineColor = (-1,1,-1)
                win.flip()
                core.wait(2)
            else:
                if keyResp == 'left' and currSpend > 0:
                    currSpend -= 1
                    marker.setPos(optPositions[currSpend])
                elif keyResp == 'right' and currSpend < 10 and startPay > currSpend and currProb > 0:
                    currSpend += 1
                    marker.setPos(optPositions[currSpend])

                currPay = startPay - currSpend
                currProb = startProb - (10*currSpend)

                if currProb < 0:
                    currProb = 0

                probDisp.setText(str(currProb) + "%")
                payDisp.setText("$" + str(currPay))

        win.flip()

    for j in spendOpts:
        spendOpts[j].setAutoDraw(False)
    marker.setAutoDraw(False)
    probLabel.setAutoDraw(False)
    probDisp.setAutoDraw(False)
    payLabel.setAutoDraw(False)
    payDisp.setAutoDraw(False)
    continueText.setAutoDraw(False)
    spendText.setAutoDraw(False)

    results = pd.DataFrame({"finalProb": [float(currProb)/100],
    "finalPay": [currPay],
    "amountSpent": [currSpend]})

    return results



def decision_results():
    # randomly select one trial for outcome
    subjectPay = 0
    payFileExists = True
    try:
        payments = pd.read_csv(payFile)
    except:
        # if this is the first participant and there is no file yet
        payFileExists = False
        pay = select_dictator_decision()

    # if there is a file already
    if payFileExists:
        # if previous participant is the dictator
        if payments.tail(1)['subjectRole'].values == "dictator":
            # copy information from previous participant
            pay = pd.DataFrame({'subject': expInfo['subject'],
                                'dictator': payments.tail(1)['dictator'].values[0],
                                'receiver': payments.tail(1)['receiver'].values[0],
                                'dictator_proposed': payments.tail(1)['dictator_proposed'].values[0],
                                'receiver_proposed': payments.tail(1)['receiver_proposed'].values[0],
                                'accept': payments.tail(1)['accept'].values[0],
                                'painProb': payments.tail(1)['painProb'].values[0],
                                'painImplement': [''],
                                'subjectRole': ['receiver'],
                                'finalProb': [np.nan],
                                'finalPay': [np.nan],
                                'amountSpent': [np.nan]})
        else:
            pay = select_dictator_decision()

    # calculate pain probabilities and result
    if pay['subjectRole'].values == 'receiver':
        subjPainProb = np.asscalar(pay['painProb'])
        subjectPay = np.asscalar(pay['receiver'])
        role = 'Receiver'
    else:
        subjPainProb = float(0)
        subjectPay = np.asscalar(pay['dictator'])
        pay['finalProb'] = float(0)
        pay['finalPay'] = pay['dictator']
        role = 'Decider'

    painProb = str(int(np.asscalar(pay['painProb']) * 100)) + "%"

    if pay['accept'].values == 1:
        accept = 'Accepted proposed allocation'
    else:
        accept = 'Rejected proposed allocation'

    gf.show_instructs(win=win,
        text=["You have completed the decision-making task.",
        "The computer will now randomly determine your outcomes for the decision-making task.",
        "Your role: %s\n\nProposed allocation to decider: %s\nProposed allocation to receiver: %s\nReceiver's chance of ice: %s\n\nDecision: %s\n\nYour pay: %s" %(str(role),
        str(pay['dictator_proposed'].values[0]), str(pay['receiver_proposed'].values[0]), str(painProb), str(accept), str(subjectPay))],
        textPos=(0,0), timeAutoAdvance=0, timeRequired=0, advanceKey='space')

    if role == 'Receiver':
        gf.show_instructs(win=win,
            text=["Because you were randomly selected to be the receiver, you will now have the opportunity to spend some of the money given to you by your partner to reduce your chances of completing the ice task again.",
            "The chances of you being required to the complete the ice task again will be reduced by 10% for each dollar you choose to spend. Any money that you spend will NOT be given to your partner. Rather, anything you spend will be kept by the experimenter.",
            "On the following screen you will use the left and right arrow keys to adjust how much you would like to spend. Press RETURN when you have selected your final decision.\n\nThe computer will then conduct a random lottery to determine if you will complete the ice task again."],
            textPos=(0,0), timeAutoAdvance=0, timeRequired=0, advanceKey='space')

        spendResults = spend_money(win=win, startProb=int(np.asscalar(pay['painProb'])*100), startPay=np.asscalar(pay['receiver']))

        pay['finalPay'] = np.asscalar(spendResults['finalPay'])
        pay['finalProb'] = np.asscalar(spendResults['finalProb'])
        pay['amountSpent'] = np.asscalar(spendResults['amountSpent'])

    painImplement = np.random.binomial(1, pay['finalProb'].values[0])

    if painImplement == 1:
        painImp = 'yes'
        pay['painImplement'] = 'yes'
    else:
        painImp = 'no'
        pay['painImplement'] = 'no'

    # sort columns alphabetically
    pay = pay.reindex_axis(sorted(pay.columns), axis=1)

    pay.to_csv(payFile, header = not payFileExists, mode = 'a', index = False)

    print "Pay: " + str(pay['finalPay'].values[0]) + "\nIce: " + str(painImp)

    gf.show_instructs(win=win,
        text=["Your final pay: %s\nComplete the ice task again? %s" %(str(pay['finalPay'].values[0]), str(painImp))],
        textPos=(0,0), timeAutoAdvance=0, timeRequired=0, advanceKey='space')

    gf.show_instructs(win=win,
        text=["You have completed the tasks.\n\nPlease open your door ajar to the let experimenter know and then wait patiently.\n\nDo not continue until the experimenter tells you."],
        timeAutoAdvance=0, timeRequired=20, advanceKey='space')
    gf.show_instructs(win=win,
        text=["Pay: " + str(pay['finalPay'].values[0]) + "\nIce: " + str(painImp)],
        timeAutoAdvance=0, timeRequired=0, advanceKey='space')

    return painImp



# ============================================================================ #
# RUN EXPERIMENT

# gf.show_instructs(win=win, text=["Welcome to the experiment!"],
#     timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], saveFile=os.path.join(saveDir, "instructs0.png"))

### Dictator Game --------------------------------------------------------------

# generate runs
# runs = generate_runs(posBlocks=posBlocks, neuBlocks=neuBlocks, negBlocks=negBlocks)

# pause for initial scans
# initial_scans()

# gf.show_instructs(win=win,
#     text=["Before beginning the actual task, you're going to complete one block of practice trials so that you can get familiar with how the task will go in the scanner.\n\nWe'll quickly review the task before starting."],
#     timeAutoAdvance=0, timeRequired=0, advanceKey=['1','2','3','4'], saveFile=os.path.join(saveDir, "instructs0.png"))



run_decision_run(trialsDf=pracBlock, saveFile=saveFilename)


# run task
# run_decision_run(trialsDf=runs[0], saveFile=saveFilename)
# run_decision_run(trialsDf=runs[1], saveFile=saveFilename)
# run_decision_run(trialsDf=runs[2], saveFile=saveFilename)
# run_decision_run(trialsDf=runs[3], saveFile=saveFilename)
# run_decision_run(trialsDf=runs[4], saveFile=saveFilename)


win.close()
core.quit()
