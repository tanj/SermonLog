from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import (
    DBSession,
    TPresenter,
    TTitle,
    )

from formalchemy import FieldSet

@view_config(route_name='presenters', renderer='sermonlog:templates/presenters.jinja2')
def presenters(request):
    try:
        pres = DBSession.query(TPresenter).all()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'presenters' : pres, 'title' : 'Presenter List'}

@view_config(route_name='edit_presenter', renderer='sermonlog:templates/edit_presenter.jinja2')
def edit_presenter(request):
    try:
        presenter = DBSession.query(TPresenter).filter(
            TPresenter.ixPresenter == int(request.matchdict['ixPresenter'])).one()
        fs = FieldSet(presenter)
        fs.configure(exclude=[fs.title])
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'presenter' : presenter, 'title' : 'Edit Presenter', 'form_render' : fs.render()}




conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_SermonLog_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
