import sqlite3, os, time

def clean():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n   --- ⚙️  Transfer have been started ---\n\n")

def convert_tool(db_path, old_db, new_db, transfer_type, columns_map):
    
    print("\n   --- ⚙️  Transfer have been started ---\n\n")

    old_conn = None
    new_conn = None
    
    try:
        old_db_path = os.path.join(db_path, f"{old_db}.db")
        new_db_path = os.path.join(db_path, f"{new_db}.db")
        
        old_conn = sqlite3.connect(old_db_path)
        new_conn = sqlite3.connect(new_db_path)
        
        old_cursor = old_conn.cursor()
        new_cursor = new_conn.cursor()
        
        old_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        old_tables = [row[0] for row in old_cursor.fetchall()]

        new_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        new_tables = [row[0] for row in new_cursor.fetchall()]

        old_table_name = ""
        new_table_name = ""

        if len(old_tables) == 1 and len(new_tables) == 1:
            old_table_name = old_tables[0]
            new_table_name = new_tables[0]
            print(f"✓ Auto-selecting single tables: FROM '{old_table_name}' TO '{new_table_name}'")
            time.sleep(2)
        else:
            print("\n⚠️  Multiple tables detected or no tables found. - specify table names")
            print(f"\n\n● Tables in '{old_db}.db': {old_tables}")
            old_table_name = input(f"⁂ Specify table name to transfer FROM: ")
            
            print(f"\n● Tables in '{new_db}.db': {new_tables}")
            new_table_name = input(f"⁂ Specify table name to transfer TO: ")
            time.sleep(1)
            clean()


        if transfer_type == 'auto':
            print("\n⚙️  Auto-detecting common columns...")
            old_cursor.execute(f'PRAGMA table_info({old_table_name})')
            old_cols = {info[1] for info in old_cursor.fetchall()}
            
            new_cursor.execute(f'PRAGMA table_info({new_table_name})')
            new_cols = {info[1] for info in new_cursor.fetchall()}
            
            common_columns = list(old_cols.intersection(new_cols))

            if 'id' in common_columns:
                print("NOTE: Ignoring 'id' column to allow automatic generation.")
                common_columns.remove('id')
            
            if not common_columns:
                print("\n⚠️  No common columns found between the two tables. Nothing to transfer.")
                return

            print(f"Found common columns: {', '.join(common_columns)}")
            
            cols_str = ', '.join(f'"{col}"' for col in common_columns)
            placeholders = ', '.join(['?'] * len(common_columns))

        elif transfer_type == 'custom' and columns_map:
            print("\n⚙️  Preparing for custom column transfer...")

            original_map_count = len(columns_map)
            columns_map = [item for item in columns_map if item[0].lower() != 'id']
            if len(columns_map) < original_map_count:
                print("NOTE: Ignoring 'id' column mapping to allow automatic generation.")

            old_cols = [item[0] for item in columns_map]
            new_cols = [item[1] for item in columns_map]
            
            cols_to_select_str = ', '.join(f'"{col}"' for col in old_cols)
            cols_to_insert_str = ', '.join(f'"{col}"' for col in new_cols)
            placeholders = ', '.join(['?'] * len(columns_map))
            
            cols_str = cols_to_select_str
            common_columns = old_cols 

        select_query = f'SELECT {cols_str} FROM {old_table_name}'
        print(f"\nExecuting: {select_query}")
        old_cursor.execute(select_query)
        rows_to_transfer = old_cursor.fetchall()
        
        if not rows_to_transfer:
            print("\n✅  The source table is empty. Nothing to transfer.")
            return

        print(f"Found {len(rows_to_transfer)} rows to transfer.")


        if transfer_type == 'auto':
           insert_query = f'INSERT INTO {new_table_name} ({cols_str}) VALUES ({placeholders})'
        else: 
           insert_query = f'INSERT INTO {new_table_name} ({cols_to_insert_str}) VALUES ({placeholders})'

        print(f"Executing insert statements...")
        new_cursor.executemany(insert_query, rows_to_transfer)
        
        new_conn.commit()
        print(f"\n✅  Success! Transferred {new_cursor.rowcount} rows.")

    except sqlite3.Error as e:
        print(f"\n❌  An SQL error occurred: {e}")
        print("Please check if file paths, table names, and column names are correct.")
        if new_conn:
            new_conn.rollback() 
            
    except Exception as e:
        print(f"\n❌  An unexpected error occurred: {e}")

    finally:
        if old_conn:
            old_conn.close()
        if new_conn:
            new_conn.close()
        print("\n   --- Database connections closed ---")
