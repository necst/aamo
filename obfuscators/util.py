import os
import fnmatch
import xml.etree.ElementTree as ET
import random
import string
import exception as e
import logging
import fileinput
import base64
import md5
from Crypto.Cipher import DES


def logger(log_info):  # Log
    logging.debug('[' + base_dir().split('/')[-2] + ']:' + log_info)


def shuffle_list(data_list):  # Shuffle a list
    random.shuffle(data_list)


def open_file_input(file_name):  # Open a file for inline editing
    try:
        return fileinput.input(file_name, inplace=1)
    except IOError as ex:
        raise e.LoadFileException(str(ex)+'\nUnable to edit inplace file ' + file_name)


def random_nop_interval():  # Randomize the number of nop(s)
    return random.sample(xrange(3), 1)[0]+1


def get_random_int(min_int, max_int):  # Get a random integer
    return random.randint(min_int, max_int)


def get_random(mixed_type, str_len):  # Get a random string of strLen lenght
    type_random = string.letters  # Mixedcase Letter
    if not mixed_type:
        type_random = string.lowercase  # Lowercase letter
    return ''.join(random.sample(type_random, str_len))


def base_name(file_name):  # Return the filename in a path
    try:
        return os.path.basename(file_name)
    except OSError as ex:
        raise e.LoadFileException(str(ex) + '\nUnable to load path for ' + file_name)


def rename(file_name, new_file_name):  # Rename a file
    try:
        os.rename(file_name, new_file_name)
    except OSError as ex:
        raise e.LoadFileException(str(ex) + '\nUnable to rename ' + file_name + ' to ' + new_file_name)


def get_valid_block_code():  # Get the block opcode
    return get_text_as_list('codeBlockValidOpCode.txt')


def get_valid_debug_code():  # Get the debug opcode
    return get_text_as_list('debugValidOpCode.txt')


def get_valid_op_code():  # Get the valid opcode list
    return get_text_as_list('nopValidOpCode.txt')


def move_decrypt_method():  # Move the decription routine into the apk class tree
    try:
        method_name = 'nvlEStringManager.smali'
        os.system('cp -R '+ob_dir() + '/' + method_name + ' ' + base_dir() + '/smali/' + method_name)
    except OSError as ex:
        raise e.OpenToolException(str(ex) + '\nUnable to move Decrypytion Method')


def get_android_method_names():  # Return the list of the method of the SDK
    return get_text_as_list('androidLibMethodsTable.txt')


def get_defunct_method():  # Return the defunct method
    return get_text_file('defunctMethod.txt')


def get_text_file(file_name):  # Get a text from a file
    try:
        with open(ob_dir() + '/' + file_name) as file_list:
            return file_list.read()
    except IOError as ex:
        raise e.LoadFileException(str(ex) + '\nUnable to load ' + file_name)


def get_text_as_list(file_name):  # Get a text file as line-per-line list
    return get_text_file(file_name).splitlines()

global_dir = ''  # The base directory
obfuscator_dir = ''  # Obfuscator resource directory


def ob_dir():  # Return the base directory
    return obfuscator_dir


def base_dir():  # Return the base directory
    return global_dir


def load_smali_file():  # Load all the smali files
    return load_files('', '*.smali', '')


def load_xml_file():  # Load all the xml files
    return load_files('', '*.xml', '')


def load_resource_file():  # Load all the resource files
    return load_files('/res/', '*', 'values')


def load_res_repository():  # Load the public resource repository
    return load_xml('/res/values/public.xml')


def save_res_repository(xml_file):  # Save the public resource repository
    save_xml('/res/values/public.xml', xml_file)


def load_manifest():  # Load the apk manifest file
    return load_xml('/AndroidManifest.xml')


def save_manifest(xml_file):  # Save the apk manifest file
    save_xml('/AndroidManifest.xml', xml_file)


def load_xml(file_name):  # Load an XML file
    try:
        parser = ET.XMLParser(encoding="utf-8")
        return ET.parse(base_dir() + file_name, parser=parser)
    except IOError as ex:
        if ex.errno == 2:
            raise e.FileNotFound
        else:
            raise e.LoadFileException(str(ex)+'\nUnable to load XML ' + base_dir() + file_name)


def save_xml(file_name, xml_file):  # Save an XML file
    try:
        xml_file.write(base_dir() + file_name)
    except IOError as ex:
        raise e.LoadFileException(str(ex)+'\nUnable to save XML ' + base_dir() + file_name)


def load_files(path_add, pattern, exclude_dir_prefix):  # Load all the files from a directory whic respect a pattern and does not start with a given prefix
    return set(find_files(base_dir() + path_add, pattern, exclude_dir_prefix))


def get_file_name(file_path):  # Extract the last dir of a path
    return file_path.split('/')[-1]


def get_file_info(file_name):  # Extract some file information from a path
    file_base = base_name(file_name)
    res_name = file_base.split('.')[0]
    dir_name = file_name[:-len(file_base)]
    file_ext = file_base[len(res_name):]
    return dir_name, res_name, file_ext


def find_files(top_dir, pattern, exclude_dir_prefix):
    '''Walk trought the directory tree and return all the files that respect the pattern and do not are in the exclude_dir_prefix folder'''
    try:
        for dir_path, dir_names, file_names in os.walk(top_dir):
                for file_name in file_names:
                    if not exclude_dir_prefix or not get_file_name(dir_path).startswith(exclude_dir_prefix):
                        if fnmatch.fnmatch(file_name, pattern):
                            yield os.path.join(dir_path, file_name)
    except (IOError, OSError) as ex:
        raise e.LoadFileException(str(ex)+'\nUnable to load ' + top_dir + ' with pattern ' + pattern + ' excluding ' + exclude_dir_prefix)


def rename_dir(source_dir, dest_dir):  # Rename a directory
    try:
        os.renames(source_dir, dest_dir)
    except OSError as ex:
        raise e.LoadFileException(str(ex) + '\nUnable to rename ' + source_dir + ' to ' + dest_dir)


def load_smali_dirs():  # Load all the class directory
    return load_dirs('/smali', '/' + get_main_exec_dir())


def load_dirs(path_add, exclude_dir_prefix):  # Load all the subdirectories from a directory
    return list(reversed(sorted(list(find_dir(base_dir() + path_add, exclude_dir_prefix)), key=len)))


def find_dir(top_dir, exclude_dir_prefix):
    '''Walk trought the directory tree and return all the directory except for the base directory and the exclude_dir_prefix folder'''
    try:
        for dir_path, dir_names, file_names in os.walk(top_dir):
            if not exclude_dir_prefix or (dir_path != top_dir and dir_path != top_dir + exclude_dir_prefix):
                yield dir_path
    except (IOError, OSError) as ex:
        raise e.LoadFileException(str(ex)+'\nUnable to load ' + top_dir + ' excluding ' + exclude_dir_prefix)


def load_all_smali_dirs():  # Load all the class directory
    smali_dir_list = load_smali_dirs()
    smali_dir_list.append(base_dir() + '/smali' + '/' + get_main_exec_dir())
    smali_dir_list.append(base_dir() + '/smali')
    return smali_dir_list


def get_defunct_class():  # Return the defunct class
    return get_text_file('defunctClass.txt')


def write_text_file(file_name, file_data):  # Write a text to a file
    try:
        with open(file_name, 'w') as file_list:
            return file_list.write(file_data)
    except IOError as ex:
        raise e.LoadFileException(str(ex) + '\nUnable to write ' + file_name)


def pad_pkcs5(file_data):
    return file_data + (8 - len(file_data) % 8) * chr(8 - len(file_data) % 8)


def get_raw_file(file_name):
    return get_binary_file(file_name)


def write_raw_file(file_name, file_data):
    write_binary_file(file_name, file_data)


def write_binary_file(file_name, file_data):
    try:
        with open(file_name, "wb+") as file_bin:
            file_bin.write(file_data)
    except IOError as ex:
        raise e.LoadFileException(str(ex) + '\nUnable to binary write ' + file_name)


def get_binary_file(file_name):
    try:
        with open(file_name, "rb+") as file_bin:
            return file_bin.read()
    except IOError as ex:
        raise e.LoadFileException(str(ex) + '\nUnable to binary load ' + file_name)


def random_res_interval():  # Randomize the number of new resource(s)
    return random.sample(xrange(10), 1)[0]+10


def save_ids_repository(xml_file):  # Save the id resources repository
    save_xml('/res/values/ids.xml', xml_file)


def move_ids_xml():  # Move the id resources index into the value resource dir
    try:
        os.system('cp -R ' + ob_dir() + '/ids.xml ' + base_dir() + '/res/values/ids.xml')
    except OSError as ex:
        raise e.OpenToolException(str(ex) + '\nUnable to move Ids xml file')


def load_res_id_repository():  # Load the ids resource repository
    try:
        return load_xml('/res/values/ids.xml')
    except e.LoadFileException:
        return None
    except e.FileNotFound:
        return None


def load_asset_file():  # Load all the resource files
    return load_files('/assets/', '*', '')


def get_asset_file(file_name):
    return get_binary_file(file_name)


def write_asset_file(file_name, file_data):
    write_binary_file(file_name, file_data)


def load_asset_dirs():  # Load all the class directory
    return load_dirs('/assets', '')


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def load_raw_file():  # Load all the resource files
    return load_files('/res/raw/', '*', '')


main_exec_dir = ''


def get_main_exec_dir():
    return main_exec_dir


def crypt_identifier(id_value):
    return 'a' + md5_data(id_value).hexdigest().lower()[:8]


def crypt_string(string_const):
    return base64.b16encode(crypt_data(string_const, '*StrGhy*', True)).lower()


def crypt_raw(file_data):
    return crypt_data(file_data, '*RawKey*')


def crypt_data(file_data, des_key, is_string=False):
    if is_string:
        file_data = file_data.encode('utf-8')
    return DES.new(des_key, DES.MODE_ECB).encrypt(pad_pkcs5(file_data))


def md5_data(file_data, is_string=False):
    if is_string:
        file_data = file_data.encode('utf-8')
    return md5.new(file_data)


def move_res_manager():
    os.system('mkdir -p ' + base_dir() + '/smali/android/app/')
    os.system('cp -rf ' + ob_dir() + '/android/app/ActivityOb.smali ' + base_dir() + '/smali/android/app/ActivityOb.smali')
    os.system('cp -rf  ' + ob_dir() + '/android/app/ServiceOb.smali ' + base_dir() + '/smali/android/app/ServiceOb.smali')
    os.system('mkdir -p ' + base_dir() + '/smali/android/content/res')
    os.system('cp -rf ' + ob_dir() + '/android/content/ContextWrapperOb.smali ' + base_dir() + '/smali/android/content/ContextWrapperOb.smali')
    os.system('cp -rf ' + ob_dir() + '/android/content/res/Base16.smali ' + base_dir() + '/smali/android/content/res/Base16.smali')
    os.system('cp -rf ' + ob_dir() + '/android/content/res/ResourcesOb.smali ' + base_dir() + '/smali/android/content/res/ResourcesOb.smali')
    os.system('cp -rf ' + ob_dir() + '/android/content/res/StringUnescape.smali ' + base_dir() + '/smali/android/content/res/StringUnescape.smali')
    os.system('cp -rf ' + ob_dir() + '/android/content/res/RawIdList.smali ' + base_dir() + '/smali/android/content/res/RawIdList.smali')
    os.system('cp -rf ' + ob_dir() + '/android/content/res/LibOb.smali ' + base_dir() + '/smali/android/content/res/LibOb.smali')


def get_string_class():
    os.system('mkdir -p ' + base_dir() + '/smali/android/content/res')
    return get_text_file('android/content/res/StringManagerOb.smali')


def get_asset_class():
    os.system('mkdir -p ' + base_dir() + '/smali/android/content/res')
    return get_text_file('android/content/res/AssetManagerOb.smali')


def get_setter_resource_flag():
    return open_file_input(list(load_files('', 'RawIdList.smali', ''))[0])


def load_lib_file():  # Load all the resource files
    return load_files('/lib/', 'lib*.so', '')


def write_lib_file(file_name, file_data):
    write_binary_file(file_name, file_data)
