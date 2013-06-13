import logging
import argparse
import sys


parser = argparse.ArgumentParser(description='ProteinPrediction by Group 23 \n\
\n\
Filesplitter')
parser.add_argument('-a', metavar='arff file', dest='arff', required=True, help='the arf file to split')
args = parser.parse_args()


try:
    with open(args.arff): pass
except IOError:
    print 'Specified arff file does not exist!'
    sys.exit(1)



FILE_NAME = 'tmps.arff'
FILE_NAME_PARTS = FILE_NAME.split('.')
FILE_COUNT = 3

loggers = []


""" 
    clear the existing files and initialize one logger per file
"""
for i in range(0, FILE_COUNT):
    
    file_name = FILE_NAME_PARTS[0] + '_' + str(i) + '.' + FILE_NAME_PARTS[1]
    
    """ clear the old files """
    with open(file_name, 'w'):
        pass
    
    """ init the loggers """
    logger = logging.getLogger(file_name)
    hdlr = logging.FileHandler(file_name)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.INFO)
    
    
    loggers.append(logger)
    
    
    
    
"""
    read from the big file
    some rules:
    1) Log the lines into all logfiles, until the line @DATA appears (mode = -1)
    2) now rotate btw the logfiles, rotate everytime the proteinkey changes (mode = 0/1/2)
    3) A protein key change happens e.g. if CY1_RHOCA_XX changes to STS_HUMAN_XX
"""
file_handle = open(FILE_NAME, "r")
mode = -1
protein_key = ''

for line in file_handle:
    
    if mode != -1:
        """ input: CY1_RHOCA_99,0.8xxxx  output: CY1_RHOCA """
        s = line[0:(line.find(','))]
        current_protein_key = s[0:(s.rfind('_'))]
        if current_protein_key != protein_key:
            protein_key = current_protein_key
            mode = (mode + 1) % FILE_COUNT 
            
        loggers[mode].info(line.strip())
    
    elif mode == -1:
        loggers[0].info(line.strip())
        loggers[1].info(line.strip())
        loggers[2].info(line.strip())
    
    if line.strip() == '@DATA':
        mode = 0
        

file_handle.close()

print "splitting ..."

