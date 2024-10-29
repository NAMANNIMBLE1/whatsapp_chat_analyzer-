from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import  Counter
import emoji

extract = URLExtract()

def fetch_stats(selected_user , df ):

    if selected_user != "OverAll":
        df = df[df['user'] == selected_user]

    #number of messages
    num_msgs = df.shape[0]

    #number of words
    words = []
    for msg in df['user']:
        words.extend(msg.split(' '))

    #number of media
    num_med = df[df['msg'] == '<Media omitted>\n'].shape[0]

    #number of links
    links = []
    for msg in df['msg']:
        links.extend(extract.find_urls(msg))  # library used above to extract the links

    return num_msgs , len(words) , num_med , len(links)



def monthly_timeline(selected_user , df):

    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(["year" , 'month'])['msg'].count().reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user , df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(df['date'])['msg'].count().reset_index()

    return timeline


def activity_map(selected_user , df ):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]

    activity_month_df = df.groupby('month')['msg'].count().reset_index()
    month_list = activity_month_df['month'].tolist()
    monthly_msg_list = activity_month_df['msg'].tolist()

    active_day_df = df.groupby('day')['msg'].count().reset_index()
    day_list = active_day_df['day'].tolist()
    day_msg_list = active_day_df['msg'].tolist()

    return activity_month_df , month_list , monthly_msg_list , active_day_df , day_list , day_msg_list


def most_chatty(df):
    person = df['user'].value_counts().head()

    percent = round((df['user'].value_counts() / df.shape[0]) * 100 , 2)

    return person , percent


def create_wordcloud(selected_user , df ):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width = 500 , height = 500 , min_font_size=10 , background_color= 'white')
    df_wc = wc.generate(df['msg'].str.cat(sep =" "))
    return df_wc



def most_common_words(selected_user , df):

    f = open('stop_hinglish.txt' , 'r')
    stop_words = f.read()

    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'Group notification']
    temp = temp[temp['msg'] != '<Media omitted>']

    words = []

    for message in temp['msg']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_words_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_words_df


def most_common_emojis(selected_user, df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['msg']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])  # Collect emojis from each message

    emoji_df =  pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return  emoji_df



def activity_heatmap(selected_user , df):

    if selected_user != "OverAll":
        df = df[df['user'] == selected_user]

    daily_activity = df.groupby(df['date'].dt.date).size().reset_index(name='message_count')
    # Set 'date' column as index and fill missing dates with zero messages
    daily_activity = daily_activity.set_index('date').asfreq('D', fill_value=0)
    daily_activity['year'] = daily_activity.index.year
    daily_activity['month'] = daily_activity.index.month
    heatmap_data_ = daily_activity.pivot_table(values='message_count', index='month', columns='year', aggfunc='sum')

    return heatmap_data_

