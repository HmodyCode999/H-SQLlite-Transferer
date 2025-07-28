import os, time, getpass

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("     ◀ H SQLlite Transferer ▶ \n\n\n")

def name():
    print()
    old_name = input("⁂ Enter the name of the old database file: ")
    time.sleep(1)
    new_name = input("\n⁂ Enter the name of the new database file: ")
    time.sleep(1)
    clear_screen()
    return old_name, new_name

def path():
    print("● Where is the database file's? \n")
    print("1. Desktop")
    print("2. Custom folder in Desktop")
    print("3. Custom path - enter full path")
    choice = input("\n\n⁂ Enter your choice: ")
    if choice == "1":
        user = getpass.getuser()
        path_val = f"C:/Users/{user}/Desktop"
    elif choice == "2":
        user = getpass.getuser()
        folder = input("\n\n⁂ Enter the folder name in Desktop: ")
        path_val = f"C:/Users/{user}/Desktop/{folder}"
    elif choice == "3":
        path_val = input("\n\n⁂ Enter the custom path: ")
    else:
        print("\n\nInvalid choice  ⚠️")
        time.sleep(3)
        clear_screen()
        return path() 
    time.sleep(1)
    clear_screen()
    return path_val

def custom_transfer():
    print("● How many columns do u want to transfer? \n")
    num = int(input("\n\n⁂ Enter the num: "))
    columns = []
    time.sleep(1)
    clear_screen()
    for i in range(num):
        print(f"      ⁜ {i+1}/{num}\n")
        print(f"⁂ Enter the name of the old column - from the old database")
        old_column = input("\n\nOld column: ")
        print(f"\n⁂ Enter the name of the new column - from the new database")
        new_column = input(f"\n\nFrom {old_column} to: ")
        columns.append((old_column, new_column))
    time.sleep(1)
    clear_screen()
    return columns

def transfer():
    print("● Auto transfer or custom transfer? \n")
    print("1. Auto transfer - data with the same name")
    print("2. Custom transfer - data with a different name")
    transfer_choice = input("\n\n⁂ Enter your choice: ")
    if transfer_choice == "1":
        print("Auto transfer...")
        time.sleep(1)
        clear_screen()
        return "auto", None 
    elif transfer_choice == "2":
        print("Custom transfer...")
        time.sleep(1)
        clear_screen()
        columns = custom_transfer()
        return "custom", columns
    else:
        print("\n\nInvalid choice  ⚠️")
        time.sleep(3)
        clear_screen()
        return transfer()

def engine(db_path, old_db, new_db, transfer_type, columns_map):
    clear_screen()
    print("     🚀  --- Engine Started ---  🚀\n\n")
    print("The engine has received the following data to start the transfer:\n")
    print(f"Path: {db_path}")
    print(f"From Database: {old_db}.db")
    print(f"To Database: {new_db}.db")
    print(f"Transfer Type: {transfer_type}")
    if columns_map:
        print("Column Mapping:")
        for old, new in columns_map:
            print(f"  '{old}' -> '{new}'")
    print("\n   --- Preparing Transfer ---")
    time.sleep(3)

    # start transfering
    os.system('cls' if os.name == 'nt' else 'clear')
    from transferTool import convert_tool
    convert_tool(db_path, old_db, new_db, transfer_type, columns_map)

def info(db_path, old_db, new_db, transfer_type, columns_map):
    print("\n\n     --- Quick Check --- ")
    print("\nPath: ", db_path)
    print("\nOld file: ", old_db)
    print("\nNew file: ", new_db)
    print("\nTransfer type: ", transfer_type)
    if columns_map:
        print("\nColumns to transfer: ")
        for old, new in columns_map:
            print(f"  From '{old}' To '{new}'")
    print("\n-----------------------\n")
    input("※ Press ENTER to back to the Faludation")
    clear_screen()
    return

def faludtion(db_path, old_db, new_db, transfer_type, columns_map):
    print("● Quick check before transfer? \n")
    print("1. Yes")
    print("2. No - start transfer")
    print("3. Exite - back to the main menu  ⌂ ")
    check = input("\n\n⁂ choise: ")
    if check == "1":
        time.sleep(1)
        clear_screen()
        info(db_path, old_db, new_db, transfer_type, columns_map)
        engine(db_path, old_db, new_db, transfer_type, columns_map)
    elif check == "2":
        time.sleep(1)
        clear_screen()
        engine(db_path, old_db, new_db, transfer_type, columns_map)
    elif check == "3":
        print("Exiting...")
        time.sleep(5)
        main()
    else:
        print("\n\nInvalid choice  ⚠️")
        time.sleep(3)
        clear_screen()
        faludtion(db_path, old_db, new_db, transfer_type, columns_map)

def exiteing():
    clear_screen()
    print("""       Thx for useing my program!\n
        u can find me at:\n\n
        Github:         HmodyCode999 \n
        H-Tree:         https://hmody-tree.netlify.app \n
        H-Portfolio:    https://hmody-site.netlify.app \n
                                                Press CTRL + Click on the links to open  """)
    input("Click ENTER")
    print("\n           Made with ❤️  by Hmody")
    time.sleep(2)
    exit()

def main():

    print("""● Do u have a new database fil? or want to creat a new one? \n
1. Already have one, thx
2. Creat a new database file
3. Exit """)
    choice = input("\n\n⁂ Enter your choice: ")
    if choice == "1":
        clear_screen()
    elif choice == "2":
        os.system('cls' if os.name == 'nt' else 'clear')
        from generateTool import new_database
        new_database()
        time.sleep(3)    
        input("\n\npress ENTER to back to the main menu  ⌂")
        clear_screen()
        main()
    elif choice == "3":
        exiteing()
    else:
        print("\n\nInvalid choice  ⚠️")
        time.sleep(3)
        clear_screen()
        main()
    

    print("""● Where is the database file's?  -  they must be at the same location\n
1. Same folder as the script
2. Custom path
3. Exit """)
    choice = input("\n\n⁂ Enter your choice: ")
    
    if choice == "1":
        time.sleep(1)
        clear_screen()
        db_path = os.getcwd() 
        old_name, new_name = name()
        transfer_type, columns = transfer()
        faludtion(db_path, old_name, new_name, transfer_type, columns)
        time.sleep(1)    
        input("\n\npress ENTER to back to the main menu  ⌂")
        clear_screen()
        main()

    elif choice == "2":
        time.sleep(1)
        clear_screen()
        db_path = path()
        old_name, new_name = name()
        transfer_type, columns = transfer()
        faludtion(db_path, old_name, new_name, transfer_type, columns)
        main()

    elif choice == "3":
        exiteing()
        
    else:
        print("\n\nInvalid choice  ⚠️")
        print("\nRestarting PROGRAM...")
        time.sleep(3)
        clear_screen()
        main()


# Run area
os.system('cls' if os.name == 'nt' else 'clear')
input("🖐️   Welcome to the SQLlite Transfer Tool     Press ENTER to continue")
print("\n\n\n\n   ⁂ Made by   Hmody    as usual(⌐■_■) ")
time.sleep(2)
clear_screen()
main()


#?       Follow us  ฅ⁠^⁠•⁠ﻌ⁠•⁠^⁠ฅ
#*     GitHub  ->  @HmodyCode999