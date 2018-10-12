# -*- coding: utf-8 -*-
"""
Script to calculate the maximum strength of a model.
It creates two anybody macros, setting a high applied load. 
This insures linearity. 
It thereby calculates the slope of the curve, and the load were
the max muscle activity is equal to 1.

For details about the concept please read the associated blog post here:
https://anyscript.org/tools/estimating-maximum-model-strength/

For details regarding running anybody simulations from python, please see
this webcast: 
https://www.youtube.com/results?search_query=anybody+webcast+batch

@author: bjkel
"""
import numpy as np
from anypytools import AnyPyProcess
from anypytools.macro_commands import ( Load, OperationRun, Dump, SetValue)

# =============================================================================
folderlist = ['flexion', 'extension', 'push', 'pull',]

macros = []
for load in [250, 255]:
    macros.append([
         Load('Main.main.any'),
         SetValue('Main.ArmModel.Loads.Dumbbell.load', load),
         OperationRun('Main.ArmStudy.InverseDynamics'),
         Dump('Main.ArmStudy.Output.MaxMuscleActivity'),
         Dump('Main.ArmModel.Loads.Dumbbell.load'),
    ])

app = AnyPyProcess(num_processes = 4)
results = app.start_macro(macros, folderlist)

load = []
maxact = []
for data in results:
    load.append(data['.load'])
    maxact.append(data['Activity'])

slope = np.zeros(4)
for i, j in zip([0,1,2,3],[0,2,4,6]):
    slope[i] = (maxact[j+1]-maxact[j])/(load[j+1]-load[j])      

maximum_load = np.zeros(4)
for i, j in zip([0,1,2,3],[0,2,4,6]):
    maximum_load[i] = 1 / slope[i] - maxact[j] / slope[i] + load[0]


''' 
The output of the maximum_load variable are the loads in newton, that 
corresponds to a MaxMuscleActivity of 1, for each of the models.

'''


