import argparse
import subprocess
import shared
import sys

parser = argparse.ArgumentParser(description='ProteinPrediction by Group 23 \n\
\n\
given c and gamma values, this program creates a model file for later predictions.')
parser.add_argument('-c', metavar='Value c', dest='cValue', required=True, help='c value')
parser.add_argument('-g', metavar='Value gamma', dest='gammaValue', required=True, help='gamma value')
parser.add_argument('-a', metavar='arff file', dest='arff', required=True, help='the arf file c and gamma is calculated for')
args = parser.parse_args()

try:
    with open(args.arff): pass
except IOError:
    print 'Arff file not found!'
    sys.exit(1)




c = args.cValue
gamma = args.gammaValue
train_in = args.arff

print "build a new model ..."
print "filter files first ..."
filtered_file = "filtered.arff"
subprocess.call(shared.filter_by_index(train_in, filtered_file), shell=True)
print "files filterd! build model ..."
print subprocess.check_output(shared.store_model_command(filtered_file, shared.MODEL_NAME, c, gamma), shell=True)
print "done!"


