import sys
import os

task_dir = sys.argv[1]
task_id = sys.argv[2]
dir_trace_files = os.listdir(task_dir)
print(dir_trace_files)
for trace_file in dir_trace_files:
	print(os.path.join(task_dir, trace_file))