# -*- coding: utf-8 -*-
"""Sentimen.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dxaemvUcFcer1ZoAKOzaPcAtILwifmZX
"""

import pandas as pd

df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Dataset_4 (1).csv')
df = df.dropna()

df.isnull().sum()/len(df)*100

df['Aplikasi'].unique()

df['Sentiment'].value_counts()

df['Sentiment_Polarity'].value_counts()

def remove_numeric(review):
    return re.sub("\d"," ", review)

df

# Commented out IPython magic to ensure Python compatibility.

#importing necessery libraries for future analysis of the dataset
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# %matplotlib inline
import seaborn as sns
np.random.seed(2020)
import nltk
nltk.download('punkt') # one time execution
nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
import re
from nltk.tokenize import word_tokenize

!pip install spacy
!pip install unidecode

import spacy
import unidecode

import spacy
import en_core_web_sm

nlp = en_core_web_sm.load()

# exclude words from spacy stopwords list
deselect_stop_words = ['no', 'not']
for w in deselect_stop_words:
    nlp.vocab[w].is_stop = False

df_new = df.copy()

df_new

def remove_whitespace(text):
    """remove extra whitespaces from text"""
    text = text.strip()
    return " ".join(text.split())

from gensim.test.utils import common_texts, get_tmpfile
from gensim.models import Word2Vec

def remove_numeric(review):
    return re.sub("\d"," ", review)

def text_preprocessing(text, 
                       extra_whitespace=True, 
                       lemmatization=True, lowercase=True, punctuations=True,
                       special_chars=True, 
                       stop_words=True, remove_num=True):
    """preprocess text with default option set to true for all steps"""
    if extra_whitespace == True: #remove extra whitespaces
      text = remove_whitespace(text)
    if lowercase == True: #convert all characters to lowercase
      text = text.lower()
    if remove_num == True: #convert all characters to lowercase
      text = remove_numeric(text)

    doc = nlp(text) #tokenise text

    clean_text = []
    
    for token in doc:
        flag = True
        edit = token.text
        # remove stop words
        if stop_words == True and token.is_stop and token.pos_ != 'NUM': 
            flag = False
        # remove punctuations
        if punctuations == True and token.pos_ == 'PUNCT' and flag == True: 
            flag = False
        # remove special characters
        if special_chars == True and token.pos_ == 'SYM' and flag == True: 
            flag = False
        # convert tokens to base form
        elif lemmatization == True and token.lemma_ != "-PRON-" and flag == True:
            edit = token.lemma_
        # append tokens edited and not removed to list 
        if edit != "" and flag == True:
            clean_text.append(edit)        
    return clean_text

hasil = []
for index, row in df_new.iterrows():
  pre = text_preprocessing(str(df_new.loc[index, 'Ulasan_Diterjemahkan']))
  hasil.append(pre)

df_new['Ulasan_Diterjemahkan'] = hasil
df_new

pre = []
for index, row in df_new.iterrows():
  df_new.loc[index, 'Ulasan_Diterjemahkan'] =  ' '.join(str(i) for i in list(df_new.loc[index, 'Ulasan_Diterjemahkan']))

df_new

df_new.to_csv('/content/drive/MyDrive/Colab Notebooks/hasil_clean2.csv', index=False)

df_new['tokenized'] = df_new.apply(lambda row: nltk.word_tokenize(str(row['Ulasan_Diterjemahkan'])), axis=1)
df_new.head()

# Python3 program to Find maximum
# length list in a nested list

def FindMaxLength(lst):
	maxList = max(lst, key = lambda i: len(i))
	maxLength = len(maxList)
	
	return maxList, maxLength
# Driver Code
lst = [['A'], ['A', 'B'], ['A', 'B', 'C']]
print(FindMaxLength(df_new['tokenized']))

list_bermasalah = df_new[df_new['Ulasan_Diterjemahkan']==''].index

df_new[df_new['Ulasan_Diterjemahkan']==' '].index

list_bermasalah.append(df_new[df_new['Ulasan_Diterjemahkan']==' '].index)

df.loc[list_bermasalah]

df_new.loc[list_bermasalah]

df_new = df_new.drop(index=list_bermasalah)

from gensim.test.utils import common_texts, get_tmpfile
from gensim.models import Word2Vec

# Word2Vec modeling. 
model = Word2Vec(df_new['Ulasan_Diterjemahkan'], size=275, window=5, min_count=1, workers=4)

# # Get specified vocabulary's vector. 
# model.wv["computer"]

# Store the vectors for train data in following file
df_word2vec = pd.DataFrame()
i = 0
for index, row in df_new.iterrows():
    model_vector = (np.mean([model[token] for token in row['Ulasan_Diterjemahkan']], axis=0)).tolist()
    # print(index)
    j = 0
    for vector_element in (model_vector):
      # print(vector_element, token)
      df_word2vec.loc[i, str(j)] = vector_element
      j += 1
    i += 1

df_word2vec

df_word2vec.to_csv('/content/drive/MyDrive/Colab Notebooks/hasil_word2vec.csv', index=False)

df_new = df_new.reset_index()
df_new



df_word2vec['Sentiment_Polarity']	= df_new['Sentiment_Polarity']
df_word2vec['Subjektivitas_Sentimen'] = df_new['Subjektivitas_Sentimen']
df_word2vec

df_word2vec.to_csv('/content/drive/MyDrive/Colab Notebooks/hasil_word2vec2.csv', index=False)
df_new.to_csv('/content/drive/MyDrive/Colab Notebooks/new2.csv', index=False)



df_word2vec.to_csv('/content/drive/MyDrive/Colab Notebooks/hasil_word2vec2.csv', index=False)
df_new.to_csv('/content/drive/MyDrive/Colab Notebooks/new2.csv', index=False)

df_word2vec = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/hasil_word2vec2.csv')
df_new = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/new2.csv')

from sklearn import preprocessing
le = preprocessing.LabelEncoder()
df_new['Sentiment'] = le.fit_transform(df_new['Sentiment'])
df_new

X_df = df_word2vec.copy()
Y_df = df_new['Sentiment']

from sklearn.model_selection import train_test_split

X_train,X_test,y_train,y_test = train_test_split(X_df,Y_df,test_size=0.2)

print(len(X_train))
print(len(y_train))

from sklearn import model_selection
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.preprocessing import label_binarize

rfc = RandomForestClassifier(bootstrap=True, ccp_alpha=0.0, class_weight=None,
                       criterion='gini', max_depth=30, max_features='auto',
                       max_leaf_nodes=None, max_samples=None,
                       min_impurity_decrease=0.0, min_impurity_split=None,
                       min_samples_leaf=1, min_samples_split=2,
                       min_weight_fraction_leaf=0.0, n_estimators=100,
                       n_jobs=None, oob_score=False, random_state=None,
                       verbose=0, warm_start=False)
rfc.fit(X_train,y_train)
rfc_predict = rfc.predict(X_test)
# rfc_cv_score = cross_val_score(rfc, X_df, Y_binar, cv=5, scoring='roc_auc')
print("=== Confusion Matrix ===")
print(confusion_matrix(y_test, rfc_predict))
print('\n')
print("=== Classification Report ===")
print(classification_report(y_test, rfc_predict))
print('\n')
# print("=== All AUC Scores ===")
# print(rfc_cv_score)
# print('\n')
# print("=== Mean AUC Score ===")
# print("Mean AUC Score - Random Forest: ", rfc_cv_score.mean())

from sklearn.metrics import f1_score, accuracy_score

print(f1_score(y_test, rfc_predict, average=None))
print(accuracy_score(y_test, rfc_predict))