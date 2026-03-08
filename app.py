import streamlit as st 
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

st.set_page_config(page_title="WhatsApp Chat Analyzer", page_icon="💬", layout="wide")

st.sidebar.title("💬 WhatsApp Chat Analyzer")
st.sidebar.markdown("---")

# File upload
uploaded_file = st.sidebar.file_uploader("Choose a chat file (.txt)")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    
    # Fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort() 
    user_list.insert(0, "Overall")
    
    selected_user = st.sidebar.selectbox("👤 Analyze for", user_list)
    
    st.sidebar.markdown("---")
    
    # Create tabs for different analyses
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["📊 Overview", "📈 Timeline", "🎨 Visuals", "💬 Text Analysis", "🔥 Activity Map", "👥 Comparisons"]
    )
    
    # ==================== TAB 1: OVERVIEW ====================
    with tab1:
        st.header(f"Overview - {selected_user}")
        
        if st.button("📉 Show Analysis", key="analyze_btn"):
            num_messages, words, num_media_messages, links = helper.fetch_stats(selected_user, df)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📨 Total Messages", num_messages)
            with col2:
                st.metric("📝 Total Words", words)
            with col3:
                st.metric("📸 Media Shared", num_media_messages)
            with col4:
                st.metric("🔗 Links Shared", links)
            
            st.markdown("---")
            
            # Message length statistics
            msg_length_stats = helper.avg_message_length(selected_user, df)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Avg Words/Message", f"{msg_length_stats['avg_words_per_message']:.2f}")
            with col2:
                st.metric("Avg Chars/Message", f"{msg_length_stats['avg_chars_per_message']:.2f}")
            with col3:
                st.metric("Max Message Length", int(msg_length_stats['max_message_length']))
            with col4:
                st.metric("Min Message Length", int(msg_length_stats['min_message_length']))
        
        # Most busy users section
        if selected_user == "Overall":
            st.subheader("👨‍💼 Most Active Users")
            busy_users, busy_users_pct = helper.most_busy_usrs(df)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**User Activity (Count)**")
                st.bar_chart(busy_users)
            
            with col2:
                st.markdown("**User Activity (Percentage)**")
                fig, ax = plt.subplots(figsize=(8, 5))
                ax.barh(busy_users_pct['Name'], busy_users_pct['percentage'], color='skyblue')
                ax.set_xlabel("Percentage (%)")
                plt.tight_layout()
                st.pyplot(fig)
    
    # ==================== TAB 2: TIMELINE ====================
    with tab2:
        st.header("📅 Timeline Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Monthly Timeline")
            timeline = helper.monthly_users(selected_user, df)
            fig, ax = plt.subplots(figsize=(12, 5))
            ax.plot(timeline['time'], timeline['message'], marker='o', linewidth=2, markersize=8, color='#1f77b4')
            ax.fill_between(range(len(timeline)), timeline['message'], alpha=0.3)
            ax.set_xlabel("Month")
            ax.set_ylabel("Number of Messages")
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)
        
        with col2:
            st.subheader("Daily Timeline")
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots(figsize=(12, 5))
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], marker='', linewidth=1.5, color='#ff7f0e')
            ax.fill_between(range(len(daily_timeline)), daily_timeline['message'], alpha=0.3, color='#ff7f0e')
            ax.set_xlabel("Date")
            ax.set_ylabel("Number of Messages")
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)
    
    # ==================== TAB 3: VISUALS ====================
    with tab3:
        st.header("🎨 Visual Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("☁️ Word Cloud")
            wc = helper.create_wordcloud(selected_user, df)
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.imshow(wc)
            ax.axis('off')
            st.pyplot(fig)
        
        with col2:
            st.subheader("🔤 Top 15 Words")
            top_words = helper.get_top_words(selected_user, df, top_n=15)
            
            if top_words:
                fig, ax = plt.subplots(figsize=(8, 8))
                words = list(top_words.keys())
                counts = list(top_words.values())
                ax.barh(words, counts, color='#2ca02c')
                ax.set_xlabel("Frequency")
                ax.invert_yaxis()
                plt.tight_layout()
                st.pyplot(fig)
            else:
                st.info("No words found for analysis")
        
        with col3:
            st.subheader("😊 Top Emojis")
            emoji_stats = helper.get_emoji_stats(selected_user, df)
            
            if emoji_stats:
                fig, ax = plt.subplots(figsize=(8, 6))
                emojis = list(emoji_stats.keys())
                counts = list(emoji_stats.values())
                # Create emoji labels
                emoji_labels = [f"{emoji} ({count})" for emoji, count in zip(emojis, counts)]
                ax.barh(emoji_labels, counts, color='#d62728')
                ax.set_xlabel("Frequency")
                ax.invert_yaxis()
                plt.tight_layout()
                st.pyplot(fig)
            else:
                st.info("No emojis found in messages")
    
    # ==================== TAB 4: TEXT ANALYSIS ====================
    with tab4:
        st.header("💬 Text & Sentiment Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Sentiment Distribution")
            sentiment_dist = helper.sentiment_analysis(selected_user, df)
            
            if len(sentiment_dist) > 0:
                fig, ax = plt.subplots(figsize=(8, 5))
                colors = ['#2ca02c', '#d62728', '#9467bd']
                ax.bar(sentiment_dist.index, sentiment_dist.values, color=colors[:len(sentiment_dist)])
                ax.set_ylabel("Number of Messages")
                ax.set_title("Message Sentiment Distribution")
                plt.tight_layout()
                st.pyplot(fig)
        
        with col2:
            st.subheader("Active Time Periods")
            active_periods = helper.active_periods(selected_user, df)
            
            if len(active_periods) > 0:
                fig, ax = plt.subplots(figsize=(8, 5))
                ax.bar(range(len(active_periods)), active_periods.values, color='#1f77b4')
                ax.set_xticks(range(len(active_periods)))
                ax.set_xticklabels(active_periods.index, rotation=45, ha='right')
                ax.set_ylabel("Number of Messages")
                ax.set_title("Messages by Time Period")
                plt.tight_layout()
                st.pyplot(fig)
    
    # ==================== TAB 5: ACTIVITY MAP ====================
    with tab5:
        st.header("🔥 Activity Heatmap & Patterns")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📅 Busiest Days")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.bar(busy_day.index, busy_day.values, color='#9467bd')
            ax.set_ylabel("Number of Messages")
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)
        
        with col2:
            st.subheader("📆 Busiest Months")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.bar(busy_month.index, busy_month.values, color='#ff7f0e')
            ax.set_ylabel("Number of Messages")
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)
        
        st.subheader("⏰ Hourly Activity Distribution")
        hourly = helper.hourly_activity(selected_user, df)
        fig, ax = plt.subplots(figsize=(14, 5))
        ax.plot(hourly.index, hourly.values, marker='o', linewidth=2, markersize=6, color='#e377c2')
        ax.fill_between(hourly.index, hourly.values, alpha=0.3, color='#e377c2')
        ax.set_xlabel("Hour of Day")
        ax.set_ylabel("Number of Messages")
        ax.set_xticks(range(0, 24))
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
        
        st.subheader("🎯 Day-Hour Heatmap")
        heatmap_data = helper.hourly_day_heatmap(selected_user, df)
        
        if heatmap_data.size > 0:
            fig, ax = plt.subplots(figsize=(14, 6))
            sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='YlOrRd', cbar_kws={'label': 'Messages'}, ax=ax)
            ax.set_xlabel("Hour of Day")
            ax.set_ylabel("Day of Week")
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("Not enough data for heatmap visualization")
    
    # ==================== TAB 6: COMPARISONS ====================
    with tab6:
        st.header("👥 User Comparisons")
        
        if selected_user == "Overall":
            st.subheader("📊 All Users Statistics Table")
            
            comparison_df = helper.user_comparison_table(df)
            
            st.dataframe(
                comparison_df.sort_values('Messages', ascending=False),
                use_container_width=True,
                height=400
            )
            
            # Download CSV option
            csv = comparison_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Comparison (CSV)",
                data=csv,
                file_name="user_comparison.csv",
                mime="text/csv"
            )
        else:
            st.info("Switch to 'Overall' view to see user comparisons")
        
        # Most active users at specific times
        st.subheader("🕐 Most Active Users by Hour")
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_hour = st.slider("Select Hour (0-23)", 0, 23, 12)
        
        with col2:
            st.write("")
        
        busy_at_hour = helper.most_active_users_by_time(df, hour=selected_hour)
        
        if len(busy_at_hour) > 0:
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.barh(busy_at_hour.index, busy_at_hour.values, color='#17becf')
            ax.set_xlabel("Number of Messages")
            ax.set_title(f"Most Active Users at {selected_hour:02d}:00")
            plt.tight_layout()
            st.pyplot(fig)
    
    # ==================== DATA PREVIEW ====================
    with st.expander("📋 View Raw Data"):
        st.subheader("Chat Data Preview")
        st.dataframe(df.head(100), use_container_width=True)
        
        if st.button("Download Full Data (CSV)"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download Full Data",
                data=csv,
                file_name="whatsapp_chat_data.csv",
                mime="text/csv"
            )

else:
    st.markdown("""
    # 💬 WhatsApp Chat Analyzer
    
    Upload your WhatsApp chat to analyze:
    - 📊 Message statistics & trends
    - 📈 Activity patterns over time
    - 🎨 Word clouds & emoji usage
    - 🔥 Heat maps of activity
    - 👥 User comparison metrics
    - 💬 Sentiment analysis
    
    ## How to Export Your Chat:
    1. Open WhatsApp and go to the chat you want to analyze
    2. Click **More Options** (⋮)
    3. Select **More** → **Export Chat**
    4. Choose **Without Media**
    5. Share the text file with this app
    """)
    
    
        
