import src.api
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/")
def index():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
        # links is now a list of url, endpoint tuples

    return render_template('all_links.html', links=links)


@app.route('/authorize/spotify')
def spotify_login():
    spotify = src.api.Spotify()
    return redirect(spotify.authorize())


@app.route('/authorize/spotify/return')
def spotify_authorize():
    spotify = src.api.Spotify()
    code = request.args.get('code')
    if code:
        spotify.login(code)

    return 'hello'


@app.route('/query')
def query():
    spotify = src.api.Spotify()
    code = request.args.get('code')
    if code:
        spotify.login(code)
    return 'hello'


@app.route('/user/')
def profile(username):
    return 'Hello Tutorialspoint'


with app.test_request_context():
    print(url_for('index'))
    print(url_for('index', _external=True))
    print(url_for('spotify_login'))
    print(url_for('spotify_login', next='/'))
    print(url_for('profile', username='Tutorials Point'))

if __name__ == '__main__':
    app.run()
