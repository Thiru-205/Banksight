import streamlit as st
import mysql.connector
import pandas as pd 



# Function to connect and fetch data
def get_data(query, params=None):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Thirumala@205",
        database="customers_data"
    )

    if params:
        df = pd.read_sql_query(query, conn, params=params)
    else:
        df = pd.read_sql_query(query, conn)

    conn.close()
    return df




# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Banksight", layout="wide")

# ------------------ SIDEBAR ------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "🏠Project Introduction",
        "📊View Database Table",
        "🔍Filter Data",
        "✏️CRUD Operations",
        "💰Credit/Debit Simulation",
        "🧠Analytical Insight",
        "💎Creator Info"])

# ------------------ PAGE 1: INTRODUCTION ------------------
if page == "🏠Project Introduction":

    st.title("🏦 Banksight - Banking Data Analysis App")

    st.image("C:/Users/user/Downloads/Bansight.jpg")

    st.subheader("📌 About the Project")

    st.write("""
    Banksight is a banking data analysis application.

    This project helps to:
    - Store banking data using MySQL  
    - Analyze customer and transaction details  
    - Perform operations like deposit and withdrawal  
    - Display insights using Streamlit dashboard  
    """)

    st.subheader("🎯 Project Goal")

    st.write("""
    The main goal of this project is to understand how banking data works
    and how we can use SQL and Python to analyze it.
    """)

    st.subheader("⚙️ Tools Used")

    st.write("""
    - Python  
    - Pandas  
    - MySQL  
    - Streamlit  
    """)

    st.subheader("📊 What This App Can Do")

    st.write("""
    - View all banking tables  
    - Filter data easily  
    - Perform CRUD operations (Create, Read, Update, Delete)  
    - Deposit and withdraw money  
    - Show analytical insights using SQL queries  
    """)

    st.markdown("### 🎥 Platform Overview")
    st.video("C:/Users/user/Downloads/Banksight.video.mp4")

    st.divider()
    st.markdown("### 📞 Contact")
    st.markdown("""
    📍 Telangana  
    📞 +91 XXXXX XXXXX  
    📧 support@banksight.com  
        """)

# ------------------ PAGE 2 ------------------
elif page == "📊View Database Table":
    st.title("📊View Database Table")

    selected_table = st.selectbox(
        "Select Table",
        ["customers", "transactions", "accounts", "loans", "branches"])
    
     # Create query
    query = f"SELECT * FROM {selected_table}"

    # Call function
    table_result = get_data(query)

    st.write("### Results")
    st.dataframe(table_result)
    
# # ------------------ PAGE 3 ------------------
elif page == "🔍Filter Data":
    st.title("🔍Filter Data")

    # Select Table
    selected_table = st.selectbox(
        "Select Table",
        ["customers", "transactions", "accounts", "loans", "branches"]
    )

    if selected_table:

        column_query = f"SHOW COLUMNS FROM {selected_table}"
        columns_df = get_data(column_query)

        column_names = columns_df["Field"].tolist()

        #  Select Column
        selected_column = st.selectbox("Choose a column", column_names)

        # Get values from that column
        value_query = f"SELECT DISTINCT {selected_column} FROM {selected_table}"
        values_df = get_data(value_query)

        values = values_df[selected_column].dropna().tolist()

        # Select Value
        selected_value = st.selectbox("Choose a value", values)

        #  Filter Query
        filter_query = f"""
            SELECT * FROM {selected_table}
            WHERE {selected_column} = %s
        """

        filtered_df = get_data(filter_query, params=(selected_value,))

        st.dataframe(filtered_df)

# ------------------ PAGE 4: CRUD OPERATIONS ------------------
elif page == "✏️CRUD Operations":
    st.title("✏️CRUD Operations - Accounts Table")

    def get_connection():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Thirumala@205",
            database="customers_data"
        )

    operation = st.selectbox(
        "Select Operation",
        ["Create", "Read", "Update", "Delete"]
    )

    # CREATE
    if operation == "Create":
        customer_id = st.text_input("Customer ID")
        balance = st.number_input("Account Balance")

        if st.button("Insert"):
            conn = get_connection()
            cursor = conn.cursor()

            query = """
            INSERT INTO accounts (customer_id, account_balance, last_updated)
            VALUES (%s, %s, NOW())
            """
            cursor.execute(query, (customer_id, balance))
            conn.commit()
            conn.close()

            st.success("✅ Record Inserted Successfully")

    # READ
    elif operation == "Read":
        query = "SELECT * FROM accounts"
        df = get_data(query)
        st.dataframe(df)

    # UPDATE
    elif operation == "Update":
        customer_id = st.text_input("Customer ID to Update")
        new_balance = st.number_input("New Balance")

        if st.button("Update"):
            conn = get_connection()
            cursor = conn.cursor()

            query = """
            UPDATE accounts
            SET account_balance = %s,
                last_updated = NOW()
            WHERE customer_id = %s
            """

            cursor.execute(query, (new_balance, customer_id))
            conn.commit()
            conn.close()

            st.success("✅ Record Updated Successfully")

    # DELETE
    elif operation == "Delete":
        customer_id = st.text_input("Customer ID to Delete")

        if st.button("Delete"):
            conn = get_connection()
            cursor = conn.cursor()

            query = "DELETE FROM accounts WHERE customer_id = %s"
            cursor.execute(query, (customer_id,))
            conn.commit()
            conn.close()

            st.success("🗑️ Record Deleted Successfully")

##-----------------------PAGE 5----------------------------------------------
elif page == "💰Credit/Debit Simulation":
    st.title("💰 Deposit / Withdraw Money")

    # ---------- DB CONNECTION FUNCTION ----------
    def get_connection():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Thirumala@205",
            database="customers_data"
        )

    # Select customer_id
    customer_id = st.text_input("Enter Customer ID")

    # Enter amount
    amount = st.number_input("Enter Amount", min_value=0.0)

    # Select action
    action = st.radio("Select Action", ["Check Balance", "Deposit", "Withdraw"])

    # ---------- CHECK BALANCE ----------
    if action == "Check Balance":
        if st.button("Check"):
            conn = get_connection()
            cursor = conn.cursor()

            query = "SELECT account_balance FROM accounts WHERE customer_id = %s"
            cursor.execute(query, (customer_id,))
            result = cursor.fetchone()

            conn.close()

            if result:
                st.success(f"💰 Balance: {result[0]}")
            else:
                st.error("Customer not found ❌")

    # ---------- DEPOSIT ----------
    elif action == "Deposit":
     if st.button("💰 Deposit Money"):
        conn = get_connection()
        cursor = conn.cursor()

        # Step 1: Update balance
        update_query = """
        UPDATE accounts
        SET account_balance = account_balance + %s,
            last_updated = NOW()
        WHERE customer_id = %s
        """
        cursor.execute(update_query, (amount, customer_id))
        conn.commit()

        # Step 2: Get updated balance
        check_query = "SELECT account_balance FROM accounts WHERE customer_id = %s"
        cursor.execute(check_query, (customer_id,))
        new_balance = cursor.fetchone()[0]

        conn.close()

        # Step 3: Show result
        st.success(f"✅ ₹{amount} Deposited Successfully")
        st.info(f"💰 Updated Balance: ₹{new_balance}")
        
    # ---------- WITHDRAW ----------
    elif action == "Withdraw":
     if st.button("💸 Withdraw Money"):
        conn = get_connection()
        cursor = conn.cursor()

        # Step 1: Check balance
        check_query = "SELECT account_balance FROM accounts WHERE customer_id = %s"
        cursor.execute(check_query, (customer_id,))
        result = cursor.fetchone()

        if result:
            current_balance = result[0]

            if current_balance >= amount:
                # Step 2: Withdraw
                withdraw_query = """
                UPDATE accounts
                SET account_balance = account_balance - %s,
                    last_updated = NOW()
                WHERE customer_id = %s
                """
                cursor.execute(withdraw_query, (amount, customer_id))
                conn.commit()

                # Step 3: Get updated balance
                cursor.execute(check_query, (customer_id,))
                new_balance = cursor.fetchone()[0]

                st.success(f"✅ ₹{amount} Withdrawn Successfully")
                st.info(f"💰 Remaining Balance: ₹{new_balance}")
                
            else:
                st.error("❌ Insufficient Balance")
        else:
            st.error("Customer not found ❌")

        conn.close()
##------------------------PAGE 5--------------------------------
elif page == "🧠Analytical Insight":
    st.title("🧠 Analytical Insight")

    Queries = {
        "1: How many customers exist per city, and what is their average account balance?":
        "SELECT c.city, COUNT(DISTINCT c.customer_id), AVG(a.account_balance) AS avg_balance FROM customers c JOIN accounts a ON c.customer_id = a.customer_id GROUP BY c.city;",

        "2:Which account type (Savings, Current, Loan, etc.) holds the highest total balance?":
        "SELECT c.account_type, SUM(a.account_balance) FROM customers c JOIN accounts a ON c.customer_id = a.customer_id GROUP BY c.account_type;",

        "3: Who are the top 10 customers by total account balance across all account types?":
        "SELECT c.customer_id, c.name, SUM(a.account_balance) AS total_balance FROM customers c JOIN accounts a ON c.customer_id = a.customer_id GROUP BY c.customer_id, c.name ORDER BY total_balance DESC LIMIT 10;",

        "4: Which customers opened accounts in 2023 with a balance above ₹1,00,000?":
        "SELECT customer_id, account_balance, last_updated FROM accounts WHERE account_balance > 100000 AND last_updated BETWEEN '2023-01-01 00:00:00' AND '2023-12-31 23:59:59';",

        "5: How many failed transactions occurred for each transaction type?":
        "SELECT COUNT(*) AS failed_transactions, txn_type FROM transactions WHERE status='failed' GROUP BY txn_type;",

        "6: What is the total number of transactions per transaction type?":
        "SELECT COUNT(*) AS total_transactions, txn_type FROM transactions GROUP BY txn_type;",

        "7: Which accounts have 5 or more high-value transactions above ₹20,000?":
        "SELECT customer_id, COUNT(*) AS high_value_txns FROM transactions WHERE amount > 20000 GROUP BY customer_id HAVING COUNT(*) >= 5;",

        "8: What is the average loan amount and interest rate by loan type (Personal, Auto, Home, etc.)?":
        "SELECT Loan_Type, AVG(Loan_Amount), AVG(Interest_Rate) FROM loans GROUP BY Loan_Type;"
    }

    selected_query = st.selectbox("Choose a Query", list(Queries.keys()))
    query_result = get_data(Queries[selected_query])

    st.write("### Query Result")
    st.dataframe(query_result)
    
# # ------------------ PAGE 6 ------------------
elif page == "💎Creator Info":
    st.title("💎Creator Info")
    st.write("**Developed by**:Thirumala Erumalla.")

