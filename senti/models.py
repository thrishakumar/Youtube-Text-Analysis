import os
import pandas as pd
from django.db import models
from django.http import HttpResponse
from textblob import TextBlob
from youtube_comment_scraper_python import *
from youtube_transcript_api import YouTubeTranscriptApi
class Link(models.Model):
    objects = None
    link = models.URLField(max_length=200)
    def __str__(self) -> object:
        return self.link
df = pd.read_csv('data.csv')
def find_subjectivity_on_single_comment(text):
    return TextBlob(text).sentiment.subjectivity
def apply_subjectivity_on_all_comments(df):
    df['Subjectivity'] = df['Comment'].apply(find_subjectivity_on_single_comment)
    return df
df = apply_subjectivity_on_all_comments(df)
def find_polarity_of_single_comment(text):
    return TextBlob(text).sentiment.polarity
def find_polarity_of_every_comment(df):
    df['Polarity'] = df['Comment'].apply(find_polarity_of_single_comment)
    return df
df = find_polarity_of_every_comment(df)
def analysis_based_on_polarity(df):
    analysis = lambda polarity: 'Positive' if polarity > 0 else 'Neutral' if polarity == 0 else 'Negative'
    df['Analysis'] = df['Polarity'].apply(analysis)
    return df
df = analysis_based_on_polarity(df)
df.to_csv('lg.csv')
filename = 'lg.csv'
response = HttpResponse(open(filename, 'rb').read(), content_type='text/csv')
response['Content-Length'] = os.path.getsize(filename)
response['Content-Disposition'] = 'attachment; filename=%s' % 'lg.csv'
srt = YouTubeTranscriptApi.get_transcript("_uQrJ0TkZlc")
df2 = pd.DataFrame(srt)
df2 = df2[["text", "start", "duration"]]
df2.to_csv('lg2.csv')
filename = 'lg2.csv'
response = HttpResponse(open(filename, 'rb').read(), content_type='text/csv')
response['Content-Length'] = os.path.getsize(filename)
response['Content-Disposition'] = 'attachment; filename=%s' % 'lg2.csv'
