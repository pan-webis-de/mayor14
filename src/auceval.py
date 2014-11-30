#!/usr/bin/env python
# -*- coding: utf-8
#
# Gibran Fuentes Pineda <gibranfp@turing.iimas.unam.mx>
# IIMAS, UNAM
# 2014
#
# -------------------------------------------------------------------------
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# -------------------------------------------------------------------------
"""
Functions to compute the AUC 
"""

import numpy as np

def polyarea(vertices):
    """
    Computes de area of a polygon given a set of vertices as xy values using
    Shoelace formula
    """
    area = 0.0
    vnum = len(vertices)
    for i in range(vnum - 1):
        area = area + vertices[i][0] * vertices[i+1][1]
        area = area - vertices[i+1][0] * vertices[i][1]

    area = area + vertices[vnum - 1][0] * vertices[0][1]
    area = area - vertices[0][0] * vertices[vnum - 1][1]

    return 0.5 * abs(area)

def read_answers(answer_filepath):
    """
    Reads answer list from a file.

    Format: 
    ProblemID1 Confidence1
    ProblemID2 Confidence2
    ProblemID3 Confidence3
    ...
    ProblemIDN ConfidenceN
    """
    answers = []
    with open(answer_filepath,'r') as text:
        for line in text:
            problem, confidence = line.split()
            answers.append(float(confidence))
    return answers

def read_truth(truth_filepath):
    """
    Reads groundtruth from a file.

    Format: 
    ProblemID1 Y/N
    ProblemID2 Y/N
    ProblemID3 Y/N
    ...
    ProblemIDN Y/N
    """
    truth = []
    with open(truth_filepath,'r') as text:
        for line in text:
            problem, answer = line.split()
            if answer == "Y":
                truth.append(1)
            else:
                truth.append(0)
    return truth

def compute_auc(answers, truth):
    """
    Computes auc based on given answers and groundtruth.
    """

    answers = np.array(answers)
    truth = np.array(truth)
    order = np.argsort(answers)[::-1]
    answers = answers[order]
    truth = truth[order]
    
    auc = 0.0
    fpnum = 0.0
    tpnum = 0.0
    falsepos = np.zeros(1)
    truepos = np.zeros(1)
    prev_answer = -np.inf
    fpprev = 0.0
    tpprev = 0.0

    posnum = np.count_nonzero(truth)
    negnum = truth.size - posnum
    
    for i in range(len(answers)):
        if answers[i] != prev_answer:
            falsepos = np.append(falsepos, fpnum)
            truepos = np.append(truepos, tpnum)

            auc = auc + polyarea([[fpprev, 0], [fpprev, tpprev], [fpnum/negnum, tpnum/posnum], [fpnum/negnum, 0]])

            prev_answer = answers[i]
            fpprev = fpnum/negnum
            tpprev = tpnum/posnum

        if truth[i] == 1:
            tpnum = tpnum + 1
        else:
            fpnum = fpnum + 1
        
    auc = auc + polyarea([[fpprev, 0], [fpprev, tpprev], [1, 1], [1, 0]])
    
    return falsepos/negnum, truepos/posnum, auc
