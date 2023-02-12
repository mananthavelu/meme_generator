"""

    Ingestors.

    An abstract base class, IngestorInterface should define two methods
    with the following class method signatures:

    def can_ingest(cls, path: str) -> boolean
    def parse(cls, path: str) -> List[QuoteModel]


"""
"""
The Quote Engine module is responsible for ingesting many types of files 
that contain quotes. For our purposes, a quote contains a body and an author:

"This is a quote body" - Author
This module will be composed of many classes and will demonstrate your 
understanding of complex inheritance, abstract classes, classmethods, 
strategy objects and other fundamental programming principles.
"""

import docx
from abc import ABC, abstractmethod
import csv
import subprocess

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


class IngestorInterface(ABC):
    """Abstract Base Class for Ingestor Interface. """
    FILE_EXTENSIONS = ['csv', 'docx', 'pdf', 'txt']

    @classmethod
    def can_ingest(cls, path):
        """Return if a given path has a valid file extension to be able to consume."""
        # Fetch the file extension
        file_extension = path.split('.')[-1]
        return file_extension in cls.FILE_EXTENSIONS

    @classmethod
    @abstractmethod
    def parse(cls, path: str):
        """Return QuoteModel for each quote.
        
        The actual implementation is in the concrete class
        """
        pass

# Separate strategy objects should realize IngestorInterface for each file
# type (csv, docx, pdf, txt).

class CSVIndexer(IngestorInterface):
    """Consumes CSV file.
    """

    # Concrete method
    @classmethod
    def parse(cls, path):
        """Return QuoteModel for each quote"""

        # Check if file type is supported
        if not cls.can_ingest(path):
            return "File type not allowed / supported"
    
        # extract the quote and author
        quote_model_objects = []
        with open(path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            header = next(reader)
            body_index = header.index('body')
            author_index = header.index('author')
            for record in reader:
                body = record[body_index]
                author = record[author_index]
                quote_model = QuoteModel(body, author)
                quote_model_objects.append(quote_model)
        return quote_model_objects

class DocxIndexer(IngestorInterface):
    """Consumes Docx file.
    """

    # Concrete method
    @classmethod
    def parse(cls, path):
        """Return QuoteModel for each quote"""

        # Check if file type is supported
        if not cls.can_ingest(path):
            return "File type not allowed / supported"
        
        # Create a document object
        document = docx.Document(docx=path)

        # extract the quote and author
        quote_model_objects = []
        for quote in document.paragraphs:
            if quote.text:
                body = quote.text.split("-")[0]
                author = quote.text.split("-")[1]
                quote_model = QuoteModel(body, author)
                quote_model_objects.append(quote_model)
        return quote_model_objects


class TxtIndexer(IngestorInterface):
    """Consumes Text file.
    """

    # Concrete method
    @classmethod
    def parse(cls, path):
        """Return QuoteModel for each quote"""

        # Check if file type is supported
        if not cls.can_ingest(path):
            return "File type not allowed / supported"
    
        # extract the quote and author
        quote_model_objects = []
        with open(path, 'r') as txt_file:
            reader = txt_file.readlines()
            for line in reader:
                body = line.split("-")[0]
                author = line.split("-")[1]
                quote_model = QuoteModel(body, author)
                quote_model_objects.append(quote_model)
        return quote_model_objects

class PDFIndexer(IngestorInterface):
    """Consumes PDF file.
    """

    # Concrete method
    @classmethod
    def parse(cls, path):
        """Return QuoteModel for each quote"""

        # Check if file type is supported
        if not cls.can_ingest(path):
            return "File type not allowed / supported"
        
        # Create a document object
        files_holder = subprocess.Popen(['pdftotext', path, '-'], stdout = subprocess.PIPE)
        output = files_holder.communicate()
        contents_of_file = output[0].decode("utf-8")
        contents = contents_of_file.split("\n")

        quote_model_objects = []

        for line in contents:
            line = line.split("-")
            body, author = tuple(line)
            quote_model = QuoteModel(body, author)
            quote_model_objects.append(quote_model)
        return quote_model_objects

# A final Ingestor class should realize the IngestorInterface abstract
# base class and encapsulate your helper classes. It should implement logic
# to select the appropriate helper for a given file based on filetype.


class Ingestor(IngestorInterface):

    @classmethod
    def can_ingest(cls, path):
        file_extension = path.split('.')[-1]
        return file_extension in cls.FILE_EXTENSIONS
    
    
    @classmethod
    def parse(cls, path):
        file_extension = path.split('.')[-1]
        condition = file_extension in cls.FILE_EXTENSIONS

        class_base = cls.__base__
        if not condition:
            return "File extension not allowed / not supported"
        parser = next((c for c in class_base.__subclasses__() if file_extension in c.FILE_EXTENSIONS), None)
        return parser.parse(path)