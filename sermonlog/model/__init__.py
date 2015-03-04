import formalchemy
from pyramid.events import NewRequest

from . import meta

def db(request):
    """
        Add the sqlalchemy session to the request.
    """
    session = request.registry.sessionmaker()
    def cleanup(request):
        session.close()
    request.add_finished_callback(cleanup)
    return session

def includeme(config):
    """
        Initialize the sqlalchemy model and formalchemy.
    """
    settings = config.registry.settings
    config.registry.sessionmaker = meta.create_sessionmaker(
        settings,
        "sqlalchemy.",
    )
    config.add_request_method(db, reify=True)

    formalchemy.config.engine = formalchemy.templates.MakoEngine(
        directories=["sermonlog/templates/formalchemy"],
        input_encoding='utf-8',
        output_encoding='utf-8',
    )
