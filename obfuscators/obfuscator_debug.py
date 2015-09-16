import util as u
import re


def add_nop_in_method(smali_file, valid_op_code):
    """Remove the debug info from the file"""
    for smali_line in u.open_file_input(smali_file):  # For each line
        line_op_code = re.search(r'^([ ]*)(?P<opCode>([^ ]+)) ', smali_line)
        if line_op_code is not None:
            op_code = line_op_code.group('opCode')
            if op_code not in valid_op_code:  # If the istruction is not a debug information
                print smali_line,  # Print the original instruction
        else:
            print smali_line,  # Print the original instruction


def change_all_file(smali_file_list, valid_op_code):
    """Remove the debug info from all the smali class file"""
    for smali_file in smali_file_list:  # For each file
        add_nop_in_method(smali_file, valid_op_code)


def obfuscate():
    """ The main obfuscator function """
    smali_file_list = u.load_smali_file()
    change_all_file(smali_file_list, u.get_valid_debug_code())
