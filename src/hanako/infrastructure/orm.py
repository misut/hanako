from sqlalchemy import Column, String, orm

BaseOrm = orm.declarative_base()


class MangaOrm(BaseOrm):
    __tablename__ = "manga"

    id = Column(String(64), primary_key=True)
    title = Column(String(512), index=True, nullable=False)
