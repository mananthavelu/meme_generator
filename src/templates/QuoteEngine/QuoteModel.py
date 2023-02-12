"""
The Quote Engine module is responsible for ingesting many types of files 
that contain quotes. For our purposes, a quote contains a body and an author:

"This is a quote body" - Author
This module will be composed of many classes and will demonstrate your 
understanding of complex inheritance, abstract classes, classmethods, 
strategy objects and other fundamental programming principles.
"""
class QuoteModel:
    """

    Load and parse the quotes and author.
    """

    def __init__(self, body, author):
        """Constructor for the QuoteModel

        Args:
            body (_type_): body of the quote
            author (_type_): author who has written the quote
        """
        self.body = body
        self.author = author

    def __repr__(self):
        return f"'{self.body}' - {self.author}"
