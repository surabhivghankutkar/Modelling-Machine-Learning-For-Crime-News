import os
from django.shortcuts import render
#from premodel import newscat2pred

import pandas as pd
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import defaultdict
from nltk.corpus import wordnet as wn
from premodel.newscat2 import Naive, SVM, Tfidf_vect, Encoder

def premodel_home(requests):
    #cmd = 'python newscat2pred.py'
    #os.system(cmd)

    testing = pd.read_csv('analysis_data.csv')

    testing['Headline'].dropna(inplace=True)

    testing['Headline'] = [entry.lower() for entry in testing['Headline']]

    testing['Headline'] = [word_tokenize(entry) for entry in testing['Headline']]

    tag_map = defaultdict(lambda: wn.NOUN)
    tag_map['J'] = wn.ADJ
    tag_map['V'] = wn.VERB
    tag_map['R'] = wn.ADV

    for index, entry in enumerate(testing['Headline']):
        # Declaring Empty List to store the words that follow the rules for this step condition is to check for Stop words and consider only alphabets
            if word not in stopwords.words('english') and word.isalpha():
                word_Final = word_Lemmatized.lemmatize(word, tag_map[tag[0]])
                Final_words.append(word_Final)
        # The final processed set of words for each iteration will be stored in 'text_final'
        testing.loc[index, 'text_final'] = str(Final_words)

    # Encoder = LabelEncoder()
    # Train_Y = Encoder.fit_transform(testing['text_final'])

    # Tfidf_vector = TfidfVectorizer(max_features=5000)
    # Tfidf_vector.fit(testing['text_final'])

    Training_X_Tfidf = Tfidf_vect.transform(testing['text_final'])

    # Naive = naive_bayes.MultinomialNB()
    # Naive.fit(Train_X_Tfidf,Train_Y)

    print("\n\n*******************Prediction*******************\n\n")
    # predict the labels on validation dataset
    prediction_NB = Naive.predict(Training_X_Tfidf)
    print("********Naive Bayes********")
    print("\n", prediction_NB)
    answers = Encoder.inverse_transform(prediction_NB)
    print("\n", answers)
    # Use accuracy_score function to get the accuracy
    # print("Naive Bayes Accuracy Score -> ",accuracy_score(answers, testing['Label'])*100)

    # Classifier - Algorithm - SVM
    # fit the training dataset on the classifier
    # SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
    # SVM.fit(Train_X_Tfidf,Train_Y)

    # predict the labels on validation dataset
    prediction_SVM = SVM.predict(Training_X_Tfidf)
    print("********SVM********")
    print("\n", prediction_SVM)
    answers1 = Encoder.inverse_transform(prediction_SVM)
    # print("SVM Accuracy Score -> ",accuracy_score(answers1, testing['Label'])*100)
    print("\n", answers1)

    # Use accuracy_score function to get the accuracy
    # print("SVM Accuracy Score -> ",accuracy_score(answers,testing['Label'])*100)
    # print(testing['Label'] + " -> " + answers)

    '''
    print(predictions_SVM)
    answer=Encoder.inverse_transform(predictions_SVM)
    #print(Test_X)
    #print(answer)

    '''

    os.remove("analysis_data.csv")
    print("file removed!!!")
    return render(requests, 'testing.html')