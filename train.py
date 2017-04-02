from __future__ import division
import pickle
from nltk.corpus import conll2000, conll2002

all_tags = []
emission_prob = {}
transition_prob = {}

fin = open('key.txt','w')

def train(data):

	emission = {}
	transition = {}
	tagcount = {}

	for tree in data:
		data_list = []
		for chunks in tree:

			if "'" in str(chunks).split()[0]:
				word = str(chunks).split()[0][3:-2]
				pos_tag = str(chunks).split()[1][2:-2]
				chunk_tag = "O"
				data_list.append((pos_tag,chunk_tag))
				print word, pos_tag, chunk_tag

			else:
				for i,parts in enumerate(str(chunks).split()):
					if i == 0:
						chunk_name = parts[1:]						
					else:
						word = parts.split('/')[0]
						pos_tag = parts.split('/')[1].replace(")","")
						#print word, pos_tag
						if i == 1:
							chunk_tag = "B-" + chunk_name
						else:
							chunk_tag = "I-" + chunk_name
						data_list.append((pos_tag,chunk_tag))
					
		
		data_list.insert(0,('START','ST'))
		data_list.append(('END','EN'))
		#print data_list	
		
		for i,tuples in enumerate(data_list):

			if tuples in emission.keys():
				emission[tuples] += 1
			else:
				emission[tuples] = 1

			if tuples[1] in tagcount.keys():
				tagcount[tuples[1]] += 1
			else:
				tagcount[tuples[1]] = 1
				all_tags.append(tuples[1])

			if i > 0:
				if (data_list[i-1][1],data_list[i][1]) in transition.keys():
					transition[(data_list[i-1][1],data_list[i][1])] += 1
				else:
					transition[(data_list[i-1][1],data_list[i][1])] = 1

	for key,value in emission.items():
		emission_prob[key] = value/tagcount[key[1]]

	for key,value in transition.items():
		transition_prob[key] = value/tagcount[key[1]]

	print transition_prob.keys()

	pickle.dump(all_tags,open('all.p','w'))
	pickle.dump(emission_prob,open('emit.p','w'))
	pickle.dump(transition_prob,open('tran.p','w'))

if __name__ == "__main__":
	
	train(conll2000.chunked_sents())