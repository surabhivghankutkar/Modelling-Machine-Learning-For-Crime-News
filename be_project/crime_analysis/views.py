from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import NewspaperURL
from bs4 import BeautifulSoup
from datetime import date
import requests
import csv

def crime_home(request):
	form = NewspaperURL(request.POST or None)
	if form.is_valid():
		data = "paper"
		if 'analyze_ht' in request.POST:
			scrapeht(data)
		elif 'analyze_ie' in request.POST:
			scrapeie(data)
		elif 'analyze_it' in request.POST:
			scrapeit(data)
		elif 'analyze_ndtv' in requests.POST:
			scrapendtv(data)
		else:
			scrapen18(data)
		form.save()
		return redirect('crime_analysis:result')
	context = {
		'form': form
	}
	return render(request, 'home.html', context)

'''def crime_home(request):
	form = NewspaperURL(request.POST or None)
	if form.is_valid():
		data = form['enter_url'].value()
		if data == "Hindustan Times":
			scrapeht()
		elif data == "Indian Express":
			scrapeie()
		else:
			scrapeit()
		form.save()
		return redirect('crime_analysis:result')
	context = {
		'form' : form
	}
	return render(request, 'home.html', context)'''

def result(request):
	return render(request, 'result.html')

def scrapeht(data):
	response = HttpResponse(content_type='csv')
	response['Content-Disposition'] = 'attachment; filename = "analysis_data.csv"'
	writer = csv.writer(response)
	writer.writerow(['Headline', 'Summary', 'Date'])

	URL = 'https://www.hindustantimes.com/cities'
	source = requests.get(URL).text
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
		writer.writerow([heading, summary_text, date1])

	for art in soup.find_all('div', class_="media-body"):
		head = art.find('div', class_="media-heading headingfour").a.text
		summ = art.p.text
		t1 = art.find('span', class_="time-dt").text
		dt1 = t1.split(" ")
		date2 = dt1[0] + " " + dt1[1] + " " + dt1[2]
		writer.writerow([head, summ, date2])
	return response

def scrapeie(data):
	response = HttpResponse(content_type='csv')
	response['Content-Disposition'] = 'attachment; filename = "analysis_data.csv"'
	writer = csv.writer(response)
	writer.writerow(['Headline', 'Summary', 'Date'])

	source = requests.get('https://indianexpress.com/section/cities/').text
	soup = BeautifulSoup(source, 'lxml')
	for city in soup.find_all('div', class_="m-article-landing m-block-link"):
		title = city.h3.a.text
		summary = city.h4.text
		date1 = date.today()
		writer.writerow([title, summary, date1])
	return response

def scrapeit(data):
	response = HttpResponse(content_type='csv')
	response['Content-Disposition'] = 'attachment; filename = "analysis_data.csv"'
	writer = csv.writer(response)
	writer.writerow(['Headline', 'Summary', 'Date'])

	source = requests.get('https://www.indiatoday.in/crime').text
	soup = BeautifulSoup(source, 'lxml')
	for news in soup.find_all('div', class_='detail'):
		title = news.h2.a.text
		summary = news.p.text
		date3 = date.today()
		writer.writerow([title, summary, date3])
	return response

def scrapendtv(data):
	Title = []
	Summary = []
	Dop = []

	response = HttpResponse(content_type='csv')
	response['Content-Disposition'] = 'attachment; filename = "analysis_data.csv"'
	writer = csv.writer(response)
	writer.writerow(['Headline', 'Summary', 'Date'])

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
		writer.writerow([t, s, d])
	return response

def scrapen18(data):
	response = HttpResponse(content_type='csv')
	response['Content-Disposition'] = 'attachment; filename = "analysis_data.csv"'
	writer = csv.writer(response)
	writer.writerow(['Headline', 'Summary', 'Date'])

	source = requests.get('https://www.news18.com/india/').text
	soup = BeautifulSoup(source, 'lxml')
	for news in soup.find_all('div', class_='blog-list-blog'):
		title = news.p.a.text
		tarray = title.split(" ")
		if 'LIVE:' not in tarray:
			sub = news.p.a['href']
			srcs = requests.get(sub).text
			soup1 = BeautifulSoup(srcs, 'lxml')
			summary = soup1.find('h2', class_='story-intro').text
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
			writer.writerow([title, summary, date1])
	return response