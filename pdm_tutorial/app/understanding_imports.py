# backend/app/understanding_imports.py
import sys
print("Python searches these directories for modules:")
for i, path in enumerate(sys.path, 1):
    print(f"{i}. {path}")
