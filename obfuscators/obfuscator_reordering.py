import util as u
import re

if_mapping = {
    'if-eq': 'if-ne',
    'if-ne': 'if-eq',
    'if-lt': 'if-ge',
    'if-ge': 'if-lt',
    'if-gt': 'if-le',
    'if-le': 'if-gt',
    'if-eqz': 'if-nez',
    'if-nez': 'if-eqz',
    'if-ltz': 'if-gez',
    'if-gez': 'if-ltz',
    'if-gtz': 'if-lez',
    'if-lez': 'if-gtz'
}


def is_beg_not_abstract_method(smali_line):  # Verify if a line is the beginning of an non-abstract method
    return re.search(r'^([ ]*?)\.method', smali_line) is not None and re.search(r' abstract ', smali_line) is None and re.search(r' native ', smali_line) is None


def is_end_method(smali_line):  # Verifiy if a line is the end of a method
    return re.search(r'^([ ]*?)\.end method', smali_line) is not None


def is_block_sign(smali_line):  # Verifiy if a smali line represent a block signpost
    return re.search(r'^\#\!Block\!\#$', smali_line) is not None


def define_code_block(smali_file, valid_op_code):
    """Try to define a code block"""
    edit_method = False  # Editing a method
    in_try = False  # In a try-catch
    for smali_line in u.open_file_input(smali_file):  # For each line
        if is_beg_not_abstract_method(smali_line) and not edit_method:  # Method start
            edit_method = True
            in_try = False
            print smali_line,  # Print the line unchanged
        elif is_end_method(smali_line) and edit_method:  # Method end
            edit_method = False
            print smali_line,  # Print the line unchanged
        elif edit_method:
            line_op_code = re.search(r'^([ ]*)(?P<opCode>([^ \n]+))([ ]|$)', smali_line)  # Match a line
            if line_op_code is not None:
                op_code = line_op_code.group('opCode')
                if re.search(r'^([ ]*?):try_start', op_code) is not None:  # Try start
                    in_try = True  # In try
                if re.search(r'^([ ]*?):try_end_', op_code) is not None:  # Try end
                    in_try = False  # Out try
                if op_code in valid_op_code and not in_try:
                    print '#!Block!#'  # Print block signpost
                    new_if = if_mapping.get(op_code, None)
                    if new_if is not None:
                        line_op_code = re.search(r'^([ ]*)(?P<opCode>([^ ]+)) (?P<regGo>[^:]*?):(?P<labelGo>[^ ]*?)$', smali_line)  # Match a line
                        if line_op_code is not None:
                            regGo = line_op_code.group('regGo')
                            labelGo = line_op_code.group('labelGo')
                            goto32_name = u.get_random(True, 15)  # Random jump name
                            print '    ' + new_if + ' ' + regGo + ':gl_' + goto32_name
                            print '    goto/32 :' + labelGo
                            print '    :gl_' + goto32_name
                    else:
                        print smali_line,
                else:
                    print smali_line,  # Print the line unchanged
            else:
                print smali_line,  # Print the line unchanged
        else:
            print smali_line,  # Print the line unchanged


def load_code_block(smali_file):
    """Read and split smali code into code blocks"""
    edit_method = False  # Editing a method
    jump_count = 0  # Current jump index
    for smali_line in u.open_file_input(smali_file):  # For each line
        if is_beg_not_abstract_method(smali_line) and not edit_method:  # Method start
            edit_method = True
            jump_count = 0
            print smali_line,  # Print the line unchanged
        elif is_end_method(smali_line) and edit_method:  # Method end
            edit_method = False
            print smali_line,  # Print the line unchanged
        elif edit_method:  # Reading method
            if is_block_sign(smali_line):  # Block signpost
                jump_name = u.get_random(True, 15)  # Random jump name
                jump_count += 1   # Increment jump count
                print '    goto/32 :l_' + jump_name + '_' + str(jump_count)
                print '    nop'
                print smali_line,
                print '    :l_' + jump_name + '_' + str(jump_count)
            else:
                print smali_line,  # Print the line unchanged
        else:
            print smali_line,  # Print the line unchanged


class Code_block:
    """"The class of a code block definition"""
    jump_id = 0  # The jump identifier
    smali_string = ''  # Smali code of the block

    def __init__(self, jump_id=0, smali_string=''):  # Init a block
        self.jump_id = jump_id or 0
        self.smali_string = smali_string or ''

    def put_code(self, smali_string):  # Add some smali code to the block
        self.smali_string = self.smali_string + smali_string


def mix_code_block(smali_file):
    """Print the code blocks in a mixed way"""
    edit_method = False  # Editing a method
    block_count = 0  # Current block index
    code_blocks = []  # Code blocks array
    for smali_line in u.open_file_input(smali_file):  # For each line
        if is_beg_not_abstract_method(smali_line) and not edit_method:  # Method start
            edit_method = True
            block_count = 0
            code_blocks = []
            print smali_line,  # Print the line unchanged
        elif is_end_method(smali_line) and edit_method:  # Method end
            edit_method = False
            u.shuffle_list(code_blocks)
            for code_block in code_blocks:
                print code_block.smali_string,
            print smali_line,  # Print the line unchanged
        elif edit_method:
            if is_block_sign(smali_line):  # Block signpost found
                block_count += 1  # Increment block index
                curr_code_block = Code_block(block_count, '')  # Read code block
                code_blocks.append(curr_code_block)  # Add to block list
            else:
                if block_count != 0:
                    curr_code_block.put_code(smali_line)  # Add smali code to current block
                else:
                    print smali_line,  # Print the line unchanged
        else:
            print smali_line,  # Print the line unchanged


def change_all_file(smali_file_list, valid_op_code):
    """Reoder all smali file"""
    for smali_file in smali_file_list:  # For all smali file
        define_code_block(smali_file, valid_op_code)
        load_code_block(smali_file)
        mix_code_block(smali_file)


def obfuscate():
    """ The main obfuscator function """
    smali_file_list = u.load_smali_file()
    change_all_file(smali_file_list, u.get_valid_block_code())
