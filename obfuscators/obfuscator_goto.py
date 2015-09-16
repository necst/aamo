import util as u
import re


def change_cfg(smali_file_list):
    """"""
    for smali_file in smali_file_list:  # For each smali file
        edit_method = False
        for smali_line in u.open_file_input(smali_file):  # For each line
            #At the beggining of non-abstract method
            if re.search(r'^([ ]*?)\.method', smali_line) is not None and re.search(r'abstract', smali_line) is None and re.search(r'native', smali_line) is None and not edit_method:
                #Append at the beginning of the method a Goto to the label located at end of the method, and a label to the real first istruction of the method itself
                print smali_line,
                print '    goto/32 :CFGGoto2'  # Goto END
                print '    :CFGGoto1'  # Label INIT
                edit_method = True  # We are in a method, and we must edit it
            #At the end of a method
            elif re.search(r'^([ ]*?)\.end method', smali_line) is not None and edit_method:
                #Append at the end of the method a Goto to the label located at beginning of the method, and a label to the real last istruction of the method itself
                print '    :CFGGoto2'  # Label END
                print '    goto/32 :CFGGoto1'  # Goto INIT
                print smali_line,
                edit_method = False  # Successefull exit from a method
            else:
                print smali_line,  # Otherwise print the line unchanged


def obfuscate():
    """ The main obfuscator function """
    change_cfg(u.load_smali_file())
