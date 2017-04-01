import string
import os
from os.path import abspath, dirname
import nltk
from nltk.tokenize import PunktSentenceTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.corpus import stopwords
example = "Will the Ministry of finance be pleased to state their monetary plans on medicine research ?"

def analyse_keywords(example):
    stop_words = set(stopwords.words("english"))
    example=example.split()
    print("Original sentence")
    print(example)
    example = [''.join(c for c in e if c not in string.punctuation) for e in example]  # removing puncts----------------
    example = [s for s in example if s]  # removing spaces-------------
    example = sorted(set(example))  # removing multiple occurences---
    filtered_sentence = []
    for w in example:
        if w not in stop_words:
            filtered_sentence.append(w)
    print("Sentence Refined!")



    filtered_sentence=[f for f in filtered_sentence if(f!='How'and f!='What'and f!="Who" and f!="Why" and f!="Where" and f!="whom" and f!="whose")]


    tagged=nltk.pos_tag(filtered_sentence)


    lm=WordNetLemmatizer()


    for i in range(len(tagged)):
        po='n'
        s=tagged[i][1]
        if s=='ADJ'or s=='JJ'or s=='JJR'or s=='JJS':
            po='a'
        if(s=='ADV'):
            po='r'
        if s== 'VBG'or s== 'VBN'or s=='VBZ'or s=='VBP' or s=='VB':
            po='v'
        filtered_sentence[i]=lm.lemmatize(tagged[i][0],po)

    print(filtered_sentence)                                    #FIltered Sentence-------------------------------

    files=["railways.txt","finance.txt","space.txt","dst.txt","external_affairs.txt","health.txt","tourism.txt","oil_gas.txt"]


    # print(os.system("ls -lrt"))
    BASE_DIR = abspath(dirname(__file__))
    print(BASE_DIR)

    found=[]
    exact_key=[]
    for i in range(len(files)):                                 #exact match of keywords-------------------
        f=open(os.path.join(BASE_DIR,files[i]))
        text=f.read().strip().split()
        text=sorted(set(text))
        text = {item.lower()for item in text}
        filtered_sentence={item.lower()for item in filtered_sentence}

        match=set(filtered_sentence)&set(text)
        if(len(match)>0):
            print("matching set")
            print(match)
            found.extend(match)
            exact_key.append(list((f.name,len(match))))
    f.close()
    print(exact_key)
    found=sorted(set(found))
    print("These are the keywords already found!!!!")
    print(found)


    left=set(filtered_sentence)-set(found)
    list_left=list(left)
    print("The words left ARE :")
    print(list_left)
    synonyms=[]
    for i in range(len(list_left)):
        for syn in wordnet.synsets(list_left[i]):
            for l in syn.lemmas():
                synonyms.append(l.name())

    synonyms=sorted(set(synonyms))
    synonyms = {item.lower() for item in synonyms}
    print("Synonyms of the keywords found in the question")
    print(synonyms)                                                             # synonyms of important words of the question-----------------------------

    syn_count=[]
    for i in range(len(files)):                                               # count for synonyms--------------------------
        fopen = open(os.path.join(BASE_DIR,files[i]))
        text = fopen.read().strip().split()
        text = sorted(set(text))
        text = {item.lower() for item in text}
        comm = set(text)&set(synonyms)
        if len(comm)>0:
            print("synonyms set" )
            print(comm)
            syn_count.append(list((fopen.name,len(comm))))                   # synoyms counted--------------------------
    fopen.close()
    print(syn_count)

    def getKey(item):
        return item[1]
    newl=[]
    print("Sorted List for synonym count is :")
    newl=sorted(syn_count,key=getKey,reverse=True)
    print(newl)                 # sorted list of synonyms count----------------



    new_match=[]
    print("Sorted List for exact match of keyword is:")
    new_match=sorted(exact_key,key=getKey,reverse=True)
    print(new_match)                                                        #sorted list of eaxctly matched items----------

    final_min = []
    if(len(new_match)==0 and len(newl)==0):
        print("No Recommendations!!")

    if(len(new_match)>0 and len(new_match)<=3):
        for i in range(len(new_match)):
            final_min.append(new_match[i][0][:-4])

    if(len(new_match)>3):
        l=len(new_match)
        for i in range(l-(l-3)):
            final_min.append(new_match[i][0][:-4])


    if (len(newl) > 0  and len(new_match)==0):
        if(len(newl)==1):
            final_min.append(newl[0][0][:-4])
        if(len(newl)>=2):
            final_min.append(newl[0][0][:-4])
            final_min.append(newl[1][0][:-4])

    if (len(newl) >0 and len(new_match)>0):
            if(len(new_match)==1):
                if((newl[0][0]!=new_match[0][0])&(newl[1][0]!=new_match[0][0])):
                    final_min.append(newl[0][0][:-4])
                    final_min.append(newl[1][0][:-4])
            if(len(new_match)==2):
                if ((newl[0][0] != new_match[0][0]) & (newl[0][0] != new_match[1][0])):
                    final_min.append(newl[0][0][:-4])
                if((newl[1][0]!=new_match[0][0])&(newl[1][0]!=new_match[1][0])):
                    final_min.append(newl[1][0][:-4])
            if(len(new_match)>2):
                if ((newl[0][0] != new_match[0][0]) & (newl[0][0] != new_match[1][0])& (newl[0][0] != new_match[2][0])):
                    final_min.append(newl[0][0][:-4])
                if ((newl[1][0] != new_match[0][0]) & (newl[1][0] != new_match[1][0])& (newl[0][0] != new_match[2][0])):
                    final_min.append(newl[1][0][:-4])



    print(final_min)

    suggestion = []
    for l in final_min:
        suggestion.append(l.split('/')[-1])
    return suggestion

# analyse_keywords(example)