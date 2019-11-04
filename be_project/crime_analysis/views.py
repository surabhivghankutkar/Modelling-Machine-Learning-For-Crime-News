from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import NewspaperURL
from bs4 import BeautifulSoup
from datetime import date
import pandas as pd
import requests
import csv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
cm = 2.54

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
import os
from django.shortcuts import render, redirect
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import defaultdict
from nltk.corpus import wordnet as wn
from premodel.newscat2 import Naive, SVM, Tfidf_vect, Encoder, RF
#from .forms import ExportPDF
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.tables import Table
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
cm = 2.54

def crime_home(request):
	return render(request, 'home.html')

def about(request):
	return render(request, 'about.html')

def analyze_crime(request):
	form = NewspaperURL(request.POST or None)
	if form.is_valid():
		if 'analyze_ht' in request.POST:
			form.save()
			return redirect('crime_analysis:ht')
		elif 'analyze_ie' in request.POST:
			form.save()
			return redirect('crime_analysis:ie')
		elif 'analyze_it' in request.POST:
			form.save()
			return redirect('crime_analysis:it')
		elif 'analyze_ndtv' in request.POST:
			form.save()
			return redirect('crime_analysis:ndtv')
		elif 'analyze_n18' in request.POST:
			form.save()
			return redirect('crime_analysis:n18')
		elif 'analyze_decc' in request.POST:
			form.save()
			return redirect('crime_analysis:decc')
		elif 'analyze_oneind' in request.POST:
			form.save()
			return redirect('crime_analysis:oneind')
		elif 'analyze_otlkind' in request.POST:
			form.save()
			return redirect('crime_analysis:otlkind')
		elif 'analyze_asian' in request.POST:
			form.save()
			return redirect('crime_analysis:asian')
		elif 'analyze_daily' in request.POST:
			form.save()
			return redirect('crime_analysis:daily')
		else:
			return redirect('premodel:prehome')
	context = {
		'form': form
	}
	return render(request, 'analyze.html', context)

def result(request):
	return render(request, 'result.html')

def paper1(request):
	form = NewspaperURL(request.POST or None)
	if form.is_valid():
		if 'go' in request.POST:
			form.save()
			testing = pd.read_csv('analysis_data.csv')
			heads = testing['Headline']
			testing['Headline'].dropna(inplace=True)
			testing['Headline'] = [entry.lower() for entry in testing['Headline']]
			testing['Headline'] = [word_tokenize(entry) for entry in testing['Headline']]
			tag_map = defaultdict(lambda: wn.NOUN)
			tag_map['J'] = wn.ADJ
			tag_map['V'] = wn.VERB
			tag_map['R'] = wn.ADV
			for index, entry in enumerate(testing['Headline']):
				# Declaring Empty List to store the words that follow the rules for this step
				Final_words = []
				# Initializing WordNetLemmatizer()
				word_Lemmatized = WordNetLemmatizer()
				# pos_tag function below will provide the 'tag' i.e if the word is Noun(N) or Verb(V) or something else.
				for word, tag in pos_tag(entry):
					# Below condition is to check for Stop words and consider only alphabets
					if word not in stopwords.words('english') and word.isalpha():
						word_Final = word_Lemmatized.lemmatize(word, tag_map[tag[0]])
						Final_words.append(word_Final)
				# The final processed set of words for each iteration will be stored in 'text_final'
				testing.loc[index, 'text_final'] = str(Final_words)

			Training_X_Tfidf = Tfidf_vect.transform(testing['text_final'])
			prediction_NB = Naive.predict(Training_X_Tfidf)
			print(prediction_NB)
			answers1 = Encoder.inverse_transform(prediction_NB)
			print(answers1)

			prediction_SVM = SVM.predict(Training_X_Tfidf)
			print(prediction_SVM)
			answers2 = Encoder.inverse_transform(prediction_SVM)
			print(answers2)

			predictions_RF = RF.predict(Training_X_Tfidf)
			print(predictions_RF)
			answers3 = Encoder.inverse_transform(predictions_RF)
			print(answers3)

			crimenb = 0
			noncrimenb = 0
			total = len(answers1)
			for news in range(0, total):
				if answers1[news] == 'CRIME':
					crimenb += 1
				else:
					noncrimenb += 1
			crime_percentnb = (crimenb / total) * 100
			noncrime_percentnb = (noncrimenb / total) * 100

			crimesvm = 0
			noncrimesvm = 0
			total = len(answers2)
			for news in range(0, total):
				if answers2[news] == 'CRIME':
					crimesvm += 1
				else:
					noncrimesvm += 1
			crime_percentsvm = (crimesvm / total) * 100
			noncrime_percentsvm = (noncrimesvm / total) * 100

			crimerf = 0
			noncrimerf = 0
			total = len(answers3)
			for news in range(0, total):
				if answers3[news] == 'CRIME':
					crimerf += 1
				else:
					noncrimerf += 1
			crime_percentrf = (crimerf / total) * 100
			noncrime_percentrf = (noncrimerf / total) * 100

			Headlines = 'Headlines'
			nb = 'Naive_Bayes'
			svm = 'SVM'
			rf = 'Random Forest'
			mapped = zip(heads, answers1, answers2, answers3)
			my_context = {
				'mapped': mapped,
				'crime_percentnb': crime_percentnb,
				'noncrime_percentnb': noncrime_percentnb,
				'crime_percentsvm': crime_percentsvm,
				'noncrime_percentsvm': noncrime_percentsvm,
				'crime_percentrf': crime_percentrf,
				'noncrime_percentrf': noncrime_percentrf,
				'Headlines': Headlines,
				'nb': nb,
				'svm': svm,
				'rf': rf,
			}
			return render(request, 'ht.html', my_context)
	return render(request, 'ht.html')

def paper2(request):
	form = NewspaperURL(request.POST or None)
	if form.is_valid():
		if 'go' in request.POST:
			form.save()
			testing = pd.read_csv('analysis_data.csv')
			heads = testing['Headline']
			testing['Headline'].dropna(inplace=True)
			testing['Headline'] = [entry.lower() for entry in testing['Headline']]
			testing['Headline'] = [word_tokenize(entry) for entry in testing['Headline']]
			tag_map = defaultdict(lambda: wn.NOUN)
			tag_map['J'] = wn.ADJ
			tag_map['V'] = wn.VERB
			tag_map['R'] = wn.ADV
			for index, entry in enumerate(testing['Headline']):
				# Declaring Empty List to store the words that follow the rules for this step
				Final_words = []
				# Initializing WordNetLemmatizer()
				word_Lemmatized = WordNetLemmatizer()
				# pos_tag function below will provide the 'tag' i.e if the word is Noun(N) or Verb(V) or something else.
				for word, tag in pos_tag(entry):
					# Below condition is to check for Stop words and consider only alphabets
					if word not in stopwords.words('english') and word.isalpha():
						word_Final = word_Lemmatized.lemmatize(word, tag_map[tag[0]])
						Final_words.append(word_Final)
				# The final processed set of words for each iteration will be stored in 'text_final'
				testing.loc[index, 'text_final'] = str(Final_words)

			Training_X_Tfidf = Tfidf_vect.transform(testing['text_final'])
			prediction_NB = Naive.predict(Training_X_Tfidf)
			print(prediction_NB)
			answers1 = Encoder.inverse_transform(prediction_NB)
			print(answers1)

			prediction_SVM = SVM.predict(Training_X_Tfidf)
			print(prediction_SVM)
			answers2 = Encoder.inverse_transform(prediction_SVM)
			print(answers2)

			predictions_RF = RF.predict(Training_X_Tfidf)
			print(predictions_RF)
			answers3 = Encoder.inverse_transform(predictions_RF)
			print(answers3)

			crimenb = 0
			noncrimenb = 0
			total = len(answers1)
			for news in range(0, total):
				if answers1[news] == 'CRIME':
					crimenb += 1
				else:
					noncrimenb += 1
			crime_percentnb = (crimenb / total) * 100
			noncrime_percentnb = (noncrimenb / total) * 100

			crimesvm = 0
			noncrimesvm = 0
			total = len(answers2)
			for news in range(0, total):
				if answers2[news] == 'CRIME':
					crimesvm += 1
				else:
					noncrimesvm += 1
			crime_percentsvm = (crimesvm / total) * 100
			noncrime_percentsvm = (noncrimesvm / total) * 100

			crimerf = 0
			noncrimerf = 0
			total = len(answers3)
			for news in range(0, total):
				if answers3[news] == 'CRIME':
					crimerf += 1
				else:
					noncrimerf += 1
			crime_percentrf = (crimerf / total) * 100
			noncrime_percentrf = (noncrimerf / total) * 100

			Headlines = 'Headlines'
			nb = 'Naive_Bayes'
			svm = 'SVM'
			rf = 'Random Forest'
			mapped = zip(heads, answers1, answers2, answers3)
			my_context = {
				'mapped': mapped,
				'crime_percentnb': crime_percentnb,
				'noncrime_percentnb': noncrime_percentnb,
				'crime_percentsvm': crime_percentsvm,
				'noncrime_percentsvm': noncrime_percentsvm,
				'crime_percentrf': crime_percentrf,
				'noncrime_percentrf': noncrime_percentrf,
				'Headlines': Headlines,
				'nb': nb,
				'svm': svm,
				'rf': rf,
			}
			return render(request, 'asian.html', my_context)
	return render(request, 'asian.html')

def paper3(request):
	form = NewspaperURL(request.POST or None)
	if form.is_valid():
		if 'go' in request.POST:
			form.save()
			testing = pd.read_csv('analysis_data.csv')
			heads = testing['Headline']
			testing['Headline'].dropna(inplace=True)
			testing['Headline'] = [entry.lower() for entry in testing['Headline']]
			testing['Headline'] = [word_tokenize(entry) for entry in testing['Headline']]
			tag_map = defaultdict(lambda: wn.NOUN)
			tag_map['J'] = wn.ADJ
			tag_map['V'] = wn.VERB
			tag_map['R'] = wn.ADV
			for index, entry in enumerate(testing['Headline']):
				# Declaring Empty List to store the words that follow the rules for this step
				Final_words = []
				# Initializing WordNetLemmatizer()
				word_Lemmatized = WordNetLemmatizer()
				# pos_tag function below will provide the 'tag' i.e if the word is Noun(N) or Verb(V) or something else.
				for word, tag in pos_tag(entry):
					# Below condition is to check for Stop words and consider only alphabets
					if word not in stopwords.words('english') and word.isalpha():
						word_Final = word_Lemmatized.lemmatize(word, tag_map[tag[0]])
						Final_words.append(word_Final)
				# The final processed set of words for each iteration will be stored in 'text_final'
				testing.loc[index, 'text_final'] = str(Final_words)

			Training_X_Tfidf = Tfidf_vect.transform(testing['text_final'])
			prediction_NB = Naive.predict(Training_X_Tfidf)
			print(prediction_NB)
			answers1 = Encoder.inverse_transform(prediction_NB)
			print(answers1)

			prediction_SVM = SVM.predict(Training_X_Tfidf)
			print(prediction_SVM)
			answers2 = Encoder.inverse_transform(prediction_SVM)
			print(answers2)

			predictions_RF = RF.predict(Training_X_Tfidf)
			print(predictions_RF)
			answers3 = Encoder.inverse_transform(predictions_RF)
			print(answers3)

			crimenb = 0
			noncrimenb = 0
			total = len(answers1)
			for news in range(0, total):
				if answers1[news] == 'CRIME':
					crimenb += 1
				else:
					noncrimenb += 1
			crime_percentnb = (crimenb / total) * 100
			noncrime_percentnb = (noncrimenb / total) * 100

			crimesvm = 0
			noncrimesvm = 0
			total = len(answers2)
			for news in range(0, total):
				if answers2[news] == 'CRIME':
					crimesvm += 1
				else:
					noncrimesvm += 1
			crime_percentsvm = (crimesvm / total) * 100
			noncrime_percentsvm = (noncrimesvm / total) * 100

			crimerf = 0
			noncrimerf = 0
			total = len(answers3)
			for news in range(0, total):
				if answers3[news] == 'CRIME':
					crimerf += 1
				else:
					noncrimerf += 1
			crime_percentrf = (crimerf / total) * 100
			noncrime_percentrf = (noncrimerf / total) * 100

			Headlines = 'Headlines'
			nb = 'Naive_Bayes'
			svm = 'SVM'
			rf = 'Random Forest'
			mapped = zip(heads, answers1, answers2, answers3)
			my_context = {
				'mapped': mapped,
				'crime_percentnb': crime_percentnb,
				'noncrime_percentnb': noncrime_percentnb,
				'crime_percentsvm': crime_percentsvm,
				'noncrime_percentsvm': noncrime_percentsvm,
				'crime_percentrf': crime_percentrf,
				'noncrime_percentrf': noncrime_percentrf,
				'Headlines': Headlines,
				'nb': nb,
				'svm': svm,
				'rf': rf,
			}
			return render(request, 'daily.html', my_context)
	return render(request, 'daily.html')

def paper4(request):
	form = NewspaperURL(request.POST or None)
	if form.is_valid():
		if 'go' in request.POST:
			form.save()
			testing = pd.read_csv('analysis_data.csv')
			heads = testing['Headline']
			testing['Headline'].dropna(inplace=True)
			testing['Headline'] = [entry.lower() for entry in testing['Headline']]
			testing['Headline'] = [word_tokenize(entry) for entry in testing['Headline']]
			tag_map = defaultdict(lambda: wn.NOUN)
			tag_map['J'] = wn.ADJ
			tag_map['V'] = wn.VERB
			tag_map['R'] = wn.ADV
			for index, entry in enumerate(testing['Headline']):
				# Declaring Empty List to store the words that follow the rules for this step
				Final_words = []
				# Initializing WordNetLemmatizer()
				word_Lemmatized = WordNetLemmatizer()
				# pos_tag function below will provide the 'tag' i.e if the word is Noun(N) or Verb(V) or something else.
				for word, tag in pos_tag(entry):
					# Below condition is to check for Stop words and consider only alphabets
					if word not in stopwords.words('english') and word.isalpha():
						word_Final = word_Lemmatized.lemmatize(word, tag_map[tag[0]])
						Final_words.append(word_Final)
				# The final processed set of words for each iteration will be stored in 'text_final'
				testing.loc[index, 'text_final'] = str(Final_words)

			Training_X_Tfidf = Tfidf_vect.transform(testing['text_final'])
			prediction_NB = Naive.predict(Training_X_Tfidf)
			print(prediction_NB)
			answers1 = Encoder.inverse_transform(prediction_NB)
			print(answers1)

			prediction_SVM = SVM.predict(Training_X_Tfidf)
			print(prediction_SVM)
			answers2 = Encoder.inverse_transform(prediction_SVM)
			print(answers2)

			predictions_RF = RF.predict(Training_X_Tfidf)
			print(predictions_RF)
			answers3 = Encoder.inverse_transform(predictions_RF)
			print(answers3)

			crimenb = 0
			noncrimenb = 0
			total = len(answers1)
			for news in range(0, total):
				if answers1[news] == 'CRIME':
					crimenb += 1
				else:
					noncrimenb += 1
			crime_percentnb = (crimenb / total) * 100
			noncrime_percentnb = (noncrimenb / total) * 100

			crimesvm = 0
			noncrimesvm = 0
			total = len(answers2)
			for news in range(0, total):
				if answers2[news] == 'CRIME':
					crimesvm += 1
				else:
					noncrimesvm += 1
			crime_percentsvm = (crimesvm / total) * 100
			noncrime_percentsvm = (noncrimesvm / total) * 100

			crimerf = 0
			noncrimerf = 0
			total = len(answers3)
			for news in range(0, total):
				if answers3[news] == 'CRIME':
					crimerf += 1
				else:
					noncrimerf += 1
			crime_percentrf = (crimerf / total) * 100
			noncrime_percentrf = (noncrimerf / total) * 100

			Headlines = 'Headlines'
			nb = 'Naive_Bayes'
			svm = 'SVM'
			rf = 'Random Forest'
			mapped = zip(heads, answers1, answers2, answers3)
			my_context = {
				'mapped': mapped,
				'crime_percentnb': crime_percentnb,
				'noncrime_percentnb': noncrime_percentnb,
				'crime_percentsvm': crime_percentsvm,
				'noncrime_percentsvm': noncrime_percentsvm,
				'crime_percentrf': crime_percentrf,
				'noncrime_percentrf': noncrime_percentrf,
				'Headlines': Headlines,
				'nb': nb,
				'svm': svm,
				'rf': rf,
			}
			return render(request, 'decc.html', my_context)
	return render(request, 'decc.html')

def paper5(request):
	form = NewspaperURL(request.POST or None)
	if form.is_valid():
		if 'go' in request.POST:
			form.save()
			testing = pd.read_csv('analysis_data.csv')
			heads = testing['Headline']
			testing['Headline'].dropna(inplace=True)
			testing['Headline'] = [entry.lower() for entry in testing['Headline']]
			testing['Headline'] = [word_tokenize(entry) for entry in testing['Headline']]
			tag_map = defaultdict(lambda: wn.NOUN)
			tag_map['J'] = wn.ADJ
			tag_map['V'] = wn.VERB
			tag_map['R'] = wn.ADV
			for index, entry in enumerate(testing['Headline']):
				# Declaring Empty List to store the words that follow the rules for this step
				Final_words = []
				# Initializing WordNetLemmatizer()
				word_Lemmatized = WordNetLemmatizer()
				# pos_tag function below will provide the 'tag' i.e if the word is Noun(N) or Verb(V) or something else.
				for word, tag in pos_tag(entry):
					# Below condition is to check for Stop words and consider only alphabets
					if word not in stopwords.words('english') and word.isalpha():
						word_Final = word_Lemmatized.lemmatize(word, tag_map[tag[0]])
						Final_words.append(word_Final)
				# The final processed set of words for each iteration will be stored in 'text_final'
				testing.loc[index, 'text_final'] = str(Final_words)

			Training_X_Tfidf = Tfidf_vect.transform(testing['text_final'])
			prediction_NB = Naive.predict(Training_X_Tfidf)
			print(prediction_NB)
			answers1 = Encoder.inverse_transform(prediction_NB)
			print(answers1)

			prediction_SVM = SVM.predict(Training_X_Tfidf)
			print(prediction_SVM)
			answers2 = Encoder.inverse_transform(prediction_SVM)
			print(answers2)

			predictions_RF = RF.predict(Training_X_Tfidf)
			print(predictions_RF)
			answers3 = Encoder.inverse_transform(predictions_RF)
			print(answers3)

			crimenb = 0
			noncrimenb = 0
			total = len(answers1)
			for news in range(0, total):
				if answers1[news] == 'CRIME':
					crimenb += 1
				else:
					noncrimenb += 1
			crime_percentnb = (crimenb / total) * 100
			noncrime_percentnb = (noncrimenb / total) * 100

			crimesvm = 0
			noncrimesvm = 0
			total = len(answers2)
			for news in range(0, total):
				if answers2[news] == 'CRIME':
					crimesvm += 1
				else:
					noncrimesvm += 1
			crime_percentsvm = (crimesvm / total) * 100
			noncrime_percentsvm = (noncrimesvm / total) * 100

			crimerf = 0
			noncrimerf = 0
			total = len(answers3)
			for news in range(0, total):
				if answers3[news] == 'CRIME':
					crimerf += 1
				else:
					noncrimerf += 1
			crime_percentrf = (crimerf / total) * 100
			noncrime_percentrf = (noncrimerf / total) * 100

			Headlines = 'Headlines'
			nb = 'Naive_Bayes'
			svm = 'SVM'
			rf = 'Random Forest'
			mapped = zip(heads, answers1, answers2, answers3)
			my_context = {
				'mapped': mapped,
				'crime_percentnb': crime_percentnb,
				'noncrime_percentnb': noncrime_percentnb,
				'crime_percentsvm': crime_percentsvm,
				'noncrime_percentsvm': noncrime_percentsvm,
				'crime_percentrf': crime_percentrf,
				'noncrime_percentrf': noncrime_percentrf,
				'Headlines': Headlines,
				'nb': nb,
				'svm': svm,
				'rf': rf,
			}
			return render(request, 'ie.html', my_context)
	return render(request, 'ie.html')

def paper6(request):
	form = NewspaperURL(request.POST or None)
	if form.is_valid():
		if 'go' in request.POST:
			form.save()
			testing = pd.read_csv('analysis_data.csv')
			heads = testing['Headline']
			testing['Headline'].dropna(inplace=True)
			testing['Headline'] = [entry.lower() for entry in testing['Headline']]
			testing['Headline'] = [word_tokenize(entry) for entry in testing['Headline']]
			tag_map = defaultdict(lambda: wn.NOUN)
			tag_map['J'] = wn.ADJ
			tag_map['V'] = wn.VERB
			tag_map['R'] = wn.ADV
			for index, entry in enumerate(testing['Headline']):
				# Declaring Empty List to store the words that follow the rules for this step
				Final_words = []
				# Initializing WordNetLemmatizer()
				word_Lemmatized = WordNetLemmatizer()
				# pos_tag function below will provide the 'tag' i.e if the word is Noun(N) or Verb(V) or something else.
				for word, tag in pos_tag(entry):
					# Below condition is to check for Stop words and consider only alphabets
					if word not in stopwords.words('english') and word.isalpha():
						word_Final = word_Lemmatized.lemmatize(word, tag_map[tag[0]])
						Final_words.append(word_Final)
				# The final processed set of words for each iteration will be stored in 'text_final'
				testing.loc[index, 'text_final'] = str(Final_words)

			Training_X_Tfidf = Tfidf_vect.transform(testing['text_final'])
			prediction_NB = Naive.predict(Training_X_Tfidf)
			print(prediction_NB)
			answers1 = Encoder.inverse_transform(prediction_NB)
			print(answers1)

			prediction_SVM = SVM.predict(Training_X_Tfidf)
			print(prediction_SVM)
			answers2 = Encoder.inverse_transform(prediction_SVM)
			print(answers2)

			predictions_RF = RF.predict(Training_X_Tfidf)
			print(predictions_RF)
			answers3 = Encoder.inverse_transform(predictions_RF)
			print(answers3)

			crimenb = 0
			noncrimenb = 0
			total = len(answers1)
			for news in range(0, total):
				if answers1[news] == 'CRIME':
					crimenb += 1
				else:
					noncrimenb += 1
			crime_percentnb = (crimenb / total) * 100
			noncrime_percentnb = (noncrimenb / total) * 100

			crimesvm = 0
			noncrimesvm = 0
			total = len(answers2)
			for news in range(0, total):
				if answers2[news] == 'CRIME':
					crimesvm += 1
				else:
					noncrimesvm += 1
			crime_percentsvm = (crimesvm / total) * 100
			noncrime_percentsvm = (noncrimesvm / total) * 100

			crimerf = 0
			noncrimerf = 0
			total = len(answers3)
			for news in range(0, total):
				if answers3[news] == 'CRIME':
					crimerf += 1
				else:
					noncrimerf += 1
			crime_percentrf = (crimerf / total) * 100
			noncrime_percentrf = (noncrimerf / total) * 100

			Headlines = 'Headlines'
			nb = 'Naive_Bayes'
			svm = 'SVM'
			rf = 'Random Forest'
			mapped = zip(heads, answers1, answers2, answers3)
			my_context = {
				'mapped': mapped,
				'crime_percentnb': crime_percentnb,
				'noncrime_percentnb': noncrime_percentnb,
				'crime_percentsvm': crime_percentsvm,
				'noncrime_percentsvm': noncrime_percentsvm,
				'crime_percentrf': crime_percentrf,
				'noncrime_percentrf': noncrime_percentrf,
				'Headlines': Headlines,
				'nb': nb,
				'svm': svm,
				'rf': rf,
			}
			return render(request, 'it.html', my_context)
	return render(request, 'it.html')

def paper7(request):
	form = NewspaperURL(request.POST or None)
	if form.is_valid():
		if 'go' in request.POST:
			form.save()
			testing = pd.read_csv('analysis_data.csv')
			heads = testing['Headline']
			testing['Headline'].dropna(inplace=True)
			testing['Headline'] = [entry.lower() for entry in testing['Headline']]
			testing['Headline'] = [word_tokenize(entry) for entry in testing['Headline']]
			tag_map = defaultdict(lambda: wn.NOUN)
			tag_map['J'] = wn.ADJ
			tag_map['V'] = wn.VERB
			tag_map['R'] = wn.ADV
			for index, entry in enumerate(testing['Headline']):
				# Declaring Empty List to store the words that follow the rules for this step
				Final_words = []
				# Initializing WordNetLemmatizer()
				word_Lemmatized = WordNetLemmatizer()
				# pos_tag function below will provide the 'tag' i.e if the word is Noun(N) or Verb(V) or something else.
				for word, tag in pos_tag(entry):
					# Below condition is to check for Stop words and consider only alphabets
					if word not in stopwords.words('english') and word.isalpha():
						word_Final = word_Lemmatized.lemmatize(word, tag_map[tag[0]])
						Final_words.append(word_Final)
				# The final processed set of words for each iteration will be stored in 'text_final'
				testing.loc[index, 'text_final'] = str(Final_words)

			Training_X_Tfidf = Tfidf_vect.transform(testing['text_final'])
			prediction_NB = Naive.predict(Training_X_Tfidf)
			print(prediction_NB)
			answers1 = Encoder.inverse_transform(prediction_NB)
			print(answers1)

			prediction_SVM = SVM.predict(Training_X_Tfidf)
			print(prediction_SVM)
			answers2 = Encoder.inverse_transform(prediction_SVM)
			print(answers2)

			predictions_RF = RF.predict(Training_X_Tfidf)
			print(predictions_RF)
			answers3 = Encoder.inverse_transform(predictions_RF)
			print(answers3)

			crimenb = 0
			noncrimenb = 0
			total = len(answers1)
			for news in range(0, total):
				if answers1[news] == 'CRIME':
					crimenb += 1
				else:
					noncrimenb += 1
			crime_percentnb = (crimenb / total) * 100
			noncrime_percentnb = (noncrimenb / total) * 100

			crimesvm = 0
			noncrimesvm = 0
			total = len(answers2)
			for news in range(0, total):
				if answers2[news] == 'CRIME':
					crimesvm += 1
				else:
					noncrimesvm += 1
			crime_percentsvm = (crimesvm / total) * 100
			noncrime_percentsvm = (noncrimesvm / total) * 100

			crimerf = 0
			noncrimerf = 0
			total = len(answers3)
			for news in range(0, total):
				if answers3[news] == 'CRIME':
					crimerf += 1
				else:
					noncrimerf += 1
			crime_percentrf = (crimerf / total) * 100
			noncrime_percentrf = (noncrimerf / total) * 100

			Headlines = 'Headlines'
			nb = 'Naive_Bayes'
			svm = 'SVM'
			rf = 'Random Forest'
			mapped = zip(heads, answers1, answers2, answers3)
			my_context = {
				'mapped': mapped,
				'crime_percentnb': crime_percentnb,
				'noncrime_percentnb': noncrime_percentnb,
				'crime_percentsvm': crime_percentsvm,
				'noncrime_percentsvm': noncrime_percentsvm,
				'crime_percentrf': crime_percentrf,
				'noncrime_percentrf': noncrime_percentrf,
				'Headlines': Headlines,
				'nb': nb,
				'svm': svm,
				'rf': rf,
			}
			return render(request, 'ndtv.html', my_context)
	return render(request, 'ndtv.html')

def paper8(request):
	form = NewspaperURL(request.POST or None)
	if form.is_valid():
		if 'go' in request.POST:
			form.save()
			testing = pd.read_csv('analysis_data.csv')
			heads = testing['Headline']
			testing['Headline'].dropna(inplace=True)
			testing['Headline'] = [entry.lower() for entry in testing['Headline']]
			testing['Headline'] = [word_tokenize(entry) for entry in testing['Headline']]
			tag_map = defaultdict(lambda: wn.NOUN)
			tag_map['J'] = wn.ADJ
			tag_map['V'] = wn.VERB
			tag_map['R'] = wn.ADV
			for index, entry in enumerate(testing['Headline']):
				# Declaring Empty List to store the words that follow the rules for this step
				Final_words = []
				# Initializing WordNetLemmatizer()
				word_Lemmatized = WordNetLemmatizer()
				# pos_tag function below will provide the 'tag' i.e if the word is Noun(N) or Verb(V) or something else.
				for word, tag in pos_tag(entry):
					# Below condition is to check for Stop words and consider only alphabets
					if word not in stopwords.words('english') and word.isalpha():
						word_Final = word_Lemmatized.lemmatize(word, tag_map[tag[0]])
						Final_words.append(word_Final)
				# The final processed set of words for each iteration will be stored in 'text_final'
				testing.loc[index, 'text_final'] = str(Final_words)

			Training_X_Tfidf = Tfidf_vect.transform(testing['text_final'])
			prediction_NB = Naive.predict(Training_X_Tfidf)
			print(prediction_NB)
			answers1 = Encoder.inverse_transform(prediction_NB)
			print(answers1)

			prediction_SVM = SVM.predict(Training_X_Tfidf)
			print(prediction_SVM)
			answers2 = Encoder.inverse_transform(prediction_SVM)
			print(answers2)

			predictions_RF = RF.predict(Training_X_Tfidf)
			print(predictions_RF)
			answers3 = Encoder.inverse_transform(predictions_RF)
			print(answers3)

			crimenb = 0
			noncrimenb = 0
			total = len(answers1)
			for news in range(0, total):
				if answers1[news] == 'CRIME':
					crimenb += 1
				else:
					noncrimenb += 1
			crime_percentnb = (crimenb / total) * 100
			noncrime_percentnb = (noncrimenb / total) * 100

			crimesvm = 0
			noncrimesvm = 0
			total = len(answers2)
			for news in range(0, total):
				if answers2[news] == 'CRIME':
					crimesvm += 1
				else:
					noncrimesvm += 1
			crime_percentsvm = (crimesvm / total) * 100
			noncrime_percentsvm = (noncrimesvm / total) * 100

			crimerf = 0
			noncrimerf = 0
			total = len(answers3)
			for news in range(0, total):
				if answers3[news] == 'CRIME':
					crimerf += 1
				else:
					noncrimerf += 1
			crime_percentrf = (crimerf / total) * 100
			noncrime_percentrf = (noncrimerf / total) * 100

			Headlines = 'Headlines'
			nb = 'Naive_Bayes'
			svm = 'SVM'
			rf = 'Random Forest'
			mapped = zip(heads, answers1, answers2, answers3)
			my_context = {
				'mapped': mapped,
				'crime_percentnb': crime_percentnb,
				'noncrime_percentnb': noncrime_percentnb,
				'crime_percentsvm': crime_percentsvm,
				'noncrime_percentsvm': noncrime_percentsvm,
				'crime_percentrf': crime_percentrf,
				'noncrime_percentrf': noncrime_percentrf,
				'Headlines': Headlines,
				'nb': nb,
				'svm': svm,
				'rf': rf,
			}
			return render(request, 'n18.html', my_context)
	return render(request, 'n18.html')

def paper9(request):
	form = NewspaperURL(request.POST or None)
	if form.is_valid():
		if 'go' in request.POST:
			form.save()
			testing = pd.read_csv('analysis_data.csv')
			heads = testing['Headline']
			testing['Headline'].dropna(inplace=True)
			testing['Headline'] = [entry.lower() for entry in testing['Headline']]
			testing['Headline'] = [word_tokenize(entry) for entry in testing['Headline']]
			tag_map = defaultdict(lambda: wn.NOUN)
			tag_map['J'] = wn.ADJ
			tag_map['V'] = wn.VERB
			tag_map['R'] = wn.ADV
			for index, entry in enumerate(testing['Headline']):
				# Declaring Empty List to store the words that follow the rules for this step
				Final_words = []
				# Initializing WordNetLemmatizer()
				word_Lemmatized = WordNetLemmatizer()
				# pos_tag function below will provide the 'tag' i.e if the word is Noun(N) or Verb(V) or something else.
				for word, tag in pos_tag(entry):
					# Below condition is to check for Stop words and consider only alphabets
					if word not in stopwords.words('english') and word.isalpha():
						word_Final = word_Lemmatized.lemmatize(word, tag_map[tag[0]])
						Final_words.append(word_Final)
				# The final processed set of words for each iteration will be stored in 'text_final'
				testing.loc[index, 'text_final'] = str(Final_words)

			Training_X_Tfidf = Tfidf_vect.transform(testing['text_final'])
			prediction_NB = Naive.predict(Training_X_Tfidf)
			print(prediction_NB)
			answers1 = Encoder.inverse_transform(prediction_NB)
			print(answers1)

			prediction_SVM = SVM.predict(Training_X_Tfidf)
			print(prediction_SVM)
			answers2 = Encoder.inverse_transform(prediction_SVM)
			print(answers2)

			predictions_RF = RF.predict(Training_X_Tfidf)
			print(predictions_RF)
			answers3 = Encoder.inverse_transform(predictions_RF)
			print(answers3)

			crimenb = 0
			noncrimenb = 0
			total = len(answers1)
			for news in range(0, total):
				if answers1[news] == 'CRIME':
					crimenb += 1
				else:
					noncrimenb += 1
			crime_percentnb = (crimenb / total) * 100
			noncrime_percentnb = (noncrimenb / total) * 100

			crimesvm = 0
			noncrimesvm = 0
			total = len(answers2)
			for news in range(0, total):
				if answers2[news] == 'CRIME':
					crimesvm += 1
				else:
					noncrimesvm += 1
			crime_percentsvm = (crimesvm / total) * 100
			noncrime_percentsvm = (noncrimesvm / total) * 100

			crimerf = 0
			noncrimerf = 0
			total = len(answers3)
			for news in range(0, total):
				if answers3[news] == 'CRIME':
					crimerf += 1
				else:
					noncrimerf += 1
			crime_percentrf = (crimerf / total) * 100
			noncrime_percentrf = (noncrimerf / total) * 100

			Headlines = 'Headlines'
			nb = 'Naive_Bayes'
			svm = 'SVM'
			rf = 'Random Forest'
			mapped = zip(heads, answers1, answers2, answers3)
			my_context = {
				'mapped': mapped,
				'crime_percentnb': crime_percentnb,
				'noncrime_percentnb': noncrime_percentnb,
				'crime_percentsvm': crime_percentsvm,
				'noncrime_percentsvm': noncrime_percentsvm,
				'crime_percentrf': crime_percentrf,
				'noncrime_percentrf': noncrime_percentrf,
				'Headlines': Headlines,
				'nb': nb,
				'svm': svm,
				'rf': rf,
			}
			return render(request, 'oneind.html', my_context)
	return render(request, 'oneind.html')

def paper10(request):
	form = NewspaperURL(request.POST or None)
	if form.is_valid():
		if 'go' in request.POST:
			form.save()
			testing = pd.read_csv('analysis_data.csv')
			heads = testing['Headline']
			testing['Headline'].dropna(inplace=True)
			testing['Headline'] = [entry.lower() for entry in testing['Headline']]
			testing['Headline'] = [word_tokenize(entry) for entry in testing['Headline']]
			tag_map = defaultdict(lambda: wn.NOUN)
			tag_map['J'] = wn.ADJ
			tag_map['V'] = wn.VERB
			tag_map['R'] = wn.ADV
			for index, entry in enumerate(testing['Headline']):
				# Declaring Empty List to store the words that follow the rules for this step
				Final_words = []
				# Initializing WordNetLemmatizer()
				word_Lemmatized = WordNetLemmatizer()
				# pos_tag function below will provide the 'tag' i.e if the word is Noun(N) or Verb(V) or something else.
				for word, tag in pos_tag(entry):
					# Below condition is to check for Stop words and consider only alphabets
					if word not in stopwords.words('english') and word.isalpha():
						word_Final = word_Lemmatized.lemmatize(word, tag_map[tag[0]])
						Final_words.append(word_Final)
				# The final processed set of words for each iteration will be stored in 'text_final'
				testing.loc[index, 'text_final'] = str(Final_words)

			Training_X_Tfidf = Tfidf_vect.transform(testing['text_final'])
			prediction_NB = Naive.predict(Training_X_Tfidf)
			print(prediction_NB)
			answers1 = Encoder.inverse_transform(prediction_NB)
			print(answers1)

			prediction_SVM = SVM.predict(Training_X_Tfidf)
			print(prediction_SVM)
			answers2 = Encoder.inverse_transform(prediction_SVM)
			print(answers2)

			predictions_RF = RF.predict(Training_X_Tfidf)
			print(predictions_RF)
			answers3 = Encoder.inverse_transform(predictions_RF)
			print(answers3)

			crimenb = 0
			noncrimenb = 0
			total = len(answers1)
			for news in range(0, total):
				if answers1[news] == 'CRIME':
					crimenb += 1
				else:
					noncrimenb += 1
			crime_percentnb = (crimenb / total) * 100
			noncrime_percentnb = (noncrimenb / total) * 100

			crimesvm = 0
			noncrimesvm = 0
			total = len(answers2)
			for news in range(0, total):
				if answers2[news] == 'CRIME':
					crimesvm += 1
				else:
					noncrimesvm += 1
			crime_percentsvm = (crimesvm / total) * 100
			noncrime_percentsvm = (noncrimesvm / total) * 100

			crimerf = 0
			noncrimerf = 0
			total = len(answers3)
			for news in range(0, total):
				if answers3[news] == 'CRIME':
					crimerf += 1
				else:
					noncrimerf += 1
			crime_percentrf = (crimerf / total) * 100
			noncrime_percentrf = (noncrimerf / total) * 100

			Headlines = 'Headlines'
			nb = 'Naive_Bayes'
			svm = 'SVM'
			rf = 'Random Forest'
			mapped = zip(heads, answers1, answers2, answers3)
			my_context = {
				'mapped': mapped,
				'crime_percentnb': crime_percentnb,
				'noncrime_percentnb': noncrime_percentnb,
				'crime_percentsvm': crime_percentsvm,
				'noncrime_percentsvm': noncrime_percentsvm,
				'crime_percentrf': crime_percentrf,
				'noncrime_percentrf': noncrime_percentrf,
				'Headlines': Headlines,
				'nb': nb,
				'svm': svm,
				'rf': rf,
			}
			return render(request, 'otlkind.html', my_context)
	return render(request, 'otlkind.html')

def scrapeht(data):
	csv_file = open('analysis_data.csv', 'w', encoding='utf-8')
	csv_writer = csv.writer(csv_file)
	csv_writer.writerow(['Headline', 'Summary', 'Date'])

	source = requests.get('https://www.hindustantimes.com/cities').text
	soup = BeautifulSoup(source, 'lxml')

	for article in soup.find_all('div', {'class': 'random-content clearfix'}):
		heading = article.h3.a.text
		sub = article.h3.a['href']
		srcs = requests.get(sub).text
		soup1 = BeautifulSoup(srcs, 'lxml')
		summary_text = ''
		summary = soup1.find("div", class_="storyArea").find_all('h2')
		for element in summary:
			summary_text += '\n' + ''.join(element.find_all(text=True))
		t = article.find('span', class_="time-dt").text
		dt = t.split(" ")
		date1 = dt[0] + " " + dt[1] + " " + dt[2]
		csv_writer.writerow([heading, summary_text, date1])

	for art in soup.find_all('div', class_="media-body"):
		head = art.find('div', class_="media-heading headingfour").a.text
		summ = art.p.text
		t1 = art.find('span', class_="time-dt").text
		dt1 = t1.split(" ")
		date2 = dt1[0] + " " + dt1[1] + " " + dt1[2]
		csv_writer.writerow([head, summ, date2])
	return redirect('crime_analysis:paper1')

def scrapeasian(data):
	csv_file = open('analysis_data.csv', 'w', encoding='utf-8')
	csv_writer = csv.writer(csv_file)
	csv_writer.writerow(['Headline', 'Summary', 'Date'])

	source = requests.get('https://www.asianage.com/india').text
	soup = BeautifulSoup(source, 'lxml')

	for news in soup.find_all('div', class_='top-stories-box col-lg-6 col-md-6 col-sm-6'):
		title = news.h3.a.text
		sub = "https://www.asianage.com" + news.h3.a['href']
		source1 = requests.get(sub).text
		soup1 = BeautifulSoup(source1, 'lxml')
		summary = soup1.find('div', class_='storyBody').find('p').text
		t = soup1.find('div', class_='col-sm-4 col-xs-12 date').text
		dt = t.split(" ")
		dop = dt[2] + " " + dt[3] + " " + dt[4]
		csv_writer.writerow([title, summary, dop])
	return redirect('crime_analysis:paper2')

def scrapedaily(data):
	csv_file = open('analysis_data.csv', 'w', encoding='utf-8')
	csv_writer = csv.writer(csv_file)
	csv_writer.writerow(['Headline', 'Summary', 'Date'])

	source = requests.get('https://www.dailyexcelsior.com/national-news/').text
	soup = BeautifulSoup(source, 'lxml')
	title1 = soup.find('div', class_='td_module_4 td_module_wrap td-animation-stack').find('h3').find('a').text
	summ = soup.find('div', class_='td-excerpt').text
	summ1 = summ.split("\n")
	summary1 = summ1[2]
	date1 = date.today()
	csv_writer.writerow([title1, summary1, date1])

	for news in soup.find_all('div', class_='item-details'):
		title2 = news.h3.a.text
		sub = news.h3.a['href']
		source1 = requests.get(sub).text
		soup1 = BeautifulSoup(source1, 'lxml')
		summ2 = soup1.find('div', class_='td-post-content').find('p').text
		summ3 = summ2.split("\n")
		slen = len(summ3)
		date2 = date.today()
		if slen <= 1:
			summary2 = summ3[0]
			csv_writer.writerow([title2, summary2, date2])
		else:
			summary2 = summ3[1]
			csv_writer.writerow([title2, summary2, date2])
	return redirect('crime_analysis:paper3')

def scrapedecc(data):
	csv_file = open('analysis_data.csv', 'w', encoding='utf-8')
	csv_writer = csv.writer(csv_file)
	csv_writer.writerow(['Headline', 'Summary', 'Date'])

	source = requests.get('https://www.deccanchronicle.com/nation').text
	soup = BeautifulSoup(source, 'lxml')
	for news in soup.find_all('div', class_='col-sm-12 col-xs-12 tstry-feed-sml-a'):
		sub = "https://www.deccanchronicle.com" + news.a['href']
		source1 = requests.get(sub).text
		soup1 = BeautifulSoup(source1, 'lxml')
		title = soup1.find('h1', class_='headline').find('span').text
		dop = soup1.find('div', class_='col-sm-6 col-xs-12 noPadding noMargin').text
		dt = dop.split(" ")
		date1 = dt[2] + " " + dt[3] + " " + dt[4]
		summ = soup1.find('div', class_='story-body').find('p').text
		csv_writer.writerow([title, summ, date1])
	return redirect('crime_analysis:paper4')

def scrapeie(data):
	csv_file = open('analysis_data.csv', 'w', encoding='utf-8')
	csv_writer = csv.writer(csv_file)
	csv_writer.writerow(['Headline', 'Summary', 'Date'])

	source = requests.get('https://indianexpress.com/section/cities/').text
	soup = BeautifulSoup(source, 'lxml')
	for city in soup.find_all('div', class_="m-article-landing m-block-link"):
		title = city.h3.a.text
		summary = city.h4.text
		date1 = date.today()
		csv_writer.writerow([title, summary, date1])
	return redirect('crime_analysis:paper5')

def scrapeit(data):
	csv_file = open('analysis_data.csv', 'w', encoding='utf-8')
	csv_writer = csv.writer(csv_file)
	csv_writer.writerow(['Headline', 'Summary', 'Date'])

	source = requests.get('https://www.indiatoday.in/crime').text
	soup = BeautifulSoup(source, 'lxml')
	for news in soup.find_all('div', class_='detail'):
		title = news.h2.a.text
		summary = news.p.text
		date3 = date.today()
		csv_writer.writerow([title, summary, date3])
	return redirect('crime_analysis:paper6')

def scrapendtv(data):
	Title = []
	Summary = []
	Dop = []

	csv_file = open('analysis_data.csv', 'w', encoding='utf-8')
	csv_writer = csv.writer(csv_file)
	csv_writer.writerow(['Headline', 'Summary', 'Date'])

	source = requests.get('https://www.ndtv.com/india?pfrom=home-mainnavgation').text
	soup = BeautifulSoup(source, 'lxml')
	for head in soup.find_all('div', class_='nstory_header'):
		title = head.a.text
		Title.append(title)

	for summ in soup.find_all('div', class_='nstory_intro'):
		summary = summ.text
		Summary.append(summary)

	for date1 in soup.find_all('div', class_='nstory_dateline'):
		temp = date1.text
		doplist = temp.split(" ")
		i = 0
		while doplist[i] != "|":
			i += 1
		dop = doplist[i + 2] + " " + doplist[i + 3] + " " + doplist[i + 4]
		Dop.append(dop)

	num = len(Title)
	for i in range(0, num):
		t = Title[i]
		s = Summary[i]
		d = Dop[i]
		csv_writer.writerow([t, s, d])
	return redirect('crime_analysis:paper7')

def scrapen18(data):
	csv_file = open('analysis_data.csv', 'w', encoding='utf-8')
	csv_writer = csv.writer(csv_file)
	csv_writer.writerow(['Headline', 'Summary', 'Date'])

	source = requests.get('https://www.news18.com/india/').text
	soup = BeautifulSoup(source, 'lxml')
	for news in soup.find_all('div', class_='blog-list-blog'):
		title = news.p.a.text
		tarray = title.split(" ")
		if 'LIVE:' not in tarray:
			sub = news.p.a['href']
			srcs = requests.get(sub).text
			soup1 = BeautifulSoup(srcs, 'lxml')
			summary = soup1.find('h2', class_='story-intro')
			if summary == None:
				continue
			summary = summary.text
			t = soup1.find('div', class_="author fleft").find('span').text
			dt = t.split(" ")
			dt1 = list(dt[0])
			i = 0
			length = len(dt1) + 1
			while dt1[i] != ':':
				i += 1
			i += 1
			month = dt1[i:length]
			Month = ''.join(month)
			date1 = Month + " " + dt[1] + " " + dt[2]
			csv_writer.writerow([title, summary, date1])
	return redirect('crime_analysis:paper8')

def scrapeoneind(data):
	csv_file = open('analysis_data.csv', 'w', encoding='utf-8')
	csv_writer = csv.writer(csv_file)
	csv_writer.writerow(['Headline', 'Summary', 'Date'])

	source = requests.get('https://www.oneindia.com/').text
	soup = BeautifulSoup(source, 'lxml')
	for news in soup.find_all('div', class_='news-desc'):
		sub = news.a['href']
		subarr = str(sub[0:5])
		if "https" != subarr:
			sub = "https://www.oneindia.com" + news.a['href']
			source1 = requests.get(sub).text
			soup1 = BeautifulSoup(source1, 'lxml')
			title = soup1.find('h1', class_='heading').text
			dt = soup1.find('div', class_='time-date date-time').find('span').text
			dt1 = dt.split(" ")
			date1 = dt1[3] + " " + dt1[4] + " " + dt1[5]
			summmary = soup1.find('div', class_='oi-article-lt').find('p').text
			csv_writer.writerow([title, summmary, date1])
	return redirect('crime_analysis:paper9')

def scrapeotlkind(data):
	csv_file = open('analysis_data.csv', 'w', encoding='utf-8')
	csv_writer = csv.writer(csv_file)
	csv_writer.writerow(['Headline', 'Summary', 'Date'])

	source = requests.get('https://www.outlookindia.com/website/section/national/19/').text
	soup = BeautifulSoup(source, 'lxml')

	for news in soup.find_all('div', class_='content_serach'):
		title = news.find('div', class_='cont_head').find('a').text
		summary = news.find('div', class_='descriptn').text
		date1 = date.today()
		csv_writer.writerow([title, summary, date1])
	return redirect('crime_analysis:paper10')