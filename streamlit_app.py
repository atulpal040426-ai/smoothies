import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

st.title("🥤 Pending Smoothie Orders")

session = get_active_session()

# Get pending orders
my_dataframe = session.table("smoothies.public.orders") \
    .filter(col("ORDER_FILLED") == False) \
    .to_pandas()

# Normalize column names
my_dataframe.columns = [c.upper() for c in my_dataframe.columns]

# Show editable table
edited_df = st.data_editor(my_dataframe, use_container_width=True)

# Save button
if st.button("Save Changes"):

    for index, row in edited_df.iterrows():

        if row["ORDER_FILLED"] == True:

            order_uid = row["ORDER_UID"]

            # ✅ FIX: use f-string instead of %s
            update_query = f"""
            UPDATE smoothies.public.orders
            SET ORDER_FILLED = TRUE
            WHERE ORDER_UID = {order_uid}
            """

            session.sql(update_query).collect()

    st.success("Orders updated successfully!")
    st.rerun()
