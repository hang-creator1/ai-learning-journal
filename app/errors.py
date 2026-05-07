"""Domain errors with stable codes for clients."""


class RagError(Exception):
    """Base error — clients receive {error: code, detail: str}."""

    code: str = "rag_error"
    status_code: int = 400

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)


class InvalidFileError(RagError):
    code = "invalid_file"
    status_code = 415


class EmptyFileError(RagError):
    code = "empty_file"
    status_code = 400


class InvalidParameterError(RagError):
    code = "invalid_parameter"
    status_code = 422


class CollectionNotFoundError(RagError):
    code = "collection_not_found"
    status_code = 404
