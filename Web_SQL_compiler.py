
import streamlit as st
import sqlite3
import pandas as pd
import os
from streamlit_option_menu import option_menu

# Function to execute SQL query
def execute_query(query, c):
    c.execute(query)
    data = c.fetchall()
    return data

# Function to fetch database schema
def fetch_schema(conn):
    query = "SELECT name, sql FROM sqlite_master WHERE type='table';"
    schema = pd.read_sql_query(query, conn)
    return schema

# Dictionary to hold example questions related to each database
example_questions = {
    'test.db': [
        "What are the names of all the tables in the database?",
        "How many rows are in the 'employees' table?",
        "What are the columns in the 'customers' table?"
    ],
    'College.db': [
        "List all the student details studying in fourth semester ‘C’ section.",
        "Compute the total number of male and female students in each semester and in each section.",
        "Create a view of Test1 marks of student USN ‘1BI15CS101’ in all Courses."
        "Calculate the FinalIA (average of best two test marks) and update the corresponding table for all students.",
        "---"
        "\nCategorize students based on the following criterion:",
        "If FinalIA = 17 to 20 then CAT = ‘Outstanding’",
        "If FinalIA = 12 to 16 then CAT = ‘Average’",
        "If FinalIA< 12 then CAT = ‘Weak’",
        "Give these details only for 8th semester A, B, and C section students."
    ],
    # Add more databases and questions as needed
    'Company.db': [
        "Make a list of all project numbers for projects that involve an employee whose last name is ‘Scott’, either as a worker or as a manager of the department that controls the project.",
        "Show the resulting salaries if every employee working on the ‘IoT’ project is given a 10 percent raise.",
        "Find the sum of the salaries of all employees of the ‘Accounts’ department, as well as the maximum salary, the minimum salary, and the average salary in this department",
        "Retrieve the name of each employee who works on all the projects controlled by department number 5 (use NOT EXISTS operator).",
        "For each department that has more than five employees, retrieve the department number and the number of its employees who are making more than Rs. 6,00,000."
    ],
    'Movies.db': [
        "List the titles of all movies directed by ‘Hitchcock’.",
        "Find the movie names where one or more actors acted in two or more movies.",
        "List all actors who acted in a movie before 2000 and also in a movie after 2015 (use JOIN operation).",
        "Find the title of movies and number of stars for each movie that has at least one rating and find the highest number of stars that movie received. Sort the result by movie title.",
        "Update rating of all movies directed by ‘Steven Spielberg’ to 5."
    ],
    'Salesaman.db': [
        "Count the customers with grades above Bangalore’s average",
        "Find the name and numbers of all salesman who had more than one customer",
        "List all the salesman and indicate those who have and don’t have customers in their cities (Use UNION operation.)",
        "Create a view that finds the salesman who has the customer with the highest order of a day.",
        "Demonstrate the DELETE operation by removing salesman with id 1000. All his orders must also be deleted."
    ],
    'library.db': [
        "Retrieve details of all books in the library – id, title, name of publisher, authors, number of copies in each Programme, etc.",
        "Get the particulars of borrowers who have borrowed more than 3 books, but from Jan 2017 to Jun 2017.",
        "Delete a book in BOOK table. Update the contents of other tables to reflect this data manipulation operation.",
        "Partition the BOOK table based on year of publication. Demonstrate its working with a simple query.",
        "Create a view of all books and its number of copies that are currently available in the Library."
    ]
}

# Function to handle the home page
def home_page():
    st.title('SQL Playground - Created by Shashank V H')

    # Header
    st.header('Welcome to SQL Playground')
    st.write('Explore and query various databases.')

    # Help Section
    st.header('Help')
    with st.expander("ℹ️ How to Use"):
        st.markdown("""
        1. **Select Database**: Choose a database from the dropdown.
        2. **See Schema**: Click the button to view the database schema.
        3. **Execute SQL Query**: Enter your SQL query and click execute.

        For more details, refer to the questions section for examples.
        """)


    # Path to the 'databases' folder
    databases_path = 'databases'

    # List of available databases in the 'databases' folder
    databases = [f for f in os.listdir(databases_path) if f.endswith('.db')]

    # Database selection
    selected_db = st.selectbox('Select Database', databases)

    if selected_db:
        # Display example questions related to the selected database
        if selected_db in example_questions:
            st.subheader('Questions')
            for question in example_questions[selected_db]:
                st.write(f"- {question}")

        # Connect to the selected database
        conn = sqlite3.connect(os.path.join(databases_path, selected_db))
        c = conn.cursor()

        # Show schema of the selected database
        if st.button('See Schema'):
            schema = fetch_schema(conn)
            st.write('Database Schema:')
            st.write(schema)

        # SQL query input
        st.subheader('Execute SQL Query')
        query = st.text_area('Enter SQL Query')

        if st.button('Execute'):
            if query.strip():
                try:
                    result = execute_query(query, c)
                    if result:
                        df_result = pd.DataFrame(result, columns=[i[0] for i in c.description])
                        st.write(df_result)
                    else:
                        st.warning('No results found.')
                except Exception as e:
                    st.error(f'Error executing query: {str(e)}')
            else:
                st.warning('Please enter a SQL query.')

        conn.close()

# Function to handle the projects page
def projects_page():
    st.title("Projects Page")
    st.write("Explore My Projects here!")
    st.write("- [Django documentation](https://shashankvh.pythonanywhere.com)")
    st.write("- [Terminal Portfolio](https://shashankvh.pythonanywhere.com/terminal)")
    # Add more project links if needed

# Function to handle the contact page
def contact_page():
    st.title("Contact Page")
    st.write("For any queries or assistance, please contact me.")
    st.write("- [email](https://mail.google.com/mail/?view=cm&fs=1&to=shashankvmh4@gmail.com&su=connect)")
    st.write("- [linkedin](https://www.linkedin.com/in/shashank-v-h-a13538229/)")


# Main function to run Streamlit app
def main():
    # st.title('SQL Playground - Created by Shashank V H')

    # Sidebar menu
    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",  # required
            options=["Home", "Projects", "Contact"],  # required
            icons=["house", "book", "envelope"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
        )

    # Display content based on selected menu item
    if selected == "Home":
        home_page()
    elif selected == "Projects":
        projects_page()
    elif selected == "Contact":
        contact_page()
    elif selected in example_questions:
        display_database_info(selected)


if __name__ == '__main__':
    main()
