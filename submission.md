# Project 4 MixTape Bug Hunt

## AI Usage 
<!-- 
how you used AI tools during codebase navigation and debugging, what they helped you understand, and where you verified or overrode their output
-->
**Instance 1** Explanation of Database Tables in Models.py (Milestone 1 & 2)

- *What I gave the AI:*
I am going to give you a models.py file, SQLAlchemy models for all entities. Please describe each table, including each table's columns and primary or foreign keys. Attached Models.py file.

- *What it produced:*

```
Here is a comprehensive breakdown of the SQLAlchemy models defined in your `models.py` file, detailing each table, its columns, and its keys.
---
## 1. Primary Entity Tables

### `user` (User Model)

Represents the users of the Mixtape application.

* **Columns:**
* `id` (String 36): **Primary Key**. Auto-generated UUID.
* `username` (String 64): Unique name for the user, cannot be empty.
* `email` (String 120): Unique email address, cannot be empty.
* `listening_streak` (Integer): Current daily streak, defaults to 0.
* `last_listened_at` (DateTime): Timestamp of when they last played music.
* `created_at` (DateTime): The account creation timestamp.

### `song` (Song Model)

Tracks songs shared within the platform.

* **Columns:**
* `id` (String 36): **Primary Key**. Auto-generated UUID.
* `title` (String 200): Song title, cannot be empty.
* `artist` (String 200): Artist name, cannot be empty.
* `album` (String 200): Album name (optional).
* `genre` (String 100): Genre name (optional).
* `shared_by` (String 36): **Foreign Key** referencing `user.id`. Identifies who shared it.
* `shared_at` (DateTime): Timestamp of when it was shared.
* `share_note` (Text): A message/caption left by the user who shared it.

### `playlist` (Playlist Model)

Represents a collection of songs grouped together.

* **Columns:**
* `id` (String 36): **Primary Key**. Auto-generated UUID.
* `name` (String 200): Playlist title, cannot be empty.
* `created_by` (String 36): **Foreign Key** referencing `user.id`. The creator.
* `created_at` (DateTime): Timestamp of when it was made.
* `is_collaborative` (Boolean): Flag indicating if other users can add songs, defaults to `True`.

### `tag` (Tag Model)

Metadata labels that can be applied to songs (e.g., "Chill", "90s").

* **Columns:**
* `id` (String 36): **Primary Key**. Auto-generated UUID.
* `name` (String 64): Unique name of the tag, cannot be empty.

---

## 2. Activity & Engagement Tables

### `listening_event` (ListeningEvent Model)

Tracks user listening history.

* **Columns:**
* `id` (String 36): **Primary Key**. Auto-generated UUID.
* `user_id` (String 36): **Foreign Key** referencing `user.id`. The listener.
* `song_id` (String 36): **Foreign Key** referencing `song.id`. The played song.
* `listened_at` (DateTime): Timestamp of the playback.

### `rating` (Rating Model)

Stores numerical ratings (1–5) given to songs by users.

* **Columns:**
* `id` (String 36): **Primary Key**. Auto-generated UUID.
* `user_id` (String 36): **Foreign Key** referencing `user.id`.
* `song_id` (String 36): **Foreign Key** referencing `song.id`.
* `score` (Integer): Rating value (1 to 5).
* `rated_at` (DateTime): Timestamp of the rating.

* **Constraints:**
* `unique_user_song_rating`: A unique constraint preventing the same user from rating the exact same song multiple times.

### `notification` (Notification Model)

Alerts sent to users about activities.

* **Columns:**
* `id` (String 36): **Primary Key**. Auto-generated UUID.
* `user_id` (String 36): **Foreign Key** referencing `user.id`. The recipient.
* `notification_type` (String 64): Category of the notification.
* `body` (Text): The alert message.
* `created_at` (DateTime): Timestamp of when it was triggered.
* `read` (Boolean): Tracks if the user has viewed it, defaults to `False`.

---

## 3. Association / Junction Tables

These tables establish many-to-many relationships between the main entities.

### `friendships`

A self-referencing relationship mapping symmetric connections between users.

* **Columns:**
* `user_id` (String 36): **Composite Primary Key** & **Foreign Key** referencing `user.id`.
* `friend_id` (String 36): **Composite Primary Key** & **Foreign Key** referencing `user.id`.

### `song_tags`

Maps the tags that have been assigned to songs.

* **Columns:**
* `song_id` (String 36): **Composite Primary Key** & **Foreign Key** referencing `song.id`.
* `tag_id` (String 36): **Composite Primary Key** & **Foreign Key** referencing `tag.id`.

### `playlist_entries`

A rich junction table linking songs to playlists. Unlike standard join tables, this one tracks extra metadata about the pairing.

* **Columns:**
* `playlist_id` (String 36): **Composite Primary Key** & **Foreign Key** referencing `playlist.id`.
* `song_id` (String 36): **Composite Primary Key** & **Foreign Key** referencing `song.id`.
* `position` (Integer): The order track number of the song within the playlist.
* `added_by` (String 36): **Foreign Key** referencing `user.id`. Tracks who added that specific song.
* `added_at` (DateTime): Timestamp of when the song was added to the playlist.
```

- *What I changed or overrode:*
I didn't change or overrode anything intially, this was my guide to write out the codebase map for milestone 1. This helped me understand the database schemas and tables, sketched them out in my notes. This utimately helped me find bug # 3, the song appearing twice. The songs can appear as duplicates because the function uses an .outerjoin() on the song_tags table, the many to many junction table relationship causes the duplicates,

**Instance 2** Explanation of Python Method .weekday() method in streak_services.py (Milestone 2 & 3)

- *What I gave the AI:*
Can you explain what the Python .weekday() method returns and what does it returning 6 mean?

- *What it produced:*
```
The Python .weekday() method belongs to the datetime module's date and datetime objects. Its entire job is to look at a specific calendar date and tell you what day of the week it falls on.Instead of returning a word like "Monday" or "Sunday," it returns an integer between 0 and 6.🔢 The Day Mapping ScalePython uses a zero-indexed tracking system for the days of the week, starting precisely on Monday:Integer Returned Day of the Week 0 Monday 1 Tuesday 2 Wednesday 3 Thursday 4 Friday 5 Saturday 6 Sunday☀️ What does returning 6 mean?If the .weekday() method returns 6, it means the date you evaluated is a Sunday.💻 Quick Code ExampleHere is how it looks in action if you were to check a date:Pythonfrom datetime import date

# Let's check July 5, 2026
my_date = date(2026, 7, 5)

print(my_date.weekday())  
# Output: 6 (which tells us July 5, 2026 is a Sunday)
💡 Quick Tip: If you ever prefer the numbers to match a standard calendar where Sunday is 0 and Saturday is 6, Python offers an alternative method called .isoweekday(). However, .isoweekday() shifts the scale from 1 (Monday) to 7 (Sunday). Stick to .weekday() if you want a clean 0–6 index starting on Monday!
```
- *What I changed or overrode:*
This explanation helped me find the Bug # 1, 6 meant Sunday was the day of the week. I knew the condition today.weekday() != 6 was not needed in the condtional statement. The listening streak wouldn't increment on Sundays. For my bug fix, I removed the condition, conducted streak service pytests and passed them to verify the fix worked.

## CodeBase Map

### app.py
The entry point. This is where the Flask app is initialized, config is loaded, blueprints from routes/ are registered: /songs, /playlists, /users, and /feed. The database (models.py) is linked.

#### Data Flow:
User wants to get a playlist of songs 
 
GET '/<playlist_id>/songs'

Route Layer: get_songs(playlist_id) => wired function that gets called for that route

Service Layer: get_playlist_songs(playlist_id) => returns a list of dicts, each dict represents a song, and its properties 

Model Layer: the songs are queried and ordered by their position in the playlist

### models.py
Creates Primary Entity Tables: user, song, playlist, tag

Creates Activity & Engagement Tables: listening_event, rating, notification

Creates Association/Junction Tables(many to many relationships): friendships, song_tags, playlist_entries

#### Data Flow:
User listens to a song
 
POST '/<song_id>/listen'

Route Layer: listen(song_id) => wired function that gets called

Service Layer: 

record_listening_event(user_id, song_id) => Record that a user listened to a song using the Listening Event Object and update their streak(update_listening_streak(user, now) method called). Listening Event Object returned

update_listening_streak(user,now) => Update a user's listening streak based on their last listening date. Doesn't return anything

Model Layer: The user's instance model (primary entity table) is updated, the listening_streak is changed.

### /routes/songs.py
Users can search for a song using it's id, rate a song, get song details, and listen to a song.

#### Data Flow:
User rates a song

POST /songs/<song_id>/rate

Route Layer: rate(song_id) => wired function that gets called.

Service Layer: notify_song_rated() => Save a user's rating for a song.

Model Layer: The rating is stored directly on the rating's model (activity & engagement table).

### /routes/playlists.py
User has the ability to create a playlist, retrieve a playlist's metadata, get the songs of a playlist, and add songs to a playlist. 

#### Data Flow:
User creates a playlist

POST /

Route Layer: create() => wired function that gets called.

Service Layer: create_playlist(name, created_by, is_collaborative) => Create a new playlist.

Model Layer: A new playlist instance is created and returned from the service function described above.

### /routes/users.py
User's general data (instance data), listening_streak, and notifications can be retrieved. Can mark a notification as read.

#### Data Flow:
Want to retrieve a user's listening streak.

GET /<user_id>/streak

Route Layer: streak(user_id) => wired function that gets called

Service Layer: get_streak(user_id) => Get the current listening streak for a user.

Model Layer: retrieving the user's instance, which contains the listening streak column

### /routes/feed.py
Users can see what songs their friends are listening to and get a general activity feed of recent listening events from all friends.

### Data Flow:
The user can see what songs his or her friends are listening to.

GET /<user_id>/listening-now

Route Layer:  listening_now(user_id) => wired function that gets called

Service Layer: get_friends_listening_now(user_id) => Return a list of friends who have listened to something recently and the song they were listening to. Returns a list of dicts, each with 'friend', 'song', and 'listened_at' keys, ordered by most recent first.

Model Layer: The user's instance is retrieved using the user_id, provided as input. Listening_Events tuples are retrieved using filtering (to retrieve the user's friends by friend_id and listened_at column >= cutoff date condition, so the songs are recently listerned to).

## Root Cause Analysis

### Issue number and title: Bug #5 The Last Song in a Playlist Never Shows Up

### How you reproduced it 
<!-- What steps did you take to confirm the bug exists before touching any code? What inputs, sequence of actions, or data condition triggered the behavior? 
-->
I choose a random playlist id from the playlist table in mixtape.db, saved the id and looked at playlist_entries table where that id appeared 7 times. So that playlist had 7 entries or songs. So I entered the command below with the playlist id is the input.

CLI Command
```
curl http://127.0.0.1:5000/playlists/9beddee5-13c4-4bfe-872b-4a12b06bb3c9/songs
```

Output:
```
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
```

### How you found the root cause 
<!--— Which files did you look at? What was your navigation path? What moment made you confident you'd found the right place — not just a suspicious area, but the specific cause?
-->
GET /<playlist_id>/songs

Route Layer /routes/playlists.py: get_songs(playlist_id) => route wired method

Service Layer /services/playlist_service.py: get_playlist_songs(playlist_id) => returns all songs in the playlist

I went to the routes folder, playlists.py caught my eye. In the route file, I followed the get_songs(playlist_id). This wired function calls get_playlist_songs(playlist_id) in the service folder to playlist_service.py. In the service function, I saw whats returned is a list of dicts in representing the songs, but for loop stops iterating at the last element (excluding it). I knew that was the error.

I recognized out the count returned is 6, but the actual number of songs in the playlist are 7.

### The root cause 
<!-- — In plain English, explain exactly what was wrong. Not "there was a bug in the streak logic" — explain the specific condition, comparison, or missing step that caused the problem.
-->
Not all the songs are being iterated through, the last element is being excluded, this is a display bug.

### Your fix and side-effect check 
<!--
— What did you change and why does that change fix the root cause? What related functionality did you check afterward to confirm you didn't break anything? 
-->
Fix:  
```
return [song.to_dict() for song in songs]
```
I changed the for loop to where all elements are iterated through, it fixes the root cause because every song dict will be returned, all songs will be displayed for a playlist. I tested for the side-effect check by using the pytests provided.

CLI Command
```
pytest tests/test_playlists.py
```

Output:
```
collected 3 items                                                                                                       
tests/test_playlists.py ...                      [100%]

==================3 passed in 0.89s ===================================================
```

### Issue number and title: Bug #3 The Same Song Keeps Showing Up Twice in Search

### How you reproduced it 
<!-- What steps did you take to confirm the bug exists before touching any code? What inputs, sequence of actions, or data condition triggered the behavior? 
-->
I choose a random song name from the song table in mixtape.db, saved the name. So I entered the command below where part of the "Harlem Renaissance" song name is the input. Got CLI errors when using spacing for a query parameter.

CLI Command
```
curl 'http://localhost:5000/songs/search?q=Harlem'
```

Output:
```
{
"count":3,
"results": [
    {"album":null,"artist":"Uptown Collective","genre":"hip-hop","id":"7f543c35-f871-4214-9d19-a220df1a8518","share_note":null,"shared_at":"2026-06-30T18:34:53.378402","shared_by":"efb43ec2-2656-4b8a-ad65-1609d5170319","tags":["rap","hip-hop","soul"],"title":"Harlem Renaissance"},
    {"album":null,"artist":"Uptown Collective","genre":"hip-hop","id":"7f543c35-f871-4214-9d19-a220df1a8518","share_note":null,"shared_at":"2026-06-30T18:34:53.378402","shared_by":"efb43ec2-2656-4b8a-ad65-1609d5170319","tags":["rap","hip-hop","soul"],"title":"Harlem Renaissance"},
    {"album":null,"artist":"Uptown Collective","genre":"hip-hop","id":"7f543c35-f871-4214-9d19-a220df1a8518","share_note":null,"shared_at":"2026-06-30T18:34:53.378402","shared_by":"efb43ec2-2656-4b8a-ad65-1609d5170319","tags":["rap","hip-hop","soul"],"title":"Harlem Renaissance"},
    ]
}
```

### How you found the root cause 
<!--— Which files did you look at? What was your navigation path? What moment made you confident you'd found the right place — not just a suspicious area, but the specific cause?
-->

GET /search?q=Harlem

Route Layer /routes/songs.py: search() => route wired method

Service Layer /services/streak_service.py: search_songs(query) => Search for songs by title or artist name

The song named "Harlem Renaissance" has 3 tags (e.g., "rap", "hip-hop", "soul"), the database returns 3 rows for that same song. Therefore, we get three identical song database objects. The pattern is the number of duplicate song titles = the # of tags for that song. The reason for this is because of the outer join on song (Primary Entity Table) and song_tags (Association / Junction Table) creates many to many relationships

### The root cause 
<!-- — In plain English, explain exactly what was wrong. Not "there was a bug in the streak logic" — explain the specific condition, comparison, or missing step that caused the problem.
-->
The underlying SQL query creates a new row for every combination of a song and a tag, duplicates are created this way. 

### Your fix and side-effect check 
<!--
— What did you change and why does that change fix the root cause? What related functionality did you check afterward to confirm you didn't break anything? 
-->
Fix: 
```
results = (
        db.session.query(Song)
        .outerjoin(song_tags, Song.id == song_tags.c.song_id)
        .filter(
            db.or_(
                Song.title.ilike(f"%{query}%"),
                Song.artist.ilike(f"%{query}%"),
            )
        )
        .distinct()
        .all()
)
```

I added the distinct() method after the filtering, SQLAlchemy tells the underlying database engine to remove duplicate rows from the final SQL query results before returning them to Python. This is the exact fix needed to overcome the duplication side-effect caused by the .outerjoin(). I tested for the side-effect check by using the pytests provided.

CLI Command 

```
pytest tests/test_search.py
```

Output:

```
collected 5 items                                                                                              
tests/test_search py .....                                                                                       [100%]

======= 5 passed in 0.44s ===================================================
```

### Issue number and title: Bug # 1 The Listening Streak Keeps On Resetting

### How you reproduced it 
<!-- What steps did you take to confirm the bug exists before touching any code? What inputs, sequence of actions, or data condition triggered the behavior? 
-->

To reproduce the bug you had to create a situtation where a user has a listening streak active on Saturday that is more than one day, and the user has to listen to a song on Sunday. On Sunday, the listening streak, instaed of increasing by 1 (when user listens to a song on that day), resets back to 1. The current data provided didn't have a situation like this and I couldn't add data since the POST /<song_id>/listen route will use the current date, not a date you can customize. I created a debug python script where the user has a active listening streak and approaches Sunday, and the listening streak resets to 1. As input, I choose July 5, 2026 to simulate Sunday, created a User object from models.py, had the listening_streak to 7 on July 4, 2026 (Saturday).

CLI Command
```
python3 debug_streak.py
```

Output
```
BEFORE Sunday (Saturday): Listening Streak: 7
Simulating Sunday with last listened on Saturday
Listening During Sunday, Listening Streak: 1
```

### How you found the root cause 
<!--— Which files did you look at? What was your navigation path? What moment made you confident you'd found the right place — not just a suspicious area, but the specific cause?
-->

POST /<song_id>/listetn route

Route Layer /routes/songs.py: def listen(song_id) => wired function for that route  

Service Layer /services/streak_service.py: record_listening_event(user_id, song_id) => update_listening_streak(user, now)

Model Layer: A new Listening Event instance is created, and stored in the DB, listening streak column is updated in the User's instance

I read the record_listening_event service method, update_listening_streak is called inside it. I moved on to that function and found this condition today.weekday() != 6. I used a AI tool to find what .weekday() method returns and what a return value of 6 means. I learned the method returns the day of the week as a integer, Monday = 0, and Sunday = 6. So I figured out that the streak doesn't increment on Sunday, the condition to increment the listening streak becomes false and the code falls to the else block, resetting the streak to 1.

### The root cause 
<!-- — In plain English, explain exactly what was wrong. Not "there was a bug in the streak logic" — explain the specific condition, comparison, or missing step that caused the problem.
-->
The streak only increments if today is not Sunday. If today is Sunday, even if the user listened yesterday (Saturday), the steak doesn't increase by 1 but resets to 1.

### Your fix and side-effect check 
<!--
— What did you change and why does that change fix the root cause? What related functionality did you check afterward to confirm you didn't break anything? 
-->
Fix:

```
    if days_since_last == 0:
        # Already updated today — no change needed
        return
    elif days_since_last == 1:
        user.listening_streak += 1
    else:
        user.listening_streak = 1
```

I just removed the condition in the else if clause that checks whether the date is not equal to Sunday. This fixes the root cause now because when a user is listening to a song on Sunday with a active listening streak, the else if clause will be ran, incrementing the streak, not resetting it. The else won't be ran. I tested for the side-effect check by using the pytests provided.

CLI Command 

```
pytest tests/test_streaks.py
```

Output:

```
collected 5 items                                                                                                       

tests/test_streaks.py .....                                                                                       [100%]

=================================================== 5 passed in 0.42s ===================================================
```






