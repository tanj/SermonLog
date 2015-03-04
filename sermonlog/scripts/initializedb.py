import os
import sys
import transaction
import pysword.books


from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..model.meta import (
    create_sessionmaker,
    Base,
    TTitle,
    TPresenter,
    TBibleBook,
    TChapter,
    TEventType,
    )

import re

def roman_to_int(n):
    n = str(n).upper()
    numeral_map = zip((1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1),
                      ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I'))

    i = result = 0
    for integer, numeral in numeral_map:
        while n[i:i + len(numeral)] == numeral:
            result += integer
            i += len(numeral)
    return result

def roman_to_int_repl(match):
    return str(roman_to_int(match.group(0)))

roman_regex = re.compile(r'\b(?=[MDCLXVI]+\b)M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\b')


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    DBSession = create_sessionmaker(settings, "sqlalchemy.")()
    Base.metadata.create_all(DBSession.bind)

    with transaction.manager:
        titles = [TTitle(sTitle='Rev'),
                  TTitle(sTitle='Mr'),
                  TTitle(sTitle='Mrs'),
                  TTitle(sTitle='Miss'),
                  TTitle(sTitle='Ms'),
                  TTitle(sTitle='Dr'),
                  TTitle(sTitle='Sir'),]
        DBSession.add_all(titles)

        presenters = [TPresenter(title=titles[0],
                                 sFirstName='Joel',
                                 sLastName='Overduin',
                                 sSaName='Pastor Joel Overduin'),
                      TPresenter(title=titles[0],
                                 sFirstName='Carl',
                                 sLastName='Schouls',
                                 sSaName='Pastor Carl A. Schouls'),
                      TPresenter(title=titles[1],
                                 sFirstName='Russel',
                                 sLastName='Herman',
                                 sSaName='Russel Herman'),
                      TPresenter(title=titles[1],
                                 sFirstName='Michael',
                                 sLastName='Jaatinen',
                                 sSaName='Michael Jaatinen'),
                      TPresenter(title=titles[1],
                                 sFirstName='Arie',
                                 sLastName='VanDyk'
                                 ),
                      TPresenter(title=titles[0],
                                 sFirstName='Richard',
                                 sLastName='Miller',
                                 sSaName='Richard J. Miller'),
                      TPresenter(title=titles[1],
                                 sFirstName='Brad',
                                 sLastName='Pennings'
                                 ),
                      TPresenter(title=titles[0],
                                 sFirstName='David',
                                 sLastName='Lipsy',
                                 sSaName='Pastor David Lipsy'),
                      TPresenter(title=titles[0],
                                 sFirstName='Pieter',
                                 sLastName='VanderMeyden',
                                 sSaName='Rev. Pieter VanderMeyden'),
                      TPresenter(title=titles[0],
                                 sFirstName='David',
                                 sLastName='Van Brugge',
                                 sSaName='David Van Brugge'),
                      TPresenter(title=titles[0],
                                 sFirstName='John',
                                 sLastName='Koopman',
                                 sSaName='John Koopman'),
                      TPresenter(title=titles[0],
                                 sFirstName='Henry',
                                 sLastName='Van Essen',
                                 sSaName='Pastor Henry VanEssen'),
                      TPresenter(title=titles[0],
                                 sFirstName='Stanley',
                                 sLastName='McKenzie',
                                 sSaName='Stanley McKenzie'),
                      TPresenter(title=titles[0],
                                 sFirstName='Henry',
                                 sLastName='Bartsch',
                                 sSaName='Rev. Henry Bartsch'),
                      TPresenter(title=titles[0],
                                 sFirstName='Timothy',
                                 sLastName='Bergsma',
                                 sSaName='Tim Bergsma'),
                      TPresenter(title=titles[1],
                                 sFirstName='Gerald',
                                 sLastName='Harke'
                                 ),
                      TPresenter(title=titles[0],
                                 sFirstName='Ian',
                                 sLastName='MacLeod',
                                 sSaName='Ian MacLeod'),
                      TPresenter(title=titles[0],
                                 sFirstName='C.',
                                 sLastName='Heiberg',
                                 sSaName='Rev. C. Heiberg'),
                      TPresenter(title=titles[1],
                                 sFirstName='Ken',
                                 sLastName='Pennings',
                                 sSaName='Ken Pennings'),
                      TPresenter(title=titles[1],
                                 sFirstName='John',
                                 sLastName='Procee',
                                 sSaName='John Procee'),
                      TPresenter(title=titles[5],
                                 sFirstName='Lawrence',
                                 sLastName='Bilkes',
                                 sSaName='L. W. Bilkes'),
                      TPresenter(title=titles[0],
                                 sFirstName='Cornelis',
                                 sLastName='Pronk',
                                 sSaName='Rev. Cornelis (Niel) Pronk'),
                      TPresenter(title=titles[0],
                                 sFirstName='Harold',
                                 sLastName='Zekveld',
                                 sSaName='Harry Zekveld'),
                      TPresenter(title=titles[1],
                                 sFirstName='Brian',
                                 sLastName='Luth'
                                 ),
                      TPresenter(title=titles[0],
                                 sFirstName='David',
                                 sLastName='Kranendonk',
                                 sSaName='Rev. David Kranendonk'),
                      TPresenter(title=titles[0],
                                 sFirstName='John',
                                 sLastName='van Eyk',
                                 sSaName='John van Eyk'),
                      TPresenter(title=titles[0],
                                 sFirstName='Bartel',
                                 sLastName='Elshout',
                                 sSaName='Rev. Bartel Elshout'),
                      TPresenter(title=titles[0],
                                 sFirstName='Ken',
                                 sLastName='Herfst',
                                 sSaName='Rev. Ken Herfst'),
                      TPresenter(title=titles[0],
                                 sFirstName='Robert',
                                 sLastName='VanDoodewaard',
                                 sSaName='Rob VanDoodewaard'),
                      TPresenter(title=titles[0],
                                 sFirstName='Scott',
                                 sLastName='Dibbet',
                                 sSaName='Scott Dibbet'),
                      TPresenter(title=titles[0],
                                 sFirstName='Eric',
                                 sLastName='Moerdyk',
                                 sSaName='Pastor Eric Moerdyk'),]
        DBSession.add_all(presenters)

        chapters = []
        for testament, books in pysword.books.testaments.items():
            iOrder = 1
            for b in books:
                tbook = TBibleBook(bOldTestament= (testament == 'ot'),
                                   # sermon audio doesn't like roman numerals so replace them with integers
                                   sBook=roman_regex.sub(roman_to_int_repl, b.name),
                                   sAbbrev=b.preferred_abbreviation,
                                   iOrder=iOrder,
                                   iNumChapters=b.num_chapters)

                for chap, verses in enumerate(b.chapter_lengths):
                    chapters.append(TChapter(iChapter=chap + 1,
                                             iMaxVerse=verses,
                                             book=tbook))
                iOrder = iOrder + 1

        DBSession.add_all(chapters)

        event_types = [TEventType(sEventType='Audio Book'),
                       TEventType(sEventType='Bible Study'),
                       TEventType(sEventType='Camp Meeting'),
                       TEventType(sEventType='Chapel Service'),
                       TEventType(sEventType='Children'),
                       TEventType(sEventType='Conference'),
                       TEventType(sEventType='Current Events'),
                       TEventType(sEventType='Debate'),
                       TEventType(sEventType='Devotional'),
                       TEventType(sEventType='Funeral Service'),
                       TEventType(sEventType='Midweek Service'),
                       TEventType(sEventType='Podcast'),
                       TEventType(sEventType='Prayer Meeting'),
                       TEventType(sEventType='Question & Answer'),
                       TEventType(sEventType='Radio Broadcast'),
                       TEventType(sEventType='Special Meeting'),
                       TEventType(sEventType='Sunday - AM'),
                       TEventType(sEventType='Sunday - PM'),
                       TEventType(sEventType='Sunday Afternoon'),
                       TEventType(sEventType='Sunday School'),
                       TEventType(sEventType='Sunday Service'),
                       TEventType(sEventType='Teaching'),
                       TEventType(sEventType='Testimony'),
                       TEventType(sEventType='TV Broadcast'),
                       TEventType(sEventType='Video DVD'),
                       TEventType(sEventType='Wedding'),
                       TEventType(sEventType='Youth'),]
        DBSession.add_all(event_types)

            # TODO loop through books and build TBibleBook objects


    #     model = MyModel(name='one', value=1)
    #     DBSession.add(model)
