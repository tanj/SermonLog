from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import (
    DBSession,
    TPresenter,
    )

@view_config(route_name='presenters', renderer='sermonlog:templates/presenters.jinja2')
def presenters(request):
    try:
        pres = DBSession.query(TPresenter).all()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'presenters' : pres}
