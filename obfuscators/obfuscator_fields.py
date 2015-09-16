import util as u
import re


def crypt_identifier(param_value):
    return u.crypt_identifier(param_value)


def add_random_fields(smali_line):
    """Adds a random (in lenght and name) list of fields to the class"""
    for _ in range(u.random_nop_interval()):
        print re.sub(r':', u.get_random(True, 32) + ':', smali_line),  # Append


def get_match_line(smali_line):
    """Rename a field definition"""
    field_match = re.search(r'^([ ]*?)\.field(.*?) (?P<fieldName>([^ ]*?)):(?P<fieldType>([^ ]*?))(.*?)$', smali_line)  # Match a field definition
    if field_match is None:
        print smali_line,  # Otherwise print back the line unchanged
        return None  # Return None
    field_name = field_match.group('fieldName')  # Recover the field name
    if re.search(r'\$', field_name) is None:  # If it does not contain '$'' (no sub-field)
        smali_line = smali_line.replace(field_name + ':', crypt_identifier(field_name) + ':')  # Append
        print smali_line,
        add_random_fields(smali_line)
        return field_name  # Return the field name
    else:
        print smali_line,  # Otherwise print back the line unchanged
        return None  # Return None


def find_all_landroid_ljava_over(smali_file_list):
    """Find all the class definition subclasses of an SDK class"""
    for smali_file in smali_file_list:  # For each file
        for smali_line in u.open_file_input(smali_file):  # For each line
            class_match = re.search(r'^([ ]*?)\.class(.*?)(?P<className>L([^;]*?);)', smali_line)  # Match the class definition
            if class_match is not None:
                class_name = class_match.group('className')  # Recover the class name
                if re.search(r'Landroid|Ljava', class_name):  # If the class is a subclass of an SDK class
                    yield class_name  # Return the class name
            print smali_line,  # Print back the line unchanged


def find_all_field(smali_file_list):
    """Search for a field definition in all the the smali file"""
    for smali_file in smali_file_list:  # For each file
        for smali_line in u.open_file_input(smali_file):  # For each line
            if re.search(r'^([ ]*?)\.field', smali_line) is not None:  # If this line contains a field definition
                field_name = get_match_line(smali_line)
                if field_name is not None:
                    yield field_name  # Return the field name
            else:
                print smali_line,  # Print back the line unchanged


def change_match_line(smali_line, edited_field, class_landroid_java_over_list):
    """Rename thereference to a renamed field classes in the current line"""
    invoke_match = re.search(r'^([ ]*?)(?P<invokeType>(((i|s)get(\-)?)|((i|s)put(\-)?))([^ ]*?)) (?P<invokeParam>([vp0-9,. ]*?)) (?P<invokeObject>L(.*?);|\[L(.*?);)->(?P<invokeField>(.*?)):(?P<invokeReturn>(.*?))$', smali_line)  # Match the field reference
    if invoke_match is None:
        print smali_line,  # Otherwise print back the line unchanged
        return
    field_name = invoke_match.group('invokeField')  # Get the field name
    invoke_object = invoke_match.group('invokeObject')  # And the class name
    #If the field was renamed and do not belong to the SDK
    if field_name in edited_field and (re.search(r'^Landroid|^Ljava', invoke_object) is None or invoke_object in class_landroid_java_over_list):
        print smali_line.replace(field_name + ':', crypt_identifier(field_name) + ':'),  # Append
    else:
        print smali_line,  # Otherwise print back the line unchanged


def change_all_field(edited_field, smali_file_list, class_landroid_java_over_list):
    """Search for a filed reference in all the the smali file"""
    for smali_file in smali_file_list:  # For each file
        for smali_line in u.open_file_input(smali_file):  # For each line
            if re.search(r'^([ ]*?)(((i|s)get(\-)?)|((i|s)put(\-)?))', smali_line) is not None:  # If contains a field reference
                change_match_line(smali_line, edited_field, class_landroid_java_over_list)
            else:
                print smali_line,  # Print the line unchanged


def obfuscate():
    """ The main obfuscator function """
    smali_file_list = u.load_smali_file()  # Load smali files
    change_all_field(set(find_all_field(smali_file_list)), smali_file_list, set(find_all_landroid_ljava_over(smali_file_list)))
