import util as u
import re


def obfuscate():
    """ The main obfuscator function """
    lib_file_list = list(u.load_lib_file())
    crypt_files(lib_file_list)
    change_allfile(lib_file_list)
    smali_file_list = u.load_smali_file()  # Load smali files
    change_all_direct_method(smali_file_list, 'LibOb')


def crypt_files(file_list):
    """Crypt some files"""
    for file_name in file_list:
        file_data = u.get_asset_file(file_name)
        file_data = u.crypt_raw(file_data)
        u.write_lib_file(file_name, file_data)


def change_allfile(file_list):
    """Rename all smali class files"""
    for file_name in file_list:
        change_match_file(file_name)


def crypt_identifier(param_value):
    return (u.crypt_identifier(param_value))[:90]


def change_match_file(file_name):
    """Rename a class file appending the string"""
    dir_name, res_name, file_ext = u.get_file_info(file_name)
    u.rename(file_name, dir_name + 'lib' + crypt_identifier(res_name + file_ext) + file_ext)


def change_all_direct_method(smali_file_list, class_name):
    """Search for a method reference in all the the smali file"""
    for smali_file in smali_file_list:  # For each file
        for smali_line in u.open_file_input(smali_file):  # For each line
            if re.search(r'^([ ]*?)invoke\-', smali_line) is not None:  # If contains a method reference
                change_match_line(smali_line, class_name)
            else:
                print smali_line,  # Print the line unchanged


def change_match_line(smali_line, class_name):
    """Redirect the invokation of openAssetResource"""
    invoke_match = re.search(r'^([ ]*?)(?P<invokeType>invoke\-([^ ]*?)) {(?P<invokeParam>([vp0-9,. ]*?))}, (?P<invokeObject>(\[*?)(L(.*?);|\[(I|Z|B|S|J|F|D|C)))->(?P<invokeMethod>(.*?))\((?P<invokePass>(.*?))\)(?P<invokeReturn>(.*?))$', smali_line)  # Match the method reference
    if invoke_match is None:
        print smali_line,
        return
    method_name = invoke_match.group('invokeMethod')  # Get the method name
    invoke_object = invoke_match.group('invokeObject')   # And the class name
    invokeParam = invoke_match.group('invokeParam')  # Call parameters
    if (method_name == 'loadLibrary' or method_name == 'load') and (invoke_object == 'Ljava/lang/System;' or invoke_object == 'Ljava/lang/Runtime;'):
        if '..' in invokeParam:
            print '    invoke-static/range {'+invokeParam+'}, Landroid/content/res/' + class_name + ';->' + method_name + '(Ljava/lang/String;)V'
        else:
            print '    invoke-static {'+invokeParam+'}, Landroid/content/res/' + class_name + ';->' + method_name + '(Ljava/lang/String;)V'
    else:
        print smali_line,  # Otherwise print back the line unchanged
