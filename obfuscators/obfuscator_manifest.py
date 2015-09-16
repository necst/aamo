import util as u
import re


def crypt_identifier(param_value):
    return u.crypt_identifier(param_value)


def fix_invalid_id(smali_line):
    smali_line = smali_line.replace('$;', '@&;')
    smali_line = smali_line.replace('$/', '@&/')
    while smali_line.find('$@&') != -1:
        smali_line = smali_line.replace('$@&', '@&@&')
    return smali_line


def defix_invalid_id(smali_line):
    return smali_line.replace('@&', '$')


def get_match_line(smali_line):
    """Rename a class definition"""
    class_match = re.search(r'^([ ]*?)\.class(.*?)(?P<className>L([^;\(\) ]*?);)', smali_line)
    if class_match is None:
        print smali_line,
        return None
    class_name = class_match.group('className')  # Recover the old class name
    smali_line = smali_line.replace(class_name, 'L!' + class_name[1:])  # Append and print back the line
    smali_line = fix_invalid_id(smali_line)
    smali_line = re.sub(r'/', '!/!', smali_line)  # Append and print back the line
    smali_line = re.sub(r'L!' + get_main_exec_dir() + '!/', 'L' + get_main_exec_dir() + '/', smali_line)
    smali_line = re.sub(r'\$', '!$!', smali_line)  # Append and print back the line
    smali_line = re.sub(r';', '!;', smali_line)
    smali_line = defix_invalid_id(smali_line)
    for class_crypt in re.findall(r'(\![^\!]*?\!)', smali_line):
        smali_line = smali_line.replace(class_crypt, crypt_identifier(class_crypt[:-1][1:]))
    print smali_line,  # Append and print back the line
    return class_name  # Return the edited class name


def get_match_source_line(smali_line):
    """Rename a source definition"""
    source_match = re.search(r'^([ ]*?)\.source(.*?)\"(?P<sourceName>([^\"]*?))\"', smali_line)
    if source_match is not None:
        source_name = source_match.group('sourceName')  # Recover the old source name
        smali_line = smali_line.replace(source_name, 'a' + u.get_random(True, 8) + '.java')
    print smali_line,


def get_match_subclass_annotation(smali_line):
    """Rename a class definition"""
    class_match = re.search(r'^([ ]*?)name = \"(?P<className>[^\"]*?)\"$', smali_line)
    if class_match is None:
        print smali_line,
        return
    class_name = class_match.group('className')  # Recover the old class name
    print '    name = "' + crypt_identifier(class_name) + '"'  # Append and print back the line


def fix_safe_test(smali_file_list):
    for smali_file in smali_file_list:  # For each file
        for smali_line in u.open_file_input(smali_file):  # For each line
            if re.search(r'safetest', smali_line) is not None:
                class_match = re.search(r'(?P<className>Lcom/safetest/[^;]*?;)', smali_line)
                if class_match is None:
                    print smali_line,
                else:
                    class_name = class_match.group('className')  # Recover the old class name
                    change_match_line(smali_line,[class_name])
            else:
                print smali_line,


def find_all_class(smali_file_list):
    """Search for a class definition in all the the smali file"""
    annotation_flag = False
    signature_flag = False
    for smali_file in smali_file_list:  # For each file
        for smali_line in u.open_file_input(smali_file):  # For each line
            if re.search(r'^([ ]*?)\.source', smali_line) is not None:  # If this line contains a class definition
                get_match_source_line(smali_line)
            elif re.search(r'^([ ]*?)\.class', smali_line) is not None:  # If this line contains a class definition
                class_name = get_match_line(smali_line)
                if class_name is not None:
                    yield class_name
            elif re.search(r'^([ ]*?)\.annotation system Ldalvik/annotation/InnerClass;', smali_line) is not None:
                annotation_flag = True
                print smali_line,
            elif re.search(r'^([ ]*?)\.annotation system Ldalvik/annotation/Signature;', smali_line) is not None:
                signature_flag = True
                print smali_line,
            elif re.search(r'^([ ]*?)\.end annotation', smali_line) is not None and annotation_flag is True:
                annotation_flag = False
                print smali_line,
            elif re.search(r'^([ ]*?)\.end annotation', smali_line) is not None and signature_flag is True:
                signature_flag = False
                print smali_line,
            elif annotation_flag is True and re.search(r'^([ ]*?)name = \"', smali_line):
                get_match_subclass_annotation(smali_line)
            elif signature_flag is True and re.search(r'^([ ]*?)\"(.*)\"', smali_line):
                get_match_subclass_signature(smali_line)
            else:
                print smali_line,  # Print the line unchanged


def get_match_subclass_signature(smali_line):
    """Rename a class definition"""
    class_match = re.search(r'^([ ]*?)\"(?P<className>[^\"]*?)\"(\,)?$', smali_line)
    if class_match is None:
        print smali_line,
        return
    class_name = class_match.group('className')  # Recover the old class name
    print smali_line.replace('"' + class_name + '"', '"' + class_name + ';|Sign|' + '"')


def get_sub_class(class_name):
    """Returns all the subclasses of a class"""
    class_name = fix_invalid_id(class_name)
    while '$' in class_name:
        class_name = class_name[:class_name.rfind('$')]+';'
        yield defix_invalid_id(class_name)


def change_match_line(smali_line, edited_class):
    """Rename all the classes reference to edited classes in the current line"""
    for class_name in re.findall(r'(L[^;:\(\) ]*?;)', smali_line):  # Match all the classes references
        if class_name in edited_class:  # For each edited class
            new_class_name = 'L!' + class_name[1:]
            new_class_name = new_class_name.replace('/', '!/!')  # Rename the directory tree
            new_class_name = new_class_name.replace('L!' + get_main_exec_dir() + '!/', 'L' + get_main_exec_dir() + '/')  # Do not rename /com
            new_class_name = new_class_name.replace(';', '!;')
            smali_line = smali_line.replace(class_name, new_class_name)  # Rename
        for sub_class_name in get_sub_class(class_name):  # For each subclass
            if sub_class_name in edited_class:
                new_sub_class_name = 'L!' + sub_class_name[1:]
                new_sub_class_name = new_sub_class_name.replace('/', '!/!')  # Rename the directory tree
                new_sub_class_name = new_sub_class_name.replace('L!' + get_main_exec_dir() + '!/', 'L' + get_main_exec_dir() + '/')  # Do not rename /com
                smali_line = smali_line.replace(new_sub_class_name[:-1]+'$', new_sub_class_name[:-1] + '!$!')  # Rename
    for class_crypt in re.findall(r'(\![^\!]*?\!)', smali_line):
        smali_line = smali_line.replace(class_crypt, crypt_identifier(class_crypt[:-1][1:]))
    smali_line = smali_line.replace(';|Sign|', '')
    print smali_line,  # Print the line


def change_all_class(edited_class, smali_file_list):
    """Search for a class reference in all the the smali file"""
    for smali_file in smali_file_list:  # For each smali file
        for smali_line in u.open_file_input(smali_file):  # For each line
            if re.search(r'L([^;\(\) ]*?);', smali_line) is not None:  # If contains a class reference
                change_match_line(smali_line, edited_class)
            elif re.search(r'\;\|Sign\|', smali_line) is not None:
                print smali_line.replace(';|Sign|', ''),
            else:
                print smali_line,  # Print the line unchanged


def fix_invalid_file(smali_line):
    smali_line = smali_line + '!fine'
    smali_line = smali_line.replace('$!fine', '@&!fine')
    smali_line = smali_line.replace('!fine', '')
    smali_line = smali_line.replace('$$', '$@&')
    while smali_line.find('$@&') != -1:
        smali_line = smali_line.replace('$@&', '@&@&')
    return smali_line


def defix_invalid_file(smali_line):
    return smali_line.replace('@&', '$')


def change_allfile(smali_file_list):
    """Rename all smali class files"""
    for smali_file in smali_file_list:  # For each smali file
        change_match_file(smali_file)


def change_alldir(smali_dir_list):
    """Rename all class dirs"""
    for smali_dir in smali_dir_list:  # For each class dir
        change_match_dir(smali_dir)


def change_match_dir(dir_name):
    """Rename a class dir appending the string"""
    old_dir_name, res_name, file_ext = u.get_file_info(dir_name)
    new_res_name = crypt_identifier(res_name)
    u.rename_dir(dir_name, old_dir_name + new_res_name)


def change_match_file(file_name):
    """Rename a class file appending the string"""
    dir_name, res_name, file_ext = u.get_file_info(file_name)
    res_name = fix_invalid_file(res_name)
    new_res_name = '!' + res_name + '!'
    new_res_name = new_res_name.replace('$', '!$!')
    new_file_name = dir_name + new_res_name + file_ext
    new_file_name = defix_invalid_file(new_file_name)
    for class_crypt in re.findall(r'(\![^\!]*?\!)', new_file_name):
        new_file_name = new_file_name.replace(class_crypt, crypt_identifier(class_crypt[:-1][1:]))
    u.rename(file_name, new_file_name)


def get_res_class(edited_class):
    """Translate the class name representation from SMALI to XML"""
    for class_name in edited_class:  # For each edited class
        if class_name.startswith('L' + get_main_exec_dir() + '/'):  # Only if it starts with 'com'
            class_name = fix_invalid_id(class_name)
            class_name = class_name.replace('/', '.').replace(';', '').replace('$', '.')[1:]  # Translate
            yield defix_invalid_id(class_name)


def change_all_res_file(res_file_list, edited_class, package_name):
    """"Search in all the resource XML files a class reference"""
    for res_file in res_file_list:  # For each XML resource file
        for res_line in u.open_file_input(res_file):  # For each line
            if re.search(r'(\"|\<|\/)' + get_main_exec_dir() + '\.', res_line) is not None:  # If contain a class signpost
                res_line = change_match_res_file(res_line, edited_class)
            if re.search(r'(\"|\<|\/)\.', res_line) is not None:  # If contain a class signpost
                res_line = change_match_res_file_package(res_line, edited_class, package_name)
            print res_line,  # Print the line back  unchanged


def change_match_res_file_package(res_line, edited_class, package_name):
    """Replace all the edited classes names found in the current XML line"""
    for class_name in edited_class:  # Fo each edited class
        class_name = class_name.replace(package_name, '')
        if class_name.startswith('.'):
            new_class_name = class_name.replace('.', '!.!')  # appending
            new_class_name = new_class_name[1:]
            res_line = res_line.replace('"' + class_name, '"' + new_class_name + '!')  # Append
            res_line = res_line.replace('/' + class_name, '/' + new_class_name + '!')  # Append
            res_line = res_line.replace('<' + class_name, '<' + new_class_name + '!')  # Append
            for class_crypt in re.findall(r'(\![^\!]*?\!)', res_line):
                res_line = res_line.replace(class_crypt, crypt_identifier(class_crypt[:-1][1:]))
    return res_line  # Print the line back


def change_match_res_file(res_line, edited_class):
    """Replace all the edited classes names found in the current XML line"""
    for class_name in edited_class:  # Fo each edited class
        new_class_name = class_name.replace('.', '!.!')  # Append
        res_line = res_line.replace('"' + class_name, '"!' + new_class_name + '!')  # Append
        res_line = res_line.replace('/' + class_name, '/!' + new_class_name + '!')  # Append
        res_line = res_line.replace('<' + class_name, '<!' + new_class_name + '!')  # Append
        res_line = res_line.replace('!' + get_main_exec_dir() + '!.', get_main_exec_dir() + '.')  # Do not rename /com
        for class_crypt in re.findall(r'(\![^\!]*?\!)', res_line):
            res_line = res_line.replace(class_crypt, crypt_identifier(class_crypt[:-1][1:]))
    return res_line  # Print the line back


def change_package_name(manifest_xml):
    package_name = manifest_xml.getroot().get('package')
    new_package_name = package_name.replace('.', '!.!')  # Append
    new_package_name = '!' + new_package_name + '!'
    new_package_name = new_package_name.replace('!' + get_main_exec_dir() + '!.', get_main_exec_dir() + '.')  # Do not rename /com
    for class_crypt in re.findall(r'(\![^\!]*?\!)', new_package_name):
        new_package_name = new_package_name.replace(class_crypt, crypt_identifier(class_crypt[:-1][1:]))
    manifest_xml.getroot().set('package', new_package_name)  # Rename the package
    manifest_xml.getroot().set('{http://schemas.android.com/apk/res/android}sharedUserId', u.get_random(True, 16) + '.uid.shared')  # Rename the package
    yield 'http://schemas.android.com/apk/res/' + package_name, 'http://schemas.android.com/apk/res/' + new_package_name
    yield '<' + package_name, '<' + new_package_name
    yield '</' + package_name, '</' + new_package_name
    yield 'package="' + package_name, 'package="' + new_package_name
    yield '@*' + package_name + ':', '@*' + new_package_name + ':'
    yield '"' + package_name, '"' + new_package_name
    yield '/' + package_name + '/', '/' + new_package_name + '/'


def verify_filter(value, filter_list):
    if value is None:
        return False
    for filter_item in filter_list:
        if value.startswith(filter_item):
            return False
    return True


def change_all_res_file_package(res_file_list, rename_list):
    """"Search in all the resource XML files a reference"""
    for res_file in res_file_list:  # For each XML resource file
        for res_line in u.open_file_input(res_file):  # For each line
            change_match_res_file_of_package(res_line, rename_list)


def change_match_res_file_of_package(res_line, rename_list):
    """Replace all the edited names found in the current XML line"""
    for (rename_name, rename_new_name) in rename_list:  # Fo each edited name
        if not rename_name.startswith('!NewNoEdit!'):
            res_line = res_line.replace(rename_name, rename_new_name)
    print res_line,  # Print the line back


def rename_val(xml_file, object_name, param_name, filter_list=[], propagate_upd=True, verify_name='', default_value=''):
    objects_list = xml_file.getroot().iter(object_name)
    package_name = '{http://schemas.android.com/apk/res/android}'
    param_set_full_name = package_name + param_name
    if verify_name != '':
        param_ver_full_name = package_name + verify_name
    else:
        param_ver_full_name = param_set_full_name
    for obj in objects_list:
        param_value = obj.get(param_ver_full_name)
        if verify_filter(param_value, filter_list):
            if default_value != '':
                random_value = default_value
            else:
                if param_value.startswith('.'):
                    random_value = '.a' + u.get_random(True, 32)
                else:
                    random_value = 'a.' + u.get_random(True, 32)
            obj.set(param_set_full_name, random_value)
            if propagate_upd:
                yield param_value, random_value
            else:
                yield '!NewNoEdit!' + param_value, random_value


package_name = ''


def init_package_name():
    global package_name
    package_name = u.load_manifest().getroot().get('package')


def get_main_exec_dir():
    if u.get_main_exec_dir() == '':
        return package_name.split('.')[0]
    else:
        return u.get_main_exec_dir()


def obfuscate():
    """ The main obfuscator function """
    init_package_name()
    smali_file_list = u.load_smali_file()  # Load the smali files
    res_file_list = set(list(u.load_xml_file()) + list(smali_file_list))   # Load the XML files
    edited_class = set(find_all_class(smali_file_list))
    change_all_class(edited_class, smali_file_list)
    change_all_res_file(res_file_list, set(get_res_class(edited_class)), package_name)
    manifest_xml = u.load_manifest()  # Load the Manifest file
    task_affinity = 'a' + u.get_random(True, 7) + '.' + 'a' + u.get_random(True, 7)
    rename_list = set(
        list(change_package_name(manifest_xml)) +
        list(rename_val(manifest_xml, 'activity', 'label', ['@'], False)) +
        list(rename_val(manifest_xml, 'activity', 'process', ['@'], False)) +
        list(rename_val(manifest_xml, 'application', 'label', ['@'], False)) +
        list(rename_val(manifest_xml, 'provider', 'label', ['@'], False)) +
        list(rename_val(manifest_xml, 'provider', 'process', ['@'], False)) +
        list(rename_val(manifest_xml, 'activity-alias', 'name', ['@'], False)) +
        list(rename_val(manifest_xml, 'activity-alias', 'label', ['@'], False)) +
        list(rename_val(manifest_xml, 'service', 'label', ['@'], False)) +
        list(rename_val(manifest_xml, 'service', 'process', ['@'], False)) +
        list(rename_val(manifest_xml, 'receiver', 'label', ['@'], False)) +
        list(rename_val(manifest_xml, 'receiver', 'process', ['@'], False)) +
        list(rename_val(manifest_xml, 'intent-filter', 'label', ['@'], False)) +
        list(rename_val(manifest_xml, 'permission', 'label', ['@'], False)) +
        list(rename_val(manifest_xml, 'permission', 'description', ['@'], False)) +
        list(rename_val(manifest_xml, 'permission-group', 'label', ['@'], False)) +
        list(rename_val(manifest_xml, 'permission-group', 'description', ['@'], False)) +
        list(rename_val(manifest_xml, 'permission-tree', 'label', ['@'], False)) +
        list(rename_val(manifest_xml, 'instrumentation', 'label', ['@'], False)) +
        list(rename_val(manifest_xml, 'action', 'name', ['@', 'com.android.', 'android.'], False)) +
        list(rename_val(manifest_xml, 'activity', 'taskAffinity', ['android.', 'com.android.', '@'], False, 'name', task_affinity)) +
        list(rename_val(manifest_xml, 'application', 'taskAffinity', ['android.', 'com.android.', '@'], False, 'name', task_affinity))
        )
    log_tag_bho(manifest_xml, 'data')
    change_all_res_file_package(res_file_list, rename_list)
    u.save_manifest(manifest_xml)  # Write back the Manifest file'''
    fix_safe_test(smali_file_list)
    change_allfile(smali_file_list)
    change_alldir(u.load_smali_dirs())


def data_replace(obj, obj_sub_name, valid_value, replace_value):
    full_obj_name = '{http://schemas.android.com/apk/res/android}' + obj_sub_name
    obj_sub = obj.get(full_obj_name)
    if obj_sub is None or obj_sub in valid_value or obj_sub == '':
        return
    obj.set(full_obj_name, replace_value)


def log_tag_bho(xml_file, object_name):
    objects_list = xml_file.getroot().iter(object_name)
    for obj in objects_list:
        data_replace(obj, 'mimeType', [], '*/*')
        data_replace(obj, 'pathPattern', [], '*')
        data_replace(obj, 'pathPrefix', [], '*')
        data_replace(obj, 'host', [], '*')
        data_replace(obj, 'path', [], '*')
