import util as u
import re
import xml.etree.ElementTree as ET
import exception as e


def crypt_identifier(param_value):
    return ('a7ign' + u.crypt_identifier(param_value))[:90]


def change_meta(res_root):
    value_name = '{http://schemas.android.com/apk/res/android}name'
    for res_line in res_root.iter('meta-data'):  # For each resource
        param_value = res_line.get(value_name)
        if param_value is not None:
            if not param_value.startswith('@'):
                res_crypt_name = crypt_identifier(param_value)
                res_line.set(value_name, res_crypt_name)
                yield param_value, res_crypt_name


def change_all_res(res_root):
    """In the 'public.xml' rename all the entries of all the resources"""
    for res_line in res_root:  # For each resouce
        res_crypt_name = crypt_identifier(res_line.attrib.get('name'))
        if res_line.attrib.get('name') is not None:
            if res_line.attrib.get('name').startswith('android:'):
                return
        yield res_line.attrib.get('name'), res_crypt_name  # Return the resource name
        res_line.set('name', res_crypt_name)  # Append the string


def change_allfile(res_file_list, edited_res):
    """For all the resource file in '/res' try to change the file name"""
    for res_file in res_file_list:
        change_match_file(res_file, edited_res)


def change_match_file(file_name, edited_res):
    """Replace the file name of a resource"""
    dir_name, res_name, file_ext = u.get_file_info(file_name)
    if dict(edited_res)[res_name] is not None:
        res_crypt_name = crypt_identifier(res_name)
        new_file_name = dir_name + res_crypt_name + file_ext  # Append the string
        u.rename(file_name, new_file_name)  # Rename the file


def change_all_res_file(res_file_list, edited_res):
    """Search in all the resource XML files a resource reference"""
    for res_file in res_file_list:  # For each XML file
        if u.base_name(res_file) != 'public.xml':  # Do not edit the 'public.xml' file
            for res_line in u.open_file_input(res_file):  # For each line
                if re.search(r'@|name=|\:', res_line) is not None:  # If a resource reference is found
                    change_match_res_file(res_line, edited_res)
                else:  # Otherwise print back the line to file unchanged
                    print res_line,


def change_match_res_file(res_line, edited_res):
    """Replace into the XML the resource name"""
    res_line = re.sub(r'(@\*(.)*?)/', '\g<1>!TempSigPostPlaceHolder!', res_line)
    res_line = re.sub(r'android:', '!TempSigPostSecPlaceHolder!', res_line)
    res_line = re.sub(r'xmlns:', '!TempSigPostTirPlaceHolder!', res_line)
    res_line = re.sub(r'ns0:', '!TempSigPostPenPlaceHolder!', res_line)
    res_line = re.sub(r'http\:\/\/schemas\.android\.com\/apk\/res\/', '!TempSigPostQuadPlaceHolder!', res_line)
    res_line = re.sub(r'http\:\/\/schemas\.android\.com\/apk\/prv\/res\/', '!TempSigPostSetPlaceHolder!', res_line)
    res_line = re.sub(r'androidprv:', '!TempSigPostSisPlaceHolder!', res_line)
    for res_name, res_crypt_name in edited_res:
                #In a :res_name=" format
        res_line = res_line.replace(':' + res_name + '=', ':' + res_crypt_name + '=')
                #In a name="res_name" format
        res_line = res_line.replace('name="' + res_name + '"', 'name="' + res_crypt_name + '"')
                #In a "@/res_name" format
        res_line = res_line.replace('/' + res_name + '"', '/' + res_crypt_name + '"')
                #In a "?res_name" format
        res_line = res_line.replace('?' + res_name + '"', '?' + res_crypt_name + '"')
                #In a @/res_name format
        res_line = res_line.replace('/' + res_name + '<', '/' + res_crypt_name + '<')
                #In a res_other_name="res_name" format
    for res_name, res_crypt_name in edited_res:
        res_line = re.sub(r'(a7ign([^ ]*?)=")' + res_name + '"', '\g<1>' + res_crypt_name + '"', res_line)
    res_line = res_line.replace('!TempSigPostPlaceHolder!', '/')
    res_line = res_line.replace('!TempSigPostSecPlaceHolder!', 'android:')
    res_line = res_line.replace('!TempSigPostTirPlaceHolder!', 'xmlns:')
    res_line = res_line.replace('!TempSigPostQuadPlaceHolder!', 'http://schemas.android.com/apk/res/')
    res_line = res_line.replace('!TempSigPostPenPlaceHolder!', 'ns0:')
    res_line = res_line.replace('!TempSigPostSisPlaceHolder!', 'androidprv:')
    res_line = res_line.replace('!TempSigPostSetPlaceHolder!', 'http://schemas.android.com/apk/prv/res/')
    print res_line,  # Print back the line to file


def add_id_random_resource(res_root):
    """In the 'public.xml' add some random id resource"""
    last_id_index = 0
    for res_line in res_root:  # For each resource
        res_type = res_line.attrib.get('type')  # Return the resource type
        if res_type == 'id':  # Resource type is 'id'
            curr_id = int(res_line.attrib.get('id'), 16)
            if last_id_index < curr_id:  # Max id
                last_id_index = curr_id
    last_id_index += 1  # Next free resource id
    for count_res in range(u.random_res_interval()):  # Random number of id resource
        item_name = u.get_random(False, 16)
        res_root.append(ET.Element('public', {  # Add an id item
            'name': item_name,  # Item name
            'id': str(hex(last_id_index + count_res)),  # Item id
            'type': 'id'  # Item type
            }))
        yield item_name  # Return the added item name


def add_id_random_in_ids(ids_root, item_id_list):
    """In the 'ids.xml' add the id resources"""
    for id_item in item_id_list:
        ids_root.append(ET.Element('item', {  # Add an id item
            'name': id_item,
            'type': 'id'
            }))


def fix_ids(res_ids):
    """Apply a fix if the file 'ids.xml' does not exist"""
    if res_ids is None:
        res_ids = u.move_ids_xml()
        res_ids = u.load_res_id_repository()
    return res_ids


def obfuscate():
    """ The main obfuscator function """
    try:
        res_xml = u.load_res_repository()  # Load the 'pulbic.xml' resource repository
    except e.FileNotFound:
        return
    res_root = res_xml.getroot()  # The root of the XML file
    edited_res = set(
        list(change_all_res(res_root)) +
        list(change_meta(u.load_manifest().getroot()))
        )
    u.save_res_repository(res_xml)  # Save the 'pulbic.xml' resource repository back to file
    change_all_res_file(u.load_xml_file(), edited_res)
    change_allfile(u.load_resource_file(), edited_res)
    try:
        res_xml = u.load_res_repository()  # Load the 'pulbic.xml' resource repository
    except e.FileNotFound:
        return
    item_id_list = list(add_id_random_resource(res_root))
    u.save_res_repository(res_xml)  # Save the 'pulbic.xml' resource repository back to file
    ids_xml = fix_ids(u.load_res_id_repository())  # Load the 'ids.xml' resource repository
    ids_root = ids_xml.getroot()  # The root of the XML file
    add_id_random_in_ids(ids_root, item_id_list)
    u.save_ids_repository(ids_xml)  # Save the 'ids.xml' resource repository back to file
    append_defunct_class()


def append_defunct_class():
    """Load the defunct class """
    for smali_line in u.get_setter_resource_flag():
        if '#Res' in smali_line:
                print '    const/4 v0, 0x1'
        else:
            print smali_line,
