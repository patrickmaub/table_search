#!/usr/bin/env python3
import sys
from consts import PRESET_TABLES
from table_data_fetcher import TableDataFetcher
from markpy import format_as_markdown_table


def create_cell_list(row_names, column_headers):
    """
    Create a dictionary representing the initial state of each cell in the table.

    :param row_names: A list of row names.
    :param column_headers: A list of column names.
    :return: A dictionary with keys as tuples (row_name, column_name) and values as dictionaries containing cell data.
    """
    return {(row, col): {"Response": None, "URL": None, "Content": None, "Attempts": 0} for row in row_names for col in column_headers}


def gather_table_input():
    """
    Gather input from the user to create a new table.

    :return: Tuple containing the prompt, row names, and column headers.
    """
    column_headers = input("Enter column headers (comma separated): ").split(',')
    row_names = input("Enter row names (comma separated): ").split(',')
    prompt = input("Enter instructions on which sources to interrogate: ")
    return prompt, row_names, column_headers


def choose_table():
    """
    Allow the user to choose a preset table or define their own.

    :return: Tuple containing the chosen prompt, row names, and column headers.
    """
    print("\nChoose a preset table or enter your own:")
    for i, table in enumerate(PRESET_TABLES.values(), 1):
        print(f"{i}. {table['prompt']}")
    print(f"{len(PRESET_TABLES) + 1}. Enter your own table")

    choice = input(f"Enter your choice (1-{len(PRESET_TABLES) + 1}): ")
    try:
        choice = int(choice)
    except ValueError:
        print("Invalid input. Please enter a number.")
        return choose_table()

    if 1 <= choice <= len(PRESET_TABLES):
        chosen_table = list(PRESET_TABLES.values())[choice - 1]
        return chosen_table['prompt'], chosen_table['rows'], chosen_table['columns']
    elif choice == len(PRESET_TABLES) + 1:
        return gather_table_input()
    else:
        print("Invalid choice. Please select a valid option.")
        return choose_table()


def save_table(table_data, markdown_table, table_name):
    """
    Save the table data and markdown representation to files.

    :param table_data: The structured data for the table.
    :param markdown_table: The string representation of the table in markdown format.
    :param table_name: The name of the table.
    """
    with open(f'{table_name}.txt', 'w', encoding='utf-8') as txt_file:
        txt_file.write(str(table_data))

    with open(f'{table_name}.md', 'w', encoding='utf-8') as md_file:
        md_file.write(markdown_table)


def main_menu():
    """
    Display the main menu and handle user interactions.
    """
    created_tables = {}
    menu_options = {
        '1': "Create new table",
        '2': "Show existing tables",
        '3': "Exit"
    }

    while True:
        print("\n")
        for key, value in menu_options.items():
            print(f"{key}. {value}")
        choice = input("Enter your choice: ")

        if choice == '1':
            table_name = input("Enter a name for your table: ")
            prompt, rows, columns = choose_table()
            cells = create_cell_list(rows, columns)
            data_fetcher = TableDataFetcher(prompt, rows, columns, cells)

            try:
                filled_table = data_fetcher.fill_table()
                #print(filled_table)

                markdown_table = format_as_markdown_table(filled_table)
                save_table(filled_table, markdown_table, table_name)
                created_tables[table_name] = filled_table
            except Exception as e:
                #print the stack tracke
                import traceback
                print(traceback.format_exc())
                print(f"An error occurred while filling the table: {str(e)}")

        elif choice == '2':
            if created_tables:
                for table_name, table_data in created_tables.items():
                    print(f"\n{table_name}:\n")
                    print(format_as_markdown_table(table_data))
            else:
                print("\nNo tables have been created yet.")

        elif choice == '3':
            print("Exiting...")
            break

        else:
            print("Invalid option selected, please try again.")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting...")
        sys.exit(0)
