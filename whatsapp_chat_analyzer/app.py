import streamlit as st
import functions
import matplotlib.pyplot as plt
import  preprocessor
import seaborn as sns

# title main
st.markdown("<h1 style='text-align: center;'>Analyze the chats...</h1>", unsafe_allow_html=True)

# remove the hamburger sign
st.markdown("""
<style>
.st-emotion-cache-mnu3yk.ef3psqc6
            {
               visibility : hidden
            }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.eyeqlp53.st-emotion-cache-1pbsqtx.ex0cdmw0
            {
               visibility : hidden
            }
</style>
""", unsafe_allow_html=True)



# Upload file section
st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Upload your WhatsApp chat text file", type=["txt"])

if uploaded_file is not None:
    # Get the uploaded file data
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    # Call preprocess function to get the dataframe
    df = preprocessor.preprocess(data)

    # Display dataframe in Streamlit
    st.dataframe(df)

    # taking unique user
    user_detail = df['user'].unique().tolist()
    # removing group notification
    if 'Group notification' in user_detail:
        user_detail.remove('Group notification')

    # sorting list
    user_detail.sort()
    #insert overall options
    user_detail.insert(0 , 'OverAll')

    # drop down menu
    selected_user = st.sidebar.selectbox('show Analysis as ' , user_detail)

    if st.sidebar.button("Analyze"):

        num_msgs , words , num_med , links = functions.fetch_stats(selected_user , df)

        #overall statistics
        st.title("OverAll Basic Statistics")
        col1 , col2 , col3 , col4 = st.columns(4)
        with col1:
            st.header('Total Messages')
            st.subheader(num_msgs)
        with col2:
            st.header('Total words')
            st.subheader(words)

        with col3:
            st.header('Total media')
            st.subheader(num_med)
        with col4:
            st.header('Total links')
            st.subheader(links)


        # monthly timeline plot
        timeline = functions.monthly_timeline(selected_user , df)
        st.title("Monthly Timeline")

        fig , ax = plt.subplots()
        ax.plot(timeline['time'] , timeline['msg'] , color = 'maroon')
        plt.xticks(rotation = 90)
        st.pyplot(fig)

        #daily timeline plot
        timeline = functions.daily_timeline(selected_user , df )
        st.title("Daily Timeline")
        fig , ax = plt.subplots()
        ax.plot(timeline['date'] , timeline['msg'] , color = 'purple')
        plt.xticks(rotation = 90)
        st.pyplot(fig)


        # activity map
        st.title('Activity Map')
        col1 , col2 = st.columns(2)

        activity_month_df , month_list  , monthly_msg_list , active_day_df , day_list , day_msg_list = functions.activity_map(selected_user , df)

        with col1:
            st.header('Most Active Month')
            fig , ax = plt.subplots()
            ax.bar(activity_month_df['month'] , activity_month_df['msg'])
            ax.bar(month_list[monthly_msg_list.index(max(monthly_msg_list))] , max(monthly_msg_list) ,
                    color = 'green' , label = 'highest')
            ax.bar(month_list[monthly_msg_list.index(min(monthly_msg_list))], min(monthly_msg_list), color='red',
                    label = "lowest")
            plt.xticks(rotation = 90)
            st.pyplot(fig)

        with col2:
            st.header('Most Active Day')
            fig, ax = plt.subplots()
            ax.bar(active_day_df['day'], active_day_df['msg'])
            ax.bar(day_list[day_msg_list.index(max(day_msg_list))], max(day_msg_list), color='green',
                   label='highest')
            ax.bar(day_list[day_msg_list.index(min(day_msg_list))], min(day_msg_list), color='red',
                   label="lowest")
            plt.xticks(rotation=90)
            st.pyplot(fig)


        # most active person
        if selected_user == 'OverAll':
             st.title('Most Active User')

             person , percent = functions.most_chatty(df)
             fig , ax = plt.subplots()

             col1 , col2 = st.columns(2)
             with col1:
                 ax.bar(person.index , person , color = 'cyan')
                 st.pyplot(fig)

             with col2:
                 st.dataframe(percent)


        # world cloud
        df_wc = functions.create_wordcloud(selected_user , df)
        st.title('Most Common Words')

        fig , ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        # most common words
        col1 , col2 = st.columns(2)
        most_common_words_df = functions.most_common_words(selected_user , df)

        with col1:
            common_words = functions.most_common_words(selected_user , df)
            st.dataframe(common_words)

        with col2:
            st.title('Most Common Words')
            fig , ax = plt.subplots()
            plt.figure(figsize = (10 , 6))
            ax.barh(most_common_words_df[0] , most_common_words_df[1])
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)



        # Displaying most common emojis
        common_emoji = functions.most_common_emojis(selected_user, df)
        st.title('Most Common Emojis')
        col1 , col2 = st.columns(2)

        with col1:
            st.dataframe(common_emoji)

        with col2:
            plt.rcParams["font.family"] = "Segoe UI Emoji" # supports emoji
            fig , ax = plt.subplots()
            ax.pie(common_emoji[1].head(7),labels= common_emoji[0].head(7) ,autopct= '%1.1f%%')
            st.pyplot(fig)

        # displaying heatmap
        heatmap_data = functions.activity_heatmap(selected_user, df)
        st.title("Activity Heatmap")
        col1, col2 = st.columns(2)  # specify the number of columns here

        with col1:
            heatmap_data = functions.activity_heatmap(selected_user, df)
            st.dataframe(heatmap_data)

        with col2:
            fig, ax = plt.subplots(figsize=(10, 8))  # update figure creation here
            sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="YlGnBu", cbar=True)
            plt.title('Message Activity Heatmap')
            plt.xlabel('Year')
            plt.ylabel('Month')
            plt.yticks(ticks=range(1, 13),
                       labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
            st.pyplot(fig)


# Footer
footer = """<style>
.footer {
    position: relative; /* Changed from fixed to relative */
    width: 100%;
    background-color: rgba(0, 0, 0, 0.7); /* Semi-transparent black background */
    color: white; /* Text color */
    text-align: center;
    padding: 10px; /* Added padding for better appearance */
    bottom: 0; /* Ensure it appears at the bottom of the page */
}

a:link, a:visited {
    color: lightblue; /* Light blue color for links */
    background-color: transparent;
    text-decoration: underline;
}

a:hover, a:active {
    color: orange; /* Change hover color to orange */
    background-color: transparent;
    text-decoration: underline;
}
</style>
<div class="footer">
<p>Developed with ❤ by <a style='display: inline; text-align: center;' href="https://www.linkedin.com/in/naman-nimble-a7511b298/" target="_blank">Naman Nimble</a></p>
</div>
"""

st.markdown(footer, unsafe_allow_html=True)


