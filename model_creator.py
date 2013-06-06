import argparse
import subprocess
import shared

"""

parser = argparse.ArgumentParser(description='ProteinPrediction by Group 23 \n\
\n\
given c and gamma values, this program creates a model file for later predictions.')
parser.add_argument('-p', metavar='wekapath', dest='WEKA_PATH', required=True, help='points to the weka executable e.g. /mnt/opt/data/pp1_13_exercise/weka-3-6-9/weka.jar')
parser.add_argument('-c', metavar='Value c', dest='cValue', required=True, help='c value')
parser.add_argument('-g', metavar='Value gamma', dest='gammaValue', required=True, help='gamma value')
parser.add_argument('-a', metavar='arff file', dest='arff', required=True, help='the arf file c and gamma is calculated for')
args = parser.parse_args()

try:
   with open(args.WEKA_PATH): pass
except IOError:
   print 'Path to weka is invalid!'
   sys.exit(1)
try:
   with open(args.arff): pass
except IOError:
   print 'Arff file not found!'
   sys.exit(1)
try:
   with open(my.model): pass
except IOError:
   print 'Model file already exists!'
   sys.exit(1)


"""

c = 1
gamma = 1
train_in = "tmps_0.arff"

print "build a new model ..."
print "filter files first ..."
filtered_file = "filtered.arff"
subprocess.call(shared.filter_by_index(train_in, filtered_file))
print "files filterd! build model ..."
print subprocess.check_output(shared.store_model_command(filtered_file, shared.MODEL_NAME, c, gamma))
print "done!"

