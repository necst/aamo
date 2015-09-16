import util as u


def change_all_res_file(res_file_list):
    """Search in all the resource XML files a resource reference"""
    change_meta(u.load_manifest().getroot())
    for res_file in res_file_list:  # For each XML file
        if u.base_name(res_file) == 'strings.xml':  # Edit only the strings/colors resources
                ori_file_name = res_file
                purge_xml_tag_file(ori_file_name)
                res_file = res_file.replace(u.base_dir(), '')
                res_xml = u.load_xml(res_file)
                res_root = res_xml.getroot()
                change_match_res_string_file(res_root)
                u.save_xml(res_file, res_xml)
        if u.base_name(res_file) == 'arrays.xml' or u.base_name(res_file) == 'plurals.xml':  # Edit only the arrays/plurals resources
                ori_file_name = res_file
                purge_xml_tag_file(ori_file_name)
                res_file = res_file.replace(u.base_dir(), '')
                res_xml = u.load_xml(res_file)
                res_root = res_xml.getroot()
                change_match_res_array_file(res_root)
                u.save_xml(res_file, res_xml)


def purge_xml_tag_file(file_name):
    for xml_line in u.open_file_input(file_name):  # For each line
        xml_line = xml_line.replace('<b>', '\u003Cb\u003E')
        xml_line = xml_line.replace('</b>', '\u003C/b\u003E')
        xml_line = xml_line.replace('<i>', '\u003Ci\u003E')
        xml_line = xml_line.replace('</i>', '\u003C/i\u003E')
        xml_line = xml_line.replace('<u>', '\u003Cu\u003E')
        xml_line = xml_line.replace('</u>', '\u003C/u\u003E')
        xml_line = xml_line.replace('<font', '\u003Cfont')
        xml_line = xml_line.replace('</font>', '\u003C/font\u003E')
        print xml_line,  # Print back the line unchanged


def change_meta(res_root):
    value_name = '{http://schemas.android.com/apk/res/android}value'
    for res_line in res_root.iter('meta-data'):  # For each resource
        param_value = res_line.get(value_name)
        if param_value is not None:
            if not param_value.startswith('@'):
                res_line.set(value_name, apply_crypt(param_value))


def change_match_res_array_file(res_root):
    """Replace into the XML the string resource value"""
    for res_line in res_root.iter('string-array'):  # For each resource
        for item_line in res_line:  # For each sub-item
            if item_line.text is not None:
                if not item_line.text.startswith('@'):  # If not a resource reference
                    item_line.text = apply_crypt(item_line.text)   # Empties it!
    for res_line in res_root.iter('plurals'):  # For each resource
        for item_line in res_line:  # For each sub-item
            if item_line.text is not None:
                if not item_line.text.startswith('@'):  # If not a resource reference
                    item_line.text = apply_crypt(item_line.text)   # Empties it!


def change_match_res_string_file(res_root):
    """Replace into the XML the string resource value"""
    for res_line in res_root:  # For each resource
        res_line.text = apply_crypt(res_line.text)  # Empties it!


def apply_crypt(string_const):
    """Apply the crypto routine to the string costant"""
    if string_const is None:
        return ''
    if not u.is_number(string_const):
        return 'a7ign' + u.crypt_string(string_const)
    else:
        return string_const


def obfuscate():
    """ The main obfuscator function """
    change_all_res_file(u.load_xml_file())
    append_defunct_class()


def append_defunct_class():
    """Load the defunct class """
    for smali_line in u.get_setter_resource_flag():
        if '#Str' in smali_line:
                print '    const/4 v0, 0x1'
        else:
            print smali_line,
