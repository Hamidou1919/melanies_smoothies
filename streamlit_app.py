# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """ Choose the fruits you want in your smoothie!
  """
)


name_order = st.text_input("Name On Smoothie :")
st.write("The Name of your Smoothie wil be:", name_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections = 5
)


if ingredients_list:

    ingredients_string = ''

    for fruit_chosen in ingredients_list :
        ingredients_string += fruit_chosen + " "
        
    #st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
                values ('""" + ingredients_string + """','""" +name_order+"""')"""
    
    # st.write(my_insert_stmt)
    # st.stop()
    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
    
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response.json)
fv_dv = st.dataframe(data=st.text(fruityvice_response.json, use_container_width =True))
