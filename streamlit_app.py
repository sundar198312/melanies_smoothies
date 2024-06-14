# Import python packages
import streamlit as st
import requests, pandas as pd
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custome smoothie.
    """
)


##  option = st.selectbox(
##    "What is your favourite fruit?",
##    ("Strawberries", "Mangoes", "Peaches"))

##  st.write("You selected:", option)

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop

pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop

ingredients_list = st.multiselect(
    "Choose upto 5 ingredients:", my_dataframe, max_selections = 5
     )


if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredient_str = ''

    for fruit_chosen in ingredients_list:
        ingredient_str += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrient Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
        fv_df = st.dataframe(data=fruityvice_response.json() , use_container_width=True)

    #st.text(ingredient_str)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredient_str + """' , '""" + name_on_order + """' )"""
    
    # st.write(my_insert_stmt)
    # st.stop()
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()        
        st.success('Your Smoothie is ordered!,' + name_on_order , icon="✅")

# st.text(fruityvice_response.json())








