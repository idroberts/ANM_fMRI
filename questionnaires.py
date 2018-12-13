#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Questionnaires
authors: Ian Roberts

List of questionnaires:
    Affect Intensity Measure (Larsen & Deiner, 1987) -- affectIntensityMeasure
    Aggression Questionnaire (Buss & Perry, 1992) -- aggressionQuestionnaire
    Anger Rumination Scale (Sukhodolsky et. al, 2001) -- angerRuminationScale
    Attentional Control Scale (ACS; Derryberry & Reed, 2002) -- attentionalControlScale
    Barratt Impulsiveness Scale (BIS; Barratt et. al, 1995) -- barrattImpulsivenessScale
    Big Five Aspects Scale (DeYoung et al., 2007) -- bigFiveAspectsScale
    BIS/BAS (Carver & White, 1994) -- bisBas
    Center for Epidemiologic Studies Depression Scale – Revised (CESD-R; Eaton et al., 2004) -- centerForEpidemiologicStudiesDepressionScale
    Childhood Trauma Questionnaire (CTQ; Bernstein & Fink, 1997) -- childhoodTraumaQuestionnaire
    Compassionate and Self-Image Goals Scale (Crocker & Canevello, 2008) -- compassionateSelfImageGoals_friends
    The Dirty Dozen (Jonason & Webster, 2010) -- dirtyDozen
    Displaced Aggression Questionnaire (Denson et. al, 2006) -- displacedAggressionQuestionnaire
    Emotion Regulation Questionnaire (Gross & John, 2003) -- emotionRegulationQuestionnaire
    Extreme Valuing of Happiness Scale (Mauss et al., 2011) -- extremeValuingOfHappinessScale
    Eysenck Personality Questionnaire - Revised Short Scale (Eysenck et al., 1985) -- eysenckPersonalityQuestionnaireRevisedShortScale
    Highly Sensitive Persons Scale (HSP; Aron & Aron, 1997) -- highlySensitivePersonsScale
    Implicit Self-Theories Scale (Dweck, 1999) -- implicitSelfTheories
    Interpersonal Reactivity Index (IRI; Davis, 1980) -- interpersonalReactivityIndex
    Intolerance of Uncertainty Scale - Short Form (Carelton et. al, 2007) -- intoleranceOfUncertaintyScale
    Levenson Self-Report Psychopathy (LSRP; Levenson et. al, 1995) -- levensonSelfReportPsychopathy
    Mindful Attention Awareness Scale (MAAS; Brown & Ryan, 2003) -- mindfulAttentionAwarenessScale
    State Positive and Negative Affect Schedule (PANAS; Watson et al., 1988) -- statePANAS
    Personality Assessment Inventory – Borderline Features (PAI-BOR; Morey, 1991) -- personalityAssessmentInventoryBorderlineFeatures
    Prioritizing Happiness Scale (Catalino et al., 2014) -- prioritizingHappinessScale
    Range and Differentiation of Emotional Experience Scale (RDEES; Kang & Shaver, 2004) -- rangeAndDifferentiationOfEmotionalExperienceScale
    Rational Experiential Inventory (REI; Pancini & Epstein, 1999) -- rationalExperientialInventory
    Religious Fundamentalism Scale -- Revised (Altemeyer & Hunsberger, 2004) -- religiousFundamentalismScale
    State Trait Anger Expression Inventory - 2 -- Anger Expression (Spielberger, 1999) -- staxi2AngerExpression
    State Trait Anger Expression Inventory - 2 -- State Anger (Spielberger, 1999) -- staxi2StateAnger
    State Trait Anger Expression Inventory - 2 -- Trait Anger (Spielberger, 1999) -- staxi2TraitAnger
    State Trait Anxiety Inventory - State Anxiety (Spielberger et al., 1983) -- staiStateAnxiety
    Toronto Alexithymia Scale (TAS; Parker et al., 2001) -- torontoAlexithymiaScale
"""

import random, os, time, sys
from psychopy import visual, core, event, data, gui, logging
import pandas as pd
import numpy as np
sys.path.append("/Users/ianroberts/Dropbox/research_projects/0e_task_scripts/")
import generalFunctions as gf


#==============================================================================#
# GENERAL FUNCTIONS TO HELP RUN QUESTIONNAIRES

def run_scale_items(win, scaleItems, respScale, respKeys, scaleName, subjNum, height=None, pos=None, wrapWidth=None, units='norm'):
    """ Function for displaying scale items with response scales

        Args:
            win [visual.Window object]: Provide the window object to use.
            scaleItems [list/str]: Provide a list with scale items to present. One list item will be presented per screen.
            respScale [dictionary]: Provide the response scale dictionary created with the generate_resp_scale function.
            respKeys [list]: List of keys that participants can use.
    """

    if units == "norm":
        if pos is None:
            pos=(0.0,0.5)
        if height is None:
            height=0.08
        if wrapWidth is None:
            wrapWidth=1.4
    elif units == "pix":
        if pos is None:
            pos=(0,200)
        if height is None:
            height=40
        if wrapWidth is None:
            wrapWidth=1000

    dataColumns = ['subject', 'item', 'question', 'resp']  # names of columns for output DataFrame
    dataOutput = pd.DataFrame(index=range(len(scaleItems)), columns=dataColumns)  # create dataframe with column names and a row for each scale item
    dataOutput['subject'] = subjNum  # set subject number in dataframe

    event.clearEvents()
    # create text stimulus object for displaying scale items
    itemText = visual.TextStim(win=win, units=units, colorSpace='rgb', color=(1,1,1), font='Arial', text='', height=height, wrapWidth=wrapWidth, pos=pos)

    for i in range(len(scaleItems)):  # loop through all scale items
        dataOutput.loc[i, 'item'] = scaleName + "_" + str(i + 1)  # label scale item with scale name abbreviation and number
        dataOutput.loc[i, 'question'] = scaleItems[i]  # record text of the item that is displayed

        event.clearEvents()  # clear keyboard events
        itemText.text = scaleItems[i]  # set text to current scale item for display

        # draw scale item and response options to screen
        itemText.setAutoDraw(True)
        for respOption in respScale:
            respScale[respOption].setAutoDraw(True)

        selectedResp = None

        # display item until subject has selected a response
        while selectedResp is None:
            win.flip()

            keysPressed = event.getKeys(keyList=respKeys)

            if len(keysPressed) > 0:  # check if a key in the response keys list has been pressed
                keyResp = keysPressed[0]  # collect first key press
                selectedResp = respScale[keyResp].text  # collect the response that was selected
                respScale[keyResp].color = (-1,1,-1)  # change the selected response's color to indicate key press to the subject
                win.flip()

                core.wait(0.5)  # pause to display color change

                respScale[keyResp].color = (1,1,1)  # change back selected response's color

        dataOutput.loc[i, 'resp'] = selectedResp  # record subject's response in the dataframe

    # turn off scale item and response options
    itemText.setAutoDraw(False)
    for respOption in respScale:
        respScale[respOption].setAutoDraw(False)

    return dataOutput  # return dataframe of questionnaire responses


def run_multi_response(win, scaleItems, respScale, respKeys, scaleName, subjNum, submitKey="space"):
    """ Function for collecting multiple responses for a single item (e.g., race)

        Args:
            win [visual.Window object]: Provide the window object to use.
            scaleItems [list/str]: Provide a list with scale items to present. One list item will be presented per screen.
            respScale [dictionary]: Provide the response scale dictionary created with the generate_resp_scale function.
            respKeys [list]: List of keys that participants can use.
            submitKey [str]: Key to be used for submitting response.
    """

    respKeys.append(submitKey)  # append the submit response key to the available response keys

    dataColumns = ['subject', 'item', 'question', 'resp']  # names of columns for output DataFrame
    dataOutput = pd.DataFrame(index=range(len(scaleItems)), columns=dataColumns)  # create dataframe with column names and a row for each scale item
    dataOutput['subject'] = subjNum  # set subject number in dataframe

    event.clearEvents()

    # create text stimulus object for displaying scale items
    itemText = visual.TextStim(win=win, units='norm', colorSpace='rgb', color=(1,1,1), font='Arial', text='', height=0.08, wrapWidth=1.4, pos=(0.0, 0.8))
    continueText = visual.TextStim(win=win, units='norm', colorSpace='rgb', color=(1,1,1), font='Arial', text="Press " + submitKey.upper() + " to submit response", height=0.08, wrapWidth=1.4, pos=(0.0, -0.85))

    for i in range(len(scaleItems)):  # loop through all scale items

        if len(scaleItems) == 1:
                dataOutput.loc[i, 'item'] = scaleName  # label scale item with scale name abbreviation
        else:
            dataOutput.loc[i, 'item'] = scaleName + "_" + str(i + 1)  # label scale item with scale name abbreviation and number

        dataOutput.loc[i, 'question'] = scaleItems[i]  # record text of the item that is displayed

        event.clearEvents()  # clear keyboard events
        itemText.text = scaleItems[i]  # set text to current scale item for display

        # draw scale item and response options to screen
        itemText.setAutoDraw(True)
        continueText.setAutoDraw(True)
        for respOption in respScale:
            respScale[respOption].setAutoDraw(True)

        endResp = False
        selectedOptions = []

        # display item until subject has selected a response
        while endResp is False:
            win.flip()

            keysPressed = event.getKeys(keyList=respKeys)

            if len(keysPressed) > 0:  # check if a key in the response keys list has been pressed
                keyResp = keysPressed[0]  # collect first key press
                if keyResp != submitKey:
                    if respScale["label" + keyResp].text not in selectedOptions:  # if this response is not currently "on"
                        selectedOptions.append(respScale["label" + keyResp].text)  # collect the response that was selected
                        respScale[keyResp].color = (-1,1,-1)  # change the selected response's color to indicate key press to the subject
                        respScale["label" + keyResp].color = (-1,1,-1)
                        win.flip()
                    elif respScale["label" + keyResp].text in selectedOptions:  # if this response is currently "on"
                        selectedOptions.remove(respScale["label" + keyResp].text)  # un-collect the response that was selected
                        respScale[keyResp].color = (1,1,1)  # change the selected response's color to indicate key press to the subject (change back to white)
                        respScale["label" + keyResp].color = (1,1,1)
                        win.flip()
                else:
                    endResp = True

        for respOption in respScale:
            respScale[respOption].color = (1,1,1)  # change back selected response's color

        dataOutput.set_value(i, 'resp', selectedOptions)  # record subject's response in the dataframe

    # turn off scale item and response options
    itemText.setAutoDraw(False)
    continueText.setAutoDraw(False)
    for respOption in respScale:
        respScale[respOption].setAutoDraw(False)

    return dataOutput  # return dataframe of questionnaire responses


def openResp(win, text="", submitKey='return', subjNum=0):

    instructText = visual.TextStim(win=win, units='norm', colorSpace='rgb', color=(1,1,1), font='Arial', text='', height=0.08, wrapWidth=1.4, pos=(0.0, 0.8))
    textFeedback = visual.TextStim(win=win, units='norm', colorSpace='rgb', color=(1,1,1), font='Arial', text='', height=0.05, wrapWidth=1.4, pos=(-0.7, 0.5), alignHoriz="left", alignVert="top")

    continueInstruct = 'Press ' + submitKey + ' to submit your response'
    continueText = visual.TextStim(win=win, units='norm', colorSpace='rgb', color=(1,1,1), font='Arial', text=continueInstruct, height=0.08, wrapWidth=1.4, pos=(0.0, -0.85))

    instructText.text = text

    instructText.setAutoDraw(True)
    continueText.setAutoDraw(True)
    textFeedback.setAutoDraw(True)

    inputText = ""
    respSubmitted = False
    shift_flag = False
    keysPressed = ""

    while not respSubmitted:
        keysPressed = event.getKeys()

        i = 0
        n = len(keysPressed)

        while i < n:

            if keysPressed[i] == submitKey:
                respSubmitted = True
                break
            elif keysPressed[i] in ['backspace','delete']:
                inputText = inputText[:-1]  # lose the final character
                i = i + 1
            elif keysPressed[i] == 'space':
                inputText += ' '
                i = i + 1
            elif keysPressed[i] in ['lshift','rshift']:
                shift_flag = True
                i = i + 1
            else:
                if len(keysPressed[i]) == 1:
                    # we only have 1 char so should be a normal key,
                    # otherwise it might be 'ctrl' or similar so ignore it

                # THE shift-lock
                    if shift_flag:
                        if ord(keysPressed[i]) in range (97,123):
                            inputText += chr( ord(keysPressed[i]) - ord(' '))
                            shift_flag = False
                    # shift 1345 to !#$%
                        elif ord(keysPressed[i]) in [49,51,52,53]:
                            inputText += chr( ord(keysPressed[i]) - ord('\x10'))
                            shift_flag = False
                    # 79 to &(
                        elif ord(keysPressed[i]) in [55,57]:
                            inputText += chr( ord(keysPressed[i]) - ord('\x11'))
                            shift_flag = False
                    # 8 to *
                        elif keysPressed[i] == '8':
                            inputText += '*'
                            shift_flag = False
                    # 0 to )
                        elif keysPressed[i] == '0':
                            inputText += ')'
                            shift_flag = False
                    # 2 to @
                        elif keysPressed[i] == '2':
                            inputText += '@'
                            shift_flag = False
                    # 6 to ^ should have worked but no, always output &
                        elif keysPressed[i] == '6':
                            inputText += '^'
                            shift_flag = False
                    else:
                        inputText += keysPressed[i]

                else:
                    if shift_flag:
                        # shift special characters
                        if keysPressed[i] == 'period':
                            inputText += '>'
                            shift_flag = False
                        elif keysPressed[i] == 'comma':
                            inputText += '<'
                            shift_flag = False
                        elif keysPressed[i] == 'slash':
                            inputText += '?'
                            shift_flag = False
                        elif keysPressed[i] == 'semicolon':
                            inputText += ':'
                            shift_flag = False
                        elif keysPressed[i] == 'apostrophe':
                            inputText += '"'
                            shift_flag = False
                        elif keysPressed[i] == 'grave':
                            inputText += '~'
                            shift_flag = False
                    else:
                        #handle spaces, print special characters when no shift
                        if keysPressed[i] == 'period':
                            inputText += '.'
                            i = i + 1
                        elif keysPressed[i] == 'comma':
                            inputText += ','
                            i = i + 1
                        elif keysPressed[i] in ['slash','num_divide']:
                            inputText += '/'
                            i = i + 1
                        elif keysPressed[i] == 'semicolon':
                            inputText += ';'
                            i = i + 1
                        elif keysPressed[i] == 'apostrophe':
                            inputText += '\''
                            i = i + 1
                        elif keysPressed[i] == 'grave':
                            inputText += '`'
                            i = i + 1
                i = i + 1

        textFeedback.setText("" + inputText)

        win.flip()

    instructText.setAutoDraw(False)
    continueText.setAutoDraw(False)
    textFeedback.setAutoDraw(False)

    results = pd.DataFrame({"subject": [subjNum],
    "question": [text],
    "resp": [inputText]})

    return results


#==============================================================================#
# START OF QUESTIONNAIRE FUNCTIONS

def affectIntensityMeasure(win=None, saveFile=None, scaleName="aim", subjNum=0, endPause=1.0):
    """ Affect Intensity Measure (Larsen & Deiner, 1987)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["The following questions refer to emotional reactions to typical life events. Please indicate how YOU react to these events by placing a number from the following scale preceding each item. Please base your answers on how YOU react, not on how you think others react or how you think a person should react."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(6):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-6
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-6

    secondaryLabels = ["Never", "Almost Never", "Occasionally", "Usually", "Almost always", "Always"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.20, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["When I feel happiness, it is a quiet type of contentment.",
    "When a person in a wheelchair can't get through a door, I have strong feelings of pity.",
    "I get upset easily.",
    "When I succeed at something, my reaction is calm contentment.",
    "I get really happy or really unhappy.",
    "I'm a fairly quiet person.",
    "When I'm happy, I feel very energetic.",
    "Seeing a picture of some violent car accident in a newspaper makes me feel sick to my stomach.",
    "When I'm happy, I feel like I'm bursting with joy.",
    "I would be very upset if I got a traffic ticket.",
    "Looking at beautiful scenery really doesn't affect me much.",
    "The weather doesn't affect my mood.",
    "Others tend to get more excited about things than I do.",
    "I am not an extremely enthusiastic individual.",
    "'Calm and cool' could easily describe me.",
    "When I'm feeling well it's easy for me to go from being in a good mood to being really joyful.",
    "When I worry, it is so mild that I hardly notice it.",
    "I get overly enthusiastic.",
    "My happy moods are so strong that I feel like I'm 'in heaven'.",
    "When something bad happens, others tend to be more unhappy that I."],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def aggressionQuestionnaire(win=None, saveFile=None, scaleName="bpaq", subjNum=0, endPause=1.0):
    """ Aggression Questionnaire (Buss & Perry, 1992)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["Using the 5 point scale shown below, indicate how uncharacteristic or characteristic each of the following statements is in describing you."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(5):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-5
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-5

    secondaryLabels = ["Extremely uncharacteristic of me", "Somewhat uncharacteristic of me", "Neither uncharacteristic nor characteristic of me", "Somewhat characteristic of me", "Extremely characteristic of me"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.2, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["Some of my friends think I am a hothead.",
    "If I have to resort to violence to protect my rights, I will.",
    "When people are especially nice to me, I wonder what they want.",
    "I tell my friends openly when I disagree with them.",
    "I have become so mad that I have broken things.",
    "I can't help getting into arguments when people disagree with me.",
    "I wonder why sometimes I feel so bitter about things.",
    "Once in a while, I can't control the urge to strike another person.",
    "I am an even-tempered person.",
    "I am suspicious of overly friendly strangers.",
    "I have threatened people I know.",
    "I flare up quickly but get over it quickly.",
    "Given enough provocation, I may hit another person.",
    "When people annoy me, I may tell them what I think of them.",
    "I am sometimes eaten up with jealousy.",
    "I can think of no good reason for ever hitting a person.",
    "At times I feel I have gotten a raw deal out of life.",
    "I have trouble controlling my temper.",
    "When frustrated, I let my irritation show.",
    "I sometimes feel that people are laughing at me behind my back.",
    "I often find myself disagreeing with people.",
    "If somebody hits me, I hit back.",
    "I sometimes feel like a powder keg ready to explode.",
    "Other people always seem to get the breaks.",
    "There are people who pushed me so far that we came to blows.",
    "I know that \"friends\" talk about me behind my back",
    "My friends say that I'm somewhat argumentative.",
    "Sometimes I fly off the handle for no good reason.",
    "I get into fights a little more than the average person."],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def angerRuminationScale(win=None, saveFile=None, scaleName="ars", subjNum=0, endPause=1.0):
    """ Anger Rumination Scale (Sukhodolsky et. al, 2001)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["Fill out the following questionnaire to the best of your ability. Please be completely honest. Your responses will remain strictly confidential. Rate each of the items below using the scale below."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(4):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-4
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-4

    secondaryLabels = ["Almost never", "", "", "Almost always"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.45, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["I ruminate about my past anger experiences.",
    "I ponder about the injustices that have been done to me.",
    "I keep thinking about events that angered me for a long time.",
    "I have long living fantasies of revenge after the conflict is over.",
    "I think about certain events from a long time ago and they still make me angry.",
    "I have difficulty forgiving people hwo have hurt me.",
    "After an argument is over, I keep fighting with this person in my imagination.",
    "Memories of being aggravated pop up into my mind before I fall asleep.",
    "Whenever I experience anger, I keep thinking about it for a while.",
    "I have had times when I could not stop being preoccupied with a particular conflict.",
    "I analyze events that make me angry.",
    "I think about the reasons people treat me badly.",
    "I have day dreams and fantasies of a violent nature.",
    "I feel angry about certain things in my life.",
    "When someone makes me angry I can't stop thinking about how to get back at this person.",
    "When someone provokes me, I keep wondering why this should have happened to me.",
    "Memories of even minor annoyances bother me for a while.",
    "When something makes me angry, I turn this matter over and over again in my mind.",
    "I re-enact the anger episode in my mind after it has happened."],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def attentionalControlScale(win=None, saveFile=None, scaleName="acs", subjNum=0, endPause=1.0):
    """ Attentional Control Scale (ACS; Derryberry & Reed, 2002)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["Read each statement and then indicate how true the statement is of you in general."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(4):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-4
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-4

    secondaryLabels = ["Almost Never", "Sometimes", "Often", "Always"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.45, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["It's very hard for me to concentrate on a difficult task when there are noises around.",
    "When I need to concentrate and solve a problem, I have trouble focusing my attention.",
    "When I am working hard on something, I still get distracted by events around me.",
    "My concentration is good even if there is music in the room around me.",
    "When concentrating, I can focus my attention so that I become unaware of what's going on in the room around me.",
    "When I am reading or studying, I am easily distracted if there are people talking in the same room.",
    "When trying to focus my attention on something, I have difficulty blocking out distracting throughts.",
    "I have a hard time concentrating when I'm excited about something.",
    "When concentrating I ignore feelings of hunger or thirst.",
    "I can quickly switch from one task to another.",
    "It takes me a while to get really involved in a new task.",
    "It is difficult for me to coordiante my attention between the listening and writing required when taking notes during lectures.",
    "I can become interested in a new topic very quickly when I need to.",
    "It is easy for me to read or write while I'm also talking on the phone.",
    "I have trouble carrying on two conversations at once.",
    "I have a hard time coming up with new ideas quickly.",
    "After being interrupted or distracted, I can easily shift my attention back to what I was doing before.",
    "When a distracting thought comes to mind, it is easy for me to shift my attention away from it.",
    "It is easy for me to alternate between two different tasks.",
    "It is hard for me to break away from one way of thinking about something and look at it from another point of view."],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def barrattImpulsivenessScale(win=None, saveFile=None, scaleName="bis", subjNum=0, endPause=1.0):
    """ Barratt Impulsiveness Scale (BIS; Barratt et. al, 1995)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["People differ in the ways they act and think in different situations. This is a test to measure some of the ways in which you act and think. Read each statement and mark the appropriate circle. Do not spend too much time on any statement. Answer quickly and honestly."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(4):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-4
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-4

    secondaryLabels = ["Rarely/Never", "Occaisionally", "Often", "Almost Always/Always"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.45, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["I plan tasks carefully.",
    "I do things without thinking.",
    "I make-up my mind quickly.",
    "I am happy-go-lucky.",
    "I don't \"pay attention\".",
    "I have \"racing\" thoughts.",
    "I plan trips well ahead of time.",
    "I am self controlled.",
    "I concentrate easily.",
    "I save regularly.",
    "I \"squirm\" at plays or lectures.",
    "I am a careful thinker.",
    "I plan for job security.",
    "I say things without thinking.",
    "I like to think about complex problems.",
    "I change jobs.",
    "I act \"on impulse\".",
    "I get easily bored when solving thought problems.",
    "I act on the spur of the moment.",
    "I am a steady thinker.",
    "I change residences.",
    "I buy things on impulse.",
    "I can only think about one thing at a time.",
    "I change hobbies.",
    "I spend or charge more than I earn.",
    "I often have extraneous thoughts when thinking.",
    "I am more interested in the present that the future.",
    "I am restless at the theater or lectures.",
    "I like puzzles.",
    "I am future oriented."],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def bigFiveAspectsScale(win=None, saveFile=None, scaleName="bfas", subjNum=0, endPause=1.0):
    """ Big Five Aspects Scale (DeYoung et al., 2007)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["Here are a number of characteristics that may or may not describe you. For example, do you agree that you seldom feel blue, compared to most other people? Please press the number that best indicates the extent to which you agree or disagree with each statement listed below. Be as honest as possible, but rely on your initial feeling and do not think too much about each item. Thank you."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(5):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-5
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-5

    secondaryLabels = ["Strongly Disagree", "", "Neither Agree\nnor Disagree", "", "Strongly Agree"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.45, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["I seldom feel blue.",
    "I am not interested in other people's problems.",
    "I carry out my plans.",
    "I make friends easily.",
    "I am quick to understand things.",
    "I get angry easily",
    "I respect authority.",
    "I leave my belongings around.",
    "I take charge.",
    "I enjoy the beauty of nature.",
    "I am filled with doubts about things.",
    "I feel others' emotions.",
    "I waste my time.",
    "I am hard to get to know.",
    "I have difficulty understanding abstract ideas.",
    "I rarely get irritated.",
    "I believe that I am better than others.",
    "I like order.",
    "I have a strong personality.",
    "I believe in the importance of art.",
    "I feel comfortable with myself.",
    "I inquiry about others' well-being.",
    "I find it difficult to get down to work.",
    "I keep others at a distance.",
    "I can handle a lot of information.",
    "I get upset easily.",
    "I hate so seem pushy.",
    "I keep things tidy.",
    "I lack the talent for incluencing people.",
    "I love to reflect on things.",
    "I feel threatened easily.",
    "I can't be bothered with other's needs.",
    "I mess things up.",
    "I reveal little about myself.",
    "I like to solve complex problems.",
    "I keep my emotions under control.",
    "I take advantage of others.",
    "I follow a schedule.",
    "I know how to captivate people.",
    "I get deeply immersed in music.",
    "I rarely feel depressed.",
    "I sympathize with others' feelings.",
    "I finish what I start.",
    "I warm up quickly to others.",
    "I avoid philosophical discussions.",
    "I change my mood a lot.",
    "I avoid imposing my will on others.",
    "I am not bothered by messy people.",
    "I wait for others to lead the way.",
    "I do not like poetry.",
    "I worry about things.",
    "I am indifferent to the feelings of others.",
    "I don't put my mind on the task at hand.",
    "I rarely get caught up in the excitement.",
    "I avoid difficult reading material.",
    "I rarely lose my composure.",
    "I rarely put people under pressure.",
    "I want everything to be \"just right\".",
    "I see myself as good leader.",
    "I seldom notice the emotional aspects of paintings and pictures.",
    "I am easily discouraged.",
    "I take no time for others.",
    "I get things done quickly.",
    "I am not a very enthuisiastic person.",
    "I have a rich vocabulary.",
    "I am a person whose moods go up and down easily.",
    "I insult people.",
    "I am not bothered by disorder.",
    "I can talk others into doing things.",
    "I need a creative outlet.",
    "I am not embarassed easily.",
    "I take an interest in other people's lives.",
    "I always know what I am doing.",
    "I show my feelings when I'm happy.",
    "I think quickly.",
    "I am not easily annoyed.",
    "I seek conflict.",
    "I dislike routine.",
    "I hold back my opinions.",
    "I seldom get lost in thought.",
    "I become overwhelmed by events.",
    "I don't have a soft side.",
    "I postpone decisions.",
    "I have a lot of fun.",
    "I learn things slowly.",
    "I get easily agitated.",
    "I love a good fight.",
    "I see that rules are observed.",
    "I am the first to act.",
    "I seldom daydream.",
    "I am afraid of many things.",
    "I like to do things for others.",
    "I am easily distracted.",
    "I laugh a lot.",
    "I formulate ideas clearly.",
    "I can be stirred up easily.",
    "I am out for my own personal gain.",
    "I what every detail taken care of.",
    "I do not have an assertive personality.",
    "I see beauty in things that others might not notice."],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def bisBas(win=None, saveFile=None, scaleName="bisbas", subjNum=0, endPause=1.0):
    """ BIS/BAS (Carver & White, 1994)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["Each item of this questionnaire is a statement that a person may either agree with or disagree with. For each item, indicate how much you agree or disagree with what the item says. Please respond to all the items; do not leave any blank. Please be as accurate and honest as you can be. Respond to each item as if it were the only item. That is, don't worry about being \"consistent\" in your responses."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(4):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-4
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-4

    secondaryLabels = ["Very True for Me", "Somewhat True for Me", "Somewhat False for Me", "Very False for Me"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.45, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["A person's family is the most important thing in life.",
    "Even if something bad is about to happen to me, I rarely experience fear or nervousness.",
    "I go out of my way to get things I want.",
    "When I'm doing well at something I love to keep at it.",
    "I'm always willing to try something new if I think it will be fun.",
    "How I dress is important to me.",
    "When I get something I want, I feel excited and energized.",
    "Criticism or scolding hurts me quite a bit.",
    "When I want something I usually go all-out to get it.",
    "I will often do things for no other reason than that they might be fun.",
    "It's hard for me to find the time to do things such as get a haircut.",
    "If I see a chance to get something I want I move on it right away.",
    "I feel pretty worried or upset when I think or know somebody is angry at me.",
    "When I see an opportunity for something I like I get excited right away.",
    "I often act on the spur of the moment.",
    "If I think something unpleasant is going to happen I usually get pretty \"worked up\".",
    "I often wonder why people act the way they do.",
    "When good things happen to me, it affects me strongly.",
    "I feel worried when I think I have done poorly at something important.",
    "I crave excitement and new sensations.",
    "When I go after something I use a \"no holds barred\" approach.",
    "I have very few fears compared to my friends.",
    "It would excite me to win a contest.",
    "I worry about making mistakes."],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def centerForEpidemiologicStudiesDepressionScale(win=None, saveFile=None, scaleName="cesdr", subjNum=0, endPause=1.0):
    """ Center for Epidemiologic Studies Depression Scale – Revised (CESD-R; Eaton et al., 2004)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["Next is a list of ways you might have felt or behaved. Please indicate how often you have felt this way DURING THE PAST WEEK."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(4):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-4
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-4

    secondaryLabels = ["Rarely or none of the time\n(less than 1 day)", "Some or a little of the time\n(1-2 days)", "Occasionally or a moderate amount of time\n(3-4 days)", "Most or all of the time\n(5-7 days)"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.2, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.30, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["I was bothered by things that usually don't bother me.",
    "I did not feel like eating; my appetite was poor.",
    "I felt that I could not shake off the blues even with help from my family and friends.",
    "I felt that I was just as good as other people.",
    "I had trouble keeping my mind on what I was doing.",
    "I felt depressed.",
    "I felt that everything I did was an effort.",
    "I felt hopeful about the future.",
    "I thought my life had been a failure.",
    "I felt fearful.",
    "My sleep was restless.",
    "I was happy.",
    "I talked less than usual.",
    "I felt lonely.",
    "People were unfriendly.",
    "I enjoyed life.",
    "I had crying spells.",
    "I felt sad.",
    "I felt that people dislike me.",
    "I could not get \"going\"."],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def childhoodTraumaQuestionnaire(win=None, saveFile=None, scaleName="ctq", subjNum=0, endPause=1.0):
    """ Childhood Trauma Questionnaire (CTQ; Bernstein & Fink, 1997)
        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["Please indicate how true the following statements were about living in your family prior to age 13. Use a five point scale from 1=never true to 5=very often true."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(5):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-5
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-5

    secondaryLabels = ["Never true", "Rarely true", "Sometimes true", "Often true", "Very often true"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.45, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["I didn't have enough to eat.",
    "I knew that there was someone to take care of me and protect me.",
    "People in my family called me things like \"stupid\", \"lazy\", or \"ugly\".",
    "My parents were too drunk or high to take care of the family.",
    "There was someone in my family who helped me feel that I was important or special.",
    "I had to wear dirty clothes.",
    "I felt loved.",
    "I thought that my parents wished I had never been born.",
    "I got hit so hard by someone in my family that I had to see a doctor or go to the hospital.",
    "There was nothing I wanted to change about my family.",
    "People in my family hit me so hard that it left me with bruises or marks.",
    "I was punished with a belt (a strap), a board (a stick), a chord, or some other hard object.",
    "People in my family looked out for each other.",
    "People in my family said hurtful or insulting things to me.",
    "I believe that I was physically abused.",
    "I had the perfect childhood.",
    "I got hit or beaten so badly that it was noticed by someone like a teacher, neighbor, or doctor.",
    "I felt that someone in my family hated me.",
    "People in my family felt close to each other.",
    "Someone tried to touch me in a sexual way.",
    "Someone threatened to hurt me or tell lies about me unless I did something sexual with them.",
    "I had the best family in the world.",
    "Someone tried to make me do sexual things or watch sexual things.",
    "Someone molested me.",
    "I believe that I was emotionally abused.",
    "There was someone to take me to the doctor if I needed it.",
    "I believe that I was sexually abused.",
    "My family was a source of strength and support."],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def compassionateSelfImageGoals_friends(win=None, saveFile=None, scaleName="csigf", subjNum=0, endPause=1.0):
    """ Compassionate and Self-Image Goals Scale (Crocker & Canevello, 2008)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["In the past week, in the area of friendships, how much did you want or try to:"],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(5):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-5
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-5

    secondaryLabels = ["Not at all", "A little", "Somewhat", "A lot", "Extremely"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.45, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["avoid doing things that aren't helpful to me or others",
    "avoid the possibility of being wrong",
    "get others to recognize or acknowledge your positive qualities",
    "avoid being selfish or self-centered",
    "have compassion for others' mistakes and weaknesses",
    "avoid being rejected by others",
    "avoid taking risks or making mistakes",
    "be constructive in your comments to others",
    "avoid showing your weaknesses",
    "avoid doing anything that would be harmful to others",
    "be supportive of others",
    "make a positive difference in someone else's life",
    "convince others that you are right"],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def compassionateSelfImageGoals_general(win=None, saveFile=None, scaleName="csigg", subjNum=0, endPause=1.0):
    """ Compassionate and Self-Image Goals Scale (Crocker & Canevello, 2008)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    # gf.show_instructs(win=win,
    # text=["In general, how much do you want or try to:"],
    # timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(5):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-5
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-5

    secondaryLabels = ["Not at all", "A little", "Somewhat", "A lot", "Extremely"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.45, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["In general, how much do you want or try to:\n\navoid doing things that aren't helpful to me or others",
    "In general, how much do you want or try to:\n\navoid the possibility of being wrong",
    "In general, how much do you want or try to:\n\nget others to recognize or acknowledge your positive qualities",
    "In general, how much do you want or try to:\n\navoid being selfish or self-centered",
    "In general, how much do you want or try to:\n\nhave compassion for others' mistakes and weaknesses",
    "In general, how much do you want or try to:\n\navoid being rejected by others",
    "In general, how much do you want or try to:\n\navoid taking risks or making mistakes",
    "In general, how much do you want or try to:\n\nbe constructive in your comments to others",
    "In general, how much do you want or try to:\n\navoid showing your weaknesses",
    "In general, how much do you want or try to:\n\navoid doing anything that would be harmful to others",
    "In general, how much do you want or try to:\n\nbe supportive of others",
    "In general, how much do you want or try to:\n\nmake a positive difference in someone else's life",
    "In general, how much do you want or try to:\n\nconvince others that you are right"],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def curiosityAboutMorbidEvents(win=None, saveFile=None, scaleName="came", subjNum=0, endPause=1.0):
    """ Curiosity About Morbid Events (CAME; Zuckerman & Litle, 1986)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["Use the scale provided to indicate your agreement with the following statements. Please provide your honest answer."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(7):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-7
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-7

    secondaryLabels = ["Strongly disagree", "Disagree", "Somewhat disagree", "Neither agree nor disagree", "Somewhat agree", "Agree", "Strongly agree"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.2, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["I like to watch sports like prize fighting or ice hockey that sometimes get a bit violent.",
    "Most horror movies are fairly amusing.",
    "I would like to see an autopsy being performed.",
    "I enjoy being mildly frightened by horror movies.",
    "If I could travel back in time to ancient Rome I would be curious enough to visit the coliseums to watch gladiators fight each other and wild animals to the death.",
    "Television news focuses too much on the violent effects of accidents, war, and crime.",
    "When I see a serious auto accident on the road and it is apparent that there is no need for further help, I still slow down in order to see what has happened.",
    "Most horror movies are disgusting.",
    "I am curious about crime and therefore usually read the detailed news accounts about murders and other violent crimes.",
    "I would like to see a bull-fight.",
    "I am not interested in watching car races because the drivers are sometimes killed or seriously injured in them.",
    "Under no circumstances would I like to see a person being killed.",
    "I think I would like to witness an execution.",
    "It does not bother me to see extreme violence portrayed in movies or television.",
    "Television news should show us the results of war and crime, no matter how gory, so we do not have any illusions about these topics.",
    "I do not generally read detailed news accounts of murders and other wolent crimes.",
    "I would not want to look at a dead person.",
    "I would not like to watch a major surgical operation being performed."],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def dirtyDozen(win=None, saveFile=None, scaleName="dd", subjNum=0, endPause=1.0):
    """ The Dirty Dozen (Jonason & Webster, 2010)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["Fill out the following questionnaire to the best of your ability. Please be completely honest. Your responses will remain strictly confidential. Rate each of the items below using the scale below."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(9):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-9
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-9

    secondaryLabels = ["Disagree Strongly", "Disagree", "Disagree Moderately", "Disagree Slightly", "Neither Agree Nor Disagree", "Agree Slightly", "Agree Moderately", "Agree", "Agree Strongly"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.8, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.1, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["I tend to manipulate others to get my way.",
    "I have used deceit or lied to get my way.",
    "I have used flattery to get my way.",
    "I tend to exploit others towards my own end.",
    "I tend to lack remorse.",
    "I tend to be unconcerned with the morality of my actions.",
    "I tend to be callous or insensitive.",
    "I tend to be cynical.",
    "I tend to want others to admire me.",
    "I tend to want others to pay attention to me.",
    "I tend to seek prestige or status.",
    "I tend to expect special favors from others."],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def disgustSensitivityScale(win=None, saveFile=None, scaleName="dssr", subjNum=0, endPause=1.0):
    """ Disgust Sensitivity Scale - Revised (Olatunji et al., 2007)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """

    #### Part 1 of the DSS-R

    # display scale instructions
    gf.show_instructs(win=win,
    text=["Please indicate how much you agree with each of the following statements, or how true it is about you."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(5):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-5
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-5

    secondaryLabels = ["Strongly disagree\n(very untrue about me)", "Mildly disagree\n(somewhat untrue about me)", "Neither Agree Nor Disagree", "Mildy agree\n(somewhat true about me)", "Strongly agree\n(very true about me)"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.8, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.25, win=win, bold=True)

    # run scale
    dssPart1 = run_scale_items(win=win,
    scaleItems=["I might be willing to try eating monkey meat, under some circumstances.",
    "It would bother me to be in a science class, and to see a human hand preserved in a jar.",
    "It bothers me to hear someone clear a throat full of mucous.",
    "I never let any part of my body touch the toilet seat in public restrooms.",
    "I would go out of my way to avoid walking through a graveyard.",
    "Seeing a cockroach in someone else's house doesn't bother me.",
    "It would bother me tremendously to touch a dead body.",
    "If I see someone vomit, it makes me sick to my stomach.",
    "I probably would not go to my favorite restaurant if I found out that the cook had a cold.",
    "It would not upset me at all to watch a person with a glass eye take the eye out of the socket.",
    "It would bother me to see a rat run across my path in a park.",
    "I would rather eat a piece of fruit than a piece of paper.",
    "Even if I was hungry, I would not drink a bowl of my favorite soup if it had been stirred by a used but thoroughly washed flyswatter.",
    "It would bother me to sleep in a nice hotel room if I knew that a man had died of a heart attack in that room the night before."],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName + "1", subjNum=subjNum)

    #### Part 2 of the DSS-R

    # display scale instructions
    gf.show_instructs(win=win,
    text=["How disgusting would you find each of the following experiences?"],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(5):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-5
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-5

    secondaryLabels = ["Not disgusting at all", "Slightly disgusting", "Moderately disgusting", "Very disgusting", "Extremely disgusting"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.8, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.15, win=win, bold=True)

    # run scale
    dssPart2 = run_scale_items(win=win,
    scaleItems=["You see maggots on a piece of meat in an outdoor garbage pail.",
    "You see a person eating an apple with a knife and fork.",
    "While you are walking through a tunnel under a railroad track, you smell urine.",
    "You take a sip of soda, and then realize that you drank from the glass that an acquaintance of yours had been drinking from.",
    "Your friend's pet cat dies, and you have to pick up the dead body with your bare hands.",
    "You see someone put ketchup on vanilla ice cream, and eat it.",
    "You see a man with his intestines exposed after an accident.",
    "You discover that a friend of yours changes underwear only once a week.",
    "A friend offers you a piece of chocolate shaped like dog doo.",
    "You accidentally touch the ashes of a person who has been cremated.",
    "You are about to drink a glass of milk when you smell that it is spoiled.",
    "As part of a sex education class, you are required to inflate a new unlubricated condom, using your mouth.",
    "You are walking barefoot on concrete, and you step on an earthworm."],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName + "2", subjNum=subjNum)

    results = pd.concat([dssPart1, dssPart2])
    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)
    elif saveFile is None:
        return results

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def displacedAggressionQuestionnaire(win=None, saveFile=None, scaleName="daq", subjNum=0, endPause=1.0):
    """ Displaced Aggression Questionnaire (Denson et. al, 2006)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["Directions: Fill out the following questionnaire to the best of your ability. Please be completely honest. Your responses will remain strictly confidential. Rate each of the items below using the scale below. Take your time and pay attention to the wording. Sometimes the items are worded differently."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(7):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-7
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-7

    secondaryLabels = ["Extremely Uncharacteristic of Me", "", "", "", "", "", "Extremely Characteristic of Me"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.2, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["I keep thinking about events that angered me for a long time.",
    "I get \"worked up\" just thinking about things that have upset me in the past.",
    "I often find myself thinking over and over about things that have made me angry.",
    "Sometimes I can't help thinking about times when someone made me mad.",
    "Whenever I experience anger, I keep thinking about it for a while.",
    "After an argument is over, I keep fighting with this person in my imagination.",
    "I re-enact the anger episode in my mind after it has happened.",
    "I feel angry about certain things in my life.",
    "I think about certain events from a long time ago and they still make me angry.",
    "When angry, I tend to focus on my thoughts and feelings for a long period of time.",
    "When someone or something makes me angry I am likely to take it out on another person.",
    "When feeling bad, I take it out on others.",
    "When angry, I have taken it out on people close to me.",
    "Sometimes I get upset with a friend or family member even though that person is not the cause of my anger or frustration.",
    "I take my anger out on innocent others.",
    "When things don't go the way I plan, I take my frustration out at the first person I see.",
    "If someone made me angry I would likely vent my anger on another person.",
    "Sometimes I get so upset by work or school that I become hostile toward family or friends.",
    "When I am angry, I don't care who I lash out at.",
    "If I have had a hard day at work or school, I'm likely to make sure everyone knows about it.",
    "When someone makes me angry I can't stop thinking about how to get back at this person.",
    "If somebody harms me, I am not at peace until I can retaliate.",
    "I often daydream about situations where I'm getting my own back at people.",
    "I would get frustrated if I could not think of a way to get even with someone who deserves it.",
    "I think about ways of getting back at people who have made me angry long after the event has happened.",
    "If another person hurts you, it's alright to get back at him or her.",
    "The more time that passes, the more satisfaction I get from revenge.",
    "I have long living fantasies of revenge after the conflict is over.",
    "When somebody offends me, sooner or later I retaliate.",
    "If a person hurts you on purpose, you deserve to get whatever revenge you can.",
    "I never help those who do me wrong."],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def emotionRegulationQuestionnaire(win=None, saveFile=None, scaleName="erq", subjNum=0, endPause=1.0):
    """ Emotion Regulation Questionnaire (Gross & John, 2003)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["We would like to ask you some questions about your emotional life, in particular, how you control (that is, regulate and manage) your emotions. The questions below involve two distinct aspects of your emotional life. One is your emotional experience, or what you feel like inside. The other is your emotional expression, or how you show your emotions in the way you talk, gesture, or behave. Although some of the following questions may seem similar to one another, they differ in important ways. For each item, please answer by pressing the number for your response."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'], textPos=(0, 0.35))

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(7):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-7
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-7

    secondaryLabels = ["Strongly Disagree", "Disagree", "Moderately Disagree", "Neither Agree nor Disagree", "Moderately Agree", "Agree", "Strongly Agree"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.7, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.2, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["When I want to feel more positive emotion (such as joy or amusement), I change what I'm thinking about.",
    "I keep my emotions to myself.",
    "When I want to feel less negative emotion (such as sadness or anger), I change what I'm thinking about.",
    "When I am feeling positive emotions, I am careful not to express them.",
    "When I am faced with a stressful situation, I make myself think about it in a way that helps me stay calm.",
    "I control my emotions by not expressing them.",
    "When I want to feel more positive emotion, I change the way I'm thinking about the situation.",
    "I control my emotions by changing the way I think about the situation I'm in.",
    "When I am feeling negative emotions, I make sure not to express them.",
    "When I want to feel less negative emotion, I change the way I'm thinking about the situation."],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def extremeValuingOfHappinessScale(win=None, saveFile=None, scaleName="evhs", subjNum=0, endPause=1.0):
    """ Extreme Valuing of Happiness Scale (Mauss et al., 2011)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["Please press the number to indicate your agreement with each of the following statements."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(7):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-7
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-7

    secondaryLabels = ["Strongly Disagree", "Disagree", "Moderately Disagree", "Neither Agree nor Disagree", "Moderately Agree", "Agree", "Strongly Agree"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.7, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.2, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["How happy I am at any given moment says a lot about how worthwhile my life is.",
    "If I don't feel happy, maybe there is something wrong with me.",
    "I value things in life only to the extent that they influence my personal happiness.",
    "Feeling happy is extremely important to me.",
    "I am concerned about my happiness even when I feel happy.",
    "To have a meaningful life, I need to feel happy most of the time.",
    "I get somewhat distressed if I don't feel happy.",
    "If I don't feel happy, I worry about it."],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def eysenckPersonalityQuestionnaireRevisedShortScale(win=None, saveFile=None, scaleName="epqrss", subjNum=0, endPause=1.0):
    """ Eysenck Personality Questionnaire - Revised Short Scale (Eysenck et al., 1985)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["Please answer each question by pressing the button for 'yes' or 'no'. There are no right or wrong answers, and no trick questions. Work quietly and do not think too long about the exact meaning of the questions."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(2):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-2
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-2

    secondaryLabels = ["Yes", "No"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.3, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.15,
                                         secondaryWrapWidth=0.2, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["Does your mood often go up and down?",
    "Do you take much notice of what people think?",
    "Are you a talkative person?",
    "If you say you will do something, do you always keep your promise no matter how inconvenient it might be?",
    "Do you ever feel 'just miserable' for no reason?",
    "Would being in debt worry you?",
    "Are you rather lively?",
    "Were you ever greedy by helping yourself to more than your share of anything?",
    "Are you an irritable person?",
    "Would you take drugs which may have strange or dangerous effects?",
    "Do you enjoy meeting new people?",
    "Have you ever blamed someone for doing something you knew was really your fault?",
    "Are your feelings easily hurt?",
    "Do you prefer to go your own way rather than act by the rules?",
    "Can you usually let yourself go and enjoy yourself at a lively party?",
    "Are all your habits good and desirable ones?",
    "Do you often feel 'fed-up'?",
    "Do good manners and cleanliness matter much to you?",
    "Do you usually take the initiative in making new friends?",
    "Have you ever taken anything (even a pin or button) that belonged to someone else?",
    "Would you call yourself a nervous person?",
    "Do you think marriage is old-fashioned and should be done away with?",
    "Can you easily get some life into a rather dull party?",
    "Have you ever broken or lost something belonging to someone else?",
    "Are you a worrier?",
    "Do you enjoy co-operating with others?",
    "Do you tend to keep in the background on social occasions?",
    "Does it worry you if you know there are mistakes in your work?",
    "Have you ever said anything bad or nasty about anyone?",
    "Would you call yourself tense or 'highly-strung'?",
    "Do you think people spend too much time safeguarding their future with savings and insurances?",
    "Do you like mixing with people?",
    "As a child were you ever cheeky to your parents?",
    "Do you worry too long after an embarrassing experience?",
    "Do you try not to be rude to people?",
    "Do you like plenty of bustle and excitement around you?",
    "Have you ever cheated at a game?",
    "Do you suffer from 'nerves'?",
    "Would you like other people to be afraid of you?",
    "Have you ever taken advantage of someone?",
    "Are you mostly quiet when you are with other people?",
    "Do you often feel lonely?",
    "Is it better to follow society's rules than go your own way?",
    "Do other people think of you as being very lively?",
    "Do you always practice what you preach?",
    "Are you often troubled about feelings of guilt?",
    "Do you sometimes put off until tomorrow what you ought to do today?",
    "Can you get a party going?"],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)

    return results


def highlySensitivePersonsScale(win=None, saveFile=None, scaleName="hsp", subjNum=0, endPause=1.0):
    """ Highly Sensitive Persons Scale (HSP; Aron & Aron, 1997)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["This questionnaire is completely anonymous and confidential. Answer each question according to the way you personally feel, using the scale that is provided."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(7):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-7
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-7

    secondaryLabels = ["Not at all", "", "", "Moderately", "", "", "Extremely"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.30, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["Are you easily overwhelmed by strong sensory input?",
    "Do you seem to be aware of subtleties in your environment?",
    "Do other people's moods affect you?",
    "Do you tend to be more sensitive to pain?",
    "Do you find yourself needing to withdraw during busy days, into bed or into a darkened room or any place where you can have some privacy and relief from stimulation?",
    "Are you particularly sensitive to the effects of caffeine?",
    "Are you easily overwhelmed by things like bright lights, strong smells, coarse fabrics, or sirens close by?",
    "Do you have a rich, complex inner life?",
    "Are you made uncomfortable by loud noises?",
    "Are you deeply moved by the arts or music?",
    "Does your nervous system sometimes feel so frazzled that you just have to go off by yourself?",
    "Are you conscientious?",
    "Do you startle easily?",
    "Do you get rattled when you have a lot to do in a short amount of time?",
    "When people are uncomfortable in a physical environment do you tend to know what needs to be done to make it more comfortable (like changing the lighting or the seating)?",
    "Are you annoyed when people try to get you to do too many things at once?",
    "Do you try hard to avoid making mistakes or forgetting things?",
    "Do you make a point to avoid violent movies and TV shows?",
    "Do you become unpleasantly aroused when a lot is going on around you?",
    "Does being very hungry create a strong reaction in you, disrupting your concentration or mood?",
    "Do changes in your life shake you up?",
    "Do you notice and enjoy delicate or fine scents, tastes, sounds, works of art?",
    "Do you find it unpleasant to have a lot going on at once?",
    "Do you make it a high priority to arrange your life to avoid upsetting or overwhelming situations?",
    "Are you bothered by intense stimuli, like loud noises or chaotic scenes?",
    "When you must compete or be observed while performing a task, do you become so nervous or shaky that you do much worse than you would otherwise?",
    "When you were a child, did parents or teachers seem to see you as sensitive or shy?"],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def implicitSelfTheories(win=None, saveFile=None, scaleName="ist", subjNum=0, endPause=1.0):
    """ Implicit Self-Theories Scale (Dweck, 1999)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["Please indicate the extent to which you agree or disagree with the following statements. Use the scale below."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(6):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-6
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-6

    secondaryLabels = ["Very strongly agree", "Agree", "Mostly agree", "Mostly disagree", "Disagree", "Very strongly disagree"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.2, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["The kind of person someone is is something very basic about them and it can't be changed very much.",
    "People can do things differently, but the important parts of who they are can't really be changed.",
    "Everyone is a certain kind of person and there is not much that can be done to really change that."],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def interpersonalReactivityIndex(win=None, saveFile=None, scaleName="iri", subjNum=0, endPause=1.0):
    """ Interpersonal Reactivity Index (IRI; Davis, 1980)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["The following statements inquire about your thoughts and feelings in a variety of situations. For each item, indicate how well it describes you by pressing the appropriate number: 1, 2, 3, 4, or 5. READ EACH ITEM CAREFULLY BEFORE RESPONDING. Answer as honestly as you can. Thank you."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(5):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-5
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-5

    secondaryLabels = ["Does not describe me well", "", "", "", "Describes me very well"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.45, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["I daydream and fantasize, with some regularity, about things that might happen to me.",
    "I often have tender, concerned feelings for people less fortunate than me.",
    "I sometimes find it difficult to see things from the \"other guy's\" point of view.",
    "Sometimes I don't feel very sorry for other people when they are having problems.",
    "I really get involved with the feelings of the characters in a novel.",
    "In emergency situations, I feel apprehensive and ill-at-ease.",
    "I am usually objective when I watch a movie or play, and I don't often get completely caught up in it.",
    "I try to look at everybody's side of a disagreement before I make a decision.",
    "When I see someone being taken advantage of, I feel kind of protective towards them.",
    "I sometimes feel helpless when I am in the middle of a very emotional situation.",
    "I sometimes try to understand my friends better by imagining how things look from their perspective.",
    "Becoming extremely involved in a good book or movie is somewhat rare for me.",
    "When I see someone get hurt, I tend to remain calm.",
    "Other people's misfortunes do not usually disturb me a great deal.",
    "If I'm sure I'm right about something, I don't waste much time listening to other people's arguments.",
    "After seeing a play or movie, I have felt as though I were one of the characters.",
    "Being in a tense emotional situation scares me.",
    "When I see someone being treated unfairly, I sometimes don't feel very much pity for them.",
    "I am usually pretty effective in dealing with emergencies.",
    "I am often quite touched by things that I see happen.",
    "I believe that there are two sides to every question and try to look at them both.",
    "I would describe myself as a pretty soft-hearted person.",
    "When I watch a good movie, I can very easily put myself in the place of a leading character.",
    "I tend to lose control during emergencies.",
    "When I'm upset at someone, I usually try to \"put myself in his shoes\" for a while.",
    "When I am reading an interesting story or novel, I imagine how I would feel if the events in the story were happening to me.",
    "When I see someone who badly needs help in an emergency, I go to pieces.",
    "Before criticizing somebody, I try to imagine how I would feel if I were in their place."],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def intoleranceOfUncertaintyScale(win=None, saveFile=None, scaleName="ious", subjNum=0, endPause=1.0):
    """ Intolerance of Uncertainty Scale - Short Form (Carelton et. al, 2007)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["Please press the number that best corresponds to how much you agree with each statement."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(5):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-5
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-5

    secondaryLabels = ["Not at all characteristic of me", "A little characteristic of me", "Somewhat characteristic of me", "Very characteristic of me", "Entirely characteristic of me"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.2, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["Unforeseen events upset me greatly.",
    "It frustrates me not having all the information I need.",
    "Uncertainty keeps me from living a full life.",
    "One should always look ahead so as to avoid surprises.",
    "A small unforeseen event can spoil everything, even with the best of planning.",
    "When it's time to act, uncertainty paralyses me.",
    "When I am uncertain I can't function very well.",
    "I always want to know what the future has in store for me.",
    "I can't stand being taken by surprise.",
    "The smallest doubt can stop me from acting.",
    "I should be able to organize everything in advance.",
    "I must get away from all uncertain situations."],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def levensonSelfReportPsychopathy(win=None, saveFile=None, scaleName="lsrp", subjNum=0, endPause=1.0):
    """ Levenson Self-Report Psychopathy (Levenson et. al, 1995)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["Please indicate the extent to which you agree or disagree with the following questions by picking from the 7 point scale provided."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(7):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-7
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-7

    secondaryLabels = ["Disagree Strongly", "Disagree", "Slightly Disagree", "Neither Agree Nor Disagree", "Slightly Agree", "Agree", "Agree Strongly"]
    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.7, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.2, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["Success is based on survival of the fittest; I am not concerned about the losers",
    "For me, what's right is whatever I can get away with",
    "In today's world, I feel justified in doing anything I can get away with to succeed",
    "My main purpose in life is getting as many goodies as I can",
    "Making a lot of money is my most important goal",
    "I let others worry about higher values; my main concern is the bottom line",
    "People who are stupid enough to get ripped off usually deserve it",
    "Looking out for myself is my top priority",
    "I tell other people what they want to hear so they will do what I want them to do",
    "I would be upset if my success came at someone else's expense",
    "I often admire a really clever scam",
    "I make a point of trying not to hurt others in pursuit of my goals",
    "I enjoy manipulating other people's feelings",
    "I feel bad if my words or actions cause someone else to feel emotional pain",
    "Even if I were trying hard to sell something, I wouldn't lie about it",
    "Cheating is not justified because it is unfair to others",
    "I find myself in the same kinds of trouble, time after time",
    "Most of my problems are due to the fact that people don't understand me",
    "Before I do anything, I carefully consider the possible consequences",
    "I have been in a lot of shouting matches with other people",
    "When I get frustrated, I often 'let off steam' by blowing my top",
    "Love is overrated"],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def mindfulAttentionAwarenessScale(win=None, saveFile=None, scaleName="maas", subjNum=0, endPause=1.0):
    """ Mindful Attention Awareness Scale (MAAS; Brown & Ryan, 2003)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["Below is a collection of statements about your everyday experience. Using the scale, please indicate how frequently or infrequently you currently have each experience. Please answer according to what really reflects your experience rather than what you think your experience should be. Please treat each item separately from every other item."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(6):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-6
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-6

    secondaryLabels = ["Almost Always", "Very Frequently", "Somewhat Frequently", "Somewhat Infrequently", "Very Infrequently", "Almost Never"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.20, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["I could be experiencing some emotion and not be conscious of it until some time later.",
    "I break or spill things because of carelessness, not paying attention, or thinking of something else.",
    "I find it difficult to stay focused on what's happening in the present.",
    "I tend to walk quickly to get where I'm going without paying attention to what I experience along the way.",
    "I tend not to notice feelings of physical tension or discomfort until they really grab my attention.",
    "I forget a person's name almost as soon as I've been told it for the first time.",
    "It seems I am \"running on automatic,\" without much awareness of what I'm doing.",
    "I rush through activities without being really attentive to them.",
    "I get so focused on the goal I want to achieve that I lose touch with what I'm doing right now to get there.",
    "I do jobs or tasks automatically, without being aware of what I'm doing.",
    "I find myself listening to someone with one ear, doing something else at the same time.",
    "I drive places on 'automatic pilot' and then wonder why I went there.",
    "I find myself preoccupied with the future or the past.",
    "I find myself doing things without paying attention.",
    "I snack without being aware that I'm eating."],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def personalityAssessmentInventoryBorderlineFeatures(win=None, saveFile=None, scaleName="paibor", subjNum=0, endPause=1.0):
    """ Personality Assessment Inventory – Borderline Features (PAI-BOR; Morey, 1991)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["Read each statement and decide if it is an accurate statement about you."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(4):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-4
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-4

    secondaryLabels = ["False, not at all true", "Slightly true", "Mainly true", "Very true"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.20, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["My mood can shift quite suddenly.",
    "My attitude about myself changes a lot.",
    "My relationships have been stormy.",
    "My moods get quite intense.",
    "Sometimes I feel terribly empty inside.",
    "I want to let certain people know how much they've hurt me.",
    "My mood is very steady.",
    "I worry a lot about other people leaving me.",
    "People once close to me have let me down.",
    "I have little control over my anger.",
    "I often wonder what I should do with my life.",
    "I rarely feel very lonely.",
    "I sometimes do things so impulsively that I get into trouble.",
    "I've always been a pretty happy person.",
    "I can't handle separation from those close to me very well.",
    "I've made some real mistakes in the people I've picked as friends.",
    "When I'm upset, I typically do something to hurt myself.",
    "I've had times when I was so mad I couldn't do enough to express my anger.",
    "I don't get bored very easily.",
    "Once someone is my friend, we stay friends.",
    "I'm too impulsive for my own good.",
    "I spend money too easily.",
    "I'm a reckless person.",
    "I'm careful about how I spend my money."],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def statePANAS(win=None, saveFile=None, scaleName="panas_state", subjNum=0, endPause=1.0):
    """ State Positive and Negative Affect Schedule (PANAS; Watson et al., 1988)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["This scale consists of a number of words that describe different feelings and emotions. Read each item and then use the scale to indicate to what extent you feel this way RIGHT NOW, that is, AT THE PRESENT MOMENT."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(5):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-5
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-5

    secondaryLabels = ["Very slightly or not at all", "A little", "Moderately", "Quite a bit", "Extremely"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.45, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["Interested",
    "Distressed",
    "Excited",
    "Upset",
    "Strong",
    "Guilty",
    "Scared",
    "Hostile",
    "Enthusiastic",
    "Proud",
    "Irritable",
    "Alert",
    "Ashamed",
    "Inspired",
    "Nervous",
    "Determined",
    "Attentive",
    "Jittery",
    "Active",
    "Afraid"],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def statePANASX(win=None, saveFile=None, scaleName="panasx_state", subjNum=0, endPause=1.0):
    """ State Positive and Negative Affect Schedule - Extended (PANASX; Watson et al., 1994)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["This scale consists of a number of words and phrases that describe different feelings and emotions. Read each item and then use the scale to indicate to what extent you feel this way RIGHT NOW, that is, AT THE PRESENT MOMENT."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(5):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-5
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-5

    secondaryLabels = ["Very slightly or not at all", "A little", "Moderately", "Quite a bit", "Extremely"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.45, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["Cheerful",
    "Disgusted",
    "Attentive",
    "Bashful",
    "Sluggish",
    "Daring",
    "Surprised",
    "Strong",
    "Scornful",
    "Relaxed",
    "Irritable",
    "Delighted",
    "Inspired",
    "Fearless",
    "Disgusted with self",
    "Sad",
    "Calm",
    "Afraid",
    "Tired",
    "Amazed",
    "Shaky",
    "Happy",
    "Timid",
    "Alone",
    "Alert",
    "Upset",
    "Angry",
    "Bold",
    "Blue",
    "Shy",
    "Active",
    "Guilty",
    "Joyful",
    "Nervous",
    "Lonely",
    "Sleepy",
    "Excited",
    "Hostile",
    "Proud",
    "Jittery",
    "Lively",
    "Ashamed",
    "At ease",
    "Scared",
    "Drowsy",
    "Angry at self",
    "Enthusiastic",
    "Downhearted",
    "Sheepish",
    "Distressed",
    "Blameworthy",
    "Determined",
    "Frightened",
    "Astonished",
    "Interested",
    "Loathing",
    "Confident",
    "Energetic",
    "Concentrating",
    "Dissatisfied with self"],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def prioritizingHappinessScale(win=None, saveFile=None, scaleName="phs", subjNum=0, endPause=1.0):
    """ Prioritizing Happiness Scale (PHS; Catalino et al., 2014)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["We consider positive emotions to include amusement, awe, excitement, gratitude, hope, interest, joy, love, pride, serenity, and contentment. Using the scale, please select a response from 1 to 9 indicating your agreement with each statement."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(9):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-9
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-9

    secondaryLabels = ["disagree strongly", "disagree mostly", "disagree somewhat", "disagree slightly", "neither agree nor disagree", "agree slightly", "agree somewhat", "agree mostly", "agree strongly"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.9, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.20, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["A priority for me is experiencing happiness in everyday life.",
    "I look for and nurture my positive emotions.",
    "What I decide to do with my time outside of work is influenced by how much I might experience positive emotions.",
    "I structure my day to maximize my happiness.",
    "My major decisions in life (e.g., the job I choose, the house I buy) are influenced by how much I might experience positive emotions.",
    "I admire people who make their decisions based on the happiness they will gain."],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def rangeAndDifferentiationOfEmotionalExperienceScale(win=None, saveFile=None, scaleName="rdees", subjNum=0, endPause=1.0):
    """ Range and Differentiation of Emotional Experience Scale (RDEES; Kang & Shaver, 2004)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["Please rate how well each of the following statements describes you."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(5):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-5
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-5

    secondaryLabels = ["Does not describe me very well", "", "", "", "Describes me very well"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.20, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["I don't experience many different feelings in everyday life.",
    "I am aware of the different nuances or subtleties of a given emotion.",
    "I have experienced a wide range of emotions throughout my life.",
    "Each emotion has a very distinct and unique meaning to me.",
    "I usually experience a limited range of emotions.",
    "I tend to draw fine distinctions between similar feelings (e.g., depressed and blue; annoyed and irritated).",
    "I experience a wide range of emotions.",
    "I am aware that each emotion has a completely different meaning.",
    "I don't experience a variety of feelings on an everyday basis.",
    "If emotions are viewed as colors, I can notice even small variations within one kind of color (emotion).",
    "Feeling good or bad - those terms are sufficient to describe most of my feelings in everyday life.",
    "I am aware of the subtle differences between feelings I have.",
    "I tend to experience a broad range of emotions throughout my life.",
    "I am good at distinguishing subtle differences in the meaning of closely related emotion words."],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def rationalExperientialInventory(win=None, saveFile=None, scaleName="rei", subjNum=0, endPause=1.0):
    """ Rational Experiential Inventory (REI; Pancini & Epstein, 1999)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["Please indicate your agreement with the following statements by pressing the appropriate number."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(5):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-5
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-5

    secondaryLabels = ["Completely False", "", "", "", "Completely True"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.45, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["I have a logical mind.",
    "I prefer complex problems to simple problems.",
    "I believe in trusting my hunches.",
    "I am not a very analytical thinker.",
    "I trust my initial feelings about people.",
    "I try to avoid situations that require thinking in depth about something.",
    "I like to rely on my intuitive impressions.",
    "I don't reason well under pressure.",
    "I don't like situations in which I have to rely on intuition.",
    "Thinking hard and for a long time about something gives me little satisfaction.",
    "Intuition can be a very useful way to solve problems.",
    "I would not want to depend on anyone who described himself or herself as intuitive.",
    "I am much better at figuring things out logically than most people.",
    "I usually have clear, explainable reasons for my decisions.",
    "I don't think it is a good idea to rely on one's intuition for important decisions.",
    "Thinking is not my idea of an enjoyable activity.",
    "I have no problem thinking things through carefully.",
    "When it comes to trusting people, I can usually rely on my gut feelings.",
    "I can usually feel when a person is right or wrong, even if I can't explain how I know.",
    "Learning new ways to think would be very appealing to me.",
    "I hardly ever go wrong when I listen to my deepest gut feelings to find an answer.",
    "I think it is foolish to make important decisions based on feelings.",
    "I tend to use my heart as a guide for my actions.",
    "I often go by my instincts when deciding on a course of action.",
    "I'm not that good at figuring out complicated problems.",
    "I enjoy intellectual challenges.",
    "Reasoning things out carefully is not one of my strong points.",
    "I enjoy thinking in abstract terms.",
    "I generally don't depend on my feelings to help me make decisions.",
    "Using logic usually works well for me in figuring out problems in my life.",
    "I think there are times when one should rely on one's intuition.",
    "I don't like to have to do a lot of thinking.",
    "Knowing the answer without having to understand the reasoning behind it is good enough for me.",
    "Using my gut feelings usually works well for me in figuring out problems in my life.",
    "I don't have a very good sense of intuition.",
    "If I were to rely on my gut feelings, I would often make mistakes.",
    "I suspect my hunches are inaccurate as often as they are accurate.",
    "My snap judgements are probably not as good as most people's.",
    "I am not very good at solving problems that require careful logical analysis.",
    "I enjoy solving problems that require hard thinking."],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def religiousFundamentalismScale(win=None, saveFile=None, scaleName="rfs", subjNum=0, endPause=1.0):
    """ Religious Fundamentalism Scale -- Revised (Altemeyer & Hunsberger, 2004)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["This survey is a part of an investigation of general public opinion concerning a variety of social issues. You will probably find that you agree with some of the statements, and disagree with others to varying extents. Please indicate your reaction to each statement according to the scale.\n\nYou may find that you sometimes have different reactions to different parts of a statement. For example, you might very strongly disagree (\"-4\") with one idea in a statement, but slightly agree (\"+1\") with another idea in the same item. When this happens, please combine your reactions, and mark how you feel on balance (a \"-3\" in this case)."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(9):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-8
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-8

    secondaryLabels = ["Very Strongly Disagree\n-4", "Strongly Disagree\n-3", "Moderately Disagree\n-2", "Slightly Disagree\n-1", "Slightly Agree\n+1", "Moderately Agree\n+2", "Strongly Agree\n+3", "Very Strongly Agree\n+4"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.45, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["God has given humanity a complete, unfailing guide to happiness and salvation, which must be totally followed.",
    "No single book of religious teachings contains all the intrinsic, fundamental truths about life.",
    "The basic cause of evil in this world is Satan, who is still constantly and ferociously fighting against God.",
    "It is important to be a good person than to believe in God and the right religion.",
    "There is a particular set of religious teachings in this world that are so true, you can't go any \"deeper\" because they are the basic, bedrock message that God has given humanity.",
    "When you get right down to it, there are basically only two kinds of people in the world: the Righteous, who will be rewarded by God; and the rest, who will not.",
    "Scriptures may contain general truths, but they should NOT be considered completely, literally true from beginning to end.",
    "To lead the best, most meaningful life, one must belong to the one, fundamentally true religion.",
    "\"Satan\" is just the name people give to their own bad impulses. There really is no such thing as a diabolical \"Prince of Darkness\" who tempts us.",
    "Whenever science and sacred scripture conflict, science is probably right.",
    "The fundamentals of God's religion should never be tampered with, or compromised with others\' beliefs.",
    "All of the religions in the world have flaws and wrong teachings. There is no perfectly true, right religion."],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def rosenbergSelfEsteem(win=None, saveFile=None, scaleName="rse", subjNum=0, endPause=1.0, version="trait"):
    """ Rosenberg Self-Esteem

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
            version [string]: String equal to either "trait" (default) or "state". Changes scale instructions accordingly.
    """

    if version == "trait":
        # display scale instructions
        gf.show_instructs(win=win,
        text=["The following statements concern your perceptions of yourself. We are interested in how you GENERALLY FEEL. Respond to each statement by indicating how much you agree or disagree with it."],
        timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])
    elif version == "state":
        # display scale instructions
        gf.show_instructs(win=win,
        text=["The following statements concern your perceptions of yourself. We are interested in how you RIGHT NOW. Respond to each statement by indicating how much you agree or disagree with it."],
        timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(7):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-7
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-7

    secondaryLabels = ["Strongly Disagree", "", "", "Neutral/Mixed", "", "", "Strongly Agree"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.45, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["I feel that I am a person of worth, at least on an equal plane with others.",
    "I feel like a person who has a number of good qualities.",
    "All in all, I am inclined to feel like a failure.",
    "I fell as if I am able to do things as well as most other people.",
    "I feel as if I do not have much to be proud of.",
    "I take a positive attitude toward myself.",
    "On the whole, I am satisfied with myself.",
    "I wish that I could have more respect for myself.",
    "I certainly feel useless at times.",
    "At times I think that I am no good at all."],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def staxi2AngerExpression(win=None, saveFile=None, scaleName="staxi2_ax", subjNum=0, endPause=1.0):
    """ State Trait Anger Expression Inventory - 2 -- Anger Expression (Spielberger, 1999)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["Read each of the following statements that people have used to describe themselves, and then indicate using the scale how you generally feel or react. There are no right or wrong answers. Do not spend too much time on any one statement. Respond to what best describes how you generally feel or react."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(4):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-5
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-5

    secondaryLabels = ["Not at all", "Somewhat", "Moderately so", "Very much so"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.45, win=win, bold=True)

    # display scale instructions
    gf.show_instructs(win=win,
    text=["How I generally react or behave when angry or furious:"],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # run scale
    results = run_scale_items(win=win,
    scaleItems=['I control my temper.',
    'I express my anger.',
    'I take a deep breath and relax.',
    'I keep things in.',
    'I am patient with others.',
    'If someone annoys me, I\'m apt to tell him or her how I feel.',
    'I try to calm myself as soon as possible.',
    'I pout or sulk.',
    'I control my urge to express my angry feelings.',
    'I lose my temper.',
    'I try to simmer down.',
    'I withdraw from people.',
    'I keep my cool.',
    'I make sarcastic remarks to others.',
    'I try to soothe my angry feelings.',
    'I boil inside, but I don\'t show it.',
    'I control my behavior.',
    'I do things like slam doors.',
    'I endeavor to become calm again.',
    'I tend to harbor grudges that I don\'t tell anyone about.',
    'I can stop myself from losing my temper.',
    'I argue with others.',
    'I reduce my anger as soon as possible.',
    'I am secretly quite critical of others.'],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)


    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def staxi2StateAnger(win=None, saveFile=None, scaleName="staxi2_sa", subjNum=0, endPause=1.0):
    """ State Trait Anger Expression Inventory - 2 -- State Anger (Spielberger, 1999)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["A number of statements that people use to describe themselves are given in the following. Read each statement and then indicate using the scale how you feel right now. There are no right or wrong answers. Do not spend too much time on any one statement. Respond to what best describes your present feelings."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(4):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-5
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-5

    secondaryLabels = ["Not at all", "Somewhat", "Moderately so", "Very much so"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.45, win=win, bold=True)

    # display scale instructions
    gf.show_instructs(win=win,
    text=["How I feel right now:"],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # run scale
    results = run_scale_items(win=win,
    scaleItems=['I am furious.',
    'I feel irritated.',
    'I feel angry.',
    'I feel like yelling at somebody.',
    'I feel like breaking things.',
    'I am mad.',
    'I feel like banging on the table.',
    'I feel like hitting someone.',
    'I feel like swearing.',
    'I feel annoyed.',
    'I feel like kicking somebody.',
    'I feel like cursing out loud.',
    'I feel like screaming.',
    'I feel like pounding somebody.',
    'I feel like shouting out loud.'],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)


    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def staxi2TraitAnger(win=None, saveFile=None, scaleName="staxi2_ta", subjNum=0, endPause=1.0):
    """ State Trait Anger Expression Inventory - 2 -- Trait Anger (Spielberger, 1999)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["Read each of the following statements that people have used to describe themselves, and then indicate using the scale how you generally feel or react. There are no right or wrong answers. Do not spend too much time on any one statement. Respond to what best describes how you generally feel or react."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(4):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-5
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-5

    secondaryLabels = ["Not at all", "Somewhat", "Moderately so", "Very much so"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.45, win=win, bold=True)

    # display scale instructions
    gf.show_instructs(win=win,
    text=["How I generally feel:"],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # run scale
    results = run_scale_items(win=win,
    scaleItems=['I am quick tempered.',
    'I have a fiery temper.',
    'I am a hotheaded person.',
    'I get angry when I\'m  slowed down by others\' mistakes.',
    'I feel annoyed when I am not given recognition for doing good work.',
    'I fly off the handle.',
    'When I get mad, I say nasty things.',
    'It makes me furious when I am criticized in front of others.',
    'When I get frustrated, I feel like hitting someone.',
    'I feel infuriated when I do a good job and get a poor evaluation.'],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)


    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def staiStateAnxiety(win=None, saveFile=None, scaleName="stai_sa", subjNum=0, endPause=1.0):
    """ State Trait Anxiety Inventory - State Anxiety (Spielberger et al., 1983)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["A number of statements which people have used to describe themselves are given in the following. Read each statement and then indicate using the scale how you feel right now, that is, at this moment. There are no right or wrong answers. Do not spend too much time on any one statement but give the answer which seems to describe your present feelings best."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(4):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-5
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-5

    secondaryLabels = ["Not At All", "Somewhat", "Moderately So", "Very Much So"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.45, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["I feel calm.",
    "I feel secure.",
    "I am tense.",
    "I feel strained.",
    "I feel at ease.",
    "I feel upset.",
    "I am presently worrying over possible misfortunes.",
    "I feel satisfied.",
    "I feel frightened.",
    "I feel comfortable.",
    "I feel self-confident.",
    "I feel nervous.",
    "I am jittery.",
    "I feel indecisive.",
    "I am relaxed.",
    "I feel content.",
    "I am worried.",
    "I feel confused.",
    "I feel steady.",
    "I feel pleasant."],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def torontoAlexithymiaScale(win=None, saveFile=None, scaleName="tas", subjNum=0, endPause=1.0):
    """ Toronto Alexithymia Scale (TAS; Parker et al., 2001)

        Args:
            win [visual.Window object]: Provide the window object to use.
            saveFile [string]: Provide string for file to output questionnaire data.
            scaleName [string]: Abbreviation to be used to label scale items in the data output.
            subjNum [integer]: Subject's ID number.
            endPause [float]: Length of pause to insert at the end of the questionnaire (without one, the questionnaires may blend together).
    """
    # display scale instructions
    gf.show_instructs(win=win,
    text=["Please use the scale to indicate your agreement with each of the following statements."],
    timeAutoAdvance=0, timeRequired=0, advanceKey=['space'])

    # create response keys
    respKeys = []  # initialize list of response keys that subjects can use
    primaryLabels = []  # initialize list of primary response labels to be displayed on screen
    secondaryLabels = []  # initialize list of secondary response labels to be displayed on screen
    for i in range(5):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-5
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-5

    secondaryLabels = ["Completely Disagree", "Disagree", "Neutral", "Agree", "Completely Agree"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.05,
                                         secondaryWrapWidth=0.20, win=win, bold=True)

    # run scale
    results = run_scale_items(win=win,
    scaleItems=["I am often confused about what emotion I am feeling.",
    "It is difficult for me to find the right words for my feelings.",
    "I have physical sensations that even doctors don't understand.",
    "I am able to describe my feelings easily.",
    "I prefer to analyze problems rather than just describe them.",
    "When I am upset, I don't know if I am sad, frightened, or angry.",
    "I am often puzzled by sensations in my body.",
    "I prefer to just let things happen rather than to understand why they turned out that way.",
    "I have feelings that I can't quite identify.",
    "Being in touch with emotions is essential.",
    "I find it hard to describe how I feel about people.",
    "People tell me to describe my feelings more.",
    "I don't know what's going on inside me.",
    "I often don't know why I am angry.",
    "I prefer talking to people about their daily activities rather than their feelings.",
    "I prefer to watch \"light\" entertainment shows rather than psychological dramas.",
    "It is difficult for me to reveal my innermost feelings, even to close friends.",
    "I can feel close to someone, even in moments of silence.",
    "I find examination of my feelings useful in solving personal problems.",
    "Looking for hidden meanings in movies or plays distracts from their enjoyment."],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)



#==============================================================================#
# DEMOGRAPHICS QUESTIONS


def race(win=None, saveFile=None, scaleName="race", subjNum=0, endPause=1.0):
    """ Participant race

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
    for i in range(7):
        respKeys.insert(i, str(i+1))  # response keys are number keys 1-9
        primaryLabels.insert(i, str(i+1))  # primary labels are 1-9

    secondaryLabels = ["WHITE", "BLACK OR AFRICAN", "ASIAN INDIAN", "NATIVE AMERICAN OR ALASKAN NATIVE", "EAST ASIAN", "PACIFIC ISLANDER", "OTHER"]  # secondary labels

    # generate TextStim for response options
    respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                         scaleWidth=0.5, primaryPos=-0.4, primaryHeight=0.06, secondaryPos=-0.3, secondaryHeight=0.06,
                                         secondaryWrapWidth=1.0, secondaryAlign="left", win=win, bold=True, horiz=False, offset=0)


    # run scale
    results = run_multi_response(win=win,
    scaleItems=["What is your race? Select all that apply."],
    respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

    # save output file if saveFile provided
    if saveFile is not None:
        results.to_csv(saveFile, header = True, mode = 'w', index = False)

    win.flip()
    core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def sex(win=None, saveFile=None, scaleName="sex", subjNum=0, endPause=1.0):
        """ Participant sex

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
        for i in range(2):
            respKeys.insert(i, str(i+1))  # response keys are number keys 1-2
            primaryLabels.insert(i, str(i+1))  # primary labels are 1-2

        secondaryLabels = ["Male", "Female"]  # secondary labels

        # generate TextStim for response options
        respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                             scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.08,
                                             secondaryWrapWidth=0.20, win=win, bold=True)

        # run scale
        results = run_scale_items(win=win,
        scaleItems=["Sex:"],
        respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

        # save output file if saveFile provided
        if saveFile is not None:
            results.to_csv(saveFile, header = True, mode = 'w', index = False)

        win.flip()
        core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def engFirst(win=None, saveFile=None, scaleName="engFirst", subjNum=0, endPause=1.0):
        """ English as first language

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
        for i in range(2):
            respKeys.insert(i, str(i+1))  # response keys are number keys 1-2
            primaryLabels.insert(i, str(i+1))  # primary labels are 1-2

        secondaryLabels = ["Yes", "No"]  # secondary labels

        # generate TextStim for response options
        respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                             scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.08,
                                             secondaryWrapWidth=0.20, win=win, bold=True)

        # run scale
        results = run_scale_items(win=win,
        scaleItems=["Is English your primary language?"],
        respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

        # save output file if saveFile provided
        if saveFile is not None:
            results.to_csv(saveFile, header = True, mode = 'w', index = False)

        win.flip()
        core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def engFluency(win=None, saveFile=None, scaleName="engFluency", subjNum=0, endPause=1.0):
        """ English fluency

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
        for i in range(7):
            respKeys.insert(i, str(i+1))  # response keys are number keys 1-2
            primaryLabels.insert(i, str(i+1))  # primary labels are 1-2

        secondaryLabels = ["Not at all fluent", "", "", "", "", "", "Perfect fluency"]  # secondary labels

        # generate TextStim for response options
        respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                             scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.08,
                                             secondaryWrapWidth=0.20, win=win, bold=True)

        # run scale
        results = run_scale_items(win=win,
        scaleItems=["How fluent is your English?"],
        respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

        # save output file if saveFile provided
        if saveFile is not None:
            results.to_csv(saveFile, header = True, mode = 'w', index = False)

        win.flip()
        core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)


def howSerious(win=None, saveFile=None, scaleName="howSerious", subjNum=0, endPause=1.0):
        """ How seriously did the participant take the experiment

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
        for i in range(7):
            respKeys.insert(i, str(i+1))  # response keys are number keys 1-7
            primaryLabels.insert(i, str(i+1))  # primary labels are 1-7

        secondaryLabels = ["Not at all", "", "", "", "", "", "Extremely"]  # secondary labels

        # generate TextStim for response options
        respOptions = gf.generate_resp_scale(respKeys=respKeys, primaryLabels=primaryLabels, secondaryLabels=secondaryLabels,
                                             scaleWidth=0.6, primaryPos=-0.4, secondaryPos=-0.25, secondaryHeight=0.08,
                                             secondaryWrapWidth=0.5, win=win, bold=True)

        # run scale
        results = run_scale_items(win=win,
        scaleItems=["In all honesty, how seriously did you take this experiment? Note that your response will not affect your compensation in any way."],
        respScale=respOptions, respKeys=respKeys, scaleName=scaleName, subjNum=subjNum)

        # save output file if saveFile provided
        if saveFile is not None:
            results.to_csv(saveFile, header = True, mode = 'w', index = False)

        win.flip()
        core.wait(endPause)  # insert a pause before concluding (gives a brief pause to signal the end of one questionnaire and the start of the next; otherwise they run together)
