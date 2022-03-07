from wsgiref.simple_server import make_server
from algoritmika.exception import NotStatusExceptioms
from algoritmika.middleware import JSONTranslator, BasicAuthMiddleware, JWTAuthMiddleware
import falcon
from algoritmika.views import (
    ThingsResource, UserController, UsersController,
    BookBaseViews, NoteListCreateView, NoteRetrieveView,
    IssueRetrieveView, IssueListCreateView, SortedIssue,
    TackNumberFour, FilterBaseView, AuthLogin
)

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.


# falcon.App instances are callable WSGI apps
# in larger applications the app is created in a separate file

middleware = [
    JSONTranslator(),
    JWTAuthMiddleware(),

]

app = falcon.App(middleware=middleware)
app.add_error_handler(NotStatusExceptioms)

# Resources are represented by long-lived class instances
things = ThingsResource()
user_controller = UserController()
users_controller = UsersController()
books_controller = BookBaseViews()


# things will handle all requests to the '/things' URL path
app.add_route('/things', things)
app.add_route('/users/', users_controller)
app.add_route('/users/{user_id}', user_controller)
app.add_route('/books/{book_id}', books_controller)
app.add_route('/notes/{entity_id}', NoteRetrieveView())
app.add_route('/notes/', NoteListCreateView())
app.add_route('/issues/', IssueListCreateView())
app.add_route('/issues/{entity_id}', IssueRetrieveView())
app.add_route('/sorted-issues/', SortedIssue())
app.add_route('/status/{status}', TackNumberFour())
app.add_route('/filters/', FilterBaseView())
app.add_route('/login/', AuthLogin())

if __name__ == '__main__':
    with make_server(host="127.0.0.1", port=8003, app=app) as httpd:
        httpd.serve_forever()
