from sqlalchemy import (
    ForeignKey,
    Integer,
    String, Text, Unicode,
    Boolean,
    DateTime,

    engine_from_config,
    )

from formalchemy import Column

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    sessionmaker,
    relationship,
    mapper,
    backref,
    
    )

from zope.sqlalchemy import ZopeTransactionExtension

Base = declarative_base()

def _(t):
    """
        Only used to mark strings to extract for translation.
        Does not really perform any translation.
    """
    pass

class TTitle(Base):
    __tablename__ = 'tTitle'
    __label__ = 'Title'
    __plural__ = 'Titles'
    ixTitle = Column(Integer, primary_key=True)
    sTitle = Column(Unicode(10),
                    nullable=False,
                    label=_('Title'))

    def __str__(self):
        return self.sTitle

    def __repr__(self):
        return "<TTitle(ixTitle:{s.ixTitle} sTitle={s.sTitle!r})>".format(s=self)

class TPresenter(Base):
    __tablename__ = 'tPresenter'
    __label__ = 'Presenter'
    __plural__ = 'Presenters'
    ixPresenter = Column(Integer, primary_key=True)
    ixTitle = Column(Integer, ForeignKey('tTitle.ixTitle'))
    sFirstName = Column(Unicode(30), label=_('First Name'))
    sLastName = Column(Unicode(40), label=_('Last Name'))
    sSaName = Column(Unicode(70), label=_('Sermon Audio Name')) # The sermon audio name

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
    bOldTestament = Column(Boolean, label=_('Is Old Testament'))
    sBook = Column(Unicode(30), label=_('Book'))
    sAbbrev = Column(Unicode(10), label=_('Abbreviation'))
    iOrder = Column(Integer, label=_('Order'))
    iNumChapters = Column(Integer, label=_('Number of Chapters'))

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
    iChapter = Column(Integer, label=_('Chapter'))
    iMaxVerse = Column(Integer, label=_('Number of Verses')) # Each chapter gets a maximum verse

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
    sSourceName = Column(Unicode(255), label=_('Source Name'))
    sReference = Column(Unicode(255), label=_('Reference'))

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
    sEventType = Column(Unicode(50), label=_('Event Type'))

    def __repr__(self):
        r = ("<TEventType(ixEventType: {s.ixEventType}, sEventType={s.sEventType!r})>")
        return r.format(s=self)

class TSeries(Base):
    __tablename__ = 'tSeries'
    __label__ = 'Series'
    __plural__ = 'Series'
    ixSeries = Column(Integer, primary_key=True)
    sTitle = Column(Unicode(255), label=_('Title'))

    def __repr__(self):
        r = ("<TSeries(ixSeries:{s.ixSeries} sTitle{s.sTitle!r})>")
        return r.format(s=self)

class TPresentation(Base):
    __tablename__ = 'tPresentation'
    __label__ = 'Presentation'
    __plural__ = 'Presentations'
    ixPresentation = Column(Integer, primary_key=True)
    ixEventType = Column(Integer, ForeignKey('tEventType.ixEventType'))
    ixText = Column(Integer, ForeignKey('tScriptureReference.ixScriptureReference'), nullable=True)
    ixSeries = Column(Integer, ForeignKey('tSeries.ixSeries'), nullable=True)
    sTitle = Column(Unicode(255), label=_('Title'))
    sTheme = Column(Text, label=_('Theme'))
    sComments = Column(Text, label=_('Comments')) # Sermon points, general description, etc.
    dtStart = Column(DateTime, label=_('Start of Presentation')) # This will give us AM/PM info

    readings = relationship("TReading",
                            backref=backref('presentation'))

    series = relationship("TSeries",
                          backref=backref('presentation'))

    def __repr__(self):
        r = ("<TPresentation(ixPresentation: {s.ixPresentation}, ixEventType={s.ixEventType}, "
             "ixText={s.ixText}, "
             "ixSeries={s.ixSeries}, sTitle={s.sTitle!r}, sTheme={s.sTheme!r}, "
             "sComments={s.sComments!r}, dtStart={s.dtStart})>")
        return r.format(s=self)

def create_sessionmaker(settings, prefix):
    """
        Returns a session factory.
    """
    engine = engine_from_config(settings, prefix)
    return sessionmaker(
        bind=engine,
        extension=ZopeTransactionExtension(),
    )

def get_pk_map(instance):
    """
        Returns a map column_name --> value with the instance's primary keys.

        Note: This probably won't work for strangely named columns (that
        cannot act as python identifiers).
    """
    ret = {}
    for column in instance.__table__.columns:
        if column.primary_key:
            ret[column.name] = getattr(instance, column.name)

    return ret

"""
    We gather the names of all our models into model_names.
"""
#model_names = ['Person', 'Address', 'Nonid' ]
model_names = []

for (name, ent) in list(locals().items()):
    if name.startswith("_"):
        continue
    if "Base"==name:
        continue
    try:
        if issubclass(ent, Base):
            model_names.append(name)
    except:
        pass
