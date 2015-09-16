import util as u
import re


def find_all_activity_field(smali_file_list):
    """Search for an activity definition in all the the smali file"""
    for smali_file in smali_file_list:  # For each file
        for smali_line in u.open_file_input(smali_file):  # For each line
            if re.search(r'^\.super Landroid/app/Activity\;$', smali_line) is not None:  # If this line contains a field definition
                print '.super Landroid/app/ActivityOb;'
            elif re.search(r'Landroid/app/Activity\;\-\>', smali_line) is not None:
                print smali_line.replace('Landroid/app/Activity;-><', 'Landroid/app/ActivityOb;-><')
            else:
                print smali_line,  # Print back the line unchanged


def find_all_service_field(smali_file_list):
    """Search for an activity definition in all the the smali file"""
    for smali_file in smali_file_list:  # For each file
        for smali_line in u.open_file_input(smali_file):  # For each line
            if re.search(r'^\.super Landroid/app/Service\;$', smali_line) is not None:  # If this line contains a field definition
                print '.super Landroid/app/ServiceOb;'
            elif re.search(r'Landroid/app/Service\;\-\>', smali_line) is not None:
                print smali_line.replace('Landroid/app/Service;-><', 'Landroid/app/ServiceOb;-><')
            else:
                print smali_line,  # Print back the line unchanged


def obfuscate():
    """ The main obfuscator function """
    smali_file_list = u.load_smali_file()  # Load smali files
    find_all_activity_field(smali_file_list)
    find_all_service_field(smali_file_list)
    u.move_res_manager()
