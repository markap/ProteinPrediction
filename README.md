Protein Prediction
==================

A Protein Prediction Application written in Python.

The protein prediction package contains four executables:
1) filesplitter.py
2) analyzer.py
3) model_creator.py
4) predictor.py

filesplitter.py
===============
Example: python filesplitter.py -a tmps.arff
Splits an arff file into three smaller files without separating the proteins

analyzer.py
===========
Example: python analyzer.py
Allows you to try out several window length as well as different c and gamma values.
This values are important to create the later model and do the prediction.

model_creator.py
================
Example: python model_creator.py -c 1.0 -g 1.2 -a tmps.arff
Creates a model from given c, gamma and arff file. Filters the arff file first to keep 
only the important values for prediction. Takes some time to build!

predictor.py
============
Example: python predictor.py -a to_predict.arff
Takes an arff file as input, filters it and predicts the transmembrane regions. The output is a sequence
of + (for transmembrane) and - (for not transmembrane)
