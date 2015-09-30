import morepath
import sqlalchemy
from more.transaction import TransactionApp
from werkzeug.serving import run_simple


class App(TransactionApp):
    pass


@App.tween_factory()
def make_tween(app, handler):
    def add_cors(request):
        response = handler(request)
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:8000'
        return response
    return add_cors

def create_db():
    from .model import Session, Base
    engine = sqlalchemy.create_engine('sqlite:///musicgrid.db')
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine


def main():
    create_db()
    morepath.autosetup()
    #morepath.run(App())
    run_simple('localhost', 8080, App(), use_reloader=True)


def shell():
    import IPython, transaction
    create_db()
    IPython.embed()
