# Part of the PsychoPy library
# Copyright (C) 2009 Jonathan Peirce
# Distributed under the terms of the GNU General Public License (GPL).

from _visual import * #to get the template visual component
from os import path

thisFolder = path.abspath(path.dirname(__file__))#the absolute path to the folder containing this path
iconFile = path.join(thisFolder,'movie.png')

class MovieComponent(VisualComponent):
    """An event class for presenting image-based stimuli"""
    def __init__(self, exp, parentName, name='', movie='', 
        units='window units', 
        pos=[0,0], size=[0,0], ori=0, times=[0,1]):
        #initialise main parameters from base stimulus
        VisualComponent.__init__(self,parentName,name=name, units=units, 
                    pos=pos, size=size, ori=ori, times=times)
        self.exp=exp#so we can access the experiment if necess
        self.exp.requirePsychopyLibs(['visual'])
        #params
        #these are normally added but we don't want them for a movie            
        del self.params['colour']
        del self.params['colourSpace']
        self.type='Movie'
        self.params['movie']=Param(movie, valType='str', allowedTypes=[],
            updates='constant', allowedUpdates=['constant','set every repeat'],
            hint="A filename for the movie (including path)")        
            
    def writeInitCode(self,buff):
        buff.writeIndented("%(name)s=visual.MovieStim(win=win, movie=%(movie)s,\n" %(self.params))
        buff.writeIndented("    ori=%(ori)s, pos=%(pos)s, size=%(size)s)\n" %(self.params))
        
  
