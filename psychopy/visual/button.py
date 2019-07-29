#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Creates a button"""

# Part of the PsychoPy library
# Copyright (C) 2018 Jonathan Peirce
# Distributed under the terms of the GNU General Public License (GPL).

from __future__ import absolute_import, print_function

from psychopy import event
from psychopy.visual.shape import BaseShapeStim
from psychopy.visual.text import TextStim

__author__ = 'Anthony Haffey'

class ButtonStim(BaseShapeStim):
    """A class for putting a button into your experiment.

    """

    def __init__(self,
                 win,
                 borderThickness=.003,
                 labelSize=0.03,
                 pos=(0, 0),
                 labelText="text for button",
                 textColor='blue',
                 borderColor='blue',
                 buttonColor='white',
                 buttonEnabled=False,
                 disabledButtonColor='dimgrey',
                 disabledBorderColor='darkgrey',
                 disabledTextColor='darkgrey',
                 widthInCharsLen=0
                 ):


        # local variables
        super(ButtonStim, self).__init__(win)
        
        self.win = win
        self.borderThickness = borderThickness
        self.labelSize = labelSize
        self.pos = pos
        self.labelText = labelText
        self.textColor = textColor
        self.borderColor = borderColor
        self.buttonColor = buttonColor
        self.buttonEnabled = buttonEnabled
        
        self.widthInCharsLen = widthInCharsLen

        self.disabledButtonColor = disabledButtonColor
        self.disabledBorderColor = disabledBorderColor
        self.disabledTextColor = disabledTextColor
              

        self._dragging = False
        self.mouse = event.Mouse()
        self.buttonSelected = False
        
        self.createButtonUIComponents()

    def draw(self):
        self.getMouseResponses()
        for item in self.buttonItems:
            item.draw()

    def createButtonUIComponents(self):
        self.buttonItems = []

        borderC = self.borderColor
        buttonC = self.buttonColor
        textC = self.textColor

        if (self.buttonEnabled == False):
            borderC = self.disabledBorderColor
            buttonC = self.disabledButtonColor
            textC = self.disabledTextColor

        widthC = self.widthInCharsLen
        if (widthC == 0):
            widthC = len(self.labelText)

        button_width = widthC * .025
        button_x_inner_margin = .02
        button_x_outer_margin = button_x_inner_margin + self.borderThickness
        button_y_inner_margin = self.labelSize
        button_y_outer_margin = self.labelSize + self.borderThickness
        button_x_range = (0 - button_width / 2 + self.pos[0], 0 + button_width / 2 + self.pos[0])

        self.buttonBorder = BaseShapeStim(self.win, fillColor=borderC, vertices=(
            (button_x_range[0] - button_x_outer_margin, -button_y_outer_margin + self.pos[1]),
            (button_x_range[0] - button_x_outer_margin, button_y_outer_margin + self.pos[1]),
            (button_x_range[1] + button_x_outer_margin, button_y_outer_margin + self.pos[1]),
            (button_x_range[1] + button_x_outer_margin, -button_y_outer_margin + self.pos[1])))
        self.buttonInner = BaseShapeStim(self.win, fillColor=buttonC, vertices=(
            (button_x_range[0] - button_x_inner_margin, -button_y_inner_margin + self.pos[1]),
            (button_x_range[0] - button_x_inner_margin, button_y_inner_margin + self.pos[1]),
            (button_x_range[1] + button_x_inner_margin, button_y_inner_margin + self.pos[1]),
            (button_x_range[1] + button_x_inner_margin, -button_y_inner_margin + self.pos[1])))
        self.buttonInnerText = TextStim(self.win, text=self.labelText, color=textC, pos=self.pos,
                                               height=self.labelSize)
        self.buttonItems.append(self.buttonBorder)
        self.buttonItems.append(self.buttonInner)
        self.buttonItems.append(self.buttonInnerText)

    def buttonSwitch(self, switch):
        if switch:
            self.buttonBorder.color = self.buttonColor
            self.buttonInner.color = self.borderColor
            self.buttonInnerText.color = self.buttonColor
        else:
            self.buttonBorder.color = self.borderColor
            self.buttonInner.color = self.buttonColor
            self.buttonInnerText.color = self.borderColor

    def buttonContains(self, mouse):
        return self.buttonBorder.contains(mouse)

    def buttonClicked(self, mouse):
        self.buttonSelected = bool(self.buttonContains(mouse)
                                   and mouse.getPressed()[0])
        return self.buttonSelected
        
    def setDisabledColors(self, disabledButtonColor='dimgrey',
                 disabledBorderColor='darkgrey',
                 disabledTextColor='darkgrey'):
        self.disabledButtonColor = disabledButtonColor
        self.disabledBorderColor = disabledBorderColor
        self.disabledTextColor = disabledTextColor
        self.buttonGuard(self.buttonEnabled)

    def setEnabledColors(self, buttonColor='dimgrey',
                 borderColor='darkgrey',
                 textColor='darkgrey'):
        self.buttonColor = buttonColor
        self.borderColor = borderColor
        self.textColor = textColor
        self.buttonGuard(self.buttonEnabled)

    def setButtonText(self, aText):
        self.labelText = aText
        self.buttonInnerText.setText(self.labelText)

    def getButtonText(self):
        return self.labelText

    def buttonGuard(self, condition):
        if not self.buttonEnabled:
            self.buttonBorder.color = self.disabledBorderColor
            self.buttonInner.color = self.disabledButtonColor
            self.buttonInnerText.color = self.disabledTextColor
        else:
            self.buttonBorder.color = self.buttonColor
            self.buttonInner.color = self.borderColor
            self.buttonInnerText.color = self.buttonColor

    def getMouseResponses(self):
        self.buttonGuard(self.buttonEnabled)
        if not self.buttonEnabled:
            return

        if not self.buttonClicked(self.mouse):  # hovering
            self.buttonSwitch(self.buttonContains(self.mouse))

        if self.buttonClicked(self.mouse):
            self._dragging = True
            # Update current but don't set Rating (mouse is still down)
            # Dragging has to start inside a "valid" area (i.e., on the
            # slider), but may continue even if the mouse moves away from
            # the slider, as long as the mouse button is not released.
        else:  # mouse is up - check if it *just* came up
            if self._dragging:
                if self.buttonContains(self.mouse):
                    self.buttonSelected = True
                self._dragging = False
            else:
                # is up and was already up - move along
                return None

