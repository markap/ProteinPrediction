
result = 'result'

original_file = 'tmps_independent.arff'

file_handle = open(result, "r")

predictions = []

for line in file_handle:
    if line.find('>') == -1:
	predictions += list(line.strip())


file_handle.close()

file_handle = open(original_file, "r");

header_mode = True

right = 0.0
wrong = 0.0

i = 0
for line in file_handle:
    if header_mode == False:
	original_value = line.strip()[-1:]
	
	predicted_value = predictions[i]

	if original_value == predicted_value:
	    right += 1
	else:
	    wrong += 1

	i += 1
        
            
    if line.strip() == '@DATA':
        header_mode = False
 	

file_handle.close()

print right
print wrong
	

print right / (right + wrong)
