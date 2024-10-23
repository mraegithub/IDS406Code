import json
import requests
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
# json is just the file and list stored
from bs4 import BeautifulSoup
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
#Python package for parsing HTML documents. 

#testing

ostomy_one_url = 'https://www.amazon.com/Drainable-Supplies-Colostomy-Ileostomy-Approved/dp/B07RQT41YX/ref=cm_cr_arp_d_product_top?ie=UTF8'

skincare_one_url = 'https://www.amazon.com/CeraVe-Moisturizing-Cream-Daily-Moisturizer/dp/B00TTD9BRC/ref=sr_1_4?crid=2S8U53U0FJQR7&dib=eyJ2IjoiMSJ9.j7IYE0WXjFEUyEP4FpoxoOXFyqkaJhThqrg0mDmYTJ22fmvp0io745l1mO1zPR0Suh2a53XqjG-1m-xV2tOKAojZ4zMS6yQo-0kBaVBaEHR3ifHVK8-G3a5PJnBdDpqhSgexU8L4U6_o0Ce-Fu7GlLgnsk-x6Px_s9m3UOKtRFraqZn_XQMl2bdG-K7Q6HzzJsgrnAKDtYD7CDxxTi-5Z7kDXUzEi7Spa3tHwfGb7BOJFzNQSZ1iVCxpRPgkouOkm-FnkGTExiFQP5A-OUFtOIr-NoOpiiy4um-xKAkPIwo.sV9X7pmBx4xpFCzr0pLnO1cJt0qHPX06NWLLUS-Ycag&dib_tag=se&keywords=cerave&s=hpc&sprefix=cerave%2Chpc%2C134&sr=1-4'

custom_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0', 
'accept-language': 'en-US,en;q=0.5'}

response_ostomy_one = requests.get(ostomy_one_url, headers = custom_headers)

response_skincare_one = requests.get(skincare_one_url, headers = custom_headers)

skincare_one_soup = BeautifulSoup(response_skincare_one.content, "html.parser")

ostomy_one_soup = BeautifulSoup(response_ostomy_one.content, "html.parser")

reviews_element_ostomy = ostomy_one_soup.find_all('div', class_ = 'a-expander-content reviewText review-text-content a-expander-partial-collapse-content')

reviews_element_skincare = skincare_one_soup.find_all('div', class_ = 'a-expander-content reviewText review-text-content a-expander-partial-collapse-content')
title_element_skincare = skincare_one_soup.find('span', id = 'productTitle')
title_element_ostomy = ostomy_one_soup.find('span', id = 'productTitle')

title_skincare_text = title_element_skincare.text
title_ostomy_text = title_element_ostomy.text
print('\n')
print(title_skincare_text)
print('\n')
print(title_ostomy_text)
print('\n')

cloud_ostomy = ""
cloud_skincare = ""


reviews_skincare_one_text = []

reviews_ostomy_one_text = []
for span in reviews_element_ostomy:
    reviews_ostomy_one_text.append(span.text.strip())
   
for i in range (len(reviews_ostomy_one_text)):
    print('*'+reviews_ostomy_one_text[i]+'*');
    cloud_ostomy = cloud_ostomy + reviews_ostomy_one_text[i]
print('\n')
print('\n')
for span in reviews_element_skincare:
    reviews_skincare_one_text.append(span.text.strip())
   
for i in range (len(reviews_skincare_one_text)):
    print('***'+reviews_skincare_one_text[i]+'***');
    cloud_skincare = cloud_skincare + reviews_skincare_one_text[i]

df_ostomy = pd.DataFrame(reviews_ostomy_one_text, columns = ['Reviews'])

wordcloud = WordCloud(
    width=800, 
    height=400, 
    background_color="white", 
    stopwords=STOPWORDS, 
    min_font_size=10
).generate(cloud_ostomy)

plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()

wordcloud_two = WordCloud(
    width=800, 
    height=400, 
    background_color="white", 
    stopwords=STOPWORDS, 
    min_font_size=10
).generate(cloud_skincare)

plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud_two)
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()

analyzer = SIA()
df_ostomy['compound'] = [analyzer.polarity_scores(x)['compound'] for x in df_ostomy['Reviews']]
df_ostomy['negative'] = [analyzer.polarity_scores(x)['neg'] for x in df_ostomy['Reviews']]
df_ostomy['neutral'] = [analyzer.polarity_scores(x)['neu'] for x in df_ostomy['Reviews']]
df_ostomy['positive'] = [analyzer.polarity_scores(x)['pos'] for x in df_ostomy['Reviews']]
df_ostomy['sentiment']='neutral'
df_ostomy.loc[df_ostomy.compound>0.05,'sentiment']='positive'
df_ostomy.loc[df_ostomy.compound<-0.05,'sentiment']='negative'
df_ostomy.head()


print(df_ostomy['sentiment'].value_counts()['positive'])
print(df_ostomy['sentiment'].value_counts()['negative'])

#matthew's branch
print(df_ostomy)

