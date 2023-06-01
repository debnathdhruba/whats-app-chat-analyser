import streamlit as st 
import preprocessor,helper
import matplotlib.pyplot as plt
st.sidebar.title("Whatsapp Chat Analyzer")

#  upload the file
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data= bytes_data.decode("utf-8")
    df =  preprocessor.preprocess(data)
    
    
    st.dataframe(df)
    
    #  fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort() 
    user_list.insert(0,"Overall" )
    
    
    selected_user = st.sidebar.selectbox("Show analysis wrt" , user_list)
    
    #  analysis buttom 
    num_messages = 0
    words = 0
    num_media_messages = 0 
    links= 0

    if st.sidebar.button("Show Aalysis"):
       num_messages ,words, num_media_messages,links = helper.fetch_stats(selected_user, df) 
     
     
        
   #  making coloumns 
    col1 , col2 , col3 ,col4 = st.columns(4)
    
    
    with col1:
        st.header("Total Messages")
        st.title(num_messages)
    with col2:
        st.header("Total words")
        st.title(words)
    with col3:
        st.header("Share Media")
        st.title(num_media_messages)
    with col4:
        st.header("Total Links Share")
        st.title(links)            
    
    

    
        
    #   monthly timeline analysis 
    timeline = helper.monthly_users(selected_user , df )
    fig ,ax = plt.subplots()
    ax.plot(timeline['time'] , timeline['message'])
    plt.xticks(rotation = 'vertical')
    st.title("Monsthly_Timeline")
    st.pyplot(fig)
    
    
    
    # # ################# most busy users daily ##################
    
    daily_timeline = helper.daily_timeline(selected_user , df )
    fig ,ax = plt.subplots()
    ax.plot(daily_timeline['only_date'] , daily_timeline['message'])
    plt.xticks(rotation = 'vertical')
    st.title("Daily_Timeline")
    st.pyplot(fig)
    
    
    
    
    
    ######################3#  Activity map ########################3
    st.title('Activity Map')
    col1,col2 = st.columns(2)

    with col1:
        st.header("Most busy day")
        busy_day = helper.week_activity_map(selected_user,df)
        fig,ax = plt.subplots()
        ax.bar(busy_day.index,busy_day.values,color='purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    with col2:
        st.header("Most busy month")
        busy_month = helper.month_activity_map(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(busy_month.index, busy_month.values,color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
    
    
    
    
    
    
    #  most busy users monthly
    
    if selected_user == 'Overall':
       
        x, p_df = helper.most_busy_usrs(df)
        fig , ax =  plt.subplots()
         
        col1 , col2 = st.columns(2) 
        
        with col1:
            st.title("Most Busy Users")
            ax.bar(x.index , x.values)
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig )
            
        with col2:
            st.title('Most Busy Usrs')
            st.dataframe(p_df, width=500 , height=350) 
            
            
    
     
         
     
     
     #  wordcloud 
    st.title("WordCloud") 
    df_wc =helper.create_wordcloud(selected_user , df)
    fig ,ax =plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)
    
    
        
