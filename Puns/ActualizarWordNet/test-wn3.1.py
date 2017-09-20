import os

nltkdata_dir = "/home/pascu/nltk_data/"

nltkdata_wn = nltkdata_dir + 'corpora/wordnet/'


if not os.path.exists(nltkdata_wn+'wn3.0'):
	os.mkdir(nltkdata_wn+'wn3.0')
os.system('mv '+nltkdata_wn+"* "+nltkdata_wn+"wn3.0/")


wn31 = "http://wordnetcode.princeton.edu/wn3.1.dict.tar.gz"
if not os.path.exists('wn3.1.dict.tar.gz'):
	os.system('wget '+wn31)
os.system("tar zxf wn3.1.dict.tar.gz -C "+nltkdata_wn)
os.system("mv "+nltkdata_wn+"dict/* "+nltkdata_wn)
os.rmdir(nltkdata_wn + 'dict')

# Creating lexnames file.

dbfiles = nltkdata_wn+'dbfiles'
with open(nltkdata_wn+'lexnames', 'w') as fout:
	for i,j in enumerate(sorted(os.listdir(dbfiles))):
		pos = j.partition('.')[0]
		if pos == "noun":
			syncat = 1
		elif pos == "verb":
			syncat = 2
		elif pos == "adj":
			syncat = 3
		elif pos == "adv":
			syncat = 4
		elif j == "cntlist":
			syncat = "cntlist"
		fout.write("\t".join([str(i).zfill(2),j,str(syncat)])+"\n")
		
from nltk.corpus import wordnet as wn

# Checking generated lexnames file.
for i, line in enumerate(open(nltkdata_wn + 'lexnames','r')):
	index, lexname, _ = line.split()
	##print line.split(), int(index), i
	assert int(index) == i
	
# Testing wordnet function.
print (wn.synsets('dog'))
for i in wn.all_synsets():
	print (i, i.pos(), i.definition())
	
