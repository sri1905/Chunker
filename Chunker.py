import sys
import nltk
import pickle
#from pos_tagger import *
from tok_func import *
from nltk.corpus import conll2000, conll2002


all_tags = pickle.load(open('all.p','r'))
emission_prob = pickle.load(open('emit.p','r'))
transition_prob = pickle.load(open('tran.p','r'))

def hmm(tokens,i,ender,best_score = {}):
	ans_list = []
	new_score = {}
	if i == 1:
		for k in all_tags :
			try:
				transition_part = transition_prob[('ST',k)] 
			except KeyError :
				transition_part = 0.000001

			try:
				emission_part = emission_prob[(tokens[i],k)] 
			except KeyError :
				emission_part = 0.000001
			
			new_score[(tokens[1],k)] = transition_part * emission_part

	elif i == ender - 1 :
		maximum = -1
		chosen_tag = ""
		for keys,values in best_score.items() :
			
			try :
				transition_part = transition_prob[(keys[1],"EN")]
			except KeyError :
				transition_part = 0.000001
			temp_score = transition_part * values
			if temp_score > maximum :
				maximum = temp_score
				chosen_tag = keys[1]
			
		
		ans_list.append(chosen_tag)
		return ans_list

	else :
		best = {}
		for k in all_tags :

			maximum = -1
			try:
				emission_part = emission_prob[(tokens[i],k)] 
			except KeyError :
				emission_part = 0.000001

			for keys,values in best_score.items() :
				try :
					transition_part = transition_prob[(keys[1],k)]
				except KeyError :
					transition_part = 0.000001
				temp_score = emission_part * transition_part * values

				if temp_score > maximum :
					maximum = temp_score
					chosen_tag = keys[1]
			best[k] = chosen_tag
			new_score[(tokens[i],k)] = maximum
			
	ans_list = hmm(tokens,i+1,ender,new_score)
	last_tag = ans_list[-1]
	if i != 1:
		ans_list.append(best[last_tag])	
	return ans_list


if __name__ == "__main__" :
	
	sentence = raw_input("Enter a sentence - ")


	if sentence[-1] not in  [".","?","!"] :
		sentence += "."
	
	sent_list = tokenize(sentence)
	pos_output = nltk.pos_tag(sentence.split())
	
	tokens = []
	output_purpose_tokens = []

	for i in pos_output :
		tokens.append(i[1])
		output_purpose_tokens.append(i[1])
	tokens.insert(0,'START')
	tokens.append('END')
	ender = len(tokens)

	ans_list = hmm(tokens,1,ender)
	ans_list.reverse()

	output_list = []
	for i,toks in enumerate(output_purpose_tokens):
		tup = (sent_list[i],toks,ans_list[i])
		output_list.append(tup)
	print(output_list)