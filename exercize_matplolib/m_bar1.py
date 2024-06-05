import csv
import numpy as np
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')

data = pd.read_csv('data_bar.csv')

ids = data['Responder_id']
lang_responses = data['LanguagesWorkedWith']

language_counter = Counter()

for response in lang_responses:
    language_counter.update(response.split(';'))
languages = []
popularity = []
for item in language_counter.most_common(15):
    languages.append(item[0])
    popularity.append(item[1])

languages.reverse()
popularity.reverse()

max_p = max(popularity)
min_p = min(popularity)

print(max_p)

plt.barh(languages, popularity, shadow=True)
plt.title('Most Popular Languages')
plt.xlabel('Number of People Who Use')
plt.tight_layout()
plt.show()