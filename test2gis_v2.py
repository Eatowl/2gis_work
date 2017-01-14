#!/usr/bin/python
# -*- coding: utf-8 -*-

from pandas import read_csv
import re

work_list = []

def list_formation_func(work_list, j):

	for i in data_file:
		work_list.append(data_file[i][j])

	return work_list

def check_list_func(work_list): 		#костыль х)

	if type(work_list[len(work_list)-2]) == float:
		work_list[len(work_list)-2] = str(work_list[len(work_list)-2])

	return work_list

def split_func(string):			#строка приводится к оптимальному виду для сравнения
	
	test_list = []

	word_list = re.sub('[;#,.\+-]',' ', string)
	if '"' in word_list:							
		word_list = word_list.replace('"', '')
	word_list = word_list.split(' ')

	for i in word_list:
		if i == '':
			word_list.remove(i)

	for i in word_list:
		test_list.append(unicode(i, 'utf-8').upper())

	return test_list

def record_func(result_list):

	output_file.write("\n")
	output_file.writelines("%s;" % i for i in result_list)	

	return True

def choice_func(work_list):
	
	count = 0
	best = 0
	result_list = []

	name_2gis = split_func(work_list[1])
	address_2gis = split_func(work_list[2])

	for i in range(4, len(work_list), 7):

		ext_name = ' '.join(split_func(work_list[i]))
		ext_address = ' '.join(split_func(work_list[i + 1]))

		for n in name_2gis:
			if ext_name.find(n) != -1:
				count += 1

		for a in address_2gis:
			if ext_address.find(a) != -1:
				count += 1

		if count > best:
			best = count
			result_list = []
			for j in range(i - 4, i + 2):
				result_list.append(work_list[j])

		count = 0
	record_func(result_list)

	return True

data_file = read_csv("testdata-small.csv",";")
output_file = open("outdata.csv", "wb")
output_file.write("id;name;address;ext_id;ext_name;ext_address;")

for j in range(len(data_file)):		#формируются списки гипотез сгруппированные по индексу 2gis
	if j == 0:
		work_list = list_formation_func(work_list, j)
	elif data_file['id'][j] == data_file['id'][j - 1]:
		work_list = list_formation_func(work_list, j)
	else:
		work_list = check_list_func(work_list)
		choice_func(work_list)
		work_list = []; 
		work_list = list_formation_func(work_list, j)

choice_func(work_list)
output_file.close()