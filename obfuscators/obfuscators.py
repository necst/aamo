#! /usr/bin/env python

import logging
import sys
import os
from datetime import datetime
import subprocess as sub

import util as u
import exception as e

import obfuscator_rebuild
import obfuscator_defunct
import obfuscator_renaming
import obfuscator_goto
import obfuscator_string
import obfuscator_indirections
import obfuscator_nop
import obfuscator_debug
import obfuscator_branch
import obfuscator_reordering
import obfuscator_reflection
import obfuscator_fields
import obfuscator_manifest
import obfuscator_resource
import obfuscator_raw
import obfuscator_restring
import obfuscator_asset
import obfuscator_intercept
import obfuscator_lib

base_dir = os.path.abspath(os.path.dirname(__file__))
obfuscator_resource_dir = base_dir + 'obfuscators'
obfuscator_log_file = base_dir + 'obfuscators.log'

debug = False
cleanup = True
enable_logging = True


def popen(com_str):
    p = sub.Popen(com_str, shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
    out, err = p.communicate()
    if enable_logging:
        u.logger(out)
        u.logger(err)
    if 'Exception' in out or 'Exception' in err:
        if 'method index is too large' in out or 'method index is too large' in err:
            raise e.AndroidLimitException('Unable run :' + com_str)
        elif 'java.lang.ArrayIndexOutOfBoundsException' in out or 'java.lang.ArrayIndexOutOfBoundsException' in err:
            raise e.AndroidRandomException('Unable run :' + com_str)
        else:
            raise e.RunningObfuscatorException('Unable run :' + com_str)


def clean_temp(sample_tf_dir):  # Clear the temporary support directory
    try:
        if enable_logging:
            u.logger('Directory cleaned: ' + sample_tf_dir)
        popen('rm -rf ' + sample_tf_dir + '/app')
    except OSError as ex:
        raise e.OpenToolException(str(ex) + '\nUnable to clean ' + sample_tf_dir)


def backsmali(sample_tf_dir, sample_file_name):  # Backsmali an apk file
    try:
        if enable_logging:
            u.logger('Backsmali: ' + sample_file_name + ' into ' + sample_tf_dir)
        popen('apktool d --force --no-debug-info ' + sample_file_name + ' ' + sample_tf_dir + '/app')
        if os.path.isdir(u.base_dir()+'/smali/com'):
            u.main_exec_dir = 'com'
        elif os.path.isdir(u.base_dir()+'/smali/org'):
            u.main_exec_dir = 'org'
        else:
            u.main_exec_dir = ''
    except OSError as ex:
        raise e.OpenToolException(str(ex) + '\nUnable to backsmali ' + sample_file_name + ' into ' + sample_tf_dir)


def smali(sample_tf_dir, sample_file_name):  # Smali an apk file
    try:
        if enable_logging:
            u.logger('Smali: ' + sample_file_name + ' from ' + sample_tf_dir)
        popen('apktool b --force-all ' + sample_tf_dir + '/app' + ' ' + sample_file_name)
    except OSError as ex:
        raise e.OpenToolException(str(ex) + '\nUnable to smali ' + sample_file_name + ' from ' + sample_tf_dir)


def sign_apk(sample_file_name):  # Sign an apk file with a SHA1 key
    try:
        if enable_logging:
            u.logger('Sign: ' + sample_file_name)
        popen('jarsigner -sigalg MD5withRSA -digestalg SHA1 -keystore ' + obfuscator_resource_dir + '/resignKey.keystore -storepass resignKey ' + sample_file_name + ' resignKey')
    except OSError as ex:
        raise e.OpenToolException(str(ex) + '\nUnable to sign ' + sample_file_name)


def zip_align(sample_file_name):  # Align the file
    try:
        if enable_logging:
            u.logger('Zip: ' + sample_file_name)
        popen('cp ' + sample_file_name + ' ' + sample_file_name + '_old.apk')
        popen('zipalign -f 8 ' + sample_file_name + '_old.apk' + ' ' + sample_file_name)
        popen('rm -f ' + sample_file_name + '_old.apk')
    except OSError as ex:
        raise e.OpenToolException(str(ex) + '\nUnable to zipalign ' + sample_file_name)


def design_apk(sample_file_name):  # Remove a signature from an apk file
    try:
        if enable_logging:
            u.logger('DeSign: ' + sample_file_name)
        popen('zip -d ' + sample_file_name + ' /META-INF/*')  # Delete the META-INF folder from the apk root
    except OSError as ex:
        raise e.OpenToolException(str(ex) + '\nUnable to delete META-INF from ' + sample_file_name)


def init(sample_tf_dir):  # Initialize the obfuscator routine
    reload(sys)
    sys.setdefaultencoding('utf-8')
    u.obfuscator_dir = obfuscator_resource_dir
    u.global_dir = sample_tf_dir + '/app'
    logging.basicConfig(filename=obfuscator_log_file, level=logging.DEBUG)
    if enable_logging:
        u.logger('Obfuscators Initialize: ' + u.obfuscator_dir + ' ' + u.global_dir)


def apply_resign(sample_file_name):  # Resign an apk file
    try:
        design_apk(sample_file_name)
        sign_apk(sample_file_name)
    except e.OpenToolException as ex:
        raise e.RunningObfuscatorException(str(ex))


def apply_zip(sample_file_name):  # Zipaling an apk file
    try:
        zip_align(sample_file_name)
    except e.OpenToolException as ex:
        raise e.RunningObfuscatorException(str(ex))


def apply_py_obfuscator(sample_file_name, sample_tf_dir, obfuscatorPy):
    '''Apply an obfuscator'''
    try:
        if enable_logging:
            u.logger('Python Obfuscator!')
        #backsmali(sample_tf_dir, sample_file_name)
        obfuscatorPy.obfuscate()
        if debug:
            smali(sample_tf_dir, sample_file_name)
        #sign_apk(sample_file_name)
        #clean_temp(sample_tf_dir)
    except (e.OpenToolException, e.LoadFileException) as ex:
        raise e.RunningObfuscatorException(str(ex) + '\nUnable run python obfuscator')


def run_obfuscator_resigned(sample_file_name, sample_tf_dir):
    try:
        if enable_logging:
            u.logger('Obfuscator Resign')
        apply_resign(sample_file_name)
    except e.OpenToolException as ex:
        raise e.RunningObfuscatorException(str(ex) + '\nUnable to apply Resign')


def run_obfuscator_zip(sample_file_name, sample_tf_dir):
    try:
        if enable_logging:
            u.logger('Obfuscator Align')
        apply_zip(sample_file_name)
    except e.RunningObfuscatorException as ex:
        raise e.RunningObfuscatorException(str(ex) + '\nUnable to apply Align')


def run_obfuscator_rebuild(sample_file_name, sample_tf_dir):
    try:
        if enable_logging:
            u.logger('Obfuscator Rebuild')
        apply_py_obfuscator(sample_file_name, sample_tf_dir, obfuscator_rebuild)
    except e.RunningObfuscatorException as ex:
        raise e.RunningObfuscatorException(str(ex) + '\nUnable to apply Rebuild')


def run_obfuscator_defunct(sample_file_name, sample_tf_dir):
    try:
        if enable_logging:
            u.logger('Obfuscator Defunct')
        apply_py_obfuscator(sample_file_name, sample_tf_dir, obfuscator_defunct)
    except e.RunningObfuscatorException as ex:
        raise e.RunningObfuscatorException(str(ex) + '\nUnable to apply Defunct')


def run_obfuscator_renaming(sample_file_name, sample_tf_dir):
    try:
        if enable_logging:
            u.logger('Obfuscator Renaming')
        apply_py_obfuscator(sample_file_name, sample_tf_dir, obfuscator_renaming)
    except e.RunningObfuscatorException as ex:
        raise e.RunningObfuscatorException(str(ex) + '\nUnable to apply Renaming')


def run_obfuscator_goto(sample_file_name, sample_tf_dir):
    try:
        if enable_logging:
            u.logger('Obfuscator Goto')
        apply_py_obfuscator(sample_file_name, sample_tf_dir, obfuscator_goto)
    except e.RunningObfuscatorException as ex:
        raise e.RunningObfuscatorException(str(ex) + '\nUnable to apply Goto')


def run_obfuscator_string(sample_file_name, sample_tf_dir):
    try:
        if enable_logging:
            u.logger('Obfuscator String')
        apply_py_obfuscator(sample_file_name, sample_tf_dir, obfuscator_string)
    except e.RunningObfuscatorException as ex:
        raise e.RunningObfuscatorException(str(ex) + '\nUnable to apply String')


def run_obfuscator_indirections(sample_file_name, sample_tf_dir):
    try:
        if enable_logging:
            u.logger('Obfuscator Indirections')
        apply_py_obfuscator(sample_file_name, sample_tf_dir, obfuscator_indirections)
    except e.RunningObfuscatorException as ex:
        raise e.RunningObfuscatorException(str(ex) + '\nUnable to apply Indirections')


def run_obfuscator_nop(sample_file_name, sample_tf_dir):
    try:
        if enable_logging:
            u.logger('Obfuscator Nop')
        apply_py_obfuscator(sample_file_name, sample_tf_dir, obfuscator_nop)
    except e.RunningObfuscatorException as ex:
        raise e.RunningObfuscatorException(str(ex) + '\nUnable to apply Nop')


def run_obfuscator_debug(sample_file_name, sample_tf_dir):
    try:
        if enable_logging:
            u.logger('Obfuscator Debug')
        apply_py_obfuscator(sample_file_name, sample_tf_dir, obfuscator_debug)
    except e.RunningObfuscatorException as ex:
        raise e.RunningObfuscatorException(str(ex) + '\nUnable to apply Debug')


def run_obfuscator_branch(sample_file_name, sample_tf_dir):
    try:
        if enable_logging:
            u.logger('Obfuscator Branch')
        apply_py_obfuscator(sample_file_name, sample_tf_dir, obfuscator_branch)
    except e.RunningObfuscatorException as ex:
        raise e.RunningObfuscatorException(str(ex) + '\nUnable to apply Branch')


def run_obfuscator_reordering(sample_file_name, sample_tf_dir):
    try:
        if enable_logging:
            u.logger('Obfuscator Reordering')
        apply_py_obfuscator(sample_file_name, sample_tf_dir, obfuscator_reordering)
    except e.RunningObfuscatorException as ex:
        raise e.RunningObfuscatorException(str(ex) + '\nUnable to apply Reordering')


def run_obfuscator_reflection(sample_file_name, sample_tf_dir):
    try:
        if enable_logging:
            u.logger('Obfuscator Reflection')
        apply_py_obfuscator(sample_file_name, sample_tf_dir, obfuscator_reflection)
    except e.RunningObfuscatorException as ex:
        raise e.RunningObfuscatorException(str(ex) + '\nUnable to apply Reflection')


def run_obfuscator_fields(sample_file_name, sample_tf_dir):
    try:
        if enable_logging:
            u.logger('Obfuscator Field')
        apply_py_obfuscator(sample_file_name, sample_tf_dir, obfuscator_fields)
    except e.RunningObfuscatorException as ex:
        raise e.RunningObfuscatorException(str(ex) + '\nUnable to apply Fields')


def run_obfuscator_manifest(sample_file_name, sample_tf_dir):
    try:
        if enable_logging:
            u.logger('Obfuscator Manifest')
        apply_py_obfuscator(sample_file_name, sample_tf_dir, obfuscator_manifest)
    except e.RunningObfuscatorException as ex:
        raise e.RunningObfuscatorException(str(ex) + '\nUnable to apply Manifest')


def run_obfuscator_resource(sample_file_name, sample_tf_dir):
    try:
        if enable_logging:
            u.logger('Obfuscator Resource')
        apply_py_obfuscator(sample_file_name, sample_tf_dir, obfuscator_resource)
    except e.RunningObfuscatorException as ex:
        raise e.RunningObfuscatorException(str(ex) + '\nUnable to apply Resource')


def run_obfuscator_raw(sample_file_name, sample_tf_dir):
    try:
        if enable_logging:
            u.logger('Obfuscator Raw')
        apply_py_obfuscator(sample_file_name, sample_tf_dir, obfuscator_raw)
    except e.RunningObfuscatorException as ex:
        raise e.RunningObfuscatorException(str(ex) + '\nUnable to apply Raw')


def run_obfuscator_restring(sample_file_name, sample_tf_dir):
    try:
        if enable_logging:
            u.logger('Obfuscator Restring')
        apply_py_obfuscator(sample_file_name, sample_tf_dir, obfuscator_restring)
    except e.RunningObfuscatorException as ex:
        raise e.RunningObfuscatorException(str(ex) + '\nUnable to apply Restring')


def run_obfuscator_asset(sample_file_name, sample_tf_dir):
    try:
        if enable_logging:
            u.logger('Obfuscator Asset')
        apply_py_obfuscator(sample_file_name, sample_tf_dir, obfuscator_asset)
    except e.RunningObfuscatorException as ex:
        raise e.RunningObfuscatorException(str(ex) + '\nUnable to apply Asset')


def run_obfuscator_intercept(sample_file_name, sample_tf_dir):
    try:
        if enable_logging:
            u.logger('Obfuscator Intercept')
        apply_py_obfuscator(sample_file_name, sample_tf_dir, obfuscator_intercept)
    except e.RunningObfuscatorException as ex:
        raise e.RunningObfuscatorException(str(ex) + '\nUnable to apply Intercept')


def run_obfuscator_lib(sample_file_name, sample_tf_dir):
    try:
        if enable_logging:
            u.logger('Obfuscator Lib')
        apply_py_obfuscator(sample_file_name, sample_tf_dir, obfuscator_lib)
    except e.RunningObfuscatorException as ex:
        raise e.RunningObfuscatorException(str(ex) + '\nUnable to apply Lib')


#The obfuscator DB Name to Method mapping
obfuscator_mapping = {
    'Resigned': run_obfuscator_resigned,
    'Alignment': run_obfuscator_zip,
    'Rebuild': run_obfuscator_rebuild,
    'Defunct': run_obfuscator_defunct,
    'Renaming': run_obfuscator_renaming,
    'Goto': run_obfuscator_goto,
    'StringEncrypt': run_obfuscator_string,
    'Indirections': run_obfuscator_indirections,
    'Nop': run_obfuscator_nop,
    'Debug': run_obfuscator_debug,
    'ArithmeticBranch': run_obfuscator_branch,
    'Reordering': run_obfuscator_reordering,
    'Reflection': run_obfuscator_reflection,
    'Fields': run_obfuscator_fields,
    'Manifest': run_obfuscator_manifest,
    'Resource': run_obfuscator_resource,
    'Raw': run_obfuscator_raw,
    'Restring': run_obfuscator_restring,
    'Asset': run_obfuscator_asset,
    'Intercept': run_obfuscator_intercept,
    'Lib': run_obfuscator_lib
}


def clean_apk(sample_file_name):  # Clear the temporary apk
    try:
        if enable_logging:
            u.logger('Apk cleaned: ' + sample_file_name)
        popen('rm -f ' + sample_file_name)
    except OSError as ex:
        raise e.OpenToolException(str(ex) + '\nUnable to clean ' + sample_file_name)


def obfuscate_sample(sample_file_name, obfuscator_list, sample_tf_dir):
    '''This function obfucate a sample with the obfuscators in the list using a temporary directory as support'''
    init(sample_tf_dir)
    if enable_logging:
        u.logger('Obfuscate Request: %s - %s - %s' % (sample_file_name, obfuscator_list, sample_tf_dir))
    else:
        u.logger('Obfuscate Request')
    if not debug:
        clean_temp(sample_tf_dir)
    backsmali(sample_tf_dir, sample_file_name)
    start_time = datetime.utcnow()
    if enable_logging:
        u.logger('Obfuscate Start: ' + str(start_time))
    try:
        for obfuscator_item in obfuscator_list:
            obfuscator_method = obfuscator_mapping[obfuscator_item]
            obfuscator_method(sample_file_name, sample_tf_dir)
    except KeyError as ex:
        raise e.RunningObfuscatorException('Invalid obfuscator id ' + str(ex))
    end_time = datetime.utcnow()
    if enable_logging:
        u.logger('Obfuscate Stop: ' + str(end_time))
    u.logger('Obfuscate Time: ' + str(end_time-start_time))
    if cleanup:
        sample_ob_file_name = sample_file_name + 'Ob'
    else:
        sample_ob_file_name = sample_file_name
    smali(sample_tf_dir, sample_ob_file_name)
    sign_apk(sample_ob_file_name)
    if not debug:
        clean_temp(sample_tf_dir)
        if cleanup:
            clean_apk(sample_file_name)
    u.logger('### SUCCESS ### {' + str(end_time-start_time) + '}')


def apply_dir(filename, obfuscator_to_apply, mode=0, retry=0):
    try:
        obfuscate_sample(adam_base_dir + 'input/' + filename, obfuscator_to_apply, adam_base_dir + 'temp/' + filename[:-4])
        sys.exit(0)
    except e.AndroidLimitException as ex:
        u.logger('### ERROR ### ' + str(ex) + ' ### ERROR ###')
        u.logger('### WARNING ###')
        if mode == 0:
            apply_dir(filename, [o for o in obfuscator_to_apply if o != 'Reflection'], 1)
        elif mode == 1:
            apply_dir(filename, [o for o in obfuscator_to_apply if o != 'Indirections'], 2)
        else:
            sys.exit(1)
    except e.AndroidRandomException as ex:
        u.logger('### ERROR ### ' + str(ex) + ' ### ERROR ###')
        if retry == 0:
            u.logger('### WARNING ###')
            apply_dir(filename, obfuscator_to_apply, mode, retry + 1)
        else:
            u.logger('### FAILURE ###')
            sys.exit(2)
    except Exception as ex:
        u.logger('### ERROR ### ' + str(ex) + ' ### ERROR ###')
        u.logger('### FAILURE ###')
        sys.exit(2)


'''obfuscator_to_apply = ['Resigned',
                       'Alignment',
                       'Rebuild',
                       'Fields',
                       'Debug',
                       'Indirections',
                       'Defunct',
                       'StringEncrypt',
                       'Renaming',
                       'Reordering',
                       'Goto',
                       'ArithmeticBranch',
                       'Nop',
                       'Asset',
                       'Intercept',
                       'Raw',
                       'Resource',
                       'Lib',
                       'Restring',
                       'Manifest',
                       'Reflection'
                       ]
'''

obfuscator_to_apply = ['Lib'
                       ]

def main():
    try:
        apply_dir(sys.argv[1], obfuscator_to_apply)
    except Exception, e:
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
