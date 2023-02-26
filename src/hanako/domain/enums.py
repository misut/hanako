import enum


class MangaLanguage(str, enum.Enum):
    NONE = "none"
    ALL = "all"
    ENGLISH = "english"
    JAPANESE = "japanese"
    KOREAN = "korean"
