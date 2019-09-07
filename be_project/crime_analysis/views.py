from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import NewspaperURL
#from .models import Data1
from bs4 import BeautifulSoup
from datetime import date
import requests
import csv
from django.shortcuts import render_to_response
import random
import datetime
import time

def crime_home(request):
	form = NewspaperURL(request.POST or None)
	if form.is_valid():
		data = form['enter_url'].value()
		if data == "Hindustan Times":
			scrapeht(data)
		elif data == "Indian Express":
			scrapeie(data)
		else:
			scrapeit(data)
		#getfile(data)
		form.save()
		return redirect('crime_analysis:demo_piechart')
	context = {
		'form' : form
	}
	return render(request, 'home.html', context)

def demo_piechart(request):
    xdata = ["Apple", "Apricot", "Avocado", "Banana", "Boysenberries", "Blueberries", "Dates", "Grapefruit", "Kiwi", "Lemon"]
    ydata = [52, 48, 160, 94, 75, 71, 490, 82, 46, 17]

    extra_serie = {"tooltip": {"y_start": "", "y_end": " cal"}}
    chartdata = {'x': xdata, 'y1': ydata, 'extra1': extra_serie}
    charttype = "pieChart"

    data = {
        'charttype': charttype,
        'chartdata': chartdata,
    }
    return render_to_response('pie.html', data)

def result(request):
	return render(request, 'result.html')

'''def getfile(data):
	response = HttpResponse(content_type='csv')
	response['Content-Disposition'] = 'attachment; filename = "analysis_data.csv"'
	writer = csv.writer(response)
	writer.writerow(['Headline', 'Summary', 'Date'])
	x = str(data)
	print(x)
	if data == "H Times" or x is "www.hindustantimes.com":
		print(x,"Inside For Loop")
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
			#print("Heading: " + heading,"Summary: " + summary_text,sep='\n')

		for art in soup.find_all('div', class_="media-body"):
			head = art.find('div', class_="media-heading headingfour").a.text
			summ = art.p.text
			t1 = art.find('span', class_="time-dt").text
			dt1 = t1.split(" ")
			date2 = dt1[0] + " " + dt1[1] + " " + dt1[2]
			writer.writerow([head, summ, date2])
		return response
	elif x is "Indian Express" or x is "www.indianexpress.com":
		source = requests.get('https://indianexpress.com/section/cities/').text
		soup = BeautifulSoup(source, 'lxml')
		for city in soup.find_all('div', class_="m-article-landing m-block-link"):
			title = city.h3.a.text
			summary = city.h4.text
			date1 = date.today()
			writer.writerow([title, summary, date1])
		return response
	else:
		source = requests.get('https://www.indiatoday.in/crime').text
		soup = BeautifulSoup(source, 'lxml')
		for news in soup.find_all('div', class_='detail'):
			title = news.h2.a.text
			summary = news.p.text
			date3 = date.today()
			writer.writerow([title, summary, date3])
		return response'''

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
	# print("Heading: " + heading,"Summary: " + summary_text,sep='\n')

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