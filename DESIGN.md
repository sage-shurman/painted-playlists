# Project Design Overview

## Overview

This project is a web application that imports playlists from Spotify and allows users to add photos to their playlists in an instagram-like feed. It is built using Django, a high-level Python web framework. (It includes lots of logging for debugging purposes.)

## Key Features

- **Spotify Integration**: Connect Spotify account via OAuth, import selected playlists.
- **Custom Song Art**: Upload custom images for each song
- **Visual Dashboard**: Instagram-like grid displaying playlists and songs

## User Interface (UI) Design

- **Dashboard**: Displays user's playlists in a grid layout.
- **Playlist Detail**: Shows all songs with custom images and options to edit.
- **Authentication Pages**: Login, registration, and Spotify OAuth flow.

Tailwind CSS is used for a modern, responsive, and consistent design.

## API Endpoints

### Authentication
- `POST /register/` - Register a new user.
- `POST /login/` - User login.
- `POST /logout/` - User logout.

### Spotify Integration
- `GET /spotify/login/` - Initiate Spotify OAuth.
- `GET /spotify/callback/` - Handle Spotify OAuth callback.
- `POST /spotify/import-playlist/` - Import a Spotify playlist.

### Playlists
- `GET /playlists/` - List user's playlists.
- `POST /playlists/` - Create a new playlist.
- `GET /playlists/<playlist_id>/` - View playlist details.
- `PUT /playlists/<playlist_id>/` - Update playlist.
- `DELETE /playlists/<playlist_id>/` - Delete playlist.

### Songs
- `POST /playlists/<playlist_id>/songs/` - Add a song to a playlist.
- `PUT /playlists/<playlist_id>/songs/<song_id>/` - Update song details or image.
- `DELETE /playlists/<playlist_id>/songs/<song_id>/` - Remove a song from a playlist.

## Security Considerations

- **Secure Storage**: Use environment variables for sensitive data.
- **Input Validation**: Sanitize all user inputs.
- **Authentication**: Use Django’s built-in authentication system.
- **Access Control**: Ensure users can only access and modify their own data.

## Future Enhancements

- **Individualized Spotify**: Allow user's to access their own Spotify account with a distinctive User model.
- **Collaborative Playlists**: Allow multiple users to contribute to a single playlist.
- **Advanced Analytics**: Provide insights into listening habits and playlist performance.
- **Social Sharing**: Enable sharing playlists on social media.
- **Mobile Applications**: Develop native mobile apps for iOS and Android.
- **Additional Music Services**: Integrate with other platforms like Apple Music or YouTube Music.

## Tools and Technologies

- **Django**: For rapid development of secure and maintainable websites.
- **Tailwind CSS**: For creating custom designs.
- **Spotipy**: For the Spotify Web API.
- **SQLite**: For a lightweight disk-based database.

## Data Model

The data model consists of three main entities: `User`, `Playlist`, and `Song`. The `User` entity is provided by Django's built-in authentication system. Each `Playlist` is associated with a `User`, and each `Song` is associated with a `Playlist`.

This project currently works for one user.

    User {
        int id
        string username
        string password
        string email
    }
    Playlist {
        int id
        string title
        string description
        datetime created_at
    }
    Song {
        int id
        string title
        string spotify_track_id
        string photo
        datetime added_at
    }
    SpotifyToken {
        int id
        string access_token
        string refresh_token
        string token_type
        int expires_in
        string scope
        datetime created_at
    }
    User ||--o{ Playlist : owns
    Playlist ||--o{ Song : contains
    User ||--o| SpotifyToken : has
```

This diagram illustrates the relationships between the entities in the data model. Each user can have multiple playlists, each playlist can contain multiple songs, and each user can have one Spotify token for authentication.
