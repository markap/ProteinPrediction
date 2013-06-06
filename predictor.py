import argparse


parser = argparse.ArgumentParser(description='ProteinPrediction by Group 23 \n\
\n\
prediction program')
parser.add_argument('-p', metavar='wekapath', dest='WEKA_PATH', required=True, help='points to the weka executable e.g. /mnt/opt/data/pp1_13_exercise/weka-3-6-9/weka.jar')
parser.add_argument('-a', metavar='arff file', dest='arff', required=True, help='arff file for predictions')
args = parser.parse_args()


try:
   with open(args.WEKA_PATH): pass
except IOError:
   print 'Path to weka is invalid!'
   sys.exit(1)
try:
   with open(args.arff): pass
except IOError:
   print 'Specified arff file does not exist!'
   sys.exit(1)
try:
   with open(my.model): pass
except IOError:
   print 'Model file does not exist! Please run model_creator first.'
   sys.exit(1)

