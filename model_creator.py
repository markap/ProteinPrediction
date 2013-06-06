import subprocess
import shared



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

