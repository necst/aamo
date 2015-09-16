import util as u
import re


def add_nop_in_method(smali_file, valid_op_code):
    """Add multiple nop sequence of random lenght (1-3) between two nop-valid istruction"""
    for smali_line in u.open_file_input(smali_file):  # For each line
        print smali_line,  # Print the original instruction
        line_op_code = re.search(r'^([ ]*)(?P<opCode>([^ ]+)) ', smali_line)
        if line_op_code is not None:
            op_code = line_op_code.group('opCode')
            if op_code in valid_op_code:
                nop_count = u.random_nop_interval()  # Randomize the number of nop(s)
                print '    nop\n' * nop_count  # Print the nop(s)


def change_all_file(smali_file_list, valid_op_code):
    """Add the nop in all the smali class file"""
    for smali_file in smali_file_list:  # For each file
        add_nop_in_method(smali_file, valid_op_code)


def obfuscate():
    """ The main obfuscator function """
    smali_file_list = u.load_smali_file()
    change_all_file(smali_file_list, u.get_valid_op_code())
