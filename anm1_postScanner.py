#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ANM1_postScanner
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
expName = 'ANM1_postScanner'  # experiment name
expVersion = 1.5  # experiment version
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

def partnerTaskQuestions(win=None, saveFile=None, partner=None, endPause=1.0):
    """ Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """

    if partner == 'pos':
        partnerShape = posShape
    elif partner == 'neu':
        partnerShape = neuShape
    elif partner == 'neg':
        partnerShape = negShape

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(5):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-6
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-6

    secondaryLabels = ["Not at all", "A little", "Moderately", "A lot", "Extremely"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.5, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.20, win=win, bold=True)

    partnerShape.radius = 80
    partnerShape.pos = (0, 300)
    partnerShape.setAutoDraw(True)

    # run scale
    results_1 = qs.run_scale_items(win=win,
    scaleItems=["How much more do you think this partner NEEDED help when the chance of having to hold a hand in ice water was 80% versus 20%?",
    "How much more do you think this partner DESERVED to be helped when the chance of having to hold a hand in ice water was 80% versus 20%?",
    "How much did the likelihood of this partner having to hold a hand in ice water again influence your decisions?",
    "How much did any of your prior knowledge about this partner influence your decisions?"],
    respScale=respOptions, respKeys=respKeys, scaleName=partner, subjNum=expInfo['subject'], pos=(0,0.2))


    boxCoords = gf.spacer(items=9, space=500, anchor=-200, units='pix')

    boxes = {}
    respLabels = {}
    for i in range(len(boxCoords)):
        respLabels[i] = visual.TextStim(win=win, text= '$' + str(i), pos = boxCoords[i], units="pix", height=40)
        boxes[i] = visual.Rect(win=win, units="pix", lineWidth=10, fillColor=[-1,-1,-1], width=80, height=80, pos=boxCoords[i])

    mouse = event.Mouse(visible=True, win=win)  # create mouse

    results_2 = pd.DataFrame({'partner': partner,
                              'subject': expInfo['subject'],
                              'resp': np.nan,
                              'scaleName': 'partnerSpend'}, index=[0])

    for j in range(len(boxes)):
        boxes[j].setAutoDraw(True)
        respLabels[j].setAutoDraw(True)
    qText = visual.TextStim(win=win, text="", pos=(0,80), height=40, wrapWidth=1000, units='pix')
    qText.setText("If given $20 with an 80% chance of having to hold a hand in ice water again, how much do you think this partner would spend to reduce the chances of ice water?\n\n(Use the mouse to respond)")
    qText.setAutoDraw(True)
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

        if resp is not None:
            boxes[resp].fillColor = [1,1,1]
            respLabels[resp].color = [-1,-1,-1]
            win.flip()
            core.wait(1)

            clicks, clickTimes = mouse.getPressed(getTime=True)
            results_2["resp"] = resp
            # results.loc[i, "rt"] = clickTimes[0]

            qText.setAutoDraw(False)
            for j in range(len(boxes)):
                boxes[j].setAutoDraw(False)
                respLabels[j].setAutoDraw(False)
            win.flip()

            boxes[resp].fillColor = [-1,-1,-1]
            respLabels[resp].color = [1,1,1]
            break

    mouse.setVisible(0)

    if partner in ['pos', 'neg']:
        boxCoords = gf.spacer(items=11, space=500, anchor=-200, units='pix')

        boxes = {}
        respLabels = {}
        for i in range(len(boxCoords)):
            respLabels[i] = visual.TextStim(win=win, text=str(i), pos = boxCoords[i], units="pix", height=40)
            boxes[i] = visual.Rect(win=win, units="pix", lineWidth=10, fillColor=[-1,-1,-1], width=80, height=80, pos=boxCoords[i])

        mouse = event.Mouse(visible=True, win=win)  # create mouse

        results_3 = pd.DataFrame({'partner': partner,
                                  'subject': expInfo['subject'],
                                  'resp': np.nan,
                                  'scaleName': 'partnerPDchoice'}, index=[0])

        for j in range(len(boxes)):
            boxes[j].setAutoDraw(True)
            respLabels[j].setAutoDraw(True)
        qText = visual.TextStim(win=win, text="", pos=(0,100), height=40, wrapWidth=1000, units='pix')
        qText.setText("In the first task you completed before the scanner, how many of the initial 10 points did this partner send to partners on average?")
        qText.setAutoDraw(True)
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
                results_3["resp"] = resp
                # results.loc[i, "rt"] = clickTimes[0]

                qText.setAutoDraw(False)
                for j in range(len(boxes)):
                    boxes[j].setAutoDraw(False)
                    respLabels[j].setAutoDraw(False)
                partnerShape.setAutoDraw(False)
                win.flip()

                boxes[resp].fillColor = [-1,-1,-1]
                respLabels[resp].color = [1,1,1]
                break

        mouse.setVisible(0)

    partnerShape.setAutoDraw(False)

    if partner in ['pos', 'neg']:
        results = pd.concat([results_1, results_2, results_3])
    else:
        results = pd.concat([results_1, results_2])

    # save output file if saveFile provided
    # if saveFile is not None:
    #     results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)
    return results


def deceptionQs(win=None, saveFile=None, scaleName="deceptionQs", subjNum=0, endPause=1.0):
    """ Questions about deception for after funnel debriefing

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["You will now be asked a few brief questions. These are similar to the ones the experimenter just asked you.\n\nPlease provide your honest answers to the following questions about your thoughts DURING the experiment."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(5):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-5
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-5

    secondaryLabels = ["Not at all", "", "", "", "", "Completely"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.20, win=win, bold=True)

    # run scale
    results = qs.run_scale_items(win=win,
    scaleItems=["Did you believe that your partners were actual people?",
    "Did you believe that you and your partners would be paid according to your choices?",
    "Did you believe that your partner faced the risk of having to holding a hand in the ice water again after the experiment?",
    "Did you believe that you were seeing your partner's real choices at the beginning of the experiment?"],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)



def taskStrategyQs(win=None, saveFile=None, scaleName="taskStrategyQs", subjNum=0, endPause=1.0):
    """ Questions about task strategy

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["The following questions are about how you completed the task."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(7):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-5
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-5

    secondaryLabels = ["Not at all", "", "", "", "", "", "Extremely"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.20, win=win, bold=True)

    # run scale
    results = qs.run_scale_items(win=win,
    scaleItems=["To what extent did you rely on your gut feelings to make your decisions?",
    "To what extent did you try to use mathematical reasoning to make your decisions?",
    "To what extent did you feel conflicted when making your decisions?",
    "To what extent did you feel like you needed to exert self-control to not be selfish?",
    "To what extent did you carefully consider each proposal?",
    "To what extent did you try to think through all the options fully?",
    "To what extent did your choices on previous trials influence your choices on later trials?",
    "To what extent did you try to make the choice that would be the most fair for both you and your partner?"],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)



# ============================================================================ #
# RUN EXPERIMENT

gf.show_instructs(win=win, text=["Now we have a few quick questions for you about the task you just completed.",
    "The following are questions about your decisions with each of your partners."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], saveFile=os.path.join(saveDir, "instructs0_.png"), units='pix')

partners = ['pos', 'neu', 'neg']
random.shuffle(partners)

partnerQs_1 = partnerTaskQuestions(win=win, partner=partners[0])
partnerQs_2 = partnerTaskQuestions(win=win, partner=partners[1])
partnerQs_3 = partnerTaskQuestions(win=win, partner=partners[2])
partnerQs = pd.concat([partnerQs_1, partnerQs_2, partnerQs_3])

partnerQs.to_csv(os.path.join(saveDir, "%04d_%s_%s_%s.csv") %(int(expInfo['subject']), expInfo['startTime'], expInfo['expName'], 'partnerQs'),
    header = True, mode = 'w', index = False)

taskStrategyQs(win=win, subjNum=expInfo['subject'], saveFile=os.path.join(saveDir, "%04d_%s_%s_%s.csv") %(int(expInfo['subject']), expInfo['startTime'], expInfo['expName'], 'taskStrategyQs'))

gf.show_instructs(win=win, text=["Next we have a few brief questionnaires."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], saveFile=os.path.join(saveDir, "instructs0_.png"), units='pix')

qs.dirtyDozen(win=win, subjNum=expInfo['subject'], saveFile=os.path.join(saveDir, "%04d_%s_%s_%s.csv") %(int(expInfo['subject']), expInfo['startTime'], expInfo['expName'], 'dirtyDozen'))
qs.compassionateSelfImageGoals_general(win=win, subjNum=expInfo['subject'], saveFile=os.path.join(saveDir, "%04d_%s_%s_%s.csv") %(int(expInfo['subject']), expInfo['startTime'], expInfo['expName'], 'csigg'))

taskStrategy = qs.openResp(win=win, text="How did you make your choices while completing this task? For example, did you use any choice rules such as 'Always accept proposals of a certain type'? Describe any strategies you used by typing your response.", subjNum=expInfo['subject'])
hypothesisGuess = qs.openResp(win=win, text="What do you think this study has been about? Type your response.", subjNum=expInfo['subject'])
confusing = qs.openResp(win=win, text="Please share any thoughts or reactions you had while completing the study. Your feedback helps us when designing future studies. For example, did you find any parts confusing or awkward?", subjNum=expInfo['subject'])

openResponseQs = pd.concat([taskStrategy, hypothesisGuess, confusing])
openResponseQs.to_csv(os.path.join(saveDir, "%04d_%s_%s_%s.csv") %(int(expInfo['subject']), expInfo['startTime'], expInfo['expName'], 'openResponseQs'), header = True, mode = 'w', index = False)

qs.howSerious(win=win, subjNum=expInfo['subject'], saveFile=os.path.join(saveDir, "%04d_%s_%s_%s.csv") %(int(expInfo['subject']), expInfo['startTime'], expInfo['expName'], 'howSerious'))

# pause for funnel debriefing
gf.show_instructs(win=win,
    text=["You have completed the experiment.\n\nPlease let the experimenter know."],
    timeAutoAdvance=0, timeRequired=0, secretKey=['p'])

deceptionQs(win=win, subjNum=expInfo['subject'], saveFile=os.path.join(saveDir, "%04d_%s_%s_%s.csv") %(int(expInfo['subject']), expInfo['startTime'], expInfo['expName'], 'deceptionQs'))

gf.show_instructs(win=win,
    text=["You're all done!"],
    timeAutoAdvance=0, timeRequired=0, secretKey=['p'])

win.close()
core.quit()
