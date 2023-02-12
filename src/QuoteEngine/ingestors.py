    """
    Ingestors
    An abstract base class, IngestorInterface should define two methods
    with the following class method signatures:

    def can_ingest(cls, path: str) -> boolean
    def parse(cls, path: str) -> List[QuoteModel]
    Separate strategy objects should realize IngestorInterface for each file
    type (csv, docx, pdf, txt).

    A final Ingestor class should realize the IngestorInterface abstract
    base class and encapsulate your helper classes. It should implement logic to select the appropriate helper for a given file based on filetype.

    """
class IngestorInterface(ABC):

    @classmethod
    def can_ingest(cls, path) -> boolean:

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
    