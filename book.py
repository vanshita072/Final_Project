class Book:
    """
    Represents a book in the library.

    Attributes:
        GENRE_NAMES (dict): A dictionary mapping genre IDs to genre names.
    """
    # Class constant for genre names
    GENRE_NAMES = {
        0: "Romance",
        1: "Mystery",
        2: "Science Fiction",
        3: "Thriller",
        4: "Young Adult",
        5: "Children’s Fiction",
        6: "Self-help",
        7: "Fantasy",
        8: "Historical Fiction",
        9: "Poetry"
    }

    def __init__(self, isbn, title, author, genre, available=True):
        """
        Initializes a Book instance.

        Parameters:
            isbn (str): The ISBN of the book.
            title (str): The title of the book.
            author (str): The author of the book.
            genre (int): The genre ID of the book.
            available (bool, optional): Availability status of the book. Defaults to True.
        """
        self.__isbn = isbn
        self.__title = title
        self.__author = author
        self.__genre = genre
        self.__available = available

    # Standard getters
    def get_isbn(self):
        """
        Returns the ISBN of the book.

        Returns:
            str: The ISBN of the book.
        """
        return self.__isbn

    def get_title(self):
        """
        Returns the title of the book.

        Returns:
            str: The title of the book.
        """
        return self.__title

    def get_author(self):
        """
        Returns the author of the book.

        Returns:
            str: The author of the book.
        """
        return self.__author

    def get_genre(self):
        """
        Returns the genre ID of the book.

        Returns:
            int: The genre ID of the book.
        """
        return self.__genre

    def get_available(self):
        """
        Returns the availability status of the book.

        Returns:
            bool: True if the book is available, False otherwise.
        """
        return self.__available

    # get_genre_name method
    def get_genre_name(self):
        """
        Returns the genre name of the book based on its genre ID.

        Returns:
            str: The name of the genre.
        """
        return self.GENRE_NAMES.get(self.__genre)

    # get_availability method
    def get_availability(self):
        """
        Returns the availability status of the book as a string.

        Returns:
            str: "Available" if the book is available, "Borrowed" otherwise.
        """
        return "Available" if self.__available else "Borrowed"

    # Standard setters
    def set_isbn(self, isbn):
        """
        Sets the ISBN of the book.

        Parameters:
            isbn (str): The new ISBN of the book.
        """
        self.__isbn = isbn

    def set_title(self, title):
        """
        Sets the title of the book.

        Parameters:
            title (str): The new title of the book.
        """
        self.__title = title

    def set_author(self, author):
        """
        Sets the author of the book.

        Parameters:
            author (str): The new author of the book.
        """
        self.__author = author

    def set_genre(self, genre):
        """
        Sets the genre ID of the book.

        Parameters:
            genre (int): The new genre ID of the book.
        """
        self.__genre = genre

    # borrow_it method
    def borrow_it(self):
        """
        Marks the book as borrowed by setting its availability to False.
        """
        self.__available = False

    # return_it method
    def return_it(self):
        """
        Marks the book as available by setting its availability to True.
        """
        self.__available = True

    # String representation
    def __str__(self):
        """
        Returns a string representation of the book, including ISBN, title, author, genre, and availability.

        Returns:
            str: The formatted string representation of the book.
        """
        return f"{self.__isbn} {self.__title:<30} {self.__author:<25} {self.get_genre_name():<20} {self.get_availability()}"
