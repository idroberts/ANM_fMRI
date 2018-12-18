#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ANM1_preScanner
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
import smtplib

# load experiment functions
import generalFunctions as gf
import questionnaires as qs

# general experiment settings
expName = 'ANM1_preScanner'  # experiment name
expVersion = 2.5  # experiment version
DEBUG = False  # set debug mode (if True: not fullscreen and subject number is 9999)
monitor = 'testMonitor'  # display name
overallTrialNum = 0  # initialize overall trial number to be 0
textFont = 'Arial'


# set up counterbalances
partnerColors = list(itertools.permutations([(1,1,-1),  # yellow
                                             (-1,-1,1),  # blue
                                             (1,-1,-1)]))  # red
partnerShapes = list(itertools.permutations([3, 4, 32]))  # number of edges
respOrders = ['LtoR', 'RtoL']
blockSets = list(itertools.permutations([1, 2, 3]))
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
expInfo = gf.subject_info(entries=['subject'], debug=DEBUG,
                          debugValues=[9999], expName=expName, expVersion=expVersion,
                          counterbalance=nCondCombos)

# get partner cue combo
partnerConds = [partnerColors, partnerShapes]
partnerCombos = list(itertools.product(*partnerConds))
random.seed(1928)
random.shuffle(partnerCombos)
partnerCounterbalance = expInfo['subject'] % len(partnerCombos)


win = visual.Window(size=(1200, 700), fullscr=fullscreen, units='pix', monitor=monitor, colorSpace='rgb', color=(-1,-1,-1))
runTimeTest = info.RunTimeInfo(win=win, refreshTest=True)
currRefreshRate = runTimeTest['windowRefreshTimeAvg_ms'] / 1000
print currRefreshRate


saveDir = os.path.join(os.getcwd(), 'data', 'subject_' + str(expInfo['subject']))
if not os.path.exists(saveDir):
    os.makedirs(saveDir)

payFile = os.path.join(os.getcwd(), 'data', 'payFile.csv')
dgQuizFile = os.path.join(os.getcwd(), 'stim', 'anm1_dgQuiz.csv')
pdQuizFile = os.path.join(os.getcwd(), 'stim', 'anm1_pdQuiz.csv')
pracBlock = pd.read_csv(os.path.join(os.getcwd(), 'stim', 'anm1_practice1_trials.csv'))

# practice trials with 8 sec resp deadline
pracBlock_8sec = pracBlock.loc[range(0,6),:].copy()  # trim to just 6 trials (2 each partner)
pracBlock_8sec.reset_index(drop=True, inplace=True)
pracPartnerOrder = ['pos', 'neu', 'neg']
random.shuffle(pracPartnerOrder)  # randomly order partners
pracBlock_8sec.loc[range(0,2), 'partner'] = pracPartnerOrder[0]  # label partners
pracBlock_8sec.loc[range(2,4), 'partner'] = pracPartnerOrder[1]
pracBlock_8sec.loc[range(4,6), 'partner'] = pracPartnerOrder[2]
pracBlock_8sec['blockSet'] = 'anm1_practice1_trials.csv'
pracBlock_8sec['propDur'] = 8
pracBlock_8sec['instructsDur'] = 0
pracBlock_8sec['instructsJitterDur'] = 0
pracBlock_8sec.loc[[0,2,4], 'instructsDur'] = 10.0
pracBlock_8sec.loc[[0,2,4], 'instructsJitterDur'] = random.sample([1.5, 2.5, 3.5], 3)
pracBlock_8sec['partnerBlockTrialNum'] = [1,2] * 3
pracBlock_8sec['partnerBlockNum'] = 0
pracBlock_8sec['overallPartnerTrialNum'] = 0
pracBlock_8sec = pracBlock_8sec.reindex_axis(sorted(pracBlock_8sec.columns), axis=1)  # sort columns alphabetically

# practice trials with 4 sec resp deadline
pracBlock_4sec = pracBlock.loc[range(6,12),:].copy()  # trim to just 6 trials (2 each partner)
pracBlock_4sec.reset_index(drop=True, inplace=True)
random.shuffle(pracPartnerOrder)  # randomly order partners
pracBlock_4sec.loc[range(0,2), 'partner'] = pracPartnerOrder[0]  # label partners
pracBlock_4sec.loc[range(2,4), 'partner'] = pracPartnerOrder[1]
pracBlock_4sec.loc[range(4,6), 'partner'] = pracPartnerOrder[2]
pracBlock_4sec['blockSet'] = 'anm1_practice1_trials.csv'
pracBlock_4sec['propDur'] = 4
pracBlock_4sec['instructsDur'] = 0
pracBlock_4sec['instructsJitterDur'] = 0
pracBlock_4sec.loc[[0,2,4], 'instructsDur'] = 10.0
pracBlock_4sec.loc[[0,2,4], 'instructsJitterDur'] = random.sample([1.5, 2.5, 3.5], 3)
pracBlock_4sec['partnerBlockTrialNum'] = [1,2] * 3
pracBlock_4sec['partnerBlockNum'] = 0
pracBlock_4sec['overallPartnerTrialNum'] = 0
pracBlock_4sec = pracBlock_4sec.reindex_axis(sorted(pracBlock_4sec.columns), axis=1)  # sort columns alphabetically



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

# resp options ordering (ordering stored in 2nd element)
respOrder = subjectConds[0]

partnerSymbols = pd.DataFrame({"partner": ["pos", "neu", "neg"],
                               "color": [posColor, neuColor, negColor],
                               "shape": [posShape.edges, neuShape.edges, negShape.edges],
                               "subject": expInfo['subject'],
                               "counterbalance": expInfo['counterbalance']})
partnerSymbols.to_csv(os.path.join(saveDir, "%04d_%s_%s_%s.csv") %(int(expInfo['subject']), expInfo['startTime'], expInfo['expName'], 'partnerSymbols'), header = True, mode = 'w', index = False)

posShape.lineColor = posColor
posShape.fillColor = posColor
neuShape.lineColor = neuColor
neuShape.fillColor = neuColor
negShape.lineColor = negColor
negShape.fillColor = negColor

# for impressions
impPartnerOrder = ["pos", "neg"]
random.shuffle(impPartnerOrder)

## settings for dictator game
dflt = 20  # default outcome amount

posRect = visual.Rect(win=win, width=1300, height=850, lineWidth=10, lineColor=posColor, units="pix")
neuRect = visual.Rect(win=win, width=1300, height=850, lineWidth=10, lineColor=neuColor, units="pix")
negRect = visual.Rect(win=win, width=1300, height=850, lineWidth=10, lineColor=negColor, units="pix")
pracRect = visual.Rect(win=win, width=1300, height=850, lineWidth=10, lineColor=(1,1,1), units="pix")
respRect = visual.Rect(win=win, pos=(0,20), width=850, height=350, lineWidth=10, lineColor=(-0.1, -0.1, -0.1), units="pix")

partnerBlockText = visual.TextStim(win=win, text='For the following trials, your partner will be:', pos=(0,250), color=(1,1,1), font=textFont, height=50, units="pix", wrapWidth=1000)
pauseText = visual.TextStim(win=win, text='Please take a moment to rest', pos=(0,0), color=(1,1,1), font=textFont, height=0.1, units="norm", wrapWidth=1.0)
preparingScannerText = visual.TextStim(win=win, text='Preparing scanner...', pos=(0,0), color=(1,1,1), font=textFont, height=0.1, units="norm")
waitingForScannerText = visual.TextStim(win=win, text='Waiting for scanner...', pos=(0,0), color=(1,1,1), font=textFont, height=0.1, units="norm")
initialScansText = visual.TextStim(win=win, text='Taking initial scans...', pos=(0,0), color=(1,1,1), font=textFont, height=0.1, units="norm")

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
respKeys = ['m', 'comma', 'period', 'slash']  # list of response keys that subjects can use
if respOrder == 'LtoR':
    keyboardImageFile = os.path.join("stim", "keyboard_LtoR.png")
    respLabels = ['strong\n  no', 'no', 'yes', 'strong\n  yes']  # initialize list of response labels to be displayed on screen
    acceptKeys = ['period', 'slash']
    rejectKeys = ['m', 'comma']
    respDecode = {'m': 1, 'comma': 2, 'period': 3, 'slash': 4}
else:
    keyboardImageFile = os.path.join("stim", "keyboard_RtoL.png")
    respLabels = ['strong\n  yes', 'yes', 'no', 'strong\n  no']  # initialize list of response labels to be displayed on screen
    acceptKeys = ['m', 'comma']
    rejectKeys = ['period', 'slash']
    respDecode = {'m': 4, 'comma': 3, 'period': 2, 'slash': 1}
# generate TextStim for response options
respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=respLabels,
                                     scaleWidth=400, primaryPos=-300, primaryHeight=40, win=win, bold=True, units='pix')

# instructsImage = visual.ImageStim(win=win, pos=(0,-0.3), image=respOptsImage, size=(1.0, 0.75), units="norm")


# get neutral partner color (for loading task instruction images)
neuColorText = 'yellow'
if neuColor == (1,1,-1):
    neuColorText = 'yellow'
elif neuColor == (-1,-1,1):
    neuColorText = 'blue'
elif neuColor == (1,-1,-1):
    neuColorText = 'red'

mouse = event.Mouse(visible=False, win=win)  # create mouse

# ============================================================================ #
# CUSTOM FUNCTIONS FOR TASKS

def painDial(win, duration=120):

    def moveMouse(x,y):
        mouse.setPos([x,y])
        win.winHandle._mouse_x = x  # hack to change pyglet window
        win.winHandle._mouse_y = y

    # create objects for pain dial
    marker = visual.Line(win=win, start=(0, 40), end=(0, -40), lineWidth=30, lineColor=(-1, 0, 1))  # create marker
    scaleLine = visual.Line(win=win, start=(-500,0), end=(500,0), lineWidth=5)  # create line for scale
    mouse = event.Mouse(visible=False, win=win)  # create mouse
    practiceInstructs = visual.TextStim(win=win, text="Practice using the scale:", pos=(0,300), height=40, units='pix')
    lowLabel = visual.TextStim(win=win, text="No pain at all", pos=(-500,70), wrapWidth=120, height=20)
    highLabel = visual.TextStim(win=win, text="Worst pain imaginable", pos=(500,70), wrapWidth=100, height=20)

    # set mouse starting position
    moveMouse(-500,0)
    marker.pos = (-500,0)
    win.flip()

    # initialize variables for tracking mouse position and time
    mousePosRecord = []
    timePointRecord = []

    recordClock = core.Clock()
    prevTimePoint = 0

    keysPressed = []
    marker.lineColor = (1, -1, -1)  # make marker red during practice

    # pain dial practice
    while len(keysPressed) < 1:
        scaleLine.draw()
        marker.draw()
        practiceInstructs.draw()
        lowLabel.draw()
        highLabel.draw()

        currentMousePos = mouse.getPos()[0]
        if currentMousePos >= 500:
            currentMousePos = 500
        elif currentMousePos <= -500:
            currentMousePos = -500

        marker.pos = (currentMousePos, 0)
        win.flip()

        keysPressed = event.getKeys(keyList='space')  # load keys that have been pressed


    # set mouse starting position
    moveMouse(-500,0)
    marker.pos = (-500,0)
    win.flip()

    mousePosRecord = []
    timePointRecord = []

    recordClock = core.Clock()
    prevTimePoint = 0

    keysPressed = []
    marker.lineColor = (-1, 0, 1)  # make marker blue during actual recording

    # pain dial recording
    while recordClock.getTime() < duration:  # record up to 2 minutes
        scaleLine.draw()
        marker.draw()
        lowLabel.draw()
        highLabel.draw()

        currentMousePos = mouse.getPos()[0]
        if currentMousePos >= 500:
            currentMousePos = 500
        elif currentMousePos <= -500:
            currentMousePos = -500

        marker.pos = (currentMousePos, 0)
        win.flip()

        if int(recordClock.getTime()) > prevTimePoint:  # record mouse position and time every ~1 sec
            currentTime = recordClock.getTime()
            mousePosRecord.append(currentMousePos)
            timePointRecord.append(currentTime)
            prevTimePoint = int(currentTime)

        keysPressed = event.getKeys(keyList='space')  # load keys that have been pressed
        if len(keysPressed) > 0:  # if space is pressed, end pain dial recording
            break

    # save results to dataframe
    results = pd.DataFrame({'mousePos': mousePosRecord, 'timeSec': timePointRecord})
    results['subject'] = expInfo['subject']
    results['expName'] = expInfo['expName']
    results['expVersion'] = expInfo['expVersion']

    return results


def numericalMapping(win, saveFile):

    def moveMouse(x,y):
        mouse.setPos([x,y])
        win.winHandle._mouse_x = x  # hack to change pyglet window
        win.winHandle._mouse_y = y

    gf.show_instructs(win=win,
    text=["In this task you will be presented with an individual number and a number line.\n\nYour task is to indicate on the line, where you believe the number belongs. Use the mouse to move the marker on the line and left click to submit your response.\n\nDo not attempt to calculate the correct position on the line.\n\nWe are interested in your intuition. Please respond as quickly as possible."],
    units='pix', wrapWidth=1200, textPos=(0,50))

    nums = [2, 5, 18, 34, 56, 78, 100, 122, 147, 150, 163, 179, 246, 366, 486, 606, 722, 725, 738, 754, 818, 938]
    random.shuffle(nums)

    results = pd.DataFrame({'item': nums + [np.nan]})
    results['resp'] = np.nan
    results['rt'] = np.nan
    results['subject'] = expInfo['subject']
    results['expName'] = expInfo['expName']
    results['expVersion'] = expInfo['expVersion']

    nRows = results.shape[0]

    # create objects for pain dial
    marker = visual.Line(win=win, start=(0, 30), end=(0, -30), units="pix", lineWidth=5, lineColor=(-1, 0, 1))  # create marker
    scaleLine = visual.Line(win=win, start=(-500,-100), end=(500,-100), units="pix", lineWidth=5)  # create line for scale
    mouse = event.Mouse(visible=False, win=win)  # create mouse
    trialInstructs = visual.TextStim(win=win, text="Imagine that the line below runs from 0 to 1000. The left most point represents 0 and the right most point represents 1000.\n\nWhere does the following number belong on the line?\n\n\n\n\n\n\n\nPlease respond as quickly as possible.", pos=(0,200), height=25, wrapWidth=1200)
    numDisplay = visual.TextStim(win=win, text="", pos=(0,150), height=80, bold=True)
    lowLabel = visual.TextStim(win=win, text="0", pos=(-500,-40), units="pix", wrapWidth=0.2, height=40)
    highLabel = visual.TextStim(win=win, text="1000", pos=(500,-40), units="pix", wrapWidth=0.25, height=40)

    scaleLine.setAutoDraw(True)
    marker.setAutoDraw(True)
    trialInstructs.setAutoDraw(True)
    numDisplay.setAutoDraw(True)
    lowLabel.setAutoDraw(True)
    highLabel.setAutoDraw(True)

    for i, thisTrial in results.iterrows():

        if i == (nRows - 1):
            break

        numDisplay.setText(str(int(results.loc[i, "item"])))

        keysPressed = []
        marker.lineColor = (-1, 0, 1)  # make marker blue during actual recording

        moveMouse(-500,-100)
        marker.pos = (-500,-100)
        win.flip()

        win.callOnFlip(mouse.clickReset)

        # Continue until response
        while True:

            currentMousePos = mouse.getPos()[0]
            if currentMousePos >= 500:
                currentMousePos = 500
            elif currentMousePos <= -500:
                currentMousePos = -500

            marker.pos = (currentMousePos, -100)
            win.flip()

            keysPressed = event.getKeys(keyList='space')  # load keys that have been pressed
            clicks, clickTimes = mouse.getPressed(getTime=True)
            if clickTimes[0] != 0:
                results.loc[i, "resp"] = currentMousePos + 500
                results.loc[i, "rt"] = clickTimes[0]
                marker.lineColor = (1, -1, -1)  # make marker red during practice
                win.flip()
                core.wait(2)
                break

    scaleLine.setAutoDraw(False)
    marker.setAutoDraw(False)
    trialInstructs.setAutoDraw(False)
    numDisplay.setAutoDraw(False)
    lowLabel.setAutoDraw(False)
    highLabel.setAutoDraw(False)

    compBefore = qs.openResp(win=win, text="Have you completed this line task before in other studies? If so, approximately how many times?\n\nType your response.", subjNum=expInfo['subject'])
    results.loc[nRows-1, "item"] = compBefore.loc[0, "question"]
    results.loc[nRows-1, "resp"] = compBefore.loc[0, "resp"]

    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)


def prisonersDilemma(saveFile=None):

    partnerChoices = [10, 9, 10, 3, 1, 5, 7, 5, 9, 7]
    random.shuffle(partnerChoices)

    results = pd.DataFrame({'partnerChoice': partnerChoices})
    results['resp'] = np.nan
    results['rt'] = np.nan
    results['subject'] = expInfo['subject']
    results['expName'] = expInfo['expName']
    results['expVersion'] = expInfo['expVersion']

    boxCoords = gf.spacer(items=11, space=500, anchor=-200, units='pix')

    boxes = {}
    respLabels = {}
    for i in range(len(boxCoords)):
        respLabels[i] = visual.TextStim(win=win, text=str(i), pos = boxCoords[i], units="pix", height=40)
        boxes[i] = visual.Rect(win=win, units="pix", lineWidth=10, fillColor=[-1,-1,-1], width=80, height=80, pos=boxCoords[i])

    firstMoveText = visual.TextStim(win=win, text="", pos=(0,200), height=40, wrapWidth=800, units='pix')

    mouse = event.Mouse(visible=True, win=win)  # create mouse

    for i, thisTrial in results.iterrows():
        firstMoveText.setAutoDraw(True)
        for j in range(len(boxes)):
            boxes[j].setAutoDraw(True)
            respLabels[j].setAutoDraw(True)
        firstMoveText.setText("The other player sent %d of their 10 points.\n\nThese points get tripled and you will receive %d points.\n\nHow many of your 10 points would you like to send?" %(results.loc[i, "partnerChoice"], results.loc[i, "partnerChoice"]*3))
        resp = None
        win.callOnFlip(mouse.clickReset)

        while True:
            win.flip()
            if mouse.isPressedIn(boxes[0], buttons=[0]):
                resp = 0
            elif mouse.isPressedIn(boxes[1], buttons=[0]):
                resp = 1
            elif mouse.isPressedIn(boxes[2], buttons=[0]):
                resp = 2
            elif mouse.isPressedIn(boxes[3], buttons=[0]):
                resp = 3
            elif mouse.isPressedIn(boxes[4], buttons=[0]):
                resp = 4
            elif mouse.isPressedIn(boxes[5], buttons=[0]):
                resp = 5
            elif mouse.isPressedIn(boxes[6], buttons=[0]):
                resp = 6
            elif mouse.isPressedIn(boxes[7], buttons=[0]):
                resp = 7
            elif mouse.isPressedIn(boxes[8], buttons=[0]):
                resp = 8
            elif mouse.isPressedIn(boxes[9], buttons=[0]):
                resp = 9
            elif mouse.isPressedIn(boxes[10], buttons=[0]):
                resp = 10

            if resp is not None:
                boxes[resp].fillColor = [1,1,1]
                respLabels[resp].color = [-1,-1,-1]
                win.flip()
                core.wait(1)

                clicks, clickTimes = mouse.getPressed(getTime=True)
                results.loc[i, "resp"] = resp
                results.loc[i, "rt"] = clickTimes[0]

                firstMoveText.setAutoDraw(False)
                for j in range(len(boxes)):
                    boxes[j].setAutoDraw(False)
                    respLabels[j].setAutoDraw(False)
                win.flip()
                core.wait(1)

                boxes[resp].fillColor = [-1,-1,-1]
                respLabels[resp].color = [1,1,1]
                break

    mouse.setVisible(0)

    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)


def prisonersDilemma_guesses(saveFile=None):

    neuShape.radius = 80
    neuShape.pos = (0, -100)
    neuShape.setAutoDraw(True)

    gf.show_instructs(win=win,
    text=["We are also interested in what people expect other's will choose to do in this task.\n\nPlease try to imagine what you think the third participant might choose to do as the second partner. Simply make your best guesses."],
    units='pix', wrapWidth=1200, textPos=(0,200))

    neuShape.setAutoDraw(False)
    neuShape.pos = (0, 0)

    partnerChoices = [10, 9, 10, 3, 1, 5, 7, 5, 9, 7]
    random.shuffle(partnerChoices)

    results = pd.DataFrame({'partnerChoice': partnerChoices})
    results['resp'] = np.nan
    results['rt'] = np.nan
    results['subject'] = expInfo['subject']
    results['expName'] = expInfo['expName']
    results['expVersion'] = expInfo['expVersion']

    boxCoords = gf.spacer(items=11, space=500, anchor=-300, units='pix')

    boxes = {}
    respLabels = {}
    for i in range(len(boxCoords)):
        respLabels[i] = visual.TextStim(win=win, text=str(i), pos = boxCoords[i], units="pix", height=40)
        boxes[i] = visual.Rect(win=win, units="pix", lineWidth=10, fillColor=[-1,-1,-1], width=80, height=80, pos=boxCoords[i])

    firstMoveText = visual.TextStim(win=win, text="", pos=(0,50), height=40, wrapWidth=800, units='pix')

    mouse = event.Mouse(visible=True, win=win)  # create mouse

    for i, thisTrial in results.iterrows():
        firstMoveText.setAutoDraw(True)
        for j in range(len(boxes)):
            boxes[j].setAutoDraw(True)
            respLabels[j].setAutoDraw(True)
        neuShape.setAutoDraw(True)
        firstMoveText.setText("The first player sends %d of their 10 points. These points get tripled to be %d points.\n\n\n\n\n\n\n\n\nHow many out of 10 points do you think this participant would send?" %(results.loc[i, "partnerChoice"], results.loc[i, "partnerChoice"]*3))
        resp = None
        win.callOnFlip(mouse.clickReset)

        while True:
            win.flip()
            if mouse.isPressedIn(boxes[0], buttons=[0]):
                resp = 0
            elif mouse.isPressedIn(boxes[1], buttons=[0]):
                resp = 1
            elif mouse.isPressedIn(boxes[2], buttons=[0]):
                resp = 2
            elif mouse.isPressedIn(boxes[3], buttons=[0]):
                resp = 3
            elif mouse.isPressedIn(boxes[4], buttons=[0]):
                resp = 4
            elif mouse.isPressedIn(boxes[5], buttons=[0]):
                resp = 5
            elif mouse.isPressedIn(boxes[6], buttons=[0]):
                resp = 6
            elif mouse.isPressedIn(boxes[7], buttons=[0]):
                resp = 7
            elif mouse.isPressedIn(boxes[8], buttons=[0]):
                resp = 8
            elif mouse.isPressedIn(boxes[9], buttons=[0]):
                resp = 9
            elif mouse.isPressedIn(boxes[10], buttons=[0]):
                resp = 10

            if resp is not None:
                boxes[resp].fillColor = [1,1,1]
                respLabels[resp].color = [-1,-1,-1]
                win.flip()
                core.wait(1)

                clicks, clickTimes = mouse.getPressed(getTime=True)
                results.loc[i, "resp"] = resp
                results.loc[i, "rt"] = clickTimes[0]

                firstMoveText.setAutoDraw(False)
                for j in range(len(boxes)):
                    boxes[j].setAutoDraw(False)
                    respLabels[j].setAutoDraw(False)
                neuShape.setAutoDraw(False)
                win.flip()
                core.wait(1)

                boxes[resp].fillColor = [-1,-1,-1]
                respLabels[resp].color = [1,1,1]
                break

    mouse.setVisible(0)

    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)


def prisoners_dilemma_feedback():

    posDecisions = pd.DataFrame({'first': [10, 9, 10, 3, 1, 5, 7, 5, 9, 7],
    'second': [10, 10, 10, 8, 7, 10, 10, 10, 10, 10]})

    negDecisions = pd.DataFrame({'first': [10, 9, 10, 3, 1, 5, 7, 5, 9, 7],
    'second': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]})

    posDecisions = posDecisions.reindex(np.random.permutation(posDecisions.index))
    posDecisions = posDecisions.reset_index(drop = True)

    negDecisions = negDecisions.reindex(np.random.permutation(negDecisions.index))
    negDecisions = negDecisions.reset_index(drop = True)


    if impPartnerOrder[0] == "pos":
        partnerShape = posShape
        decisions = posDecisions
    elif impPartnerOrder[0] == "neg":
        partnerShape = negShape
        decisions = negDecisions

    partnerShape.pos = (0,200)
    partnerShape.radius = 70

    partnerShape.setAutoDraw(True)

    gf.show_instructs(win=win,
        text=['This participant was randomly selected to decide second. This means they got to see their partners\' decisions first before deciding how much to send.\n\nContinue to view their decisions.'],
        timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], textPos=(0,-100), units='pix')

    partnerShape.setAutoDraw(False)

    partnerShape.pos = (0,-100)
    partnerShape.radius = 50

    firstDecision = visual.TextStim(win=win, units="pix", colorSpace='rgb', color=(1,1,1), font='Arial', height=40, text="", pos=(0,200), wrapWidth=1000)
    secondDecision = visual.TextStim(win=win, units="pix", colorSpace='rgb', color=(1,1,1), font='Arial', height=40, text="", pos=(0,-200), wrapWidth=1000)
    contText = visual.TextStim(win=win, units="pix", colorSpace='rgb', color=(1,1,1), font='Arial', height=40, text="Press space to continue", pos=(0,-400))

    for i, thisTrial in decisions.iterrows():
        firstDecision.setText("The first partner sent %d out of 10 points, which tripled to become %d." %(decisions.loc[i, "first"], decisions.loc[i, "first"]*3))
        secondDecision.setText("Sent %d out of 10 points, which tripled to become %d." %(decisions.loc[i, "second"], decisions.loc[i, "second"]*3))

        event.clearEvents()

        while not event.getKeys(keyList = ['space']):
            contText.draw()
            firstDecision.draw()
            win.flip()

        event.clearEvents()

        while not event.getKeys(keyList = ['space']):
            contText.draw()
            firstDecision.draw()
            secondDecision.draw()
            partnerShape.draw()
            win.flip()

        win.flip()
        core.wait(1)

    gf.show_instructs(win=win,
        text=['You have viewed all of this participant\'s decisions.\n\nContinue to view the next participant\'s decisions.'],
        timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], units='pix')

    if impPartnerOrder[1] == "pos":
        partnerShape = posShape
        decisions = posDecisions
    elif impPartnerOrder[1] == "neg":
        partnerShape = negShape
        decisions = negDecisions

    partnerShape.pos = (0,200)
    partnerShape.radius = 70

    partnerShape.setAutoDraw(True)

    gf.show_instructs(win=win,
        text=['This participant was randomly selected to decide second. This means they got to see their partners\' decisions first before deciding how much to send.\n\nContinue to view their decisions.'],
        timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], textPos=(0,-100), units='pix')

    partnerShape.setAutoDraw(False)

    partnerShape.pos = (0,-100)
    partnerShape.radius = 50

    for i, thisTrial in decisions.iterrows():
        firstDecision.setText("The first partner sent %d out of 10 points, which tripled to become %d." %(decisions.loc[i, "first"], decisions.loc[i, "first"]*3))
        secondDecision.setText("Sent %d out of 10 points, which tripled to become %d." %(decisions.loc[i, "second"], decisions.loc[i, "second"]*3))

        event.clearEvents()

        while not event.getKeys(keyList = ['space']):
            contText.draw()
            firstDecision.draw()
            win.flip()

        event.clearEvents()

        while not event.getKeys(keyList = ['space']):
            contText.draw()
            firstDecision.draw()
            secondDecision.draw()
            partnerShape.draw()
            win.flip()

        win.flip()
        core.wait(1)

    gf.show_instructs(win=win,
        text=['You have viewed all of this participant\'s decisions.'],
        timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], units='pix')


def wait_for_others(totalWait=1000, p1delay=0, p2delay=400, p4delay=900):
    """ Function for 'waiting' for other participants to be ready
    """

    posShape.pos = labelPositions[0]
    posShape.radius = 40
    neuShape.pos = labelPositions[1]
    neuShape.radius = 40
    negShape.pos = labelPositions[2]
    negShape.radius = 40

    waitingText = visual.TextStim(win=win, pos=(-200,300), text="Waiting for other participants...", font=textFont, bold=True, height=40, wrapWidth=800, units="pix")
    p3WaitText = visual.TextStim(win=win, pos=(-70,-150), text="You", font=textFont, bold=True, height=40, units="pix")
    p1WaitBox = visual.Rect(win=win, width=40, height=40, lineColor=(1,1,1), lineWidth=5.0, pos=(70,150), fillColor=(1,-1,-1), units="pix")
    p2WaitBox = visual.Rect(win=win, width=40, height=40, lineColor=(1,1,1), lineWidth=5.0, pos=(70,0), fillColor=(1,-1,-1), units="pix")
    p3WaitBox = visual.Rect(win=win, width=40, height=40, lineColor=(1,1,1), lineWidth=5.0, pos=(70,-150), fillColor=(-1,1,-1), units="pix")
    p4WaitBox = visual.Rect(win=win, width=40, height=40, lineColor=(1,1,1), lineWidth=5.0, pos=(70,-300), fillColor=(1,-1,-1), units="pix")

    waitingText.setAutoDraw(True)
    posShape.setAutoDraw(True)
    neuShape.setAutoDraw(True)
    negShape.setAutoDraw(True)
    p3WaitText.setAutoDraw(True)
    p1WaitBox.setAutoDraw(True)
    p2WaitBox.setAutoDraw(True)
    p3WaitBox.setAutoDraw(True)
    p4WaitBox.setAutoDraw(True)

    p1switch = False
    p2switch = False
    p4switch = False

    for frameN in range(totalWait):
        win.flip()

        if frameN > p1delay and not p1switch:
            p1WaitBox.fillColor = (-1,1,-1)
            p1switch = True

        if frameN > p2delay and not p2switch:
            p2WaitBox.fillColor = (-1,1,-1)
            p2switch = True

        if frameN > p4delay and not p4switch:
            p4WaitBox.fillColor = (-1,1,-1)
            p4switch = True

    waitingText.setAutoDraw(False)
    posShape.setAutoDraw(False)
    neuShape.setAutoDraw(False)
    negShape.setAutoDraw(False)
    p3WaitText.setAutoDraw(False)
    p1WaitBox.setAutoDraw(False)
    p2WaitBox.setAutoDraw(False)
    p3WaitBox.setAutoDraw(False)
    p4WaitBox.setAutoDraw(False)


def partner_pain_feedback():

    cuePositions = [-200, 0, 200]
    random.shuffle(cuePositions)  # randomize cue positions

    posShape.pos = (cuePositions[0], 0)
    posShape.radius = 50
    neuShape.pos = (cuePositions[1], 0)
    neuShape.radius = 50
    negShape.pos = (cuePositions[2], 0)
    negShape.radius = 50

    leftPainText = visual.TextStim(win=win, units='pix', colorSpace='rgb', color=(1,1,1), font='Arial', text="7", height=70, wrapWidth=100, pos=(-200,-100))
    centerPainText = visual.TextStim(win=win, units='pix', colorSpace='rgb', color=(1,1,1), font='Arial', text="7", height=70, wrapWidth=100, pos=(0,-100))
    rightPainText = visual.TextStim(win=win, units='pix', colorSpace='rgb', color=(1,1,1), font='Arial', text="7", height=70, wrapWidth=100, pos=(200,-100))

    posShape.setAutoDraw(True)
    neuShape.setAutoDraw(True)
    negShape.setAutoDraw(True)
    leftPainText.setAutoDraw(True)
    centerPainText.setAutoDraw(True)
    rightPainText.setAutoDraw(True)

    gf.show_instructs(win=win,
       text=["Partners' pain ratings on scale from 1 (not at all) to 7 (extremely):"],
       timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], units='pix')

    posShape.setAutoDraw(False)
    neuShape.setAutoDraw(False)
    negShape.setAutoDraw(False)
    leftPainText.setAutoDraw(False)
    centerPainText.setAutoDraw(False)
    rightPainText.setAutoDraw(False)


def coldPressorQs(win=None, saveFile=None, scaleName="coldPressorQs", subjNum=0, endPause=1.0):
    """ Questions about cold pressor

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """

    # display scale instructions
    gf.show_instructs(win=win,
    text=["Now, use the scale provided to indicate your response to the following questions.\n\nUse the number keys at the top of the keyboard to respond." ],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], units='pix')

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(7):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-7
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-7

    secondaryLabels = ["Not at all", "", "", "", "", "", "Extremely"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=400, primaryPos=-300, primaryHeight=40, secondaryPos=-200, secondaryHeight=30,
                                         secondaryWrapWidth=200, win=win, bold=True, units='pix')

    # run scale
    results = qs.run_scale_items(win=win,
    scaleItems=["Overall, how PAINFUL did you find it to hold your hand in the ice water?",
    "Overall, how PLEASANT was it to hold your hand in the ice water?",
    "Overall, how UNPLEASANT was it to hold your hand in the ice water?"],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)
    else:
        return results

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)



def partnerImpression(win=None, saveFile=None, scaleName="partnerImpression", subjNum=0, endPause=1.0, partner=None):
    """ Person Perception Scale

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(9):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-9
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-9

    secondaryLabels = ["Not at all", "", "", "", "", "", "", "", "Extremely"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=500, primaryPos=-300, primaryHeight=40, secondaryPos=-250, secondaryHeight=30,
                                         secondaryWrapWidth=200, win=win, bold=True, units='pix')

    if partner == "pos":
        partnerShape = posShape
    elif partner == "neu":
        partnerShape = neuShape
    elif partner == "neg":
        partnerShape = negShape

    partnerShape.pos = (0,280)
    partnerShape.radius = 80

    # ratings of task behavior
    if partner in ["pos", "neg"]:

        gf.show_instructs(win=win,
        text=["First, you will rate your impressions of this participant's decisions during the previous task. Your responses are completely anonymous and will not be shown to any of the other participants. Please provide your honest ratings.",
        "Use the scale provided to indicate your agreement with each of the statements."],
        timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], units='pix')

        partnerShape.setAutoDraw(True)

        # run scale
        choiceRatings = qs.run_scale_items(win=win,
        scaleItems=["This person was generous",
        "This person was selfish",
        "This person was fair",
        "This person was foolish",
        "This person was selfless",
        "This person was greedy",
        "This person was cooperative",
        "This person was reasonable",
        "This person was mean-spirited",
        "This person was kind-hearted",
        "This person was rational"],
        respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum, pos=(0,50), height=35, wrapWidth=1200, units='pix')

        partnerShape.setAutoDraw(False)

        gf.show_instructs(win=win,
        text=["Next, you will be asked to rate your general impressions of this participant."],
        timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], units='pix')

    elif partner == "neu":

        gf.show_instructs(win=win,
        text=["We would also like to get your impressions of the other participant in this session whose decisions you did not see. Even though you have not seen of the decisions made by this participant, we would like for you to give your general impression of what you think this person is probably like."],
        timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], units='pix')

    # display scale instructions
    gf.show_instructs(win=win,
    text=["Use the scale provided to indicate your agreement with each of the statements. Your responses are completely anonymous and will not be shown to any of the other participants. Please provide your honest impression." ],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], units='pix')

    partnerShape.setAutoDraw(True)

    # run scale
    results = qs.run_scale_items(win=win,
    scaleItems=["This person is sensitive to physical pain",
    "This person finds the ice water very painful",
    "This person is considerate",
    "This person is intelligent",
    "This person is just",
    "This person is clever",
    "This person is capable",
    "This person is efficient",
    "This person is fair",
    "This person is friendly",
    "This person is warm in relations with others",
    "This person is competent",
    "This person is innocent",
    "This person is reliable",
    "This person is affectionate",
    "This person gives up easily",
    "This person is trustworthy",
    "This person is self-confident",
    "This person is foolish",
    "This person stands up well under pressure",
    "This person is caring",
    "This person is empathetic",
    "This person feels superior",
    "This person has leadership qualities",
    "To what extent do you care about this person's welfare?\n\nFor this question, think of someone whose welfare you value very highly (e.g., a best friend or favorite family member). Now think of someone whose welfare you do not value highly (e.g., someone you know nothing about at all). Give your response in comparison to these two extremes.",
    "To what extent would you like for good things to happen for this person?\n\nFor this question, think of someone for whom you very strongly want to see good things happen (e.g., a best friend or favorite family member). Now think of someone for whom you do not feel this very strongly (e.g., someone you know nothing about at all). Give your response in comparison to these two extremes.",
    "To what extent would you dislike for bad things to happen for this person?\n\nFor this question, think of someone for whom you very strongly do not want to see bad things happen (e.g., a best friend or favorite family member). Now think of someone for whom you do not feel this very strongly (e.g., someone you know nothing about at all). Give your response in comparison to these two extremes.",
    "To what extent would you like for this person to get the things they want?\n\nFor this question, think of someone who you very strongly want to see get what they want (e.g., a best friend or favorite family member). Now think of someone for whom you do not feel this very strongly (e.g., someone you know nothing about at all). Give your response in comparison to these two extremes."],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum, pos=(0,50), height=35, wrapWidth=1200, units='pix')

    partnerShape.setAutoDraw(False)

    results['partner'] = partner

    if partner in ["pos", "neg"]:
        choiceRatings['partner'] = partner
        results = pd.concat([choiceRatings, results])

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)
    else:
        return results

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


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
    # notReady = True
    # while notReady:
    #     keysPressed = event.getKeys(keyList = ['space', 'q'])
    #     if len(keysPressed) > 0:
    #         if keysPressed[0] == 'space':
    #             notReady =  False
    #         elif keysPressed[0] == 'q':
    #             win.close()
    #             core.quit()
    #     win.flip()
    # event.clearEvents()
    # preparingScannerText.setAutoDraw(False)

    # WAIT FOR SCANNER START
    # waitingForScannerText.setAutoDraw(True)
    # event.clearEvents()
    # while not event.getKeys(keyList = ['5']):
    #     win.flip()
    # event.clearEvents()
    # waitingForScannerText.setAutoDraw(False)


    # Assign runNumber based on existing csv file. Read the csv file and find the largest block number and add 1 to it to reflect this block's number.
    try:
        runNumber = max(pd.read_csv(saveFile)['runNumber']) + 1
        trialsDf['runNumber'] = runNumber
    except:  # if fail to read csv, then it's block 1
        runNumber = 1
        trialsDf['runNumber'] = runNumber

    blockClock.reset()

    # initialize variable for storing partner on previous trial
    prevPartner = []

    # run block trials
    for i, thisTrial in trialsDf.iterrows():

        # if new partner on this trial, give task instructions
        if trialsDf.loc[i, 'partner'] != prevPartner:

            # change partner rect cue and shape
            if trialsDf.loc[i, 'partner'] == 'pos':
                partnerCue = posRect
                partnerShape = posShape
            elif trialsDf.loc[i, 'partner'] == 'neu':
                partnerCue = neuRect
                partnerShape = neuShape
            elif trialsDf.loc[i, 'partner'] == 'neg':
                partnerCue = negRect
                partnerShape = negShape
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
        probText.setAutoDraw(True)
        trialsDf.loc[i, 'need_onset'] = blockClock.getTime()
        timer = core.CountdownTimer(trialsDf.loc[i, 'needDur'])
        while timer.getTime() > 0:
            win.flip()
        probText.setAutoDraw(False)

        # JITTER
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
        trialsDf.loc[i, 'prop_onset'] = blockClock.getTime()
        timer = core.CountdownTimer(trialsDf.loc[i, 'propDur'])
        while timer.getTime() > 0:
            keysPressed = event.getKeys(keyList=respKeys, timeStamped=rtClock)  # load keys that have been pressed

            if len(keysPressed) > 0:  # check if a key has been pressed yet
                if keyResp is None:  # check if another key response has already been recorded
                    trialsDf.loc[i, 'resp_onset'] = blockClock.getTime()
                    keyResp, RT = keysPressed[0]  # access first key response and corresponding RT
                    # RTfromClock = rtClock.getTime()  # record RT from rtClock

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
        fixation.setAutoDraw(True)
        trialsDf.loc[i, 'iti_onset'] = blockClock.getTime()
        timer = core.CountdownTimer(trialsDf.loc[i, 'itiDur'])
        while timer.getTime() > 0:
            win.flip()
        fixation.setAutoDraw(False)

    posRect.setAutoDraw(False)
    neuRect.setAutoDraw(False)
    negRect.setAutoDraw(False)
    pracRect.setAutoDraw(False)

    trialsDf['endTime'] = str(time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime()))

    # append block data to save file
    trialsDf.to_csv(saveFilename, header = writeHeader, mode = 'a', index = False)

    return trialsDf


# ============================================================================ #
# RUN EXPERIMENT

gf.show_instructs(win=win, text=["Welcome to the experiment!"],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], saveFile=os.path.join(saveDir, "instructs0_.png"), units='pix')

painRecord = painDial(win=win, duration=120)
painRecord.to_csv(os.path.join(saveDir, "%04d_%s_%s_%s.csv") %(int(expInfo['subject']), expInfo['startTime'], expInfo['expName'], 'painDial'), header = True, mode = 'w', index = False)
gf.show_instructs(win=win, text=["You may remove your hand from the ice water."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], saveFile=os.path.join(saveDir, "instructs0_.png"), units='pix')
coldPressorQs(win=win, saveFile=os.path.join(saveDir, "%04d_%s_%s_%s.csv") %(int(expInfo['subject']), expInfo['startTime'], expInfo['expName'], 'coldPressorQs'), subjNum=expInfo['subject'])

gf.show_instructs(win=win, text=["You have completed the ice task.\n\nPlease wait patiently. Do NOT continue until the experimenter tells you to do so."],
   timeAutoAdvance=0, timeRequired=0, secretKey=['p'], units='pix')

# initial instructions
gf.show_instructs(win=win,
    text=['In today\'s experiment, you will complete tasks with other participants.\n\nThe goal of the first part of the study is to examine how people make decisions with others.',
    'Depending on your choices during the tasks, you will have the opportunity to earn money. You will be paid in cash at the end of the experiment.',
    'For this task, you will be paired with other participants. Your choices will influence how much money you and your partners earn.',
    'Because your decisions can have a big impact on your partners\' payoffs, think carefully about your partners throughout the experiment.',
    'In the next sections, we will describe precisely the instructions for the first task you will be completing. Pay attention to these instructions. It is critical that you understand the instructions in order to complete the task.',
    'For each trial in the following task, you will be paired with a different partner. Your partners will be other participants.'],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], saveFile=os.path.join(saveDir, "instructs1a_.png"), units='pix')

gf.show_instructs(win=win,
    text=['On each trial, both you and your partner will start with 10 points.\n\nEach of you will decide how many of your points you would like to send to the other.'],
    timeAutoAdvance=0, timeRequired=0, textPos=(0,300), advanceKey=['space'], image=os.path.join(os.getcwd(), 'taskInstructs', 'pdInstructs_1.png'),
    imageDim=(900,450), imagePos=(0, -100),
    saveFile=os.path.join(saveDir, "instructs1b_.png"), units='pix')

gf.show_instructs(win=win,
    text=['One person will be randomly selected to go first. Any points that are sent will be tripled before being given to the other partner.\n\nFor example, if Partner A sends all 10 points, Partner B will receive 30 points.'],
    timeAutoAdvance=0, timeRequired=0, textPos=(0,300), advanceKey=['space'], image=os.path.join(os.getcwd(), 'taskInstructs', 'pdInstructs_2.png'),
    imageDim=(900,450), imagePos=(0, -100),
    saveFile=os.path.join(saveDir, "instructs1c_.png"), units='pix')

gf.show_instructs(win=win,
    text=['The second person will get to see how much the first person sent before deciding how many of their 10 points to send.'],
    timeAutoAdvance=0, timeRequired=0, textPos=(0,300), advanceKey=['space'], image=os.path.join(os.getcwd(), 'taskInstructs', 'pdInstructs_3.png'),
    imageDim=(900,450), imagePos=(0, -100),
    saveFile=os.path.join(saveDir, "instructs1d_.png"), units='pix')

gf.show_instructs(win=win,
    text=['Again, any points that are sent will be tripled before being to given to the other. If Partner B sends all 10 points, Partner A will receive 30 points.'],
    timeAutoAdvance=0, timeRequired=0, textPos=(0,300), advanceKey=['space'], image=os.path.join(os.getcwd(), 'taskInstructs', 'pdInstructs_4.png'),
    imageDim=(900,450), imagePos=(0, -100),
    saveFile=os.path.join(saveDir, "instructs1e_.png"), units='pix')

gf.show_instructs(win=win,
    text=['Therefore, if both partners decide to send all 10 of their points, then both partners will end with 30 points.'],
    timeAutoAdvance=0, timeRequired=0, textPos=(0,300), advanceKey=['space'], image=os.path.join(os.getcwd(), 'taskInstructs', 'pdInstructs_5.png'),
    imageDim=(900,450), imagePos=(0, -100),
    saveFile=os.path.join(saveDir, "instructs1f_.png"), units='pix')

gf.show_instructs(win=win,
    text=['If neither partner sends any points, then both partners will end with 10 points (the 10 they each started with).'],
    timeAutoAdvance=0, timeRequired=0, textPos=(0,300), advanceKey=['space'], image=os.path.join(os.getcwd(), 'taskInstructs', 'pdInstructs_1.png'),
    imageDim=(900,450), imagePos=(0, -100),
    saveFile=os.path.join(saveDir, "instructs1g_.png"), units='pix')

gf.show_instructs(win=win,
    text=['If one partner sends all 10 points and the other partner doesn\'t send anything, then the one partner will end with 0 points and the other will end with 40 points (the 10 points they started with plus 30 from the other partner).'],
    timeAutoAdvance=0, timeRequired=0, textPos=(0,300), advanceKey=['space'], image=os.path.join(os.getcwd(), 'taskInstructs', 'pdInstructs_6.png'),
    imageDim=(900,450), imagePos=(0, -100),
    saveFile=os.path.join(saveDir, "instructs1h_.png"), units='pix')

gf.show_instructs(win=win,
    text=['The computer will randomly assign you to either decide first or second for all of your decisions.\n\nIf you are selected to decide first, your decision will be given to another participant later.',
    'If you are selected to decide second, you will receive the decisions of a few other participants and be asked to make your decisions as the second partner.',
    'One of your decisions from a task in today\'s experiment will be randomly selected to count for real money. Treat every trial as if it could be the one and only trial that determines how much you and your partner receive.',
    'The decisions made by you and your partner will be completely anonymous. Neither of you will receive any identifying information about the other. The only information that either partner will receive is how many points were sent by the other partner.',
    'Your decisions may be shown to other participants besides your partner, but again your decisions will be completely anonymous. The other participants will simply be asked to observe and rate the decisions being made.',
    'The computer will now randomly select whether you will decide first or second in this task.',
    'You have been selected to decide second.\n\nYou will be sent points by several partners. For each partner, you will then decide how many of your points to send. Each decision will be with a different partner.',
    'Before beginning the task, you will complete a brief quiz over the instructions you\'ve just read to make sure you\'ve understood the task.'],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], saveFile=os.path.join(saveDir, "instructs1i_.png"), units='pix')

pdQuizResults = gf.task_quiz(win=win, quizFile=pdQuizFile, subjNum=expInfo['subject'])
pdQuizResults.to_csv(os.path.join(saveDir, "%04d_%s_%s_prisonersDilemmaQuiz.csv") %(int(expInfo['subject']), expInfo['startTime'], expInfo['expName']), header = True, mode = 'w', index = False)

gf.show_instructs(win=win,
    text=['You have completed the quiz. If you have any questions about the task, please ask the experimenter before continuing.\n\nContinue when you are ready to begin. Use the mouse to left click on your decision for each trial.'],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], saveFile=os.path.join(saveDir, "instructs2_.png"), units='pix')

prisonersDilemma(saveFile=os.path.join(saveDir, "%04d_%s_%s_%s.csv") %(int(expInfo['subject']), expInfo['startTime'], expInfo['expName'], 'prisonersDilemma'))

gf.show_instructs(win=win,
    text=['You have completed the task.\n\nIn addition to studying people\'s decisions, we are also interested in understanding how people perceive the decisions of others. Therefore, we are now going to have you rate the decisions made by two other participants.',
    'Right now, in the other rooms, there are other participants completing the same experiment as you. You will see the decisions that were made by two of these other participants. The participants whose decisions you will see will be randomly selected.'],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], saveFile=os.path.join(saveDir, "instructs3_.png"), units='pix')

# Present partner cues
# Setup partner cues for instructions
cuePositions = [-200, 0, 200]
random.shuffle(cuePositions)  # randomize cue positions

posShape.pos = (cuePositions[0], -100)
posShape.radius = 70
neuShape.pos = (cuePositions[1], -100)
neuShape.radius = 70
negShape.pos = (cuePositions[2], -100)
negShape.radius = 70

posShape.setAutoDraw(True)
neuShape.setAutoDraw(True)
negShape.setAutoDraw(True)

gf.show_instructs(win=win,
   text=["For today's experiment, the other participants in your session will be represented to you by colorful shapes. This way all your interactions will be kept anonymous.\n\nHere are the shapes that will be used to represent each of the other participants:"],
   timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], saveFile=os.path.join(saveDir, "instructs4_.png"), units='pix')

posShape.setAutoDraw(False)
neuShape.setAutoDraw(False)
negShape.setAutoDraw(False)

gf.show_instructs(win=win,
    text=['Pay careful attention to the information that you receive about each of the other participants because you will soon be asked to provide ratings about them.',
    'You now will need to wait until all the other participants have completed their decisions. Continue to the next screen to wait until each participant is ready. When each participant is ready, the box next to their symbol will turn green.'],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], saveFile=os.path.join(saveDir, "instructs5_.png"), units='pix')

# loading screen
labelPositions = [(-70,150), (-70,0), (-70,-300)]
random.shuffle(labelPositions)
wait_for_others(totalWait=1500, p1delay=0, p2delay=900, p4delay=1400)

gf.show_instructs(win=win,
    text=['All the other participants have completed their decisions. You will now be presented with the decisions of two of the other participants.'],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], saveFile=os.path.join(saveDir, "instructs6_.png"), units='pix')

prisoners_dilemma_feedback()

prisonersDilemma_guesses(saveFile=os.path.join(saveDir, "%04d_%s_%s_%s.csv") %(int(expInfo['subject']), expInfo['startTime'], expInfo['expName'], 'prisonersDilemmaGuesses'))

gf.show_instructs(win=win,
    text=['In addition to viewing the decisions of some of the other participants, we are also going to present you with information about the other participants\' tolerance for cold based on the ice task you all completed earlier.\n\nOn the next screen, you will see how painful each of the other three participants in your current session rated the ice water on a scale of 1 (not at all) to 7 (extremely).'],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], saveFile=os.path.join(saveDir, "instructs7_.png"), units='pix')

partner_pain_feedback()

gf.show_instructs(win=win,
    text=["Now that you have been given some information about the other participants, you will answer a few questions about them.",
    "We're interested in knowing what your impressions of the other participants are. On the following screens, you will complete a survey about each participant."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], saveFile=os.path.join(saveDir, "instructs8_.png"), units='pix')

p1Impressions = partnerImpression(win=win, subjNum=expInfo['subject'], partner=impPartnerOrder[0])
p2Impressions = partnerImpression(win=win, subjNum=expInfo['subject'], partner=impPartnerOrder[1])
p3Impressions = partnerImpression(win=win, subjNum=expInfo['subject'], partner="neu")
p123Impressions = pd.concat([p1Impressions, p2Impressions, p3Impressions])
p123Impressions.to_csv(os.path.join(saveDir, "%04d_%s_%s_%s.csv") %(int(expInfo['subject']), expInfo['startTime'], expInfo['expName'], 'partnerImpressions'), header = True, mode = 'w', index = False)


gf.show_instructs(win=win,
    text=["In addition to the other tasks that you are completing today, we're also interested in getting a measure of your numerical intuition. Next, you will complete a brief task assessing this."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], saveFile=os.path.join(saveDir, "instructs9_.png"), units='pix')

numericalMapping(win=win, saveFile=os.path.join(saveDir, "%04d_%s_%s_%s.csv") %(int(expInfo['subject']), expInfo['startTime'], expInfo['expName'], 'numericalMapping'))

### Dictator Game --------------------------------------------------------------

gf.show_instructs(win=win,
    text=["You have completed the numerical intuition task.",
    "You will now receive instructions for the task that you will be completing in the fMRI scanner.",
    "For this task, we are interested in understanding how people make decisions about outcomes that affect not only themselves, but also other people. Depending on your choices during the task, you will have the opportunity to earn from $0 up to $40. You will be paid in cash at the end of the experiment.",
    "In the other rooms, there are other people participating. They will be your partners. Depending on your choices, you might end up causing one of them to end up with $0 up to $40.",
    "The decision you make can have a large impact on the other participant's payoffs. Like you, they signed up for this experiment. Since your decisions can have a big impact on their payoffs, think carefully about your partners throughout the experiment.",
    "Additionally, one of your partners may have to hold a hand in the ice water again. We will describe this soon.",
    "In the next sections, we will describe precisely the instructions for the task you will be completing. Pay attention to these instructions. It is critical that you understand the instructions, since they affect your ability to make good decisions -- and potentially more money!",
    "In this task, you will be deciding how to allocate money between yourself and a partner.\n\nYou will always be partnered with one of the other participants in your current session. The same anonymous symbol will be used to indicate the same person as before.\n\nThink about this person as you make your decisions."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], saveFile=os.path.join(saveDir, "instructs10a_.png"), units='pix')

gf.show_instructs(win=win,
    text=["On each trial of this task, you will see a proposal. On one side of the screen you will see the amount of money you will receive if you decide to accept the proposal. On the other side of the screen, you will see the amount of money your partner will receive if you accept the proposal. We'll call this the 'proposed allocation'.",
    "In the example below, the proposed allocation is for you to receive $23 and your partner to receive $15.\n\nThe amounts of money will always range between $0 and $40, for both you and the other person.",
    "If you decide to reject the offer, both you and your partner will each receive $20.\n\nWe will call this the 'default allocation', which will be the same for all trials.",
    "In every trial, therefore, you are choosing between the proposed allocation (the offer displayed on the screen) and the default allocation (you each receive $20).",
    "For instance, if you accepted the proposed allocation shown below, this would indicate that you prefer $23 for you ($3 above the default of $20), and $15 total for the other person ($5 below the default of $20)."],
    timeAutoAdvance=0, timeRequired=0, textPos=(0,250), wrapWidth=1200, advanceKey=['space'], image=os.path.join(os.getcwd(), 'screenShots', 'prechoice_%s_%d_%s.png' %(neuColorText, neuShape.edges, subjectConds[2])),
    imageDim=(500,313), imagePos=(0, -100),
    saveFile=os.path.join(saveDir, "instructs10b_.png"), units='pix')

gf.show_instructs(win=win,
    text=["Although we are asking you to choose between accepting and rejecting the proposed allocation, we would also like to get a sense of how strongly you feel about this choice. So you should indicate your choice on the following four-point scale:"],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], image=respOptsImageFile, imageDim=(659,381), imagePos=(0,-100), saveFile=os.path.join(saveDir, "instructs11_.png"), textPos=(0,250), units='pix', wrapWidth=1200)

gf.show_instructs(win=win,
    text=["To make your decisions, you should place your right-hand fingers on the keys shown below:"],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], image=keyboardImageFile, imageDim=(800,485), imagePos=(0,-100), saveFile=os.path.join(saveDir, "instructs12a_.png"), textPos=(0,250), units='pix')

gf.show_instructs(win=win,
    text=["It is important to note: Either 'Strong No' or 'No' are counted as choosing the default allocation. Either 'Strong Yes' or 'Yes' are counted as choosing the proposed allocation. You are still just choosing whether to accept or reject the proposal, but you are also indicating how strongly you prefer the proposed or default options."],
    timeAutoAdvance=0, timeRequired=0, textPos=(0,250), advanceKey=['space'], image=os.path.join(os.getcwd(), 'taskInstructs', 'yesNoInstructs.png'),
    imageDim=(700,200), imagePos=(0, -100),
    saveFile=os.path.join(saveDir, "instructs12b_.png"), units='pix')

gf.show_instructs(win=win,
    text=["You will be required to make your decision within 4 seconds of the appearance of the proposal. If you do not make a response within that amount of time, the computer will randomly select either the proposed or default allocation for that trial.\n\nIt is therefore in your best interest to respond in a timely manner according to your preference."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], saveFile=os.path.join(saveDir, "instructs12c_.png"), textPos=(0,250), units='pix')

gf.show_instructs(win=win,
    text=["A grey box will appear when you make your response to let you know that your choice has been recorded."],
    timeAutoAdvance=0, timeRequired=0, textPos=(0,250), advanceKey=['space'], image=os.path.join(os.getcwd(), 'screenShots', 'postchoice_%s_%d_%s.png' %(neuColorText, neuShape.edges, subjectConds[2])),
    imageDim=(500,313), imagePos=(0, -100),
    saveFile=os.path.join(saveDir, "instructs12d_.png"), units='pix')

gf.show_instructs(win=win,
    text=["There is another element to this task. On each trial before you see the proposal, you will first see a percentage, such as 78%.",
    "This percentage indicates the likelihood that your partner will be required to hold a hand in the ice water again at the end of the experiment. For example, if the percentage was 78%, this would mean there is a 78% chance your partner will have to hold a hand in the ice water again (and a 22% chance that they will not).",
    "At the end of the experiment, your partner will have the opportunity to spend some of the money you gave them on that trial to reduce their chances of having to hold a hand in ice water again, if they wish.",
    "Each dollar your partner spends will reduce their chances of having to hold a hand in ice water again by 10%.\n\nAny money that they spend will be returned to the experimenter. They will keep any money that they don't spend as their final payment.",
    "For example, if they have an 78% chance of having to holding their hand in ice water and choose to spend $7 out of $20, their chances would be reduced to 8% (-10% for each $1 spent) and they would keep $13 ($7 less than the $20 you gave them).",
    "After they've made their choice, the computer will conduct a random lottery using the final probability to determine if your partner will have to hold a hand in ice water again.",
    "Therefore, your decisions will determine not only how much money your partner receives as payment, but also how much they can afford to reduce the chances of having to hold a hand in the ice water."],
    timeAutoAdvance=0, timeRequired=0, textPos=(0,250), wrapWidth=1200, advanceKey=['space'], image=os.path.join(os.getcwd(), 'screenShots', 'need_%s.png' %(neuColorText)),
    imageDim=(500,313), imagePos=(0, -100),
    saveFile=os.path.join(saveDir, "instructs12e_.png"), units='pix')

gf.show_instructs(win=win,
    text=["Throughout the experiment, you will often see a '+' in the middle of the screen. Please keep your eyes on this center cross when it appears."],
    timeAutoAdvance=0, timeRequired=0, textPos=(0,250), advanceKey=['space'], image=os.path.join(os.getcwd(), 'screenShots', 'fix_%s.png' %(neuColorText)),
    imageDim=(500,313), imagePos=(0, -100),
    saveFile=os.path.join(saveDir, "instructs12f_.png"), units='pix')

gf.show_instructs(win=win,
    text=["You will complete a few blocks of trials. In each block, you will make sets of decisions with each of your partners. You will be told who your partner is each time you start a new set of decisions. This will be the other person whose payoff will be affected by your decisions during that set.\n\nThe screen telling you who your partner is will look like this:",
    "In addition to the screen displaying your partner at the beginning of each set, you will also always see a colored border around the screen to remind you who your current partner is.",
    "You will complete 5 sets with each partner."],
    timeAutoAdvance=0, timeRequired=0, textPos=(0,250), wrapWidth=1200, advanceKey=['space'], image=os.path.join(os.getcwd(), 'screenShots', 'partner_%s_%d.png' %(neuColorText, neuShape.edges)),
    imageDim=(500,313), imagePos=(0, -100),
    saveFile=os.path.join(saveDir, "instructs12g_.png"), units='pix')

gf.show_instructs(win=win,
    text=["How do your choices on each trial translate into a payment at the end?\n\nAt the end of the experiment, we will randomly pair you with another participant and randomly select ONE trial from among all the decisions you made for that partner. The results of this trial will count for real money.\n\nThe likelihood of your partner having to hold a hand in the ice water will also be determined by this trial.",
    "Therefore, you should treat every trial when it appears as if it could be the one and only trial that finally determines how much you and your partner receive at the end of the experiment.",
    "You will now have some practice trials. These trials will not count for anything, but are just to give you a sense for the timing and feel of the task."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], wrapWidth=1200, saveFile=os.path.join(saveDir, "instructs12h_.png"), textPos=(0,100), units='pix')

gf.show_instructs(win=win,
    text=["Before you get started, here is a quick summary:"],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'],
    image=os.path.join(os.getcwd(), 'taskInstructs', 'instructSummary_%s_%d_%s.png' %(neuColorText, neuShape.edges, subjectConds[2])),
    textPos=(0,400),
    imageDim=(1200,675), imagePos=(0,0),
    saveFile=os.path.join(saveDir, "instructs12i_.png"), units='pix')

gf.show_instructs(win=win,
    text=["During the practice trials you will have a key at the bottom of the screen letting you know what button you pressed.\n\nThis key will be removed for the actual task. Please use the practice trials to make sure that you are responding as you intend."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], saveFile=os.path.join(saveDir, "instructs12j_.png"), textPos=(0,250), units='pix')

gf.show_instructs(win=win,
    text=["Remember the keys for each response:"],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], image=keyboardImageFile, imageDim=(800,485), imagePos=(0,-100), saveFile=os.path.join(saveDir, "instructs12k_.png"), textPos=(0,250), units='pix')

gf.show_instructs(win=win,
    text=["If you have any questions about the task, please ask the experimenter now. Otherwise, please proceed to the practice trials.",
    "For this first set of practice trials you will have 8 seconds rather than the usual 4 seconds to make your decisions. This is so you can first get familiar with the screens and how the response keys work.\n\nContinue when you are ready for the practice trials to begin."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], saveFile=os.path.join(saveDir, "instructs12l_.png"), textPos=(0,250), units='pix')

run_decision_run(trialsDf=pracBlock_8sec, saveFile=saveFilename)

gf.show_instructs(win=win,
    text=["Now you complete another set of practice trials, but this time you will only have 4 seconds to make your decisions. This is the same amount of time that you'll have in the actual task.\n\nContinue when you are ready for the practice trials to begin."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], saveFile=os.path.join(saveDir, "instructs12m_.png"), textPos=(0,250), units='pix')

run_decision_run(trialsDf=pracBlock_4sec, saveFile=saveFilename)

gf.show_instructs(win=win,
   text=["You have completed the practice trials.",
   "PRIVACY: As stated earlier, you will be making decisions about how to allocate money between yourself and another person. Importantly, all the decisions you make are secret and anonymous. The other person will never know your choices. All they will find out is what the one trial selected to count for real money is, what the proposed and default offers on that trial were, and what the outcome was.",
   "To make sure your choices are truly anonymous, a computer program will be used to randomly determine which trial counts for payment.",
   "Your partner will not be told who you are, and does not have enough information to link your choices to you.",
   "All of the data about your choices will be identified by an anonymous code that will have no connection to your personal information.",
   "Your decisions are anonymous and secret.",
   "If you have any questions about the experiment, please ask the experimenter now.",
   "Again, it is important that throughout this experiment, you consider both your feelings about the transfer and the potential impact on the other person. Your decisions can have a big impact on the payment they receive for the experiment and how much they can reduce their chances of having to hold a hand in ice water, so consider both the pros and cons of each of the transfers.",
   "Take your time! There are a number of transfers to consider, and each has both pros and cons. Try to think carefully about what the other person would in your shoes and how you might feel about the outcome.",
   "Before you begin, we would like to ask you a few questions to make sure that you have understood the task.\n\nContinue to take the short quiz."],
   timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], saveFile=os.path.join(saveDir, "instructs13_.png"), units='pix')

dgQuizResults = gf.task_quiz(win=win, quizFile=dgQuizFile, subjNum=expInfo['subject'])
dgQuizResults.to_csv(os.path.join(saveDir, "%04d_%s_%s_dictatorGameQuiz.csv") %(int(expInfo['subject']), expInfo['startTime'], expInfo['expName']), header = True, mode = 'w', index = False)

gf.show_instructs(win=win,
   text=["You have completed the quiz. If you have any questions, please be sure to ask the experimenter.\n\n\nLet the experimenter know that you have completed the task instructions."],
   timeAutoAdvance=0, timeRequired=0, secretKey=['p'], saveFile=os.path.join(saveDir, "instructs14_.png"), units='pix')

win.close()
core.quit()
