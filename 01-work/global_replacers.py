"""
This python file contains the main functions for the program.
"""
import re

def replace_local_lattice(new_values : list, file_location : str):
    """
    Replaces the local lattice values in the global header with the new values. The header has to already have valid definitions.
    :param new_values: List of new values, e.g. [1,2,3,4]
    :param file_location: Location of the global header file, e.g. '/home/user/src/global.h'
    :return: None
    """
    # Open the global.h file and read the lines
    with open(file_location, 'r') as f:
        lines = f.readlines()

    # Regex pattern for #define lines
    pattern = re.compile(r'#define L(\w+) (.+)')

    # Dictionary to store #define variables
    defines = {}

    # Find #define variables and store them in the dictionary
    for line in lines:
        match = pattern.match(line)
        if match:
            defines[match.group(1)] = match.group(2)

    # Open the source code file and replace #define variables
    with open(file_location, 'r') as f:
        global_h = f.read()

    # Replace the defined values with the new values
    for key, value in defines.items():
        global_h = global_h.replace('#define L' + key + ' ' + value, '#define L' + key + ' ' + str(new_values[int(key)]))

    # Write the modified source code back to the file
    with open(file_location, 'w') as f:
        f.write(global_h)

def replace_process_grid(new_values : list, file_location : str):
    """
    Replaces the process grid values in the global header with the new values. The header has to already have valid definitions.
    :param new_values: List of new values, e.g. [1,2,3,4]
    :param file_location: Location of the global header file, e.g. '/home/user/src/global.h'
    :return: None
    """
    # Open the global.h file and read the lines
    with open(file_location, 'r') as f:
        lines = f.readlines()

    # Regex pattern for #define lines
    pattern = re.compile(r'#define NPROC(\w+) (.+)')

    # Dictionary to store #define variables
    defines = {}

    # Find #define variables and store them in the dictionary
    for line in lines:
        match = pattern.match(line)
        if match:
            defines[match.group(1)] = match.group(2)

    # Open the source code file and replace #define variables
    with open(file_location, 'r') as f:
        global_h = f.read()

    # Replace the defined values with the new values    
    for key, value in defines.items():
        if key.isdigit():
            global_h = global_h.replace('#define NPROC' + key + ' ' + value, '#define NPROC' + key + ' ' + str(new_values[int(key)]))
        # else:
        #     print(f"Warning: Invalid key '{key}' - cannot convert to integer.")
            

    # Write the modified source code back to the file
    with open(file_location, 'w') as f:
        f.write(global_h)


def replace_name(new_name: str, file_location: str):
    """
    Replaces the name in the include file with the new name.
    :param new_name: New name, e.g. 'my_new_name'
    :param file_location: Location of the include file, e.g. '/home/user/src/include/include.h'
    :return: None
    """
    with open(file_location, 'r') as f:
        content = f.read()

    content = re.sub(r'(name\s+)\S+', r'\1' + new_name, content)

    with open(file_location, 'w') as f:
        f.write(content)
