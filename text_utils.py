from __future__ import division
from gensim import utils 
import numpy as np
import logging
from pprint import pprint   # pretty-printer
import re, string
from normalizer import en_stopwords, slang_list
from nltk.corpus import stopwords
from nltk.stem.porter import *
import elongated as e
import requests
import os
import preprocessor as p

ps = PorterStemmer()
p

stop = set(stopwords.words('english'))

def download_file(file_url,directory='DOWNLOADS'):
	"""
		TO DOWLOADN FILE FROM SPECIFIC URL
	"""
	if not os.path.exists(directory):
		os.makedirs(directory)

	outfile = lambda fname: os.path.join(directory, fname)
	r = requests.get(file_url, allow_redirects=True)
	open(outfile(file_url.split('/')[-1]), 'wb').write(r.content)
	return outfile(file_url.split('/')[-1])

def stemmer(docs):
	"""
		TO STEM TEXT USING PORTER STEMMER NLTK
	"""
	def _stem(text):
		intermediate = re.sub("[^a-zA-Z]", " ", text).lower()
		intermediate = [''.join(i.split('-')) if '-' in i else i for i in strip_links(intermediate).split()]
		intermediate = [i for i in intermediate if i not in stop]
		intermediate = [ps.stem(i) for i in intermediate]
		return intermediate

	if isinstance(docs, list):
		processed = []
		for document in docs:
			intermediate = _stem(document)
			processed.append(intermediate)
	else:
		processed = _stem(docs)

	return processed

def clean_tweets(tweets):
	"""
		TO CLEAN TWEETS FROM SLANG AND ELONGATED WORDS
	"""
	intermediate = slang_cleanser(cleaning_elongated(p.clean(tweets)))
	return intermediate

def cleaning_elongated(docs):

	def elongizer(text):
		intermediate = utils.tokenize(text, lower=True, errors='ignore')
		if e.has_long(text):
			intermediate = [e.remove_consecutive_dups(i) for i in intermediate if i not in stop]
		else:
			intermediate = [i for i in intermediate if i not in stop]

		return intermediate

	if isinstance(docs, list):
		processed = []
		for document in docs:
			intermediate = elongizer(document)
			processed.append(intermediate)
	else:
		processed = elongizer(docs)

	return ' '.join(processed)

def slang_cleanser(docs):
	'''Clean up slang words'''
	def slanger(text):
		intermediate = utils.tokenize(text, lower=True, errors='ignore')
		intermediate = [i for i in intermediate if i not in stop]
		processed = ' '.join(slang_list.get(y, y) for y in intermediate)
		return processed

	if isinstance(docs, list):
		processed = []
		for doc in docs:
			intermediate = slanger(doc)
			processed.append(intermediate)
	else:
		processed = slanger(docs)

	return processed

def strip_links(text):
    link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links         = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ', ')    
    return text

def strip_all_entities(text):
    # entity_prefixes = ['@','#']
    entity_prefixes = ['@']

    for separator in  string.punctuation:
        if separator not in entity_prefixes :
            text = text.replace(separator,' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)

# remove words that appear only once
def remove_unfrequent(str_list):
	from collections import defaultdict
	frequency = defaultdict(int)
	for text in str_list:
	    for token in text:
	        frequency[token] += 1
	texts = [[token for token in text if frequency[token] > 1]
	         for text in texts]
	return texts


def merge_multiple_lines(filepath,separator=',',column='text'):
	df = pd.read_csv(filepath, sep=separator)
	temp = []
	for index, row in df.iterrows():
	    temp.append(row[column].strip().lower().replace('rt',''))

	return " ".join(temp)

def get_files(dir_path):
	files = os.listdir(dir_path)
	return [dir_path+'/'+i for i in files]

def get_latest_dataset(dir_path,dataset='candidate'):
	import glob
	import os

	list_of_files = glob.glob('%s/%s*'%(dir_path,dataset)) # * means all if need specific format then *.csv
	latest_file = max(list_of_files, key=os.path.getctime)
	return latest_file

def stringify_values_list(lst):
    t=[]
    for j in lst:
        if j:
            t += j.encode("utf-8").split('-')
    return " ".join(list(set(t))).encode("utf-8")
    
def open_file_by_url(url_file,filetype='csv'):
	import csv  
	import urllib2
	response = urllib2.urlopen(url_file)
	if filetype == 'csv':
		data = csv.reader(response)
	else:
		data = response
	return data

def jsd_distance(list_a, list_b):
    """
    	Jensen-Shannon Distance is a standard way to 
    	measure similarity between 2 probability distribution, giving the value from 0 to 1, 0 means close, 1 means far away.
    """
    list_a = np.array(list_a)
    list_b = np.array(list_b)
    eps = 1e-32
    M = 0.5*(list_a+list_b+eps)
    result = np.sqrt(0.5*(np.sum(list_a*np.log(list_a/M+eps)) + np.sum(list_b*np.log(list_b/M+eps))))
    return 1 - result