#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
General PsychoPy Experiment Functions
authors: Ian Roberts
"""

import random, os, time
from psychopy import visual, core, event, data, gui, logging
import pandas as pd
import numpy as np
# import smtplib
#
# def send_email(from_addr, to_addr_list, #cc_addr_list,
#               subject, message,
#               login, password,
#               host='smtp.gmail.com',
#               port=587):
#     header  = 'From: %s' %(from_addr)
#     header += 'To: %s' %(','.join(to_addr_list))
#     #header += 'Cc: %s' %(','.join(cc_addr_list))
#     header += 'Subject: %s' %(subject)
#     message = header + message
#
#     print "set info"
#     server = smtplib.SMTP(host, port)
#     print "server"
#     server.starttls()
#     print "tls"
#     server.login(login,password)
#     print "logged in"
#     problems = server.sendmail(from_addr, to_addr_list, message)
#     print "sent"
#     server.quit()
#     print "quit"


def subject_info(entries=['subject'], debug=False, debugValues=[9999], expName=None, expVersion=None, counterbalance=1):
    """ Function for dialogue box for entering subject information at start of experiment

        Args:
            entries (list/str): List of inputs to prompt in the dialogue box.
            debug (True/False): Whether to run in debug mode. In debug mode, default values are entered each entry.
            debugValues (list): List of values to enter for each entry when in debug mode.
            expName (str): Name of the experiment.
            expVersion (float): Version of the experiment.
            counterbalance (integer): How many counterbalance groups there are. Subjects are assigned to group based on modulus of subject number.
    """
    expInfo = {}  # create empty dictionary to store GUI responses

    if debug:  # if in DEBUG mode
        if len(entries) != len(debugValues):  # if each entry is not given a default debug value, quit
            core.quit()
        else:
            for i in range(len(entries)):  # fill entries with debug values
                expInfo.update({entries[i] : debugValues[i]})

    else: #if not in DEBUG mode
        for i in range(len(entries)):  # initialize entries
            expInfo.update({entries[i] : ''})
        dlg = gui.DlgFromDict(expInfo)  # create a dialogue box (function gui)
        if not dlg.OK:  # if dialogue response is NOT OK, quit
            core.quit()

    expInfo['subject'] = int(expInfo['subject'])
    expInfo['expVersion'] = expVersion  # enter experiment version
    expInfo['expName'] = expName  # enter experiment name
    expInfo['startTime'] = str(time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime()))  # create str of current date/time
    expInfo['endTime'] = ''  # initialize ending time to be saved later on

    counterbalance = int(counterbalance)
    if counterbalance > 1:
        expInfo['counterbalance'] = expInfo['subject'] % counterbalance

    return expInfo



def load_images(imagesDir=None, subDir=None, fileType=".jpg", randomize=True, setSeed=None, collapseSubDirs=False):
    """ Function for loading a folder(s) of image files

        Args:
            imagesDir (str): Filepath for parent images directory.
            subDir (list/str): List of subdirectories within the parent directory containing images to load. If there are subdirectoris a dictionary will be output.
            fileType (str): File type to match within directories.
            randomize (True/False): Whether to randomly order the images. If there are subdirectories, this will be done within subdirectory unless collapseSubDirs is True.
            setSeed (int): Set seed for randomization.
            collapseSubDirs (True/False): If True, subdirectories of images are combined into a single list. If False, subdirectory separations are maintained and a dictionary will be output.
    """
    if imagesDir is not None:  # check whether an image directory is provided
        imagesDir = os.path.join(os.getcwd(), imagesDir)  # do not include "/" at beginning or end of imagesDir
    else:  # if no image directory provided, use current working directory
        imagesDir = os.getcwd()

    images = []  # initialize list for images

    if subDir is not None:  # check whether subdirectories were provided
        imagesDict = {}  # initialize dictionary for image subdirectories

        # load image files from each subdirectory into lists
        for i in range(len(subDir)):
            currDir = os.path.join(imagesDir, subDir[i])
            imageFiles = os.listdir(currDir)
            selectedImageFiles = []
            for imageFile in imageFiles:
                if imageFile.lower().endswith(fileType):
                    selectedImageFiles.append(os.path.join(currDir, imageFile))

            temp = {}
            temp['image'] = selectedImageFiles
            temp['imgCond'] = subDir[i]
            imagesDict[subDir[i]] = pd.DataFrame.from_dict(temp)

        if collapseSubDirs:  # if True, collapse images from different subdirectories into one list
            images = pd.concat(imagesDict, ignore_index=True)
        else:  # else, maintain separation and return a dictionary
            images = imagesDict

    else:
        # load image files from directory into list
        for imageFile in os.listdir(imagesDir):
            if imageFile.lower().endswith(fileType):
                images.append(imagesDir + os.path.sep + imageFile)

    if randomize:  # if True, randomly sort order of images
        if setSeed is not None:  # set seed if there is one
            random.seed(setSeed)

        if isinstance(images, pd.DataFrame):  # if the images are in a list, randomize within the list
            images = images.reindex(np.random.permutation(images.index))
            images = images.reset_index(drop=True)
        elif isinstance(images, dict):  # if the images a separated by subdirectory, randomize within subdirectory
            for i in subDir:
                images[i] = images[i].reindex(np.random.permutation(images[i].index))
                images[i] = images[i].reset_index(drop=True)

    return images


def spacer(items=5, space=0.8, horiz=True, anchor=0.5, offset=0, units="norm"):
    """ Function for creating evenly spaced coordinates

        Args:
            items (int or list): The number of coordinates to produce. Can be a single integer or a list (length of list will be used).
            space (float): The space for the coordinates to span.
            horiz (True/False): If true, the coordinates will organized left to right. If false, they will be organized top to bottom.
            anchor (float): The coordinate for the stationary axis. (y-axis if horizontal; x-axis if vertical)
            offset (float): Where to center the coordinates (shifts right/up if positive; left/down if negative)
    """
    # convert items to length of list if given a list
    if isinstance(items, list):
        items = len(items)

    positions = []  # initialize list for positions
    final_coord = []  # initialize list for final coordinates

    if units == "norm" and abs(space) > 1:  # limit scale width to 1
        space = 1
    space = abs(space)  # prevent negative scale widths

    if items % 2 == 1:  # check if number of items is odd
        midPoint = (items + 1) / 2  # find mid point
        sidePoints = (items - 1) / 2  # calculate number of points on each side of midpoint

        spacing = space / sidePoints  # calculate even spacing for points

        positions = range((-1 * sidePoints), (sidePoints + 1))  # generate values to be multiplied by spacing

        for i in range(len(positions)):
            positions[i] *= spacing  # calculate positions

    else:  # else, the number of items is even
        sidePoints = items / 2  # calculate number of points on each side of midpoint

        spacing = space / ((sidePoints - 0.5) * 2)  # calculate even spacing for points; has to be half because of spacing around middle of screen

        positions = range((-1 * sidePoints), (sidePoints + 1))  # generate values to be multiplied by spacing
        positions.remove(0)  # remove 0 since no response option with be at the center of the screen

        for i in range(len(positions)):
            if i not in [(sidePoints - 1), sidePoints]:  # calculate points for options NOT adjacent to center of screen
                if positions[i] < 0:  # for points on left side of screen
                    positions[i] = (positions[i] + 1) * 2 * spacing
                    positions[i] -= spacing
                elif positions[i] > 0:  # for points on right side of screen
                    positions[i] = (positions[i] - 1) * 2 * spacing
                    positions[i] += spacing
            else:
                positions[i] *= spacing  # calculate points for options adjacent to center of screen

    # shift coordinates if there is an offset
    if offset != 0:
        for i in range(len(positions)):
            positions[i] += offset

    # add anchor to generate full coordinates
    if horiz:
        for i in range(len(positions)):
            final_coord.append((positions[i], anchor))
    elif not horiz:
        for i in range(len(positions)):
            final_coord.insert(0, (anchor, positions[i]))

    return final_coord


def generate_resp_scale(respKeys=None, primaryLabels=None, secondaryLabels=None, respFont='Arial', respColor=(1,1,1), scaleWidth=0.8, primaryPos=-0.8, secondaryPos=-0.7, primaryHeight=None, secondaryHeight=None, secondaryWrapWidth=0.5, secondaryAlign='center', win=None, bold=False, italic=False, horiz=True, offset=0, units="norm"):
    """ Function for generating a response scale to display

        Args:
            respKeys [list]: A list of the keys that subjects will use to respond.
            primaryLabels [list/str]: A list of the primary labels to use for each data point in the scale (often these are numbers).
            secondaryLabels [list/str]: A list of the secondary labels to use for the scale (e.g., anchor end-point labels).
            respFont [str]: Font to use for response scale.
            respColor [list/tuple]: Color for text.
            scaleWidth [float]: Value for how broadly spaced the response options should be.
            primaryPos [float]: Value for the position of the primary labels. Whether this moves the scale along the y- or x-axis depends on whether the scale is arranged horizontally or vertically (see horiz argument).
            secondaryPos [float]: Value for the position of the secondary labels. Whether this moves the scale along the y- or x-axis depends on whether the scale is arranged horizontally or vertically (see horiz argument).
            primaryHeight [float]: Size of primary labels.
            secondaryHeight [float]: Size of secondary labels.
            secondaryWrapWidth [float]: Width at which to wrap text for secondary labels.
            secondaryAlign [str]: Alignment for secondary label text (left, center, or right).
            win [visual.Window object]: Provide the window object to use.
            bold [True/False]: Whether to bold text.
            italic [True/False]: Whether to italicize text.
            horiz [True/False]: If True, scale is arranged horizontally. If False, scale is arrange vertically.
            offset [float]: Where to center the coordinates (shifts right/up if positive; left/down if negative).
    """
    respPositions = spacer(items=respKeys, space=scaleWidth, horiz=horiz, anchor=primaryPos, offset=offset, units=units)

    if respKeys is not None:
        respStim = {}  # initialize dictionary for response stimuli
        for i in range(len(respKeys)):  # generate TextStim for each response option
            respStim[respKeys[i]] = visual.TextStim(win=win, text=primaryLabels[i], font=respFont, pos=respPositions[i], colorSpace='rgb', color=respColor, bold=bold, italic=italic, height=primaryHeight, units=units)

        if secondaryLabels is not None:
            secondaryRespPositions = spacer(items=secondaryLabels, space=scaleWidth, horiz=horiz, anchor=secondaryPos, offset=offset, units=units)
            for i in range(len(secondaryLabels)):  # generate TextStim for each label
                if secondaryLabels[i] != "":  # if label is blank, don't create TextStim object
                    respStim["label" + str(i+1)] = visual.TextStim(win=win, text=secondaryLabels[i], alignHoriz=secondaryAlign, font=respFont, pos=secondaryRespPositions[i], wrapWidth=secondaryWrapWidth, colorSpace='rgb', color=respColor, bold=bold, italic=italic, height=secondaryHeight, units=units)
    else:
        respStim = []
        for i in range(len(primaryLabels)):  # generate TextStim for each response option
            respStim[i] = visual.TextStim(win=win, text=primaryLabels[i], font=respFont, pos=respPositions[i], colorSpace='rgb', color=respColor, bold=bold, italic=italic, height=primaryHeight, units=units)

    return respStim


def show_instructs(win, text, timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], secretKey=None, textPos=None, textHeight=None, advanceHeight=None, advancePos=None, wrapWidth=None, image=None, imageDim=(500,500), scaleImage=1.0, imagePos=(0,-0.5), units="norm", saveFile=None):
    ''' Display task instructions

        Args:
            text (list/str): Provide a list with instructions/text to present. One list item will be presented per page. Alternatively, provide a string filepath to a text file containing one line per screen.
            timeAutoAdvance (float): The time in seconds to wait before advancing automatically.
            timeRequired (float): The time in seconds to wait before showing 'Press space to continue' text.
    '''
    event.clearEvents()

    if units == "norm":
        if textPos is None:
            textPos=(0.0,0.5)
        if textHeight is None:
            textHeight=0.08
        if advanceHeight is None:
            advanceHeight=0.1
        if advancePos is None:
            advancePos=(0,-0.85)
        if wrapWidth is None:
            wrapWidth=1.4
    elif units == "pix":
        if textPos is None:
            textPos=(0,200)
        if textHeight is None:
            textHeight=40
        if wrapWidth is None:
            wrapWidth=1000
        if advanceHeight is None:
            advanceHeight=40
        if advancePos is None:
            advancePos=(0,-400)

    advanceKeyText = ''
    if len(advanceKey) > 1:
        advanceKeyText = 'any button'
    else:
        advanceKeyText = advanceKey[0]

    # "Continue" text displayed at the bottom of each screen
    continueInstruct = 'Press ' + advanceKeyText + ' to continue'
    continueText = visual.TextStim(win=win, units=units, colorSpace='rgb', color=(1,1,1), font='Arial', text=continueInstruct, height=advanceHeight, wrapWidth=wrapWidth, pos=advancePos)

    # instructions to be shown
    instructText = visual.TextStim(win=win, units=units, colorSpace='rgb', color=(1,1,1), font='Arial', text='', height=textHeight, wrapWidth=wrapWidth, pos=textPos)

    if image is not None:
        instructImage = visual.ImageStim(win=win, image=image, pos=imagePos, units='pix', size=(imageDim[0]*scaleImage, imageDim[1]*scaleImage))
        instructImage.setAutoDraw(True)

    textLines = []
    if isinstance(text, basestring):  # if text is string, it's a file path
        with open(text, 'r') as instructs:
            textLines = [line.strip().decode('unicode-escape') for line in instructs]
    elif isinstance(text, list):  # if text is a list, it's a strings to be used directly
        textLines = text

    for i in range(len(textLines)):  # for each item/page in the text list
        instructText.text = textLines[i]  # set text for each page
        if timeAutoAdvance == 0 and timeRequired == 0 and secretKey is None:
            noResp = True
            while noResp: #not event.getKeys(keyList = advanceKey):
                keysPressed = event.getKeys(keyList = advanceKey + ['escape'])
                if len(keysPressed) > 0:
                    if keysPressed[0] in advanceKey:
                        noResp = False
                    elif keysPressed[0] == 'escape':
                        win.close()
                        core.quit()
                continueText.draw()
                instructText.draw()
                win.flip()
        elif timeAutoAdvance != 0 and timeRequired == 0 and secretKey is None:
            # clock to calculate how long to show instructions
            # if timeAutoAdvance is not 0 (e.g., 3), then each page of text will be shown 3 seconds and will proceed AUTOMATICALLY to next page
            instructTimer = core.Clock()
            while instructTimer.getTime() < timeAutoAdvance:
                instructText.draw()
                win.flip()
        elif timeAutoAdvance == 0 and timeRequired != 0 and secretKey is None:
            instructTimer = core.Clock()
            while instructTimer.getTime() < timeRequired:
                instructText.draw()
                win.flip()
            event.clearEvents()  # clear events to ensure if participants press space before 'press space to continue' text appears, their response won't be recorded
            noResp = True
            while noResp: #not event.getKeys(keyList = advanceKey):
                keysPressed = event.getKeys(keyList = advanceKey + ['escape'])
                if len(keysPressed) > 0:
                    if keysPressed[0] in advanceKey:
                        noResp = False
                    elif keysPressed[0] == 'escape':
                        win.close()
                        core.quit()
                continueText.draw()
                instructText.draw()
                win.flip()
            win.flip()
        elif secretKey is not None:
            noResp = True
            while noResp: #not event.getKeys(keyList = advanceKey):
                keysPressed = event.getKeys(keyList = secretKey + ['escape'])
                if len(keysPressed) > 0:
                    if keysPressed[0] in secretKey:
                        noResp = False
                    elif keysPressed[0] == 'escape':
                        win.close()
                        core.quit()
                instructText.draw()
                win.flip()
    #     if saveFile is not None:
    #         win.getMovieFrame()
    #
    # if saveFile is not None:
    #     win.saveMovieFrames(saveFile)

    if image is not None:
        instructImage.setAutoDraw(False)



def task_quiz(win, quizFile, subjNum, scaleWidth=200):
    ''' Display quiz over task instructions. Returns dataframe of results.

        Args:
            win [visual.Window object]: Provide the window object to use.
            quizFile [file path string]: File path to csv file. File should have columns titled "question", "correctAns", and for the answers (i.e., "ans1", "ans2", etc.).
            subjNum [int]: Subject's ID number
    '''
    quizDf = pd.read_csv(quizFile)  # read in quiz csv file
    quizDf['subject'] = subjNum  # add column for subject number
    quizDf['incorrectResps'] = np.nan  # add column for recording number of incorrect responses

    nAns = len(quizDf.filter(regex='ans').columns)  # max number of answer alternatives

    questionText = visual.TextStim(win=win, units='pix', colorSpace='rgb', color=(1,1,1), font='Arial', text='', height=50, wrapWidth=1200, pos=(0, 300))

    respKeys = [str(i+1) for i in range(nAns)]  # create same number of response keys as max answers
    primaryLabels = [str(i) for i in respKeys]  # make primary labels number of response keys
    secondaryLabels = ["answer " + str(i+1) for i in range(nAns)]  # make secondary labels the possible answers
    ansOptions = generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels, scaleWidth=scaleWidth, primaryPos=-500, secondaryPos=-350, primaryHeight=60, secondaryHeight=35, secondaryAlign='left', secondaryWrapWidth=1000, offset=-100, win=win, horiz=False, units='pix')

    # display quiz instructions
    show_instructs(win=win, text=["Use the number keys to provide your answers. You must get each question correct before you can continue.\n\nPlease let the experimenter know if you have any questions."], timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], textPos=(0,200), units='pix')

    for i, thisQuestion in quizDf.iterrows():  # run each quiz question

        questionText.text = quizDf.loc[i, "question"]  # set quiz question text

        for ansN in range(len(secondaryLabels)):  # set text for quiz answers
            ansOptions["label" + str(ansN+1)].text = quizDf.loc[i, "ans" + str(ansN+1)]

        questionText.setAutoDraw(True)
        for ansOption in ansOptions:
            ansOptions[ansOption].setAutoDraw(True)

        event.clearEvents()
        correctResp = False
        incorrectResps = 0

        while not correctResp:
            win.flip()

            keysPressed = event.getKeys(keyList=respKeys)

            if len(keysPressed) > 0:  # check if a key in the response keys list has been pressed
                keyResp = keysPressed[0]  # collect first key press

                if keyResp == str(quizDf.loc[i, 'correctAns']):
                    ansOptions[keyResp].color = (-1,-0.2,1)  # change the selected response's color to indicate key press to the subject
                    ansOptions["label" + keyResp].color = (-1,-0.2,1)
                    correctResp = True
                elif keyResp != str(quizDf.loc[i, 'correctAns']):
                    ansOptions[keyResp].color = (1,-1,-1)  # change the selected response's color to indicate key press to the subject
                    ansOptions["label" + keyResp].color = (1,-1,-1)
                    incorrectResps += 1

                win.flip()
                core.wait(0.5)

                ansOptions[keyResp].color = (1,1,1)  # change back selected response's color
                ansOptions["label" + keyResp].color = (1,1,1)  # change back selected response's color
                event.clearEvents()

        questionText.setAutoDraw(False)
        for ansOption in ansOptions:
            ansOptions[ansOption].setAutoDraw(False)

        quizDf.loc[i, 'incorrectResps'] = incorrectResps  # record number of incorrect responses

        if incorrectResps > 0 and 'explain' in quizDf.columns:
            # if they gave a wrong answer and there is an explanation available
            show_instructs(win=win, text=['Explanation:\n\n' + quizDf.loc[i, 'explain']], timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], units='pix')

    return quizDf
