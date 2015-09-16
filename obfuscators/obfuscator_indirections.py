import util as u
import re
import StringIO


def get_reg(invoke_param):
    """Return the parameter registry list"""
    if invoke_param == '':
        return
    reg_list = re.finditer(r'(v|p)\d{1,3}', invoke_param)
    for reg_value in reg_list:
        yield reg_value.group()


def is_range(invoke_type):
    """Range value"""
    if re.search(r'range', invoke_type) is not None:
        return True
    return False


def reg_range_count(reg_list):
    """Range register count"""
    return int(reg_list[1][1:]) - int(reg_list[0][1:]) + 1


def is_void(invoke_return):
    if invoke_return == 'V':
        return True
    return False


def is_wide(invoke_return):
    if invoke_return == 'J' or invoke_return == 'D':
        return True
    return False


def is_obj(invoke_return):
    if re.search(r'L([^;]*?);|\[|\[L([^;]*?);', invoke_return) is not None:
        return True
    return False


def is_static(invoke_type):
    if re.search(r'static', invoke_type) is not None:
        return True
    return False


def is_init(invoke_method):
    if re.search(r'\<init\>|\<clinit\>', invoke_method) is not None:
        return True
    return False


def change_match_line(smali_line, invoke_type, invoke_param, invoke_object, invoke_method, invoke_pass, invoke_return, class_name, new_method):
    """Change a method call"""
    string_append = u.get_random(True, 15)

    is_range_value = is_range(invoke_type)
    is_static_value = is_static(invoke_type)

    reg_list = list(get_reg(invoke_param))
    if is_range_value:
        reg_count = reg_range_count(reg_list)
    else:
        reg_count = len(reg_list)

    is_void_value = is_void(invoke_return)
    is_wide_value = is_wide(invoke_return)
    is_obj_value = is_obj(invoke_return)

    local_reg_count = 1
    if is_void_value:
        local_reg_count = 0
    if is_wide_value:
        local_reg_count = 2

    return_str = 'return v0'
    if is_void_value:
        return_str = 'return-void'
    if is_wide_value:
        return_str = 'return-wide v0'
    if is_obj_value:
        return_str = 'return-object v0'

    move_result_str = 'move-result v0'
    if is_void_value:
        move_result_str = ''
    if is_wide_value:
        move_result_str = 'move-result-wide v0'
    if is_obj_value:
        move_result_str = 'move-result-object v0'

    add_param = ''
    if not is_static_value:
        add_param = invoke_object

    invoke_new = 'invoke-static'
    if is_range_value:
        invoke_new += '/range'

    print '    ' + invoke_new + ' {' + invoke_param + '}, ' + class_name + '->' + string_append + '(' + add_param + invoke_pass + ')' + invoke_return

    new_method.write('.method public static ' + string_append + '(' + add_param + invoke_pass + ')' + invoke_return + '\n')
    new_method.write('    .locals ' + str(local_reg_count) + '\n')
    new_method.write('    .prologue' + '\n')
    new_method.write('\n')
    new_method.write('    ' + invoke_type + ' {')
    if is_range_value:
        new_method.write('p0 .. p' + str(reg_count-1))
    else:
        for reg_index in range(0, reg_count):
            new_method.write('p' + str(reg_index))
            if reg_count != reg_index + 1:
                new_method.write(', ')
    new_method.write('}, ' + invoke_object + '->' + invoke_method + '(' + invoke_pass + ')' + invoke_return + '\n')
    new_method.write('\n')
    new_method.write('    ' + move_result_str + '\n')
    new_method.write('\n')
    new_method.write('    ' + return_str + '\n')
    new_method.write('.end method' + '\n')


def change_all_method(smali_file, new_method):
    """Redirect all the method calls"""
    for smali_line in u.open_file_input(smali_file):  # For each line
        class_match = re.search(r'^([ ]*?)\.class(.*?)(?P<className>L([^;]*?);)', smali_line)  # Match the class declaration
        if class_match is not None:
            class_name = class_match.group('className')  # Find the class name
        invoke_match = re.search(r'^([ ]*?)(?P<invokeType>invoke\-([^ ]*?)) {(?P<invokeParam>([vp0-9,. ]*?))}, (?P<invokeObject>L(.*?);|\[L(.*?);)->(?P<invokeMethod>(.*?))\((?P<invokePass>(.*?))\)(?P<invokeReturn>(.*?))$', smali_line)  # Match a method invocation
        if invoke_match is not None:
            if not is_init(invoke_match.group('invokeMethod')):
                change_match_line(smali_line, invoke_match.group('invokeType'), invoke_match.group('invokeParam'), invoke_match.group('invokeObject'), invoke_match.group('invokeMethod'), invoke_match.group('invokePass'), invoke_match.group('invokeReturn'), class_name, new_method)
            else:
                print smali_line,  # Print the line unchanged
        else:
            print smali_line,  # Print the line unchanged


def add_all_method(smali_file, new_method):
    """Add the indirection methods"""
    for smali_line in u.open_file_input(smali_file):  # For each line
        if re.search(r'^([ ]*?)# direct methods', smali_line) is not None:  # Before the directs methods
            print smali_line,  # Print the line unchanged
            print new_method.getvalue()  # Print the method
        else:
            print smali_line,  # Print the line unchanged


def change_all_file(smali_file_list):
    """Apply indirection to all smali file"""
    for smali_file in smali_file_list:  # For all smali file
        new_method = StringIO.StringIO()  # Inizialize a string buffer
        change_all_method(smali_file, new_method)
        add_all_method(smali_file, new_method)
        new_method.close()  # Close the string buffer


def obfuscate():
    """ The main obfuscator function """
    smali_file_list = u.load_smali_file()
    change_all_file(smali_file_list)
