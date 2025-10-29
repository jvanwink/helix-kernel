import os
import sys
from subprocess import call

def find_project_root(start_path):
    """Finds the root of the project by searching for a .git directory or requirements.txt."""
    if not os.path.isdir(start_path):
        current_dir = os.path.dirname(os.path.abspath(start_path))
    else:
        current_dir = os.path.abspath(start_path)
        
    while current_dir != os.path.dirname(current_dir):  # Check until the root of the filesystem
        if os.path.isdir(os.path.join(current_dir, '.git')) or os.path.isfile(os.path.join(current_dir, 'requirements.txt')) or os.path.isfile(os.path.join(current_dir, 'run_config.txt')):
            return current_dir
        current_dir = os.path.dirname(current_dir)
    return start_path  # Return the start path if no project root was found

def open_in_helix(file_paths):
    """Opens the provided file paths in Helix editor."""
    if not file_paths:
        sys.exit(1)

    # Find the project root from the first file path
    project_root = find_project_root(file_paths[0])
    # Open files in Helix, using the project root as the working directory
    # for file_path in file_paths:
    file_paths = file_paths + ['-w', project_root]
        
    call(['hx'] + file_paths)
    
if __name__ == "__main__":
    open_in_helix(sys.argv[1:])  # Pass all command line arguments except the script name
