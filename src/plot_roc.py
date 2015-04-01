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
Plots several ROCs given a configuration file
"""

import sys
import argparse
import numpy as np
import auceval
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

def read_config_file(config):
    """
    Gets answer files, plot label and groundtruth file from a given 
    configuration file.

    Format: 
    answer_filepath1:plot_label1
    answer_filepath2:plot_label2
    answer_filepath3:plot_label3
    ..
    answer_filepathN:plot_labelN
    --
    groundtruth_filepath
    """

    with open(config,'r') as f:
        text = f.readlines()
        answer_filepaths = []
        truth_filepath = ""
        for i in range(len(text)):
            text[i] = text[i].strip()
            if text[i] == "--":
                truth_filepath = text[i + 1].strip()
                break
            else:
                answer = text[i].split(":")
                answer_filepaths.append(answer)

    return answer_filepaths, truth_filepath

def plot_roc(config, showfig, figfile):
    """
    Plot ROC for several answer lists
    """

    plot_style = ['-', '--', '-.', ':']
    answer_filepaths, truth_filepath = read_config_file(config)
    truth =  auceval.read_truth(truth_filepath)
    plots = []
    pltlabels = []
    for i in range(len(answer_filepaths)):
        answers = auceval.read_answers(answer_filepaths[i][0])
        fprate, tprate, auc =  auceval.compute_auc(answers, truth)

        style = i % len(plot_style)
        plot, = plt.plot(fprate, tprate, plot_style[style])
        
        plots.append(plot)
        pltlabels.append(answer_filepaths[i][1])
        
        print "===================================="
        print answer_filepaths[i][0]
        print "AUC = ", auc

    plt.legend(plots, pltlabels)

    if figfile:
        plt.savefig(figfile, format='pdf')

    if showfig:
        plt.show()

        
def main():
    try:
        parser = argparse.ArgumentParser()
        parser = argparse.ArgumentParser(
            description="Plots several ROCs given a configuration file")
        parser.add_argument("config", type=str, 
                            help="configuration file")
        parser.add_argument('-f', '--fig', dest='fig', action='store_true',
                            help="show figure")
        parser.set_defaults(fig=False)
        parser.add_argument("-s", "--save", type=str, default="",
                            help="file where to save the figure")
        args = parser.parse_args()
        if args.config:
            plot_roc(args.config, args.fig, args.save)
        
    except SystemExit:
        print "for help use --help"
        sys.exit(2)

if __name__ == "__main__":
    main()
