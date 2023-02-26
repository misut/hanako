class CommandException(Exception):
    ...


class GalleryServiceException(CommandException):
    ...


class FetchError(GalleryServiceException):
    ...


class MangaCacheException(CommandException):
    ...


class ReadError(MangaCacheException):
    ...


class WriteError(MangaCacheException):
    ...


class MangaDownloaderException(CommandException):
    ...


class DownloadError(MangaDownloaderException):
    ...
