from urlextract import URLExtract 
from wordcloud import WordCloud
import emoji
from collections import Counter
import re
import pandas as pd
extract = URLExtract()

def fetch_stats(selected_user , df ):
    
    if selected_user != 'Overall':
        df  = df[df['user'] == selected_user] 
   
    #   No of total meassages 
    
    num_messages = df.shape[0]
    
    
        #  number of words
    words =[]
    for i in df['message']:
        words.extend(i.split())
        
    #no of media messages 
    num_media_messages= df[df['message'] == '<Media omitted>\n'].shape[0]
   
   
    # no of links shaere
    links = []
    for i in df['message']:
        links.extend(extract.find_urls(i))
            
    return num_messages , len(words) , num_media_messages ,len(links)
 
 
 
 
def most_busy_usrs(df): 
    x= df['user'].value_counts().head()
    p_df = round((df['user'].value_counts()/df.shape[0])*100).reset_index()
    p_df.rename( columns ={'user':'Name', 'count' : 'percentage'} , inplace= True)
    return x ,p_df
        
        
def create_wordcloud(selected_user ,df ):
    if selected_user != 'Overall':
        df  = df[df['user'] == selected_user] 
    wc = WordCloud(width=500 , height=500 ,min_font_size=10 , background_color='white')
#     an image is stored in  df_wc
    df_wc = wc.generate(df['message'].str.cat(sep= " "))         
    
    return df_wc

def monthly_users(selected_user , df ):
     if selected_user != 'Overall':
        df  = df[df['user'] == selected_user] 
        
   
     timeline = df.groupby(['year' , 'month']).count()['message'].reset_index()
     time = []
     for i in range (timeline.shape[0]):
          time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
     
     timeline['time'] = time
     return timeline


def daily_timeline(selected_user , df):
     if selected_user != 'Overall':
        df  = df[df['user'] == selected_user] 
        
     daily_timeline = df.groupby('only_date').count()['message'].reset_index()
     return daily_timeline
 
 
 
def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()




def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


# ==================== NEW ENHANCEMENT FEATURES ====================

def hourly_activity(selected_user, df):
    """Get messages by hour of the day"""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df['hour'].value_counts().sort_index()


def hourly_day_heatmap(selected_user, df):
    """Create a heatmap of activity by day and hour"""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    heatmap_data = df.pivot_table(index='day_name', columns='hour', values='message', aggfunc='count')
    # Reorder days
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_data = heatmap_data.reindex([d for d in day_order if d in heatmap_data.index])
    return heatmap_data


def get_emoji_stats(selected_user, df):
    """Extract and get most used emojis"""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    
    if not emojis:
        return None
    
    emoji_counter = Counter(emojis)
    return dict(emoji_counter.most_common(10))


def get_top_words(selected_user, df, top_n=15):
    """Get most frequently used words"""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # Common words to exclude
    stop_words = {
        'and', 'the', 'a', 'an', 'or', 'in', 'to', 'is', 'this', 'that', 
        'it', 'i', 'my', 'me', 'you', 'your', 'he', 'she', 'we', 'they',
        'from', 'for', 'with', 'as', 'on', 'at', 'be', 'by', 'of', 'am',
        'are', 'was', 'were', 'been', 'have', 'has', 'had', 'do', 'does',
        'did', 'media', 'omitted', 'omitted\n'
    }
    
    words = []
    for message in df['message']:
        # Remove URLs and special characters
        cleaned_msg = re.sub(r'http\S+|www\S+|<.*?>', '', message)
        msg_words = cleaned_msg.lower().split()
        words.extend([w.strip('.,!?;:') for w in msg_words if w.strip('.,!?;:') and w.lower() not in stop_words and len(w) > 2])
    
    word_counter = Counter(words)
    return dict(word_counter.most_common(top_n))


def avg_message_length(selected_user, df):
    """Get average message length statistics"""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    df_copy = df[df['message'] != '<Media omitted>\n'].copy()
    
    message_lengths = df_copy['message'].apply(lambda x: len(x.split()))
    
    return {
        'avg_words_per_message': message_lengths.mean(),
        'avg_chars_per_message': df_copy['message'].apply(len).mean(),
        'max_message_length': message_lengths.max(),
        'min_message_length': message_lengths.min()
    }


def active_periods(selected_user, df):
    """Identify most active periods in the day"""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    period_counts = df['period'].value_counts().sort_index()
    return period_counts


def user_comparison_table(df):
    """Create a comprehensive statistics table for all users"""
    users = df['user'].unique().tolist()
    if 'group_notification' in users:
        users.remove('group_notification')
    
    stats_list = []
    for user in users:
        num_messages, words, media, links = fetch_stats(user, df)
        msg_length_stats = avg_message_length(user, df)
        
        stats_list.append({
            'User': user,
            'Messages': num_messages,
            'Words': words,
            'Media': media,
            'Links': links,
            'Avg Words/Msg': round(msg_length_stats['avg_words_per_message'], 2)
        })
    
    return pd.DataFrame(stats_list)


def basic_sentiment(text):
    """Simple sentiment analysis based on keywords"""
    positive_words = {'good', 'great', 'excellent', 'amazing', 'love', 'happy', 'best', 'awesome', 'wonderful', 'nice', 'perfect', 'fantastic'}
    negative_words = {'bad', 'terrible', 'awful', 'hate', 'sad', 'worst', 'horrible', 'disgusting', 'ugly', 'poor', 'stupid', 'angry'}
    
    words = text.lower().split()
    
    positive_count = sum(1 for word in words if word.strip('.,!?;:') in positive_words)
    negative_count = sum(1 for word in words if word.strip('.,!?;:') in negative_words)
    
    if positive_count > negative_count:
        return 'Positive'
    elif negative_count > positive_count:
        return 'Negative'
    else:
        return 'Neutral'


def sentiment_analysis(selected_user, df):
    """Get sentiment distribution for messages"""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    sentiments = df['message'].apply(basic_sentiment).value_counts()
    return sentiments


def most_active_users_by_time(df, hour=None, day=None):
    """Get most active users by specific time"""
    temp_df = df.copy()
    
    if hour is not None:
        temp_df = temp_df[temp_df['hour'] == hour]
    if day is not None:
        temp_df = temp_df[temp_df['day_name'] == day]
    
    return temp_df['user'].value_counts()



