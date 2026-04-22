import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. Database Setup: We use a CSV file to act as our database 
DATA_FILE = "attendance_records.csv"

# Create the file if it doesn't exist yet
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Date", "Name", "Subject", "Status"])
    df.to_csv(DATA_FILE, index=False)

# Helper function to load data
def load_data():
    return pd.read_csv(DATA_FILE)

# 2. User Login System 
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("Attendance System Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        # Simple mock login logic
        if username == "admin" and password == "1234":
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Invalid Username or Password. Use admin / 1234")

# 3. Main Dashboard (Only visible after login) 
else:
    st.sidebar.title("Navigation")
    # Main Features Menu 
    menu = st.sidebar.radio("Go To:", ["Add Attendance", "View Attendance", "Dashboard & Graphs"])
    
    # Logout feature 
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.rerun()

    st.title("Attendance Visualization Website")

    # FEATURE 1: Add Attendance 
    if menu == "Add Attendance":
        st.header("Add New Record")
        
        with st.form("attendance_form"):
            date = st.date_input("Date")
            name = st.text_input("Student Name")
            subject = st.selectbox("Subject", ["Computer Networks", "Cybersecurity", "Python", "Mathematics"])
            status = st.radio("Attendance Status", ["Present", "Absent"])
            submit = st.form_submit_button("Save to Database")
            
            if submit and name:
                new_data = pd.DataFrame({"Date": [date], "Name": [name], "Subject": [subject], "Status": [status]})
                new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)
                st.success(f"Attendance for {name} saved successfully!")

    # FEATURE 2: View Attendance 
    elif menu == "View Attendance":
        st.header("Raw Attendance Records")
        df = load_data()
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No records found in the database.")

    # FEATURE 3: Generate Graphs & Analyze Trends 
    elif menu == "Dashboard & Graphs":
        st.header("Visual Analytics")
        df = load_data()
        
        if not df.empty:
            # Calculate overall percentage 
            total_classes = len(df)
            present_classes = len(df[df['Status'] == 'Present'])
            overall_percentage = (present_classes / total_classes) * 100
            st.metric("Overall Attendance Percentage", f"{overall_percentage:.2f}%")
            
            st.markdown("---")
            
            # Create two columns for side-by-side charts
            col1, col2 = st.columns(2)
            
            # Pie Chart: Present vs Absent 
            with col1:
                st.subheader("Overall Status (Pie Chart)")
                status_counts = df['Status'].value_counts()
                fig1, ax1 = plt.subplots()
                ax1.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', colors=['#2ecc71', '#e74c3c'])
                st.pyplot(fig1)

            # Bar Chart: Subject-wise Attendance 
            with col2:
                st.subheader("Subject-wise Presents (Bar Chart)")
                present_df = df[df['Status'] == 'Present']
                subject_counts = present_df['Subject'].value_counts()
                fig2, ax2 = plt.subplots()
                ax2.bar(subject_counts.index, subject_counts.values, color='#3498db')
                ax2.set_ylabel("Days Present")
                plt.xticks(rotation=45)
                st.pyplot(fig2)
                
            # Line Graph: Attendance Trend Over Time 
            st.markdown("---")
            st.subheader("Attendance Trend Over Time (Line Graph)")
            trend_df = df.groupby(['Date', 'Status']).size().unstack(fill_value=0)
            if 'Present' in trend_df.columns:
                fig3, ax3 = plt.subplots(figsize=(10, 4))
                ax3.plot(trend_df.index, trend_df['Present'], marker='o', color='#9b59b6', linestyle='-')
                ax3.set_ylabel("Number of Students Present")
                ax3.set_xlabel("Date")
                st.pyplot(fig3)
            else:
                st.info("Not enough data to show trend line yet.")

        else:
            st.info("Please add some attendance records first to generate graphs.")