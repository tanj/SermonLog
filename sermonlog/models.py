from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Unicode,
    DateTime,
    Boolean,
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
    __label__ = 'Title'
    __plural__ = 'Titles'
    ixTitle = Column(Integer, primary_key=True)
    sTitle = Column(Unicode(10),
                    nullable=False)

    def __repr__(self):
        return "<TTitle(ixTitle:{s.ixTitle} sTitle={s.sTitle!r})>".format(s=self)



class TPresenter(Base):
    __tablename__ = 'tPresenter'
    __label__ = 'Presenter'
    __plural__ = 'Presenters'
    ixPresenter = Column(Integer, primary_key=True)
    ixTitle = Column(Integer, ForeignKey('tTitle.ixTitle'))
    sFirstName = Column(Unicode(30))
    sLastName = Column(Unicode(40))
    sSaName = Column(Unicode(70)) # The sermon audio name

    title = relationship("TTitle")

    def __repr__(self):
        r = ("<TPresenter(ixPresenter:{s.ixPresenter} ixTitle={s.ixTitle}, sFirstName={s.sFirstName!r}, "
             "sLastName={s.sLastName!r}, sSaName={s.sSaName!r})>")
        return r.format(s=self)

class TBibleBook(Base):
    __tablename__ = 'tBibleBook'
    __label__ = 'Bible Book'
    __plural__ = 'Bible Books'
    ixBibleBook = Column(Integer, primary_key=True)
    bOldTestament = Column(Boolean)
    sBook = Column(Unicode(30))
    sAbbrev = Column(Unicode(10))
    iOrder = Column(Integer)
    iNumChapters = Column(Integer)

    def __repr__(self):
        r = ("<TBibleBook(ixBibleBook:{s.ixBibleBook} bOldTestament={s.bOldTestament}, "
             "sBook={s.sBook!r}, sAbbrev={s.sAbbrev!r}, iOrder={s.iOrder}, iNumChapters={s.iNumChapters})>")
        return r.format(s=self)

class TChapter(Base):
    "Describes the chapter and verse layout for proper references"
    __tablename__ = 'tChapter'
    __label__ = 'Chapter'
    __plural__ = 'Chapters'
    ixChapter = Column(Integer, primary_key=True)
    ixBibleBook = Column(Integer, ForeignKey('tBibleBook.ixBibleBook'))
    iChapter = Column(Integer)
    iMaxVerse = Column(Integer) # Each chapter gets a maximum verse

    book = relationship("TBibleBook",
                        backref=backref('chap_and_verse'))

    ref = relationship("TScriptureReference",
                       backref=backref('chap_and_verse'))

    def __repr__(self):
        r = ("<TChapter(ixChapter:{s.ixChapter} ixBibleBook={s.ixBibleBook}, "
             "iChapter={s.iChapter}, iMaxVerse={s.iMaxVerse})>")
        return r.format(s=self)

class TOtherSource(Base):
    __tablename__ = 'tOtherSource'
    __label__ = 'Other Source'
    __plural__ = 'Other Sources'
    ixOtherSource = Column(Integer, primary_key=True)
    sSourceName = Column(Unicode(255))
    sReference = Column(Unicode(255))

    def __repr__(self):
        r = ("<TOtherSource(ixOtherSource: {s.ixOtherSource} sSourceName={s.sSourceName!r}, "
             "sReference={s.sReference!r})>")
        return r.format(s=self)

class TScriptureReference(Base):
    __tablename__ = 'tScriptureReference'
    __label__ = 'Scripture Reference'
    __plural__ = 'Scripture References'
    ixScriptureReference = Column(Integer, primary_key=True)
    ixChapter = Column(Integer, ForeignKey('tChapter.ixChapter'))
    iVerseLower = Column(Integer, nullable = False)
    sVerseLowerPart = Column(Unicode(2), nullable=True) # for references that include 1a or 2b
    iVerseUpper = Column(Integer, nullable = True)
    sVerseUpperPart = Column(Unicode(2), nullable=True) # for references that include 1a or 2b

    def __repr__(self):
        r = ("<TScriptureReference(ixScriptureReference:{s.ixScriptureReference}, "
             "ixChapter={s.ixChapter}, iVerseLower={s.iVerseLower}, "
             "sVerseLowerPart={s.sVerseLowerPart!r}, iVerseUpper={s.iVerseUpper}, "
             "sVerseUpperPart={s.sVerseUpperPart!r})>")
        return r.format(s=self)

class TReading(Base):
    __tablename__ = 'tReading'
    __label__ = 'Reading'
    __plural__ = 'Readings'
    ixReading = Column(Integer, primary_key=True)
    ixPresentation = Column(Integer, ForeignKey('tPresentation.ixPresentation'))
    ixScriptureReference = Column(Integer, ForeignKey('tScriptureReference.ixScriptureReference'), nullable=True)
    ixOtherSource = Column(Integer, ForeignKey('tOtherSource.ixOtherSource'), nullable=True)

    scripture = relationship("TScriptureReference",
                             backref=backref('reading'))
    other_source = relationship("TOtherSource",
                                backref=backref('reading'))
    
    def __repr__(self):
        r = ("<TReading(ixReading:{s.ixReading}, ixPresentation={s.ixPresentation}, "
             "ixScriptureReference={s.ixScriptureReference}, ixOtherSource={s.ixOtherSource})>")
        return r.format(s=self)

class TEventType(Base):
    __tablename__ = 'tEventType'
    __label__ = 'Event Type'
    __plural__ = 'Event Types'
    ixEventType = Column(Integer, primary_key=True)
    sEventType = Column(Unicode(50))

    def __repr__(self):
        r = ("<TEventType(ixEventType: {s.ixEventType}, sEventType={s.sEventType!r})>")
        return r.format(s=self)

class TPresentation(Base):
    __tablename__ = 'tPresentation'
    __label__ = 'Presentation'
    __plural__ = 'Presentations'
    ixPresentation = Column(Integer, primary_key=True)
    ixEventType = Column(Integer, ForeignKey('tEventType.ixEventType'))
    ixText = Column(Integer, ForeignKey('tScriptureReference.ixScriptureReference'), nullable=True)
    sSeries = Column(Unicode(255))
    sTitle = Column(Unicode(255))
    sTheme = Column(Text)
    sComments = Column(Text) # Sermon points, general description, etc.
    dtStart = Column(DateTime) # This will give us AM/PM info

    readings = relationship("TReading",
                            backref=backref('presentation'))

    def __repr__(self):
        r = ("<TPresentation(ixPresentation: {s.ixPresentation}, ixEventType={s.ixEventType}, "
             "ixText={s.ixText}, "
             "sSeries={s.sSeries!r}, sTitle={s.sTitle!r}, sTheme={s.sTheme!r}, "
             "sComments={s.sComments!r}, dtStart={s.dtStart})>")
        return r.format(s=self)

Index('series_index', TPresentation.sSeries)
#Index('my_index', MyModel.name, unique=True, mysql_length=255)
