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

from ..models import (
    DBSession,
    Base,
    TTitle,
    )


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
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
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

    #     model = MyModel(name='one', value=1)
    #     DBSession.add(model)
