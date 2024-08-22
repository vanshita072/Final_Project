"""
Library Management System

Author: Vanshita Munday
Description:
This program manages a library's book catalog.
It allows users to perform various operations such as searching, borrowing, returning, adding, and removing books.
The application interacts with users through a command-line interface, and it saves the book catalog to and loads it from a CSV file.
The system supports two modes: general user and librarian, where librarians have additional privileges for managing the catalog.

Inputs:
- Book catalog filename (CSV format)
- User inputs for book operations (ISBN, title, author, genre)

Processing:
- Load and save book data from/to CSV files
- Search books based on various criteria
- Borrow and return books
- Add and remove books from the catalog

Outputs:
- Display book information
- Confirmation messages for operations
- Error messages for invalid operations
"""

import csv
import sys
from book import Book


class LibraryApp:
    def __init__(self):
        """
        Initializes the LibraryApp with an empty book list, default filename,
        and a flag indicating whether the user is a librarian.
        """
        self.book_list = []  # List to store books
        self.filename = ""  # Filename for loading and saving book data
        self.user_is_librarian = False  # Flag to check if the user is a librarian

    def load_books(self, filename):
        """
        Loads books from the specified CSV file into the book list.

        Parameters:
            filename (str): The path to the CSV file containing book data.

        Returns:
            int: The number of books loaded, or -1 if the file is not found.
        """
        try:
            with open(filename, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    isbn, title, author, genre, available = row
                    genre = int(genre)  # Convert genre to integer
                    available = available == 'True'  # Convert availability to boolean
                    self.book_list.append(Book(isbn, title, author, genre, available))
            return len(self.book_list)
        except FileNotFoundError:
            return -1

    def save_books(self):
        """
        Saves the current list of books to the CSV file specified by `self.filename`.
        """
        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            for book in self.book_list:
                writer.writerow([
                    book.get_isbn(),
                    book.get_title(),
                    book.get_author(),
                    book.get_genre(),
                    "True" if book.get_available() else "False"
                ])

    def search_books(self, search_value):
        """
        Searches for books in the catalog based on the provided search value.

        Parameters:
            search_value (str): The value to search for in ISBN, title, author, or genre.
        """
        results = []
        search_value = search_value.lower()  # Convert search value to lowercase for case-insensitive comparison
        for book in self.book_list:
            if (search_value in book.get_isbn().lower() or
                    search_value in book.get_title().lower() or
                    search_value in book.get_author().lower() or
                    search_value in book.get_genre_name().lower()):
                results.append(book)
        self.print_books(results)  # Print the search results

    def borrow_book(self):
        """
        Allows a user to borrow a book by providing its ISBN.
        """
        isbn = input("Enter the 13-digit ISBN (format 999-9999999999): ").strip()
        index = self.find_book_by_isbn(isbn)
        if index == -1:
            print("No book found with that ISBN.")
        elif not self.book_list[index].get_available():
            print(f"'{self.book_list[index].get_title()}' with ISBN {isbn} is not currently available.")
        else:
            self.book_list[index].borrow_it()
            print(f"'{self.book_list[index].get_title()}' with ISBN {isbn} successfully borrowed.")

    def return_book(self):
        """
        Allows a user to return a borrowed book by providing its ISBN.
        """
        isbn = input("Enter the 13-digit ISBN (format 999-9999999999): ").strip()
        index = self.find_book_by_isbn(isbn)
        if index == -1:
            print("No book found with that ISBN.")
        elif self.book_list[index].get_available():
            print(f"'{self.book_list[index].get_title()}' with ISBN {isbn} is not currently borrowed.")
        else:
            self.book_list[index].return_it()
            print(f"'{self.book_list[index].get_title()}' with ISBN {isbn} successfully returned.")

    def add_book(self):
        """
        Allows a librarian to add a new book to the catalog.
        """
        isbn = input("Enter the 13-digit ISBN (format 999-9999999999): ").strip()
        title = input("Enter title: ").strip()
        author = input("Enter author name: ").strip()
        genre_name = input("Enter genre: ").strip()

        # Get list of valid genre names from Book.GENRE_NAMES
        valid_genres = [genre for genre in Book.GENRE_NAMES.values()]

        while genre_name not in valid_genres:
            print(f"Invalid genre. Choices are: {', '.join(valid_genres)}")
            genre_name = input("Enter genre: ").strip()

        # Find the genre ID for the selected genre
        genre = next(key for key, value in Book.GENRE_NAMES.items() if value == genre_name)

        self.book_list.append(Book(isbn, title, author, genre))
        print(f"'{title}' with ISBN {isbn} successfully added.")

    def remove_book(self):
        """
        Allows a librarian to remove a book from the catalog by providing its ISBN.
        """
        isbn = input("Enter the 13-digit ISBN (format 999-9999999999): ").strip()
        index = self.find_book_by_isbn(isbn)
        if index == -1:
            print("No book found with that ISBN.")
        else:
            removed_book = self.book_list.pop(index)
            print(f"'{removed_book.get_title()}' with ISBN {isbn} successfully removed.")

    def print_books(self, book_list=None):
        """
        Prints the details of books in the specified list, or the entire catalog if no list is provided.

        Parameters:
            book_list (list, optional): List of books to print. Defaults to None, which prints the entire catalog.
        """
        if book_list is None:
            book_list = self.book_list

        if not book_list:
            print("No matching books found.")
            return

        print("ISBN           Title                     Author                    Genre                Availability")
        print("-------------- ------------------------- ------------------------- -------------------- ------------")
        for book in book_list:
            print(book)

    def find_book_by_isbn(self, isbn):
        """
        Finds a book by its ISBN and returns its index in the book list.

        Parameters:
            isbn (str): The ISBN of the book to find.

        Returns:
            int: The index of the book in the list, or -1 if not found.
        """
        for index, book in enumerate(self.book_list):
            if book.get_isbn() == isbn:
                return index
        return -1

    def main_menu(self):
        """
        Displays the main menu for general users and handles user input for various operations.
        """
        while True:
            print("\nReader's Guild Library - Main Menu")
            print("==================================")
            print("1. Search for books")
            print("2. Borrow a book")
            print("3. Return a book")
            print("0. Exit the system")
            selection = input("Enter your selection: ").strip()

            if selection == "1":
                print("\n-- Search for books --")
                search_value = input("Enter search value: ").strip()
                self.search_books(search_value)
            elif selection == "2":
                print("\n-- Borrow a book --")
                self.borrow_book()
            elif selection == "3":
                print("\n-- Return a book --")
                self.return_book()
            elif selection == "0":
                print("\n-- Exit the system --")
                self.save_books()  # Save books before exiting
                print("Good Bye!")
                sys.exit()
            elif selection == "2130":
                self.librarian_menu()  # Access librarian menu if code is entered
            else:
                print("Invalid option.")

    def librarian_menu(self):
        """
        Displays the librarian menu and handles librarian-specific actions such as adding or removing books.
        """
        while True:
            print("\nReader's Guild Library - Librarian Menu")
            print("=======================================")
            print("1. Search for books")
            print("2. Borrow a book")
            print("3. Return a book")
            print("4. Add a book")
            print("5. Remove a book")
            print("6. Print catalog")
            print("0. Exit the system")
            selection = input("Enter your selection: ").strip()

            if selection == "1":
                print("\n-- Search for books --")
                search_value = input("Enter search value: ").strip()
                self.search_books(search_value)
            elif selection == "2":
                print("\n-- Borrow a book --")
                self.borrow_book()
            elif selection == "3":
                print("\n-- Return a book --")
                self.return_book()
            elif selection == "4":
                print("\n-- Add a book --")
                self.add_book()
            elif selection == "5":
                print("\n-- Remove a book --")
                self.remove_book()
            elif selection == "6":
                print("\n-- Print book catalog --")
                self.print_books()
            elif selection == "0":
                print("\n-- Exit the system --")
                self.save_books()  # Save books before exiting
                print("Good Bye!")
                sys.exit()
            else:
                print("Invalid option.")


def main():
    """
    Main function to start the library application. Prompts for the book catalog filename,
    loads the book data, and then displays the main menu.
    """
    print("Starting the system...")
    app = LibraryApp()
    app.filename = input("Enter book catalog filename: ").strip()
    while app.load_books(app.filename) == -1:
        print("File not found. Re-enter book catalog filename: ", end='')
        app.filename = input().strip()

    print("Book catalog has been loaded.")
    app.main_menu()


if __name__ == "__main__":
    main()
