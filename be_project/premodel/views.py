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
from .forms import ExportPDF
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.tables import Table
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
cm = 2.54

def premodel_home(requests):
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

    mapped = zip(heads, answers1, answers2, answers3)
    my_context = {
        'headlines': heads,
        'predictionNB': answers1,
        'predictionSVM': answers2,
        'predictionRF': answers3,
        'mapped': mapped,
    }

    form = ExportPDF(requests.POST or None)
    if form.is_valid():
        form.save()
        os.remove("analysis_data.csv")

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=report.pdf'
        buff = io.BytesIO()
        report_pdf = SimpleDocTemplate(buff, rightMargin=100, leftMargin=100, topMargin=100, bottomMargin=100, pagesize=letter)
        elements = []

        data = []
        data.append(['Headlines', 'Naive Bayes', 'SVM', 'Random Forest'])
        for head, ans1, ans2, ans3 in mapped:
            data.append([head, ans1, ans2, ans3])
        t = Table(data)

        elements.append(t)
        report_pdf.build(elements)
        response.write(buff.getvalue())
        buff.close()
        return response

        '''doc = SimpleDocTemplate("report.pdf", pagesize=letter)
        # container for the 'Flowable' objects
        elements = []

        i = 0
        data = []
        data.append(['Headlines', 'Naive Bayes', 'SVM', 'Random Forest'])
        for head, ans1, ans2, ans3 in mapped:
            data.append([head, ans1, ans2, ans3])
            i+=1

        t = Table(data)
        #t.setStyle(TableStyle([('BACKGROUND', (1, 1), (-2, -2), colors.green),
         #                      ('TEXTCOLOR', (0, 0), (1, -1), colors.red)]))
        elements.append(t)
        # write the document to disk
        doc.build(elements)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=report.pdf'

        elements = []

        doc = SimpleDocTemplate(response, rightMargin=0, leftMargin=6.5 * cm, topMargin=0.3 * cm, bottomMargin=0)

        data = [(1, 2, 5), (3, 4, 6)]
        table = Table(data, colWidths=270, rowHeights=79)
        elements.append(table)
        doc.build(elements)
        return response'''
    #return redirect('crime_analysis:analyze_crime')
    return render(requests, 'testing.html', my_context)

def export_to_pdf(requests):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(20, 50, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='report.pdf')