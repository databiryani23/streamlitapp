import streamlit
import pandas
import requests
import snowflake.connector
from urlib.error import URLError
#Add title to streamlit app
streamlit.title('My first app')

#Add breakfast and menu.    



streamlit.header('Breakfast Favourites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text(' 🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')


##Add avocado and toast.
streamlit.text('🥑🍞 Avocado and Toast')

##Add Smoothie Header
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')



##Read file from s3
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
# Display the table on the page.
streamlit.dataframe(my_fruit_list.loc[fruits_selected])

streamlit.stop()

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    streamlit.error('Enter the fruit name you want to get information about!')
  else:
    streamlit.write('The user entered ', fruit_choice)
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
    fruityvice_normalized=pandas.json_normalize(fruityvice_response.json())
    streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()
  




my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()



my_cur.execute("select * from fruit_load_list")
data_rows=my_cur.fetchall()
streamlit.text('The fruit load list contains:')
streamlit.dataframe(data_rows)



add_fruit=streamlit.text_input('Enter fruit you want to add','fruit')
streamlit.write('Thanks for adding ',add_fruit)

my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('from streamlit')")
