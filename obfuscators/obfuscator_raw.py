import util as u
import exception as e


def append_defunct_class(raw_file):
    """Load the defunct class """
    for smali_line in u.get_setter_resource_flag():
        if '#RawList' in smali_line:
            for file_id in raw_file:
                print '    const v0, ' + file_id
                print '    invoke-static {v0}, Landroid/content/res/RawIdList;->addToList(I)V'
        elif '#Raw' in smali_line:
                print '    const/4 v0, 0x1'
        else:
            print smali_line,


def crypt_files(raw_file):
    """Crypt some files"""
    for file_name in raw_file:
        file_data = u.get_raw_file(file_name)
        file_data = u.crypt_raw(file_data)
        u.write_raw_file(file_name, file_data)


def get_all_raw_res(res_root):
    """Get all the raw resource defined in the public resource repository"""
    for res_line in res_root:  # For each resource
        res_type = res_line.attrib.get('type')  # Get the resource type
        if res_type == 'raw':  # If raw type
            yield (res_line.attrib.get('id'))  # Return the resource information


def obfuscate():
    """ The main obfuscator function """
    raw_file_list = list(u.load_raw_file())
    try:
        res_xml = u.load_res_repository()  # Load the 'pulbic.xml' resource repository
    except e.FileNotFound:
        return
    res_root = res_xml.getroot()  # The root of the XML file
    raw_id_list = list(get_all_raw_res(res_root))
    u.save_res_repository(res_xml)  # Save the 'pulbic.xml' resource repository back to file
    crypt_files(raw_file_list)
    append_defunct_class(raw_id_list)
