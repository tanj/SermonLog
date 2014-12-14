from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Unicode,
    DateTime,
    ForeignKey,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    backref,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class TTitle(Base):
    __tablename__ = 'tTitle'
    ixTitle = Column(Integer, primary_key=True)
    sTitle = Column(Unicode(10))

class TPresenter(Base):
    __tablename__ = 'tPresenter'
    ixPresenter = Column(Integer, primary_key=True)
    ixTitle = Column(Integer, ForeignKey('tTitle.ixTitle'))
    sFirstName = Column(Unicode(30))
    sLastName = Column(Unicode(40))
    sSaName = Column(Unicode(50)) # The sermon audio name

    title = relationship("TTitle")

class TBibleBooks(Base):
    __tablename__ = 'tBibleBooks'
    ixBibleBook = Column(Integer, primary_key=True)
    sBook = Column(Unicode(30))
    iOrder = Column(Integer)

class TChapterAndVerse(Base):
    "Describes the chapter and verse layout for proper references"
    __tablename__ = 'tChapterAndVerse'
    ixChapterAndVerse = Column(Integer, primary_key=True)
    ixBibleBook = Column(Integer, ForeignKey('tBibleBooks.ixBibleBook'))
    iChapter = Column(Integer)
    iMaxVerse = Column(Integer) # Each chapter gets a maximum verse

    book = relationship("TBibleBooks",
                        backref=backref('chap_and_verse'))

    ref = relationship("TScriptureReference",
                       backref=backref('chap_and_verse'))



class TOtherSources(Base):
    __tablename__ = 'tOtherSources'
    ixOtherSources = Column(Integer, primary_key=True)
    sSourceName = Column(Unicode(255))
    sReference = Column(Unicode(255))
    

class TScriptureReference(Base):
    __tablename__ = 'tScriptureReference'
    ixScriptureReference = Column(Integer, primary_key=True)
    ixChapterAndVerse = Column(Integer, ForeignKey('tChapterAndVerse.ixChapterAndVerse'))
    iVerseLower = Column(Integer, nullable = False)
    iVerseUpper = Column(Integer, nullable = True)


class TReading(Base):
    __tablename__ = 'tReading'
    ixReading = Column(Integer, primary_key=True)
    ixPresentation = Column(Integer, ForeignKey('tPresentation.ixPresentation'))
    ixScriptureReference = Column(Integer, ForeignKey('tScriptureReference.ixScriptureReference'), nullable=True)
    ixOtherSources = Column(Integer, ForeignKey('tOtherSources.ixOtherSources'), nullable=True)

    scripture = relationship("TScriptureReference",
                             backref=backref('reading'))
    other_source = relationship("TOtherSources",
                                backref=backref('reading'))
    

class TEventType(Base):
    __tablename__ = 'tEventType'
    ixEventType = Column(Integer, primary_key=True)
    sEventType = Column(Unicode(50))

class TPresentation(Base):
    __tablename__ = 'tPresentation'
    ixPresentation = Column(Integer, primary_key=True)
    ixEventType = Column(Integer, ForeignKey('tEventType.ixEventType'))
    sSeries = Column(Unicode(255))
    sTitle = Column(Unicode(255))
    sTheme = Column(Text)
    sComments = Column(Text) # Sermon points, general description, etc.
    ixText = Column(Integer, ForeignKey('tScriptureReference.ixScriptureReference'), nullable=True)
    dtStart = Column(DateTime) # This will give us AM/PM info

    readings = relationship("TReading",
                            backref=backref('presentation'))

Index('series_index', TPresentation.sSeries)
#Index('my_index', MyModel.name, unique=True, mysql_length=255)
