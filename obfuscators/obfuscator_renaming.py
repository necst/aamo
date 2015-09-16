import util as u
import re


def crypt_identifier(param_value):
    return u.crypt_identifier(param_value)


def get_match_line(smali_line, android_method_list, is_rename):
    """Rename a method definition"""
    method_match = re.search(r'^([ ]*?)\.method(.*?) (?P<invokeMethod>([^ ]*?))\((?P<invokePass>(.*?))\)(?P<invokeReturn>(.*?))$', smali_line)  # Match a method definition
    if method_match is None:
        print smali_line,  # Otherwise print back the line unchanged
        return None  # Return None
    method_name = method_match.group('invokeMethod')  # Recover the method name
    if method_name not in android_method_list:  # For non SDK method
        if is_rename:
            print smali_line.replace(method_name + '(', crypt_identifier(method_name) + '('),  # Append
        else:
            print smali_line,
        return method_name  # Return the method name
    else:
        print smali_line,  # Otherwise print back the line unchanged
        return None  # Return None


def find_all_landroid_ljava_over(smali_file_list):
    """Find all the class definition subclasses of an SDK class"""
    for smali_file in smali_file_list:   # For each file
        for smali_line in u.open_file_input(smali_file):  # For each line
            class_match = re.search(r'^([ ]*?)\.class(.*?)(?P<className>L([^;]*?);)', smali_line)  # Match the class definition
            if class_match is not None:
                class_name = class_match.group('className')  # Recover the class name
                if re.search(r'Landroid|Ljava', class_name):  # If the class is a subclass of an SDK class
                    yield class_name  # Return the class name
            print smali_line,  # Print back the line unchanged


def find_all_direct_method(android_method_list, smali_file_list):
    """Search for a method definition in all the the smali file"""
    for smali_file in smali_file_list:  # For each file
        for smali_line in u.open_file_input(smali_file):  # For each line
        #If this line contains a non constructor method definition
            if re.search(r'^([ ]*?)\.method', smali_line) is not None and re.search(r' constructor |\<init\>|\<clinit\>', smali_line) is None:
                method_name = get_match_line(smali_line, android_method_list, True)
                if method_name is not None:
                    yield method_name  # Return the method name
            else:
                print smali_line,  # Print back the line unchanged


def change_match_line(smali_line, edited_method, class_landroid_java_over_list):
    """Rename thereference to a renamed field classes in the current line"""
    invoke_match = re.search(r'^([ ]*?)(?P<invokeType>invoke\-([^ ]*?)) {(?P<invokeParam>([vp0-9,. ]*?))}, (?P<invokeObject>(\[*?)(L(.*?);|\[(I|Z|B|S|J|F|D|C)))->(?P<invokeMethod>(.*?))\((?P<invokePass>(.*?))\)(?P<invokeReturn>(.*?))$', smali_line)  # Match the method reference
    if invoke_match is None:
        print smali_line,
        return
    method_name = invoke_match.group('invokeMethod')  # Get the method name
    invoke_object = invoke_match.group('invokeObject')   # And the class name
    #If the field was renamed and do not belong to the SDK
    if method_name in edited_method and (re.search(r'^Landroid|^Ljava', invoke_object) is None or invoke_object in class_landroid_java_over_list):
        print smali_line.replace(method_name + '(', crypt_identifier(method_name) + '('),  # Append
    else:
        print smali_line,  # Otherwise print back the line unchanged


def change_all_direct_method(edited_method, smali_file_list, class_landroid_java_over_list):
    """Search for a method reference in all the the smali file"""
    for smali_file in smali_file_list:  # For each file
        for smali_line in u.open_file_input(smali_file):  # For each line
            if re.search(r'^([ ]*?)invoke\-', smali_line) is not None:  # If contains a method reference
                change_match_line(smali_line, edited_method, class_landroid_java_over_list)
            else:
                print smali_line,  # Print the line unchanged


def find_all_native_method(smali_file_list):
    """Search for a method definition in all the the smali file"""
    for smali_file in smali_file_list:  # For each file
        for smali_line in u.open_file_input(smali_file):  # For each line
            if re.search(r'^([ ]*?)\.method', smali_line) is not None and re.search(r' native ', smali_line) is not None:
                method_name = get_match_line(smali_line, [], False)
                if method_name is not None:
                    yield method_name  # Return the method name
            else:
                print smali_line,  # Print back the line unchanged


def obfuscate():
    """ The main obfuscator function """
    smali_file_list = u.load_smali_file()  # Load smali files
    set()
    change_all_direct_method(
        set(
            find_all_direct_method(
                list(u.get_android_method_names()) + list(set(find_all_native_method(smali_file_list))),
                smali_file_list
                )
            ),
        smali_file_list,
        set(
            find_all_landroid_ljava_over(
                smali_file_list
                )
            )
        )
