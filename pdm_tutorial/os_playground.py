import os

# Currrent directory
cwd = os.getcwd()
print(f"cwd {cwd}")

# List all files in a directory
files = os.listdir("repo")
print("".join([str(file)+"\n" for file in files]).strip())

# Check if path exists
exists = os.path.exists("repo/1801811.mcam")
print(f"exists {exists}")

# Check if it's a file (not directory)
is_file = os.path.isfile("repo/1801811.mcam")
print(f"is_file {is_file}")

# Check if it's a directory
is_dir = os.path.isdir("repo")
print(f"is_dir {is_dir}")

# Get file size (in bytes)
size = os.path.getsize("repo/1801811.mcam")
print(f"size {size}")

# join paths (handles OS differnces)
path = os.path.join('repo', '1801811.mcam')
print(f"path {path}")

path = r"C:\Users\g4m3r\OneDrive\Desktop\tuts\pdm_tutorial\backend\repo\1801811.mcam"

# Get just the directory
dirname = os.path.dirname(path)
print(f"dirname {dirname}")

# Get just the filename
basename = os.path.basename(path)
print(f"basename {basename}")

# Split into directory and filename
dir_part, file_part = os.path.split(path)
print(f"dir_part {dir_part}, file_part {file_part}")

# Split filename and exension
name, ext = os.path.splitext("1801811.mcam")
print(f"name {name} ext {ext}")

# Get absolute path
abs_path = os.path.abspath('repo/1801811.mcam')
print(f"abs_path {abs_path}")


# Get the directory wehre THIS Python file lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(f"BASE_DIR {BASE_DIR}")

# Build a path to the repo
REPO_PATH = os.path.join(BASE_DIR, "backend/repo")
print(f"REPO_PATH {REPO_PATH}")

file = os.listdir(REPO_PATH)
print(f"files {files}")
