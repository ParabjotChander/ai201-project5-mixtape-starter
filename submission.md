# Project 4 MixTape Bug Hunt

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

Model Layer: The user's instance model (primary entity table) is updated, the listening_streak property is changed.

### /routes/songs.py
Users can search for a song using it's id, rate a song, get song details, and listen to a song.

#### Data Flow:
User rates a song

POST /songs/<id>/rate

Route Layer: rate(song_id) => wired function that gets called.

Service Layer: notify_song_rated() => Save a user's rating for a song.

Model Layer: The rating is stored or updated directly on the song's instance model (primary entity table).

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

Service Layer: get_friends_listening_now(user_id) => Return a list of friends who have listened to something recently, along with the song they were listening to. Returns a list of dicts, each with 'friend', 'song', and 'listened_at' keys, ordered by most recent first.

Model Layer: The user's instance is retrieved using the user_id provided as input. Listening_Events tuples are retrieved using filtering (to retrieve the user's friends by friend_id and listened_at column >= cutoff date, so the songs are recently listerned to).

## Root Cause Analysis

### Issue number and title: Bug #5 The last song in a playlist never shows up

### How you reproduced it 
<!-- What steps did you take to confirm the bug exists before touching any code? What inputs, sequence of actions, or data condition triggered the behavior? 
-->
I choose a random playlist id from the playlist table in mixtape.db, saved the id and looked at playlist_entries table where that id appeared 7 times. So that playlist had 7 entries or songs. So I entered the command below where the playlist id is the input.

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
I went to the routes folder, playlists.py caught my eye. In the route file, I followed the get_songs(playlist_id). This wired function calls get_playlist_songs(playlist_id) in the service folder to playlist_service.py. In the service function, I saw whats returned is a list of dicts in representing the songs, but for loop stops iterating at the last element (excluding it). I knew that was the error.

I recognized out the count returned is 6, but the actual number of songs in the playlist is 7.

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
I changed the for loop to where all elements are iterated through, it fixes the root cause because every song dict will be returned, all songs will be displayed for a playlist. I tested my fix by using the pytests provided.

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

### Issue number and title

### How you reproduced it 
<!-- What steps did you take to confirm the bug exists before touching any code? What inputs, sequence of actions, or data condition triggered the behavior? 
-->
### How you found the root cause 
<!--— Which files did you look at? What was your navigation path? What moment made you confident you'd found the right place — not just a suspicious area, but the specific cause?
-->

### The root cause 
<!-- — In plain English, explain exactly what was wrong. Not "there was a bug in the streak logic" — explain the specific condition, comparison, or missing step that caused the problem.
-->
### Your fix and side-effect check 
<!--
— What did you change and why does that change fix the root cause? What related functionality did you check afterward to confirm you didn't break anything? 
-->

### Issue number and title

### How you reproduced it 
<!-- What steps did you take to confirm the bug exists before touching any code? What inputs, sequence of actions, or data condition triggered the behavior? 
-->
### How you found the root cause 
<!--— Which files did you look at? What was your navigation path? What moment made you confident you'd found the right place — not just a suspicious area, but the specific cause?
-->

### The root cause 
<!-- — In plain English, explain exactly what was wrong. Not "there was a bug in the streak logic" — explain the specific condition, comparison, or missing step that caused the problem.
-->
### Your fix and side-effect check 
<!--
— What did you change and why does that change fix the root cause? What related functionality did you check afterward to confirm you didn't break anything? 
-->

## AI Usage

