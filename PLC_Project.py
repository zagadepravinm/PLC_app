import streamlit as st
import pandas as pd
import numpy as np
import mysql.connector as con
from sqlalchemy import create_engine

import matplotlib.pyplot as plt

st.title("PLC Project")
# Initialize session state for Excel_Data and current_page
if 'Excel_Data' not in st.session_state:
    st.session_state['Excel_Data'] = None
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "Home"

# Horizontally aligned buttons for navigation
col1, col2, col3 = st.columns(3)
with col1:
    home_btn = st.button("Home")
with col2:
    cleaning_btn = st.button("Data Cleaning")
with col3:
    viz_btn = st.button("Visualization")
    
# Define the current page based on button clicks
if home_btn:
    st.session_state['current_page'] = "Home"
elif cleaning_btn:
    st.session_state['current_page'] = "Data Cleaning"
elif viz_btn:
    st.session_state['current_page'] = "Visualization"


# Set the current page
current_page = st.session_state['current_page']

if current_page == "Home":
    st.header("Home")

    # File uploader for data loading
    uploaded_file = st.file_uploader("Choose an Excel or CSV file", type=["xlsx", "xls", "csv"])

    if uploaded_file is not None:
        file_type = uploaded_file.name.split('.')[-1]
        
        try:
            if file_type == 'csv':
                st.session_state['Excel_Data'] = pd.read_csv(uploaded_file)
            elif file_type in ['xlsx', 'xls']:
                st.session_state['Excel_Data'] = pd.read_excel(uploaded_file)
            else:
                st.error("Unsupported file format. Please upload a CSV or Excel file.")
            
            st.success("Data Loaded Successfully")
            st.write("Here is a preview of your data:")
            st.dataframe(st.session_state['Excel_Data'])  # Display the DataFrame on the UI
            
            # Button to proceed to Data Cleaning
            if st.button("Proceed to Data Cleaning"):
                st.session_state['current_page'] = "Data Cleaning"

        except Exception as e:
            st.error(f"An error occurred: {e}")

elif current_page == "Data Cleaning":
    st.header("Data Cleaning")

    # Button to show nulls
    if st.button("Show Nulls"):
        if st.session_state['Excel_Data'] is not None:
            null_counts = st.session_state['Excel_Data'].isnull().sum()
            cleaned_data_df = null_counts.reset_index()
            cleaned_data_df.columns = ['Columns', 'Total Null']
            st.success("Null Values Displayed Successfully")
            st.dataframe(cleaned_data_df)
        else:
            st.warning("Please load the data first.")

# Button to clean data
    if st.button("Clean Data"):
        if st.session_state['Excel_Data'] is not None:
            PLC_dataset = st.session_state['Excel_Data']
            with st.spinner("Data cleaning in progress..."):
                # Coping dataset
                OrgData=PLC_dataset.copy()
                
                
                
                
                
               
                
                ##1.PLC_dataset['Total_Exp_Mnths'])
                def convert_to_months(exp):
                    # Extract years and months using regular expressions
                    years = int(exp.split(' Year(s)')[0])
                    months = int(exp.split('Year(s) ')[1].split(' Month(s)')[0])
                    # Convert the total experience to months
                    return years * 12 + months

                # Apply the conversion function to the 'Total Experience' column
                PLC_dataset['Total_Exp_Mnths'] = PLC_dataset['Total Experience'].apply(convert_to_months)





                ##2.PLC_dataset['Experience Check']
                PLC_dataset['Experience Check'] = PLC_dataset['Total_Exp_Mnths'].apply(lambda x: '4 or more than 4 years' if x >= 48 else 'Less than 4 years')







                ##3.PLC_dataset['PLC Check']
                # Define the function to check for exact matches
                def check_plc_usage(text):
                    keywords = ["Allen Bradley", "Rockwell automation", "Rockwell","Allen brobly","Allenbradly"]
                    text_lower = text.lower()  # Convert the text to lowercase for case-insensitive comparison
                    for keyword in keywords:
                        if keyword.lower() in text_lower:
                            return "Allen Bradley Or Rockwell automation"
                    return "Other"

                # Apply the function to create the new column
                PLC_dataset['PLC Check'] = PLC_dataset['Ans(Pls share PLC applications you developed, which PLC you used)'].apply(check_plc_usage)







                ##4.PLC_dataset['NoticePeriodCheck']
                def classify_notice_period(period):
                    # Normalize text to lowercase and remove extra spaces
                    period = period.lower().replace(" ", "")
                    
                    # Define patterns to match
                    patterns = ["15daysorless", "15dayorless", "15daysorles"]
                    
                    # Check if the normalized text matches any of the patterns
                    if any(pattern in period for pattern in patterns):
                        return '15 days or less'
                    else:
                        return 'more than 15 days'  # Or another appropriate classification

                # Apply the function to create the new column
                PLC_dataset['NoticePeriodCheck'] = PLC_dataset['Ans(What is your notice period ?)'].apply(classify_notice_period)











                ##5.PLC_dataset['AllAnswered']
                # Function to determine 'pass' or 'fail' based on null values
                def check_pass_fail(row):
                    # Check if any specified columns are null
                    if row[['Ans(Do you have experience on Firewall Configuration: Yes or NO)',
                            'Ans(What is your notice period ?)',
                            'Ans(Have you Executed Compact Logix Based Systems. Pls mention Controller Part number)',
                            'Ans(Have you executed Control Logix Based Systems)',
                            'Ans(Pls share PLC applications you developed, which PLC you used)',
                            'Ans(The role requires you to travel and stay at site for weeks/months. Do you agree)']].isnull().any():
                        return 'Not All Answered'
                    else:
                        return 'All Answered'

                # Apply function to create new column
                PLC_dataset['AllAnswered'] = PLC_dataset.apply(check_pass_fail, axis=1)







                ##6.PLC_dataset['CurrentLocationCheck']
                # List of South Indian states and their key cities
                south_india_locations = ['Hyderabad', 'Bengaluru', 'Chennai', 'Kochi', 'Thiruvananthapuram', 'Visakhapatnam', 'Mysore', 'Vijayawada', 'Coimbatore','banglore','Karnataka','Kerla','TamilNadu','Andhra Pradesh']

                # Function to check if the location is in South India
                def is_south_india(location):
                    # Normalize text by converting to lowercase
                    location = location.lower()
                    # Check if any of the south india locations are in the location string
                    if any(city.lower() in location for city in south_india_locations):
                        return 'South India'
                    else:
                        return 'Other'

                # Apply the function to create the new column
                PLC_dataset['CurrentLocationCheck'] = PLC_dataset['Current Location'].apply(is_south_india)







                ##7.PLC_dataset['PreferredLocationCheck']

                # List of South Indian states and their key cities
                south_india_locations = ['Hyderabad', 'Bengaluru', 'Chennai', 'Kochi', 'Thiruvananthapuram', 'Visakhapatnam', 'Mysore', 'Vijayawada', 'Coimbatore','banglore','Karnataka','Kerla','TamilNadu','Andhra Pradesh']

                # Function to check if the location is in South India
                def is_south_india(location):
                    # Normalize text by converting to lowercase
                    location = location.lower()
                    # Check if any of the south india locations are in the location string
                    if any(city.lower() in location for city in south_india_locations):
                        return 'South India'
                    else:
                        return 'Other'

                # Apply the function to create the new column
                PLC_dataset['PreferredLocationCheck'] = PLC_dataset['Preferred Locations'].apply(is_south_india)





                ##8.Write Excel

                # PLC_dataset.to_excel(r'D:\Pravin\OneDrive - SM INFORMATICS & CONTROLS\Desktop\PLC_Project.xlsx')
                
                # Renaming columns
                PLC_dataset.rename(columns={
                    "Ans(Do you have experience on Firewall Configuration: Yes or NO)": "Renamed_Firewall_Exp",
                    "Ans(What is your notice period ?)": "Renamed_Notice_Period",
                    "Ans(Have you Executed Compact Logix Based Systems. Pls mention Controller Part number)": "Renamed_Compact_Logix_Exp",
                    "Ans(Have you executed Control Logix Based Systems)": "Renamed_Control_Logix_Exp",
                    "Ans(Pls share PLC applications you developed, which PLC you used)": "Renamed_PLC_Applications",
                    "Ans(The role requires you to travel and stay at site for weeks/months. Do you agree)": "Renamed_Travel_Agreement"
                }, inplace=True)


                 
            
                
            
                # Display cleaned data
            st.success("Data Cleaned Successfully")
            st.dataframe(st.session_state['Excel_Data'])            
            
        else:
            st.warning("Please load the data first.")

    # Button to save data to MySQL
    if st.button("Save Data"):
        if st.session_state['Excel_Data'] is not None:
            db_connection_str = 'mysql+mysqlconnector://root:1301@localhost/Mydatabase'
            engine = create_engine(db_connection_str)
            try:
                # Start loading spinner
                with st.spinner('Sending data to database...'):
               # Send data in chunks
                    chunksize = 100000 # Define the chunk size (adjust based on performance)
                    for i in range(0, len(st.session_state.Excel_Data), chunksize):
                        chunk = st.session_state.Excel_Data.iloc[i:i+chunksize]
                        chunk.to_sql('PLC_table', con=engine, if_exists='append', index=False)
                st.success("Data Saved to database Successfully")
                st.session_state.Excel_Data.to_excel(r'D:\Pravin\OneDrive - SM INFORMATICS & CONTROLS\Desktop\PLC_Project.xlsx')
            except Exception as e:
                st.error(f"An error occurred: {e}")      
        else:        
            st.warning("Please load and clean the data first.")   
                
elif current_page == "Visualization":
    st.header("Visualization")
    
    # Setup the MySQL connection
    try:
        # engine = create_engine('mysql+mysqlconnector://root:1301@localhost/Mydatabase')
        mydb = con.connect(host="localhost", database='Mydatabase',user="root", passwd="1301",use_pure=True)
        query = "SELECT * FROM PLC_table"
        df = pd.read_sql(query, mydb)
        st.success("Data Loaded from MySQL Successfully")

                # Dropdowns for filtering
        st.subheader("Apply Filters")

        # Dynamically generate dropdowns based on selected columns
        filter_columns = [
            'Experience Check', 'PLC Check', 'NoticePeriodCheck', 
            'AllAnswered', 'CurrentLocationCheck', 'PreferredLocationCheck'
        ]

        filtered_df = df.copy()

        custom_titles = {
            "AllAnswered":"If Answered The Questions Clearly",
            "Experience Check": "Experience",
            "PLC Check": "Project experience",
            "NoticePeriodCheck": "Notice Period",
            "CurrentLocationCheck": "Current location",
            "PreferredLocationCheck": "Preferred location"
        }

        # Assuming df is your DataFrame
        filtered_df = df  # Replace with your actual DataFrame

        # Iterate over the columns and display dropdowns with custom titles
        for col in filter_columns:
        # Get the custom title or default to column name
            title = custom_titles.get(col, col)
        
            # Get unique values from the column and add 'All' at the beginning
            unique_values = ['All'] + sorted(filtered_df[col].dropna().unique().tolist())
        
            # Create a selectbox for filtering
            selected_value = st.selectbox(f'Select {title}', unique_values, key=col)
    
            # Filter the DataFrame based on the selected value, unless 'All' is selected
            if selected_value != 'All':
                filtered_df = filtered_df[filtered_df[col] == selected_value]

        # Display the filtered data (modify as needed)
        filtered_df.reset_index(drop=True, inplace=True)
        filtered_df.index += 1  # Start index from 1
        st.write(filtered_df)

        # # Display filtered data in a table with selected columns
        # display_columns = [
        #     'Job Title', 'Date of application', 'Name', 'Email ID', 'Phone Number', 
        #     'Current Location', 'Preferred Locations', 'Total Experience',
        #     'Renamed_Firewall_Exp', 
        #     'Renamed_Notice_Period', 
        #     'Renamed_Compact_Logix_Exp', 
        #     'Renamed_Control_Logix_Exp', 
        #     'Renamed_PLC_Applications', 
        #     'Renamed_Travel_Agreement'
        # ]

        # st.dataframe(filtered_df[display_columns])

        
        if st.button("Extract Data"):
            filtered_df.to_excel(r'D:\Pravin\OneDrive - SM INFORMATICS & CONTROLS\Desktop\Filtered_PLC_Data.xlsx')
            st.success("Data Extracted Successfully")

   
    except Exception as e:
        st.error(f"An error occurred while fetching the data from MySQL: {e}")        




