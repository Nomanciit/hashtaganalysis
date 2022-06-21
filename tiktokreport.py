


import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import numpy as np
import cufflinks
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from tiktok import HashtagReport

st.set_page_config(page_title="Tiktok Hashtag Report", page_icon=":bar_chart:", layout="wide")

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
      df["post_created_time"] = pd.to_datetime(df.post_created_time)
      df['post_created_time'] = pd.DatetimeIndex(df.post_created_time)
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


  # ---- MAINPAGE ----
  st.title(":bar_chart: Tiktok Hashtag Report")
  mystyle = '''
      <style>
          p {
              text-align: justify;
          }
      </style>
      '''
  st.markdown(mystyle, unsafe_allow_html=True)

  st.markdown("<h1 style='text-align: center; color: Blue;'>#BLA</h1>", unsafe_allow_html=True)
  
  

  total_post_count_,retweet_count,post_play_count=ht_report.post_count(df)
  df = ht_report.engaging_people(df)
  key_people = ht_report.key_people(df)
  start_name, start_date_=ht_report.originator_name_date(df)
  location, lang=ht_report.top_location_language(df)
  impressions=ht_report.potential_impressions(df)
  # TOP KPI's

  left_column, middle_column,middle_column2,right_column = st.columns(4)
  with left_column:
      st.markdown(f'<h1 style="text-align:center;color:#b4e67b;font-size:30px;">{"Total Post Count"}</h1>', unsafe_allow_html=True)
      st.markdown(f'<h2 style="text-align: center;font-size:24px;">{total_post_count_}</h2>', unsafe_allow_html=True)

  with middle_column:
      st.markdown(f'<h1 style="text-align:center;color:#b4e67b;font-size:30px;">{"Retweet Count"}</h1>', unsafe_allow_html=True)
      st.markdown(f'<h2 style="text-align: center;font-size:24px;">{retweet_count}</h2>', unsafe_allow_html=True)
      
  with middle_column2:
      st.markdown(f'<h1 style="text-align:center;color:#b4e67b;font-size:30px;">{"Impressions"}</h1>', unsafe_allow_html=True)
      st.markdown(f'<h2 style="text-align: center;font-size:24px;">{impressions}</h2>', unsafe_allow_html=True)
  with right_column:
      st.markdown(f'<h1 style="text-align:center;color:#b4e67b;font-size:30px;">{"Play count"}</h1>', unsafe_allow_html=True)
      st.markdown(f'<h2 style="text-align: center;font-size:24px;">{post_play_count}</h2>', unsafe_allow_html=True)

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

  filter_data = df[['post_created_time','post_play_count']]
  daily_cases = filter_data.groupby(pd.Grouper(key="post_created_time", freq="D")).sum().reset_index()

  fig = daily_cases.iplot(kind="line",asFigure=True,
                                  x="post_created_time", y=['post_play_count'],title="<b>Hashtag Reach Count per Day </b>")
  st.plotly_chart(fig,use_container_width=True)
#
#
  hashtags_data = df[["screen_name"]]
  hashtags_data = hashtags_data.groupby(['screen_name']).size().to_frame().sort_values([0], ascending = False).head(5).reset_index()
  hashtags_data.columns = ['screen_name', 'count']

  # SALES BY PRODUCT LINE [BAR CHART]
  sales_by_screen_name = (
      hashtags_data.groupby(by=["screen_name"]).sum()[["count"]].sort_values(by="count")
  )
  fig__screen_names = px.bar(
      sales_by_screen_name,
      x="count",
      y=sales_by_screen_name.index,
      orientation="h",
      
      title="<b>Videos Posted by..</b>",
      color_discrete_sequence=["#05b7ff"] * len(sales_by_screen_name),
      template="plotly_dark",)
  fig__screen_names.update_layout(
      plot_bgcolor="rgba(0,0,0,0)",
      xaxis=(dict(showgrid=False))
  )
      
  df_source = df[["post_language"]]
  df_source = df_source.groupby(['post_language']).size().to_frame().sort_values([0], ascending = False).head(5).reset_index()
  df_source.columns = ['post_language', 'count']

  fig_source = px.pie(df_source,
                          values="count",
                          names="post_language",
                          title="<b>Language Used</b>",)
  fig_source.update_layout(
      plot_bgcolor="rgba(0,0,0,0)",
      xaxis=(dict(showgrid=False))
  )
    

  df_location = df[["user_location"]]
  df_location = df_location.groupby(['user_location']).size().to_frame().sort_values([0], ascending = False).head(5).reset_index()
  df_location.columns = ['user_location', 'count']

  fig_location = px.pie(df_location,
                          values="count",
                          names="user_location",
                          title="<b>User Location  </b>",)

  fig_location.update_layout(
      plot_bgcolor="rgba(0,0,0,0)",
      xaxis=(dict(showgrid=False))
      )
  hashtags_ = ['balochliberationarmy',"baloch",'#FREEBALOCHISTAN','#balochistanzindabad',"#13novbalochmartyrsday",'#balochistanisnotpakistan']
  count = [20,17,15,12,11,11]
  df1 = pd.DataFrame()
  df1['hashtags']= hashtags_
  df1['count'] = count

  
  hashtag_analysis = (
        df1.groupby(by=["hashtags"]).sum()[["count"]].sort_values(by="count")
      )
  fig_product_hashtag = px.bar(
            hashtag_analysis,
          x="count",
          y=hashtag_analysis.index,
          orientation="h",
          
          title="<b>Top Hashtag Associated</b>",
          color_discrete_sequence=["#036d99"] * len(hashtag_analysis),
          template="plotly_white",
      )
  fig_product_hashtag.update_layout(
      plot_bgcolor="rgba(0,0,0,0)",
      xaxis=(dict(showgrid=False))
      )
      
  

  left_column, right_column = st.columns(2)
  left_column.plotly_chart(fig_location, use_container_width=True)
  right_column.plotly_chart(fig_source, use_container_width=True)

  left_column2, right_column2 = st.columns(2)
  left_column2.plotly_chart(fig__screen_names, use_container_width=True)
  right_column2.plotly_chart(fig_product_hashtag, use_container_width=True)
  
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
#try:
#    if button:
#        main()
#except Exception as e:
#    st.write("Please upload file using Side bar",e)
if button:
    main()
