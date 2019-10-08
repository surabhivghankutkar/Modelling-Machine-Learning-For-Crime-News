import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, naive_bayes, svm
from sklearn.metrics import accuracy_score
#from premodel import newscat
from premodel.newscat2 import Naive, SVM, Tfidf_vect, Encoder,RF

#testing = pd.read_csv('/home/surabhi/Downloads/analysis_data.csv')
#testing = pd.read_csv('/home/surabhi/Desktop/MAJOR/testdata.csv')
testing = pd.read_csv('/home/surabhi/Desktop/MAJOR/testdata_Crime.csv')


testing['Headline'].dropna(inplace=True)

testing['Headline'] = [entry.lower() for entry in testing['Headline']]

testing['Headline']= [word_tokenize(entry) for entry in testing['Headline']]

tag_map = defaultdict(lambda : wn.NOUN)
tag_map['J'] = wn.ADJ
tag_map['V'] = wn.VERB
tag_map['R'] = wn.ADV

for index,entry in enumerate(testing['Headline']):
    # Declaring Empty List to store the words that follow the rules for this step
    Final_words = []
    # Initializing WordNetLemmatizer()
    word_Lemmatized = WordNetLemmatizer()
    # pos_tag function below will provide the 'tag' i.e if the word is Noun(N) or Verb(V) or something else.
    for word, tag in pos_tag(entry):
        # Below condition is to check for Stop words and consider only alphabets
        if word not in stopwords.words('english') and word.isalpha():
            word_Final = word_Lemmatized.lemmatize(word,tag_map[tag[0]])
            Final_words.append(word_Final)
    # The final processed set of words for each iteration will be stored in 'text_final'
    testing.loc[index,'text_final'] = str(Final_words)

Training_X_Tfidf = Tfidf_vect.transform(testing['text_final'])


prediction_NB = Naive.predict(Training_X_Tfidf)
print(prediction_NB)
answers1=Encoder.inverse_transform(prediction_NB)
print(answers1)

prediction_SVM = SVM.predict(Training_X_Tfidf)
print(prediction_SVM)
answers2=Encoder.inverse_transform(prediction_SVM)
print(answers2)

predictions_RF = RF.predict(Training_X_Tfidf)
print(predictions_RF)
answers3=Encoder.inverse_transform(predictions_RF)
print(answers3)

'''
print(predictions_SVM)
answer=Encoder.inverse_transform(predictions_SVM)
#print(Test_X)
#print(answer)

'''