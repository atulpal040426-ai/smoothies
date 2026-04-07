# Import python packages
import streamlit as st
import requests  
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

from snowflake.snowpark.functions import col
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

list_ing = st.multiselect(
    'Choose top 5', my_dataframe
)

if list_ing:

    ing_str = ''

    for i in list_ing:
        ing_str+=i + ' '
        st.subheader(i +'Nutrition Information')
        smoothiefroot_response = requests.get(
        "https://my.smoothiefroot.com/api/fruit/"+i)
        df = st.dataframe(data =smoothiefroot_response.json(), use_container_width=True )
    # st.write(ing_str)

    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders (ingredients, name_on_order)
    VALUES ('{ing_str}', '{name_on_order}')
    """

    # st.write(my_insert_stmt)
    click = st.button('submit')

    if click:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


smoothiefroot_response = requests.get(
    "https://my.smoothiefroot.com/api/fruit/watermelon"
)






