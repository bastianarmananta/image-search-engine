class ImageSearchEngineApiError(Exception):
    """Base error exception of Image Search Engine."""

    def __init__(
        self, detail: str = "Service is unavailable.", name: str = None
    ) -> None:
        self.detail = detail
        self.name = name
        super().__init__(self.detail, self.name)


class ServiceError(ImageSearchEngineApiError):
    """Failures in internal Image Search Engine services."""

    pass


class NotFoundError(ImageSearchEngineApiError):
    """Error occurred when target data not found."""

    pass
