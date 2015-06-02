import os
from collections import defaultdict
import cPickle as pickle
import sys
from optparse import OptionParser
import itertools
import ssdeep

def levenshtein(a,b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a,b = b,a
        n,m = m,n
        
    current = range(n+1)
    for i in range(1,m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1,n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)
            
    return current[n]


filename1 = sys.argv[1]

with open(filename1, 'rb') as fp:
    process_list = pickle.load(fp)

print process_list
#print process_list
#process_list.append('Searchindexer.')
#print process_list
#print "Computing hashes... \n"
baseSSdeep = []

for prosesses in process_list:
        baseSSdeep.append(ssdeep.hash(prosesses))
#print baseSSdeep
print "\n ----- Levenshtein distance in process names ----- \n"
#print "Computing score for each item... \n"

scores = []
levScores = []

for a, b in itertools.combinations(baseSSdeep, 2):
    scores.append(ssdeep.compare(a,b))
#print scores

for a, b in itertools.combinations(process_list, 2):
    score = (levenshtein(a,b))
    if score <= 2 and score != 0:
        print "Close match found"
        print str(a) + " - " + str(b) + "- Score: " + str(score) + "\n"
#print "Scores Levenshtein:"
#print levScores


