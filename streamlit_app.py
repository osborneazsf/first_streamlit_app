import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Favorties')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)


# New section to display Fruityvice API
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
     # import requests
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    # takes the json version of the response and normalize's it
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    # displays the data on the page
    streamlit.dataframe(fruityvice_normalized)

 except URLError as e:
    streamlist.error()
  
streamlit.write('The user entered ', fruit_choice)

# don't run anything after this
streamlit.stop()

# import snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

#adding a single-line text input widget

fruit_add = streamlit.text_input('What fruit would you like to add: ', '{default}')

#displaying the entered text

streamlit.write('Fruit to add is: ', fruit_add)
my_cur.execute("insert into fruit_load_list VALUES ('from streamlit')")
