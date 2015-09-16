import util as u
import re


def apply_crypt(string_const):
    return u.crypt_string(string_const)


def crypt_string(smali_line, class_name):
    """Add the call to the decrypt routine after the string definition"""
    string_const_match = re.search(r'^([ ]*?)(?P<constType>const\-string|const\-string\/jumbo) (?P<regType>v|p)(?P<regNum>\d{1,2}), \"(?P<stringConst>.*?)\"$', smali_line)
    if string_const_match is None:
        print smali_line,
        return
    v_string = string_const_match.group('regType') + string_const_match.group('regNum')
    print '    ' + string_const_match.group('constType') + ' ' + v_string + ', "' + apply_crypt(string_const_match.group('stringConst')) + '"'
    print ''
    print '    invoke-static/range {' + v_string + ' .. ' + v_string + '}, Landroid/content/res/' + class_name + ';->convertToString(Ljava/lang/String;)Ljava/lang/String;'
    print ''
    print '    move-result-object ' + v_string


def add_crypt_method(smali_file_list, class_name):
    """Search for a string in all the the smali file"""
    for smali_file in smali_file_list:  # For each file
        for smali_line in u.open_file_input(smali_file):  # For each line
            if re.search(r'^([ ]*?)const\-string', smali_line) is not None:
                crypt_string(smali_line, class_name)
            else:
                print smali_line,  # Print back the line unchanged


def get_match_line(smali_line):
    """Rename a field definition"""
    field_match = re.search(r'^([ ]*?)\.field(.*?) static final (?P<fieldName>([^ ]*?)):Ljava\/lang\/String\; = \"(?P<fieldValue>[^\"]*?)\"$', smali_line)  # Match a field definition
    if field_match is not None:
        field_name = field_match.group('fieldName')  # Recover the field name
        field_value = field_match.group('fieldValue')  # Recover the field value
        if re.search(r'\$', field_name) is None:  # If it does not contain '$'' (no sub-field)
            print smali_line.replace('"' + field_value + '"', '"' + apply_crypt(field_value) + '"')  # Append
        else:
            print smali_line,  # Otherwise print back the line unchanged
    else:
        print smali_line,  # Otherwise print back the line unchanged


def find_all_final_string_field(smali_file_list):
    """Search for a field definition in all the the smali file"""
    for smali_file in smali_file_list:  # For each file
        for smali_line in u.open_file_input(smali_file):  # For each line
            if re.search(r'^([ ]*?)\.field', smali_line) is not None:  # If this line contains a field definition
                get_match_line(smali_line)
            else:
                print smali_line,  # Print back the line unchanged


def obfuscate():
    """ The main obfuscator function """
    class_name = 'a' + u.get_random(True, 7)
    smali_file_list = u.load_smali_file()
    add_crypt_method(smali_file_list, class_name)
    find_all_final_string_field(smali_file_list)
    move_string_class(class_name)


def move_string_class(class_name):
    decrypt_class = u.get_string_class()  # Load the decrypt class from file
    decrypt_class = decrypt_class.replace('StringManagerOb', class_name)  # Random key
    u.write_text_file(u.base_dir()+'/smali/android/content/res/' + class_name + '.smali', decrypt_class)  # Write the class file
