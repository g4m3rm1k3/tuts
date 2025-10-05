""" 
Cross-Platfrom file locking implementation

Provides atomic read-modify-write operations on files.
Essential for preventing race conditions in concurrent environments
"""
import os
from pathlib import Path
from typing import Union

# Platform-specific imports
if os.name == "nt":  # Windows
    import msvcrt
else:  # Unix-like (Linux, maxOS)
    import fcntl

# Section 1: Context Manager Implementation


class LockedFile:
    """Context manager for excluive file locking.

    Usage:
        with LockedFile(path, 'r+') as f:
            data = json.load(f)
            data['key'] = 'value'
            f.seek(0)
            f.truncate()
            json.dump(data, f)

    Why this is safe:
    1. Lock is acquired before any I/O
    2. Lock is held for entire read-modify-write
    3. Lock is released even if exception occurs
    4. Other processes wait for lock before accessing
    """

    def __init__(self, filepath: Union[str, Path], mode: str = 'r'):
        """
        Initialize locked file handler
        Args:
            filepath: Path to file
            mode: File open mode ('r', 'w', 'r+', etc.)
            """
        self.filepath = Path(filepath)
        self.mode = mode
        self.file = None

    def __enter__(self):
        """ 
        Acquire lock when entering context.

        Returns:
            Open file handle wtih lock acquired
            """
        # Open file
        self.file = open(self.filepath, self.mode)

        # Acquire exclusive lock
        if os.name == 'nt':
            # Windows: Lock a byte range
            # msvcrt.locking() locks a byte range
            # We lock from poistion 0 to EOF
            file_size = os.path.getsize(self.filepath)
            if file_size == 0:
                file_size = 1  # Lock at least 1 byte

            # LK_NBLK: Non-blocking exlusive lock
            # Will rasise IOError if already locked
            try:
                msvcrt.locking(
                    self.file.fileno(),
                    msvcrt.LK_LOCK,  # Blcoking lock
                    file_size
                )
            except IOError as e:
                self.file.close()
                raise IOError(
                    f"Could not acquire lock on {self.filepath}: {e}")
        else:
            # Unix: flock() is simpler and more reliable
            # LOCK_EX: Exclusive lock
            # Blocks until lock is available
            try:
                fcntl.flock(self.file.fileno(), fcntl.LOCK_EX)
            except IOError as e:
                self.file.close()
                raise IOError(
                    f"Could not acquire lock on {self.filepath}: {e}")
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ 
        Release lock when exiting context.
        Called even if exception occurs in the with block
        """
        if self.file:
            # Release lock
            if os.name == "nt":
                try:
                    file_size = os.path.getsize(self.filepath)
                    if file_size == 0:
                        file_size = 1
                    msvcrt.locking(
                        self.file.fileno(),
                        msvcrt.LK_UNLCK,
                        file_size
                    )
                except:
                    pass
            else:
                try:
                    fnctl.flock(self.file, fileno(), fcntl.LOCK_UN)
                except:
                    pass
            # Close file
            self.file.close()

        # Propagate exceptions (return False)
        return False

# ============================================================================
# SECTION 2: Testing the Lock
# ============================================================================


if __name__ == "__main__":
    """
    Test the file locking mechanism
    """
    import json
    import threading
    import time

    test_file = Path("lock_test.json")
    test_file.write_text('{"counter": 0}')

    def safe_increment(thread_id):
        """
        Atomic increment using LockedFile
        """
        for i in range(100):
            with LockedFile(test_file, "r+") as f:
                # Read
                data = json.load(f)

                # Modify
                data['counter'] += 1

                # Write (must seek to beginning and truncate)
                f.seek(0)
                f.truncate()
                json.dump(data, f)

            # Small delay to increase chance of contention
            time.sleep(0.001)

    print("Testing file locking with multiple threads...")

    # Run three threads simultaneously
    threads = [
        threading.Thread(target=safe_increment, args=(i,))
        for i in range(3)
    ]
    for t in threads:
        t.start()

    for t in threads:
        t.join()

    # Vefiry corretness
    final = json.loads(test_file.read_text())
    expected = 300  # 3 threads x 100 increments

    print(f"Expected: {expected}")
    print(f"Got: {final['counter']}")
    print(f"Success: {final['counter'] == expected}")

    test_file.unlink()
