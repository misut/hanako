class CommandException(Exception):
    ...


class GalleryServiceException(CommandException):
    ...


class FetchError(GalleryServiceException):
    ...


class MangaDownloaderException(CommandException):
    ...


class DownloadError(MangaDownloaderException):
    ...
