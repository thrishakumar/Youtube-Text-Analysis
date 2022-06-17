from django.shortcuts import render, redirect
from .forms import LinkForm
import matplotlib.pyplot as plt
from .models import Link
import pandas as pd
from sklearn.feature_extraction import text
from wordcloud import WordCloud


def search(request):
    form = LinkForm()
    if request.method == 'POST':
        form = LinkForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('chart-url')

    data = {
        'form': form
    }
    return render(request, template_name='search.html', context=data)


def chart(request):
    df = pd.read_csv("lg.csv")
    cross_tab = pd.crosstab(index=df['Time'],
                            columns=df['Analysis'])

    cross_tab.plot(kind='bar',
                   stacked=True,
                   colormap='Paired',
                   figsize=(10, 5))

    plt.legend(loc="upper right", ncol=2)
    plt.xlabel("Time")
    plt.ylabel("Proportion")
    plt.tight_layout()
    plt.savefig('media/barchart.jpg', dpi=100)
    plt.close()

    allWords = ' '.join([twts for twts in df['Comment']])
    wordCloud = WordCloud(stopwords=text.ENGLISH_STOP_WORDS, width=1000, height=600, random_state=21,
                          max_font_size=110).generate(allWords)
    plt.imshow(wordCloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig('media/wc1.jpg', dpi=100)
    sentiment = df['Analysis'].value_counts()
    data = {
        'senti': sentiment
    }
    return render(request, template_name='chart.html', context=data)


def subtitles(request):
    df2 = pd.read_csv("lg2.csv")
    c = list()
    article_text = ' '
    for i in df2['text']:
        c.append(i)

    for p in c:
        article_text = article_text + "." + p
    import re
    # Removing Square Brackets and Extra Spaces
    article_text = re.sub(r'[[0-9]*]', ' ', article_text)

    # Removing special characters and digits
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.tokenize import sent_tokenize
    tokens = word_tokenize(article_text)

    sentence_list = nltk.sent_tokenize(article_text)

    nltk.download("stopwords")
    stop_words = stopwords.words('english')
    sentence_list = nltk.sent_tokenize(article_text)
    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stop_words:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    maximum_frequncy = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / maximum_frequncy)
    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    import heapq
    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    allWords = ' '.join([twts for twts in df2['text']])
    wordCloud = WordCloud(stopwords=text.ENGLISH_STOP_WORDS, width=1000, height=600, random_state=21,
                          max_font_size=110).generate(allWords)
    plt.imshow(wordCloud, interpolation="bilinear")
    plt.tight_layout()
    plt.axis('off')
    plt.savefig('media/wc.jpg', dpi=100)
    data = {
        'subtitles': summary
    }
    return render(request, template_name='subtitle.html', context=data)
