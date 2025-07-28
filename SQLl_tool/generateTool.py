import sqlite3, os, time, getpass

def clean():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n   --- 🛠️ Creating New SQLlite Database ---\n\n")

def new_database():
    print("\n   --- 🛠️  Creating New SQLlite Database ---\n\n")
    
    db_name = input("⁂ Enter the name for the new database file (without .db): ").strip()
    while not db_name:
        print("\n ⚠️  Database name cannot be empty.")
        time.sleep(2)
        clean()
        db_name = input("⁂ Please enter a valid name: ").strip()
    
    table_name = db_name 


    columns_definitions = []
    has_primary_key = False
    
    while True:
        try:
            time.sleep(1)
            clean()
            num_columns = int(input("⁂ How many columns do you want to create? "))
            if num_columns > 0:
                break
            else:
                print("\n⚠️  Please enter a number greater than zero.")
                time.sleep(2)
                clean()
        except ValueError:
            time.sleep(2)
            clean()
            print("\n⚠️  Invalid input. Please enter a number.")

    for i in range(num_columns):
        time.sleep(1)
        clean()
        print(f"\n--- ⁜ Defining Column {i+1}/{num_columns} ---\n\n")
        
        col_name = input(f"⁂ Enter name for column {i+1}: ").strip()
        while not col_name:
            time.sleep(2)
            clean()
            print("⚠️  Column name cannot be empty.")
            col_name = input(f"⁂ Please enter a valid name for column {i+1}: ").strip()

        while True:
            time.sleep(1)
            clean()
            print(f"●Select data type for column '{col_name}':\n")
            print("  1. Text (for names, emails, general text)")
            print("  2. Integer (for whole numbers like ID, age)")
            print("  3. Real (for decimal numbers like price, weight)\n\n")
            
            type_choice = input("⁂ Enter your choice (1, 2, or 3): ")
            
            if type_choice == '1':
                col_type = 'TEXT'
                break
            elif type_choice == '2':
                col_type = 'INTEGER'
                break
            elif type_choice == '3':
                col_type = 'REAL'
                break
            else:
                time.sleep(2)
                clean()
                print("⚠️  Invalid choice. Please select 1, 2, or 3.")

        col_definition = f'"{col_name}" {col_type}'
        if not has_primary_key:
            pk_choice = input("⁂ Make this column the PRIMARY KEY? (yes/no): ").strip().lower()
            if (pk_choice).lower == 'yes' or 'y':
                col_definition += ' PRIMARY KEY'
                has_primary_key = True

        columns_definitions.append(col_definition)

    full_definitions_str = ", ".join(columns_definitions)
    create_query = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({full_definitions_str});'
    
    conn = None
    try:

        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        db_file_path = os.path.join(desktop_path, f"{db_name}.db")
        
        print(f"\nCreating database at: {db_file_path}")
        
        conn = sqlite3.connect(db_file_path)
        cursor = conn.cursor()
        
        cursor.execute(create_query)
        conn.commit()
        
        time.sleep(1)
        clean()
        print(f"\n✅  Success! Database '{db_name}.db' with table '{table_name}' has been created on your Desktop.")

    except Exception as e:
        time.sleep(2)
        clean()
        print(f"\n❌  An error occurred: {e}")
    finally:
        if conn:
            conn.close()
            print("\n\n     --- Database connection closed ---")

new_database()


