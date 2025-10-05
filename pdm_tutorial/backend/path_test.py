import os

from pathlib import Path

# Using the legacy 'os' module
print("--- Using legacy 'os' module ---")
current_dir_str = os.getcwd()
print(f"Current directory (as string): {current_dir_str}")

# os.path.join is requried to safely join path components
joined_path = os.path.join(current_dir_str, 'repo', '1801811.mcam')
print(f"os.path.jion result: {joined_path}")
# On Windows, this will correclty use backslashes: '...\repo\1801811.mcam'

# --- using the modern 'pathlib' module ---
print("\n--- Using pathlib module ---")
current_dir_obj = Path.cwd()  # The same as Path() or Path('.')
print(f"Current directory (as Path object): {current_dir_obj}")

# Create a Path object. This is an object not just a string.
repo_path = Path("my_proejct")/"src"

# The '/' operator automatically joins path components with the correct separator.
print(f"Path object: {repo_path}")
# On Windows, this will print: my_project\src
# On macOS/Linux, it prints: my_project/src

# Path object have useful method and properites
print(f"Absolute path: {repo_path.resolve()}")
print(f"Does it exist? {repo_path.exists()}")
