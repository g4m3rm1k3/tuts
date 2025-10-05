# path_viewer.py
import os

# Get the PATH variable from the environment
path_variable = os.environ.get("PATH", "")

# Split the PATH string into a list of individual directories
# The separator is ':' on macOS/Linux and ';' on Windows
directories = path_variable.split(os.pathsep)

print("your system's PATH includes:")
for i, directory in enumerate(directories):
    print(F"{i+1}: {directory}")
