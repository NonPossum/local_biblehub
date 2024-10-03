import json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Base URL
BASE_URL = 'https://biblehub.com'

# Function to load JSON data
def load_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

# Function to display references for a selected Strong's number
def display_references(strongs_number, data):
    console = Console()
    
    # Find the record with the matching Strong's number
    result = next((item for item in data if item['strongs_number'] == strongs_number), None)
    
    if result:
        # Create a table for references
        table = Table(title=result['heading'])
        table.add_column("Reference", style="bold")
        table.add_column("Greek Text", style="cyan")
        
        # Add each reference to the table
        for occurrence in result['occurrences']:
            table.add_row(
                occurrence['reference'],
                occurrence['greek'],
            )
        
        # Display the table with references
        console.print(Panel(table, title=f"Strong's Number: {strongs_number}"))
    else:
        # If the Strong's number is not found
        console.print(Panel(f"No references found for Strong's number: {strongs_number}", style="bold red"))

# Function to search for an entry based on transliteration
def find_entry_by_transliteration(data, transliteration):
    transliteration_lower = transliteration.lower()
    return next((entry for entry in data if entry.get('Transliteration', '').lower() == transliteration_lower), None)

# Function to display details of an entry based on transliteration
def display_entry_details(entry):
    console = Console()
    
    if not entry:
        console.print(Panel("No data found for the given transliteration.", title="Error", border_style="red"))
        return

    main_table = Table(show_header=False, box=None)
    main_table.add_column("Key", style="cyan")
    main_table.add_column("Value", style="yellow")

    for key, value in entry.items():
        if key != "References" and value and value != "N/A":
            main_table.add_row(key, str(value))

    console.print(Panel(main_table, title="Word Information", border_style="blue"))

# Main part of the program
def main():
    console = Console()
    
    # Choose the mode of operation
    mode = console.input("[bold green]Choose operation mode ( s for Strong's Number / t for Transliteration): [/bold green]")
    
    # Load data from the appropriate JSON file depending on the chosen mode
    if mode.lower() == 's':
        data = load_data('ref.json')
        strongs_number = int(console.input("Enter Strong's Number: "))
        display_references(strongs_number, data)
    elif mode.lower() == 't':
        data = load_data('biblehub_data.json')
        transliteration = console.input("Enter Transliteration you want to search for: ")
        entry = find_entry_by_transliteration(data, transliteration)
        display_entry_details(entry)
    else:
        console.print(Panel("Invalid mode selection. Choose 's' or 't'.", style="bold red"))

if __name__ == "__main__":
    main()
