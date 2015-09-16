import util as u
import re


def add_arithmetic_dranch_in_method(smali_file):
    """Add a fake arithmetic branch near each valid istruction"""
    edit_method = False  # Out Method
    junk_name = None
    this_name = None
    for smali_line in u.open_file_input(smali_file):  # For each line
        #Entering non abstract method
        if re.search(r'^([ ]*?)\.method', smali_line) is not None and re.search(r' abstract ', smali_line) is None and re.search(r' native ', smali_line) is None and not edit_method:
            print smali_line,
            edit_method = True  # In method
        #Exiting method
        elif re.search(r'^([ ]*?)\.end method', smali_line) is not None and edit_method:
            if junk_name is not None and this_name is not None:
                print '    :' + junk_name
                print '    goto/32 :' + this_name
            print smali_line,
            edit_method = False  # Out Method
            junk_name = None
            this_name = None
        elif edit_method:  # If in method
            print smali_line,
            locals_match = re.search(r'^([ ]*?)\.locals (?P<localCount>([0-9]+))$', smali_line)
            if locals_match is not None:
                local_count = locals_match.group('localCount')
                if int(local_count) >= 2:  # If exist at least 2 register
                    rand_int_v0 = u.get_random_int(1, 32)  # Random integer in the first one
                    rand_int_v1 = u.get_random_int(1, 32)  # Random integer in the second one
                    #Add the fake branch
                    print ''
                    print '    const v0, ' + str(rand_int_v0)
                    print '    const v1, ' + str(rand_int_v1)
                    print '    add-int v0, v0, v1'
                    print '    add-int v0, v0, v1'
                    print '    rem-int v0, v0, v1'
                    junk_name = u.get_random(True, 15)
                    this_name = u.get_random(True, 15)
                    goto32_name = u.get_random(True, 15)
                    print '    if-gtz v0, :' + goto32_name
                    print '    goto/32 :' + junk_name
                    print '    :' + goto32_name
                    print '    :' + this_name
        else:
            print smali_line,


def change_all_file(smali_file_list):
    """Add a fake arithmetic branch to all the smali class file"""
    for smali_file in smali_file_list:  # For each file
        add_arithmetic_dranch_in_method(smali_file)


def obfuscate():
    """ The main obfuscator function """
    smali_file_list = u.load_smali_file()
    change_all_file(smali_file_list)
