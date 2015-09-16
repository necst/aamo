import util as u
import re
import StringIO

#Type class dictionary
sget_dict = {
    'I': 'Ljava/lang/Integer;->TYPE:Ljava/lang/Class;',
    'Z': 'Ljava/lang/Boolean;->TYPE:Ljava/lang/Class;',
    'B': 'Ljava/lang/Byte;->TYPE:Ljava/lang/Class;',
    'S': 'Ljava/lang/Short;->TYPE:Ljava/lang/Class;',
    'J': 'Ljava/lang/Long;->TYPE:Ljava/lang/Class;',
    'F': 'Ljava/lang/Float;->TYPE:Ljava/lang/Class;',
    'D': 'Ljava/lang/Double;->TYPE:Ljava/lang/Class;',
    'C': 'Ljava/lang/Character;->TYPE:Ljava/lang/Class;'
}

#Type cast dictionary
cast_dict = {
    'I': 'Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;',
    'Z': 'Ljava/lang/Boolean;->valueOf(Z)Ljava/lang/Boolean;',
    'B': 'Ljava/lang/Byte;->valueOf(B)Ljava/lang/Byte;',
    'S': 'Ljava/lang/Short;->valueOf(S)Ljava/lang/Short;',
    'J': 'Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;',
    'F': 'Ljava/lang/Float;->valueOf(F)Ljava/lang/Float;',
    'D': 'Ljava/lang/Double;->valueOf(D)Ljava/lang/Double;',
    'C': 'Ljava/lang/Character;->valueOf(C)Ljava/lang/Character;'
}

#Type dictionary
type_dict = {
    'I': 'Ljava/lang/Integer;',
    'Z': 'Ljava/lang/Boolean;',
    'B': 'Ljava/lang/Byte;',
    'S': 'Ljava/lang/Short;',
    'J': 'Ljava/lang/Long;',
    'F': 'Ljava/lang/Float;',
    'D': 'Ljava/lang/Double;',
    'C': 'Ljava/lang/Character;'
}

#Reverse type class cast dictionary
reverse_cast_dict = {
    'I': 'Ljava/lang/Integer;->intValue()I',
    'Z': 'Ljava/lang/Boolean;->booleanValue()Z',
    'B': 'Ljava/lang/Byte;->byteValue()B',
    'S': 'Ljava/lang/Short;->shortValue()S',
    'J': 'Ljava/lang/Long;->longValue()J',
    'F': 'Ljava/lang/Float;->floatValue()F',
    'D': 'Ljava/lang/Double;->doubleValue()D',
    'C': 'Ljava/lang/Character;->charValue()C'
}


def get_reg(invoke_param):
    """Get the register parameter list"""
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


def split_invoke_pass(invoke_pass):
    """Match an invocation type of the parameter"""
    for find_item in re.findall(r'(L[^;]*?;)|(\[L[^;]*?;)|(\[V)|(\[Z)|(\[B)|(\[S)|(\[C)|(\[I)|(\[J)|(\[F)|(\[D)|(V)|(Z)|(B)|(S)|(C)|(I)|(J)|(F)|(D)', invoke_pass):
        for find_match in find_item:
            if find_match != '':
                yield find_match


def change_match_line(smali_line, invoke_type, invoke_param, invoke_object, invoke_method, invoke_pass, invoke_return, class_name, new_method, all_method_list):
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
    new_method.write('    .locals ' + str(local_reg_count + 8 - 2) + '\n')
    new_method.write('    .prologue' + '\n')

    method_search = invoke_object + '->' + invoke_method + '(' + invoke_pass + ')'
    if method_search in all_method_list:

        list_invoke = list(split_invoke_pass(invoke_pass))
        list_count = len(list_invoke)

        new_method.write('\n')
        new_method.write('    const v0, ' + hex(list_count) + '\n')
        new_method.write('    new-array v1, v0, [Ljava/lang/Class;' + '\n')
        new_method.write('    new-array v2, v0, [Ljava/lang/Object;' + '\n')
        new_method.write('\n')

        if is_static_value:
            reg_base = 0
        else:
            reg_base = 1

        index_list = 0
        for curr_invoke in list_invoke:
            new_method.write('    const v0, ' + hex(index_list) + '\n')
            index_list += 1
            curr_dict = sget_dict.get(curr_invoke, '')
            if curr_dict != '':
                new_method.write('    sget-object v3, ' + curr_dict + '\n')
            else:
                new_method.write('    const-class v3, ' + curr_invoke + '\n')
            new_method.write('    aput-object v3, v1, v0' + '\n')

            curr_dict = cast_dict.get(curr_invoke, '')
            if curr_dict != '':
                if is_wide(curr_invoke):
                    new_method.write('    invoke-static/range {p' + str(reg_base) + ' .. p' + str(reg_base + 1) + '}, ')
                else:
                    new_method.write('    invoke-static/range {p' + str(reg_base) + ' .. p' + str(reg_base) + '}, ')
                new_method.write(curr_dict + '\n')
                new_method.write('    move-result-object v3' + '\n')
                new_method.write('    aput-object v3, v2, v0' + '\n')
                if is_wide(curr_invoke):
                    reg_base += 1
            else:
                new_method.write('    aput-object p' + str(reg_base) + ', v2, v0' + '\n')
            reg_base += 1

        new_method.write('\n')
        new_method.write('    const-string v0, "' + invoke_method + '"' + '\n')
        new_method.write('    const-class v3, ' + invoke_object + '\n')
        new_method.write('\n')
        new_method.write('    invoke-virtual {v3, v0, v1}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;' + '\n')
        new_method.write('    move-result-object v0' + '\n')
        new_method.write('\n')
        if is_static_value:
            new_method.write('    invoke-virtual {v0, v3, v2}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;' + '\n')
        else:
            new_method.write('    invoke-virtual {v0, p0, v2}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;' + '\n')
        new_method.write('    move-result-object v0' + '\n')

        if is_void_value:
            new_method.write('    return-void' + '\n')
        elif is_obj_value:
            new_method.write('    check-cast v0, ' + invoke_return + '\n')
            new_method.write('    return-object v0' + '\n')
        else:
            curr_dict = type_dict.get(invoke_return, '')
            new_method.write('    check-cast v0, ' + curr_dict + '\n')
            curr_dict = reverse_cast_dict.get(invoke_return, '')
            new_method.write('    invoke-virtual {v0}, ' + curr_dict + '\n')
            if is_wide_value:
                new_method.write('    move-result-wide v0' + '\n')
                new_method.write('    return-wide v0' + '\n')
            else:
                new_method.write('    move-result v0' + '\n')
                new_method.write('    return v0' + '\n')
        new_method.write('\n')

    else:
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


def change_all_method(smali_file, new_method, all_method_list):
    """Redirect all the method calls"""
    for smali_line in u.open_file_input(smali_file):  # For each line
        class_match = re.search(r'^([ ]*?)\.class(.*?)(?P<className>L([^;]*?);)', smali_line)  # Match the class declaration
        if class_match is not None:
            class_name = class_match.group('className')  # Find the class name
        invoke_match = re.search(r'^([ ]*?)(?P<invokeType>invoke\-([^ ]*?)) {(?P<invokeParam>([vp0-9,. ]*?))}, (?P<invokeObject>L(.*?);|\[L(.*?);)->(?P<invokeMethod>(.*?))\((?P<invokePass>(.*?))\)(?P<invokeReturn>(.*?))$', smali_line)
        if invoke_match is not None:
            if not is_init(invoke_match.group('invokeMethod')):
                change_match_line(smali_line, invoke_match.group('invokeType'), invoke_match.group('invokeParam'), invoke_match.group('invokeObject'), invoke_match.group('invokeMethod'), invoke_match.group('invokePass'), invoke_match.group('invokeReturn'), class_name, new_method, all_method_list)
            else:
                print smali_line,  # Print the line unchanged
        else:
            print smali_line,  # Print the line unchanged


def add_all_method(smali_file, new_method):
    """Add the indirection methods"""
    for smali_line in u.open_file_input(smali_file):  # For each line
        if re.search(r'^([ ]*?)# direct methods', smali_line) is not None:   # Before the directs methods
            print smali_line,  # Print the line unchanged
            print new_method.getvalue()  # Print the method
        else:
            print smali_line,  # Print the line unchanged


def change_all_file(smali_file_list, all_method_list):
    """Apply obfuscation to all smali file"""
    for smali_file in smali_file_list:  # For all smali file
        new_method = StringIO.StringIO()  # Inizialize a string buffer
        change_all_method(smali_file, new_method, all_method_list)
        add_all_method(smali_file, new_method)
        new_method.close()  # Close the string buffer


def get_match_line(smali_line, class_name):
    """Match a method declaration"""
    method_match = re.search(r'^([ ]*?)\.method(?P<methodType>.*?) (?P<invokeMethod>([^ ]*?))\((?P<invokePass>(.*?))\)(?P<invokeReturn>(.*?))$', smali_line)
    if method_match is None:
        return None
    return purge_method(class_name, method_match.group('methodType'), method_match.group('invokeMethod'), method_match.group('invokePass'))


def purge_method(class_name, method_type, invoke_method, invoke_pass):
    """Filter out the non reflectable methods"""
    #In init or constructor
    if re.search(r'\<init\>|\<clinit\>', invoke_method) is None and re.search(r' constructor ', method_type) is None and re.search(r' public ', method_type) is not None:
        return class_name + '->' + invoke_method + '(' + invoke_pass + ')'
    else:
        return None


def find_all_method(smali_file_list):
    """Match all methods declarations"""
    for smali_file in smali_file_list:  # For all smali file
        for smali_line in u.open_file_input(smali_file):  # For each line
            print smali_line,
            class_match = re.search(r'^([ ]*?)\.class(.*?)(?P<className>L([^;]*?);)', smali_line)  # Match class declaration
            if class_match is not None:
                class_name = class_match.group('className')  # Match class name
            if re.search(r'^([ ]*?)\.method', smali_line) is not None:  # Method delcaration
                method_name = get_match_line(smali_line, class_name)
                if method_name is not None:
                    yield method_name  # Return the method name


def obfuscate():
    """ The main obfuscator function """
    smali_file_list = u.load_smali_file()
    all_method_list = list(find_all_method(smali_file_list))
    change_all_file(smali_file_list, all_method_list)
