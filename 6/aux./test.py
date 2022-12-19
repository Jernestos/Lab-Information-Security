import sys
import os
trace_files = [f_name for f_name in os.listdir(".") if os.path.isfile(os.path.join(".", f_name))]

print(trace_files)