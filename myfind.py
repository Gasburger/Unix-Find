#!/usr/bin/env python3

import sys
import os
import re

USAGE = "Usage: myfind [--regex=pattern | --name=filename] directory [command]"

# You can change this function signature if desired
def find(directory, regex, name, command):
	"""A simplified find command."""
	# TODO implement the function.

	path_list = []
	non_zero_list = []

	if os.path.exists(directory) == False: 
		sys.exit(USAGE)
	else:
		pass

	if regex == None and name == None:
		for dir_path, sub_dirs, files in os.walk(directory, topdown = True):	
			path_list.append(dir_path)
			for x in files:
				path_list.append(os.path.join(dir_path, x))
	
	elif regex == None and name != None:
		for dir_path, sub_dirs, files in os.walk(directory, topdown = True):
			for x in files:
				if x == name:
					path_list.append(os.path.join(dir_path, x))
			for y in sub_dirs:
				if y == name:
					path_list.append(os.path.join(dir_path, y))

	elif regex != None and name == None:
		pattern = re.compile(regex)
		for dir_path, sub_dirs, files in os.walk(directory, topdown = True):
			for x in files:
				if pattern.search(x):
					path_list.append(os.path.join(dir_path, x))
			for y in sub_dirs:
				if pattern.search(y):
					path_list.append(os.path.join(dir_path, y))

	elif regex != None and name != None:
		sys.exit(USAGE)


	if command == None:
		for n in path_list:
			print(n)

	elif command != None:
		for i in path_list:
			pid = os.fork()

			if pid == 0:
				new_command = []
				command = command.split()

				for x in command:
					if x == "{}":
						new_command.append(i)
					else:
						val = x

						try:
							if x[0:2] == "{}":
								val = i + x[2:]

						except IndexError:
							pass

						new_command.append(val)

				try:
					os.execlp(new_command[0], *new_command)

				except Exception:
					for f in new_command:
						if f != "{}":
							new_command[0] = f
							break
					message = new_command[0]

					for __ in new_command[1:]:
						message += " " + __

					sys.exit("Error: Unable to start process '{}'".format(message))
			else:
				non_zero_list.append(os.wait())

		for e in non_zero_list:
			if e[1] != 0:
				sys.exit(1)




	# This is a placeholder which exits the program with
	# a non-zero exit code, and the argument printed to
	# stderr.
	#sys.exit(USAGE)

if __name__ == "__main__":
	# TODO parse arguments here
	exists = False
	regex = None
	command = None
	name = None
	list_index = []

	del sys.argv[0]
	for x in range(0, len(sys.argv)):
		if sys.argv[x][:3] == "--r":
			regex = sys.argv[x][8:]
			list_index.append(x)

		elif sys.argv[x][:3] == "--n":
			name = sys.argv[x][7:]
			list_index.append(x)

		else:
			pass

		if os.path.exists(sys.argv[x]):
			directory = sys.argv[x]
			exists = True
			list_index.append(x)
		else:
			if exists == True:
				pass
			else:
				exists = False

	if exists == False:
		sys.exit(USAGE)
	else:
		pass

	list_index = sorted(list_index)

	if len(sys.argv) > len(list_index):
		for x in range(0, len(sys.argv)-1):
			if x != list_index[x]:
				command = sys.argv[x]
			else:
				command = sys.argv[-1]

	else:
		command = None


	find(directory, regex, name, command)

