import pandas as pd

df = pd.read_csv('testdata.csv')
headline = df.Headline
for news in headline:
    print(news)