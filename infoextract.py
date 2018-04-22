#!/bin/tcsh
from nltk import word_tokenize, pos_tag, ne_chunk, sent_tokenize
import nltk
from nltk.corpus import wordnet as wn
from nltk import WordNetLemmatizer
from math import log
import re
import sys
all_text = open(sys.argv[1], "r").read()
doc = list((open(sys.argv[1], "r")))
answers = open(sys.argv[1] + ".templates", "w")
possible_exp = ['DEV-MUC3-\d\d\d\d', 'TST1-MUC3-\d\d\d\d' , 'TST2-MUC4-\d\d\d\d']
id_list = []
texts_list = []
contexts = open('context.txt', "w")

lmtzr = WordNetLemmatizer()

def get_info(i,text,dictionary):
	factor = dict((el,[]) for el in dictionary.keys())
	factor['ID:'].append(id_list[i])
	sents = sent_tokenize(text)
	for s in sents:
		for f in dictionary.keys():
			for p in dictionary[f]:
				if f == 'INCIDENT:':
					P = []
					for syn in wn.synsets(p):
						for l in syn.lemmas():
							l = l.name().upper()
							if l not in P:
								P.append(l)
					for q in P:
						if q in s and q not in factor[f]:
							factor[f].append(p)
				else:
					# p1 = lmtzr.lemmatize(p.lower()).upper()
					if p in s and p not in factor[f]:
						# contexts.write(f + p +'\n' + s + '\n\n\n')
						factor[f].append(p)
	for f in factor.keys():
		if len(factor[f]) == 0:
			if f == 'INCIDENT:':
				factor[f].append('ATTACK')
			else:
				factor[f].append('-')
	# for se in sents:
	# 	if factor['WEAPON:'][0] in se:
	# 		for i in factor['PERP INDIV:']:
	# 			if i in se:
	# 				factor['PERP INDIV:'] = [i]
	if 'KIDNAPPING' in factor['INCIDENT:']:
		factor['WEAPON:'] = ['-']
		factor['TARGET:'] = ['-']
	for i in ["DYNAMITE",'BOMB','ROCKET']:
		if i in factor['WEAPON:']:
			factor['INCIDENT:'] = ['BOMBING']
	if  factor['INCIDENT:'][0] == 'KIDNAPPING':
		factor['TARGET:'] = ['-']
	for i in ["MACHINE-GUN",'MACHINEGUNS','MACHINEGUN']:
		if i == factor['WEAPON:'][0]:
			factor['INCIDENT:'] = ['ATTACK']
	return factor

def feature():
	feature = ['ID:','INCIDENT:','WEAPON:','PERP INDIV:', 'PERP ORG:','TARGET:', 'VICTIM:']
	dic = dict((el,[]) for el in feature)
	with open('all_answer.txt', 'r') as in_file :
		lines = in_file.read().split("\n")
		for line in lines:
			for i in feature:
				if i in line:
					line = line.split('     ')[-1].split('/')
					ele = line[-1].strip()
					if ele not in dic[i] and ele != '-':
						dic[i].append(ele)
	dic['INCIDENT:'].append('ROBBERY')
	return dic

def cut_text(id_list, doc):
	for i, id_ in enumerate(id_list):
		Str = ''
		for j, line in enumerate(doc):
			if id_ in line:
				trig = True
			if i == len(id_list) - 1:
				if trig:
					trig = False
					while(j != len(doc) - 1):
						Str = Str + doc[j]
						j += 1

			elif id_list[i+1] in line:
				trig = False
			if trig:
				Str = Str + line
		texts_list.append(Str)
def main():
	for i in range(len(doc)):
		line = doc[i]
		for exp in possible_exp:
			val = re.search(exp, line)
			if val:
				id_list.append(line[:14])
	# print(id_list)
	# print(len(id_list))
	cut_text(id_list, doc)
	# print(texts_list[-1])
	fea = feature()
	for i, text in enumerate(texts_list):
		get_info(i,text,fea)
		answers.write('ID:' + '             ' + get_info(i,text,fea)['ID:'][-1] + '\n')
		answers.write('INCIDENT:' + '       ' + get_info(i,text,fea)['INCIDENT:'][0] + '\n')
		# for i in range(1,len(get_info(i,text,fea)['INCIDENT:'])):
		# 	answers.write('         ' + '       ' + get_info(i,text,fea)['INCIDENT:'][i] + '\n')
		answers.write('WEAPON:' + '         ' + get_info(i,text,fea)['WEAPON:'][0] + '\n')
		answers.write('PERP INDIV:' + '     ' + get_info(i,text,fea)['PERP INDIV:'][0] + '\n')
		# for i in range(1,len(get_info(i,text,fea)['PERP INDIV:'])):
		# 	answers.write('         ' + '       ' + get_info(i,text,fea)['PERP INDIV:'][i] + '\n')
		answers.write('PERP ORG:' + '       ' + get_info(i,text,fea)['PERP ORG:'][0] + '\n')
		# for i in range(1,len(get_info(i,text,fea)['PERP ORG:'])):
		# 	answers.write('         ' + '       ' + get_info(i,text,fea)['PERP ORG:'][i] + '\n')
		answers.write('TARGET:' + '         ' + get_info(i,text,fea)['TARGET:'][0] + '\n')
		for i in range(1,len(get_info(i,text,fea)['TARGET:'])):
			answers.write('         ' + '       ' + get_info(i,text,fea)['TARGET:'][i] + '\n')
		answers.write('VICTIM:' + '         ' + get_info(i,text,fea)['VICTIM:'][0] + '\n')
		for i in range(1,len(get_info(i,text,fea)['VICTIM:'])):
			answers.write('         ' + '       ' + get_info(i,text,fea)['VICTIM:'][i] + '\n')
		answers.write('\n\n')
			# print("ID:             " + get_info(i,text)['ID:'][-1])
			# print("INCIDENT:       " + get_info(i,text)['INCIDENT:'][-1])
			# print("WEAPON:         " + get_info(i,text)['WEAPON:'][-1])
			# print("PERP INDIV:     " + get_info(i,text)['PERP INDIV:'][-1])
			# print("PERP ORG:       " + get_info(i,text)['PERP ORG:'][-1])
			# print("TARGET:         " + get_info(i,text)['TARGET:'][-1])
			# print("VICTIM:         " + get_info(i,text)['VICTIM:'][-1])

main()

answers.close()
contexts.close()
