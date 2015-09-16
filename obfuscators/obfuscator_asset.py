import util as u
import re


def change_match_line(smali_line, class_name):
    """Redirect the invokation of openAssetResource"""
    invoke_match = re.search(r'^([ ]*?)(?P<invokeType>invoke\-([^ ]*?)) {(?P<invokeParam>([vp0-9,. ]*?))}, (?P<invokeObject>(\[*?)(L(.*?);|\[(I|Z|B|S|J|F|D|C)))->(?P<invokeMethod>(.*?))\((?P<invokePass>(.*?))\)(?P<invokeReturn>(.*?))$', smali_line)  # Match the method reference
    if invoke_match is None:
        print smali_line,
        return
    method_name = invoke_match.group('invokeMethod')  # Get the method name
    invoke_object = invoke_match.group('invokeObject')   # And the class name
    invokeParam = invoke_match.group('invokeParam')  # Call parameters
    if method_name == 'open' and invoke_object == 'Landroid/content/res/AssetManager;':
        if '..' in invokeParam:
            print '    invoke-static/range {'+invokeParam+'}, Landroid/content/res/' + class_name + ';->open(Landroid/content/res/AssetManager;Ljava/lang/String;)Ljava/io/InputStream;'
        else:
            print '    invoke-static {'+invokeParam+'}, Landroid/content/res/' + class_name + ';->open(Landroid/content/res/AssetManager;Ljava/lang/String;)Ljava/io/InputStream;'
    else:
        print smali_line,  # Otherwise print back the line unchanged


def change_all_direct_method(smali_file_list, class_name):
    """Search for a method reference in all the the smali file"""
    for smali_file in smali_file_list:  # For each file
        for smali_line in u.open_file_input(smali_file):  # For each line
            if re.search(r'^([ ]*?)invoke\-', smali_line) is not None:  # If contains a method reference
                change_match_line(smali_line, class_name)
            else:
                print smali_line,  # Print the line unchanged


def crypt_files(file_list):
    """Crypt some files"""
    for file_name in file_list:
        file_data = u.get_asset_file(file_name)
        file_data = u.crypt_raw(file_data)
        u.write_asset_file(file_name, file_data)


def change_allfile(file_list):
    """Rename all smali class files"""
    for file_name in file_list:
        change_match_file(file_name)


def change_match_file(file_name):
    """Rename a class file appending the string"""
    dir_name, res_name, file_ext = u.get_file_info(file_name)
    new_res_name = '!' + res_name + file_ext + '!'
    new_file_name = dir_name + new_res_name
    for class_crypt in re.findall(r'(\![^\!]*?\!)', new_file_name):
        new_file_name = new_file_name.replace(class_crypt, apply_crypt(class_crypt[:-1][1:]))
    u.rename(file_name, new_file_name)


def change_alldir(dir_list):
    """Rename all class dirs"""
    for dir_name in dir_list:  # For each class dir
        change_match_dir(dir_name)


def change_match_dir(dir_name):
    """Rename a class dir appending the string"""
    old_dir_name, res_name, file_ext = u.get_file_info(dir_name)
    new_res_name = apply_crypt(res_name)
    u.rename_dir(dir_name, old_dir_name + new_res_name)


def crypt_identifier(param_value):
    return (u.crypt_identifier(param_value))[:90]


def apply_crypt(string_const):
    """Apply the crypto routine to the string costant"""
    crypt_string = ''
    for sub_string in string_const.split('/'):
        crypt_string = '/'.join([crypt_string, crypt_identifier(sub_string)])
    return crypt_string  # Return the crypted string


def obfuscate():
    """ The main obfuscator function """
    class_name = 'a' + u.get_random(True, 7)
    asset_file_list = list(u.load_asset_file())
    crypt_files(asset_file_list)
    change_allfile(asset_file_list)
    change_alldir(u.load_asset_dirs()[:-1])
    smali_file_list = u.load_smali_file()  # Load smali files
    change_all_direct_method(smali_file_list, class_name)
    move_asset_class(class_name)


def move_asset_class(class_name):
    asset_class = u.get_asset_class()  # Load the decrypt class from file
    asset_class = asset_class.replace('AssetManagerOb', class_name)  # Random key
    u.write_text_file(u.base_dir()+'/smali/android/content/res/' + class_name + '.smali', asset_class)  # Write the class file
