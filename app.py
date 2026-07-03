"""
app.py — Mixtape

Flask application factory and database setup.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


def create_app(config=None):
    app = Flask(__name__)

    # Default configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///mixtape.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")

    if config:
        app.config.update(config)

    db.init_app(app)

    # Register blueprints
    from routes.songs import songs_bp
    from routes.playlists import playlists_bp
    from routes.users import users_bp
    from routes.feed import feed_bp

    app.register_blueprint(songs_bp, url_prefix="/songs")
    app.register_blueprint(playlists_bp, url_prefix="/playlists")
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(feed_bp, url_prefix="/feed")

    @app.route("/")
    def index():
        return "Mixtape API is running!", 200

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)


"""
Reproducing Bugs CLI Commands

Bug # 5 Bug Description: When fetching songs from a playlist.
Command to reproduce the bug: curl http://127.0.0.1:5000/playlists/9beddee5-13c4-4bfe-872b-4a12b06bb3c9/songs

Output:
{"count": 6,
"songs":[
    {"album":null,"artist":"The Wanderers","genre":"indie rock","id":"9292e63a-0437-40f5-b4d4-037bf69c90e6","share_note":null,"shared_at":"2026-06-26T18:34:53.378402","shared_by":"48d75cf1-bae3-4968-91e5-aa1a49b30375","tags":[],"title":"Midnight Drive"},
    {"album":null,"artist":"Elara Moon","genre":"ambient","id":"2b29bb8a-3959-41c0-94a4-df5d9987e6d9","share_note":null,"shared_at":"2026-06-26T18:34:53.378402","shared_by":"48d75cf1-bae3-4968-91e5-aa1a49b30375","tags":[],"title":"Still Waters"},
    {"album":null,"artist":"Coastal Highway","genre":"indie","id":"999cc5ff-cdb6-4cc4-8ae9-3f1eaba4b64f","share_note":null,"shared_at":"2026-06-26T18:34:53.378402","shared_by":"48d75cf1-bae3-4968-91e5-aa1a49b30375","tags":[],"title":"First Light"},
    {"album":null,"artist":"Street Collective","genre":"hip-hop","id":"2fe059f9-e700-418e-b06f-11cb29c292be","share_note":null,"shared_at":"2026-06-28T18:34:53.378402","shared_by":"eaaaf239-af73-4ba3-af57-640d879e3810","tags":["hip-hop"],"title":"Block Party"},
    {"album":null,"artist":"Nova Blix","genre":"lo-fi","id":"178e4d69-22f2-4b89-a991-1a1befeb4411","share_note":null,"shared_at":"2026-06-28T18:34:53.378402","shared_by":"eaaaf239-af73-4ba3-af57-640d879e3810","tags":["lo-fi"],"title":"Late Night Session"},
    {"album":null,"artist":"Solange K","genre":"r&b","id":"ed27d61d-63ad-4a05-b391-fbb16f316359","share_note":null,"shared_at":"2026-06-28T18:34:53.378402","shared_by":"eaaaf239-af73-4ba3-af57-640d879e3810","tags":["r&b"],"title":"Golden Hour"}
       ]
}

Error: The count returned is 6, but the actual number of songs in the playlist is 7.

Bug # 3 The same song keeps showing up twice in the search
Command to reproduce the bug: curl 'http://localhost:5000/songs/search?q=Harlem'

Output:
{
"count":3,
"results": [
    {"album":null,"artist":"Uptown Collective","genre":"hip-hop","id":"7f543c35-f871-4214-9d19-a220df1a8518","share_note":null,"shared_at":"2026-06-30T18:34:53.378402","shared_by":"efb43ec2-2656-4b8a-ad65-1609d5170319","tags":["rap","hip-hop","soul"],"title":"Harlem Renaissance"},
    {"album":null,"artist":"Uptown Collective","genre":"hip-hop","id":"7f543c35-f871-4214-9d19-a220df1a8518","share_note":null,"shared_at":"2026-06-30T18:34:53.378402","shared_by":"efb43ec2-2656-4b8a-ad65-1609d5170319","tags":["rap","hip-hop","soul"],"title":"Harlem Renaissance"},
    {"album":null,"artist":"Uptown Collective","genre":"hip-hop","id":"7f543c35-f871-4214-9d19-a220df1a8518","share_note":null,"shared_at":"2026-06-30T18:34:53.378402","shared_by":"efb43ec2-2656-4b8a-ad65-1609d5170319","tags":["rap","hip-hop","soul"],"title":"Harlem Renaissance"},
    ]
}

Error: The song named "Harlem Renaissance" has 3 tags (e.g., "rap", "hip-hop", "soul"), the database returns 3 rows for that single song. Therefore, we get three identical Song database objects.

Bug # 1 The listening streak is not being recorded correctly, keeps resetting on Sunday
Command to reproduce the bug: Run the following script in debug_streak.py:  python3 debug_streak.py

Output:
BEFORE Sunday (Saturday): Listening Streak: 7
Simulating Sunday with last listened on Saturday
Listening During Sunday, Listening Streak: 1
"""
