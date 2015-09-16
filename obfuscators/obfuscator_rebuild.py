#import util as u

def obfuscate():
	pass
'''	
	""" The main obfuscator function """
	asset_file_list = list(u.load_asset_file())
	raw_file_list = list(u.load_raw_file())
	file_list = set(asset_file_list + raw_file_list)
	for file_name in file_list:
		u.logger('FILE_NE: ' + str(file_name))
'''