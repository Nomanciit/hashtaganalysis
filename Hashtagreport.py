


import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import numpy as np
import cufflinks
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from htreport import HashtagReport

st.set_page_config(page_title="Hashtag Report", page_icon=":bar_chart:", layout="wide")

def main():

  def get_data():

    try:
      directory = os.getcwd()
      csv_files = os.listdir(directory)
      files_ = []
      for item_csv in csv_files:
        if item_csv.endswith(".csv"):
            files_.append(item_csv)
            print("reading file: ",str(files_[0]))
      df = pd.read_csv(str(files_[0]))
      # Add 'hour' column to dataframe
  
      df["created_at"] = pd.to_datetime(df.created_at)
      df['created_at'] = pd.DatetimeIndex(df.created_at)
      return df
      
                            
    except OSError as error:
      print(error)
      
  def remove_files():
    try:
      directory = os.getcwd()
      csv_files = os.listdir(directory)
      files_ = []
      for item_csv in csv_files:
        if item_csv.endswith(".csv"):
            os.remove(item_csv)
                            
    except OSError as error:
      print(error)

  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/


  ht_report=HashtagReport()


  df = get_data()
  print(df)
  ## ---- SIDEBAR ----

#  city = st.sidebar.multiselect(
#      "Select the City:",
#      options=df["name"].unique(),
#      default=df["name"].unique()
#  )
  #
  #customer_type = st.sidebar.multiselect(
  #    "Select the Customer Type:",
  #    options=df["Customer_type"].unique(),
  #    default=df["Customer_type"].unique(),
  #)
  #
  #gender = st.sidebar.multiselect(
  #    "Select the Gender:",
  #    options=df["Gender"].unique(),
  #    default=df["Gender"].unique()
  #)
  #
  #df_selection = df.query(
  #    "City == @city & Customer_type ==@customer_type & Gender == @gender"
  #)

  # ---- MAINPAGE ----
  st.title(":bar_chart: Hashtag Report")
  mystyle = '''
      <style>
          p {
              text-align: justify;
          }
      </style>
      '''
  st.markdown(mystyle, unsafe_allow_html=True)

  st.markdown("<h1 style='text-align: center; color: Blue;'>#PAKvWI</h1>", unsafe_allow_html=True)


  original_tweet_count_, retweet_count_, total_tweet_count_,unique_users =ht_report.original_tweet_count(df)
  df = ht_report.engaging_people(df)
  key_people = ht_report.key_people(df)
  start_name, start_date_=ht_report.originator_name_date(df)
  location, lang=ht_report.top_location_language(df)
  impressions=ht_report.potential_impressions(df)
  # TOP KPI's

  left_column, middle_column,middle_column2,right_column = st.columns(4)
  with left_column:
      st.markdown(f'<h1 style="text-align:center;color:#b4e67b;font-size:30px;">{"Total Tweets"}</h1>', unsafe_allow_html=True)
      st.markdown(f'<h2 style="text-align: center;font-size:24px;">{total_tweet_count_}</h2>', unsafe_allow_html=True)

  with middle_column:
      st.markdown(f'<h1 style="text-align:center;color:#b4e67b;font-size:30px;">{"Retweet Count"}</h1>', unsafe_allow_html=True)
      st.markdown(f'<h2 style="text-align: center;font-size:24px;">{retweet_count_}</h2>', unsafe_allow_html=True)
      
  with middle_column2:
      st.markdown(f'<h1 style="text-align:center;color:#b4e67b;font-size:30px;">{"Impressions"}</h1>', unsafe_allow_html=True)
      st.markdown(f'<h2 style="text-align: center;font-size:24px;">{impressions}</h2>', unsafe_allow_html=True)
  with right_column:
      st.markdown(f'<h1 style="text-align:center;color:#b4e67b;font-size:30px;">{"Original Tweets"}</h1>', unsafe_allow_html=True)
      st.markdown(f'<h2 style="text-align: center;font-size:24px;">{original_tweet_count_}</h2>', unsafe_allow_html=True)

  left_column_r3, middle_column_r3,middle_column2_r3,right_column_r3 = st.columns(4)
  with left_column_r3:
      st.header("")

  with middle_column_r3:
      st.header(" ")
  with middle_column2_r3:
      st.header(" ")
  with right_column_r3:
      st.header(" ")
  

  left_column_r2, middle_column_r1,middle_column2_r1,right_column_r1 = st.columns(4)
  with left_column_r2:
      st.markdown(f'<h1 style="text-align:center;color:#b4e67b;font-size:30px;">{"Startedby"}</h1>', unsafe_allow_html=True)
      st.markdown(f'<h2 style="text-align: center;font-size:18px;">{start_name}</h2>', unsafe_allow_html=True)
  with middle_column_r1:
      st.markdown(f'<h1 style="text-align:center;color:#b4e67b;font-size:30px;">{"Started On"}</h1>', unsafe_allow_html=True)
      st.markdown(f'<h2 style="text-align: center;font-size:18px;">{start_date_}</h2>', unsafe_allow_html=True)
  with middle_column2_r1:
      st.markdown(f'<h1 style="text-align:center;color:#b4e67b;font-size:30px;">{"Location"}</h1>', unsafe_allow_html=True)
      st.markdown(f'<h2 style="text-align: center;font-size:24px;">{location}</h2>', unsafe_allow_html=True)
  with right_column_r1:
      st.markdown(f'<h1 style="text-align:center;color:#b4e67b;font-size:30px;">{"Language"}</h1>', unsafe_allow_html=True)
      st.markdown(f'<h2 style="text-align: center;font-size:24px;">{lang}</h2>', unsafe_allow_html=True)

  st.markdown("""---""")

  def original_tweet(is_retweet):
    if is_retweet==1:
      return 0
    else:
      return 1

  def retweet_tweet(is_retweet):
    if is_retweet==1:
      return 1
    else:
      return 0

  df['retweeted'] = df['is_retweet'].apply(retweet_tweet)
  df['original_tweet'] = df['is_retweet'].apply(original_tweet)
  filter_data = df[['created_at','original_tweet','retweeted']]
  daily_cases = filter_data.groupby(pd.Grouper(key="created_at", freq="T")).sum().reset_index()
  #line_column = st.columns(1)

  fig = daily_cases.iplot(kind="line",asFigure=True,
                              x="created_at", y=["original_tweet","retweeted"],title="<b>Mention Graph </b>")


  st.plotly_chart(fig,use_container_width=True)


  hashtags_data = df[["hashtags"]]
  hashtags_data = hashtags_data.groupby(['hashtags']).size().to_frame().sort_values([0], ascending = False).head(5).reset_index()
  hashtags_data.columns = ['hashtags', 'count']

  # SALES BY PRODUCT LINE [BAR CHART]
  sales_by_product_line = (
      hashtags_data.groupby(by=["hashtags"]).sum()[["count"]].sort_values(by="count")
  )
  fig_product_sales = px.bar(
      sales_by_product_line,
      x="count",
      y=sales_by_product_line.index,
      orientation="h",
      
      title="<b>Top Associated Hashtags</b>",
      color_discrete_sequence=["#05b7ff"] * len(sales_by_product_line),
      template="plotly_white",
  )
  fig_product_sales.update_layout(
      plot_bgcolor="rgba(0,0,0,0)",
      xaxis=(dict(showgrid=False))
  )

  df_screen = df[["screen_name","retweet_count"]]
  retweet_by_screen_name = (
      df_screen.groupby(by=["screen_name"]).sum()[["retweet_count"]].sort_values(by="retweet_count")
  )
  fig_screen_names = px.bar(
      retweet_by_screen_name,
      x="retweet_count",
      y=retweet_by_screen_name.index,
      orientation="h",
    
      title="<b>Most retweets by User </b>",
    
      color_discrete_sequence=["#00b891"] * len(retweet_by_screen_name),
      template="plotly_dark",
  )
  fig_screen_names.update_layout(
      plot_bgcolor="rgba(0,0,0,0)",
      xaxis=(dict(showgrid=False))
  )

  left_column, right_column = st.columns(2)
  left_column.plotly_chart(fig_screen_names, use_container_width=True)
  right_column.plotly_chart(fig_product_sales, use_container_width=True)

  df_screen = df[["screen_name","original_tweet"]]
  tweet_by_screen_name = (
      df_screen.groupby(by=["screen_name"]).sum()[["original_tweet"]].sort_values(by="original_tweet")
  )
  fig_screen_names_tweets = px.bar(
      tweet_by_screen_name,
      x="original_tweet",
      y=tweet_by_screen_name.index,
      orientation="h",
    
      title="<b>Most Original tweets by User </b>",
    
      color_discrete_sequence=["#b89100"] * len(tweet_by_screen_name),
      template="plotly_dark",
  )
  fig_screen_names_tweets.update_layout(
      plot_bgcolor="rgba(0,0,0,0)",
      xaxis=(dict(showgrid=False))
  )

  df_source = df[["source"]]
  df_source = df_source.groupby(['source']).size().to_frame().sort_values([0], ascending = False).head(5).reset_index()
  df_source.columns = ['source', 'count']

  fig_source = px.pie(df_source,
                      values="count",
                      names="source",
                      title="<b>Source </b>",)



  left_column2, right_column2 = st.columns(2)
  left_column2.plotly_chart(fig_screen_names_tweets, use_container_width=True)
  right_column2.plotly_chart(fig_source, use_container_width=True)

  df_lang = df[["lang"]]
  df_lang = df_lang[df_lang['lang']!='und']
  df_lang = df_lang.groupby(['lang']).size().to_frame().sort_values([0], ascending = False).head(5).reset_index()
  df_lang.columns = ['lang', 'count']

  fig_lang = px.pie(df_lang,
                      values="count",
                      names="lang",
                      title="<b>Language Used </b>",)
  fig_lang.update_layout(legend=dict(
      yanchor="top",
      y=0.99,
      xanchor="left",
      x=0.01
  ))
          

  #Most mentioned Screen name
  screen_name_data = df[["mentions_screen_name"]]
  screen_name_data = screen_name_data.groupby(['mentions_screen_name']).size().to_frame().sort_values([0], ascending = False).head(5).reset_index()
  screen_name_data.columns = ['mentions_screen_name', 'count']


  screen_name_mentioed = (
          screen_name_data.groupby(by=["mentions_screen_name"]).sum()[["count"]].sort_values(by="count")
  )
  fig_screen_name_mentioned = px.bar(
      screen_name_mentioed,
      x="count",
      y=screen_name_mentioed.index,
      orientation="h",
      
      title="<b>Most Mentioned Screen Names </b>",
      color_discrete_sequence=["#e3d88d"] * len(screen_name_mentioed),
      template="plotly_white",
  )
  fig_screen_name_mentioned.update_layout(
      plot_bgcolor="rgba(0,0,0,0)",
      xaxis=(dict(showgrid=False))
  )
              
  left_column3, right_column3 = st.columns(2)
  left_column3.plotly_chart(fig_lang, use_container_width=True)
  right_column3.plotly_chart(fig_screen_name_mentioned, use_container_width=True)

  location_data = df[['location']]
  location_data = location_data.dropna()

  def get_cities(list_1):

    list_1 = list_1.split(",")
    if len(list_1)==1:
      return list_1[0]
    elif len(list_1)>1:
      return list_1[0]
    else:
      return ""

  def get_country(list_1):
    list_1 = list_1.split(",")
    if len(list_1)>1:
      return list_1[1]
    else:
      return ""

  location_data['cities'] = location_data['location'].apply(get_cities)
  location_data['country'] = location_data['location'].apply(get_country)

  cities = location_data.groupby(['cities']).size().to_frame().sort_values([0], ascending = False).head(5).reset_index()
  cities.columns = ['cities', 'count']

  cities_mentioned = (
          cities.groupby(by=["cities"]).sum()[["count"]].sort_values(by="count")
  )
  fig_cities_mentioned = px.bar(
      cities_mentioned,
      x="count",
      y=cities_mentioned.index,
      orientation="h",
      
      title="<b>Most Frequent Cities mentioned </b>",
      color_discrete_sequence=["#8de3d8"] * len(cities_mentioned),
      template="plotly_white",
  )
  fig_cities_mentioned.update_layout(
      plot_bgcolor="rgba(0,0,0,0)",
      xaxis=(dict(showgrid=False))
  )
  # Create some sample text
  text = 'Fun, fun, awesome, awesome, tubular, astounding, superb, great, amazing, amazing, amazing, amazing'

  # Create and generate a word cloud image:
  wordcloud = WordCloud(background_color='white',max_font_size = 50,collocations=False).generate(text)

  # Display the generated image:
  plt.figure(figsize = (20,8))
  plt.title("World Cloud")
  plt.imshow(wordcloud, interpolation='bilinear')
  plt.axis("off")


  left_column4, right_column4 = st.columns(2)
  left_column4.plotly_chart(fig_cities_mentioned, use_container_width=True)
  right_column4.pyplot(plt,use_container_width=True)
  
  # ---- HIDE STREAMLIT STYLE ----
  hide_st_style = """
              <style>
              #MainMenu {visibility: hidden;}
              footer {visibility: hidden;}
              header {visibility: hidden;}
              </style>
              """
  #st.markdown(hide_st_style, unsafe_allow_html=True)
  remove_files()
  
 
st.sidebar.header("Please Filter Here:")
uploaded_file = st.sidebar.file_uploader("Upload CSV file",type=["csv"])
button = st.sidebar.button("Generate Hashtags")
try:
    if uploaded_file:
        with open(os.path.join(uploaded_file.name),"wb") as f:
            f.write(uploaded_file.getbuffer())
            st.sidebar.success("Uploaded Successfully.....")
    
except Exception as e:
    print(e)
    pass
try:
    if button:
        main()
        
except Exception as e:
    st.write("Please upload file using Side bar",e)



