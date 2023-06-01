from urlextract import URLExtract 
from wordcloud import WordCloud
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







