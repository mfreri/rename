#!/usr/bin/env python3
# encoding: utf-8
# Original version 0.1a, from december 21, 2022.


__HELP__ = '''
Syntax:
rename original_filename new_filename
rename [options]

Options:
-e <ext1> <ext2>  Change the extension of the files from <ext1> to <ext2>.
-h, --help        Display help.
-n [extension]    Enumerate the files with the given <extension>. If no 
                  extension is passed, all files will be enumerated.
-v, --version     Display version info.

Examples:
rename -e jpeg, jpg
Change the extension of all the jpeg files to jpg.

rename file1.txt file01.txt
Change the name of file1.txt to file01.txt

rename -n jpg
Enumerate all the .jpg files from name.jpg to name_0.jpg onwards.

Distributed under GPL-3 license.
'''


__VERSION__ = "v1.0"
__RELEASE__ = "march 9, 2024"
__AUTHOR__  = "Marcelo Freri"
__CONTACT__ = "info@mfreri.com"
__VERBOSE__ = True


import os
import sys


class Colors:
	def __init__(self):
		# Text colors
		self.black = "\033[30m"
		self.red = "\033[31m"
		self.green = "\033[32m"
		self.yellow = "\033[33m"
		self.blue = "\033[34m"
		self.magenta = "\033[35m"
		self.cyan = "\033[36m"
		self.gray = "\033[37m"
		self.default = "\033[39m"


class Messages:
	# Constructor
	def __init__(self):
		pass

	# Messages
	def warning(self, message=""):
		color = Colors()
		print(color.yellow + "(!) " + message + color.default)

	def error(self, message=""):
		color = Colors()
		print(color.red + "(E) " + message + color.default)

	def info(self, message=""):
		color = Colors()
		print(color.blue + "(i) " + message + color.default)


def display_version():
	print(f"Rename {__VERSION__} - {__RELEASE__}.")
	print(f"Developed by {__AUTHOR__} <{__CONTACT__}>.")


def display_help(contact_info=True):
	print(__HELP__)
	if contact_info:
		print(f"Contact developer at <{__CONTACT__}>.")


def help_tip():
	print("Try '--help' for syntax information.")


def rename_file(src, dst):
	_msg_ = Messages()
	# Check if files src and dst exists
	if not os.path.exists(src):
		_msg_.error(f"File <{src}> doesn't exist!")
		return False
	if not os.path.isfile(src):
		_msg_.error(f"<{src}> is not a valid file!")
		return False
	if os.path.exists(dst):
		_msg_.error(f"File <{dst}> already exist!")
		return False
	# Try to rename
	if __VERBOSE__:
		print(f"'{src}' -> '{dst}'")
	try:
		os.rename(src, dst)
	except PermissionError:
		_msg_.error("File access denied! Check permission.")
		return False
	except OSError as error:
		_msg_.error(f"Unknown error! Something went wrong with error code <{error}>.")
		return False
	return True


def get_files_with_extension(extension="*"):
	names = []
	for file in os.listdir("."):
		name, ext = os.path.splitext(file)
		if extension == "*":
			names.append((name, ext))
		else:
			if ext == "." + extension:
				names.append((name, ext))
	return names


def change_extension(src, dst):
	'''
		Change the extension of the files *.src to *.dst.
		Return True if all files were renamed, False otherwise.
	'''
	out = True
	# Obtain the list of files with extension src
	file_list = get_files_with_extension(extension=src)
	for file_ext in file_list:
		src_file = file_ext[0] + file_ext[1]
		dst_file = file_ext[0] + "." + dst
		rename_out = rename_file(src_file, dst_file)
		out = out and rename_out
	return out


def enum_files(extension="*", separator = "_"):
	'''
		Enumerate the files with the given extension.
		If no extension is passed, all files will be enumerated.
		Return True if all files were renamed, False otherwise.
		<separator> is the string that will be used to separate
		the file name from the number.
		Example:
		file_a.txt -> file_a_0.txt
		file_b.txt -> file_b_1.txt
		file_c.txt -> file_c_2.txt
	'''
	num = 0
	i = 0
	out = True
	file_list = get_files_with_extension(extension=extension)
	while i < len(file_list):
		file = file_list[i]
		new_name = file[0] + separator + str(num) + file[1]
		if not os.path.exists(new_name):
			rename_out = rename_file(file[0] + file[1], new_name)
			out = out and rename_out
			i += 1
		num += 1
	return out


if __name__ == "__main__":
	msg = Messages()
	is_error = False

	# Check parameters
	if len(sys.argv) < 3:
		if "-v" in sys.argv or "--version" in sys.argv:
			display_version()
		elif "-h" in sys.argv or "--help" in sys.argv:
			display_help()
		else:
			msg.error("Invalid number of parameters!")
			help_tip()
			exit(1)
	else:
		if sys.argv[1] == "-e":
			# Change extension
			if len(sys.argv) == 4:
				if not change_extension(src=sys.argv[2], dst=sys.argv[3]):
					is_error = True
			else:
				msg.error("Invalid number of parameters!")
				help_tip()
				exit(1)
		elif sys.argv[1] == "-n":
			if len(sys.argv) == 3:
				if not enum_files(extension=sys.argv[2]):
					is_error = True
			else:
				msg.error("Invalid number of parameters!")
				help_tip()
				exit(1)
		elif len(sys.argv) == 3:
			# Rename file1 to file2
			# Separate parameters
			source_file = sys.argv[1]
			target_name = sys.argv[2]
			# Rename file
			if not rename_file(src=source_file, dst=target_name):
				is_error = True
		else:
			msg.error(f"Invalid option '{sys.argv[1]}'!")
			help_tip()
			exit(1)
	
	if is_error:
		msg.warning("Finished with errors.")
		exit(1)
	exit(0)
