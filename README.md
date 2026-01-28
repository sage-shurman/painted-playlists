# Playlist Photo App

This project is a web application that allows users to import playlists from Spotify and add custom photos to their playlists in an Instagram-like feed. It is built using Django, a high-level Python web framework. Currently, users can choose any playlist from my Spotify account and make a photo gallery with it. A future iteration of this would let users upload playlists from their own Spotify accounts.

## Video Demo
https://youtube.com/shorts/2qDNZ63MvUQ

## Features

- **Spotify Integration**: Connect your Spotify account via OAuth and import selected playlists.
- **Custom Song Art**: Upload custom images for each song.
- **Visual Dashboard**: View your playlists and songs in a visually appealing grid layout.

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory and add your Spotify API credentials and other necessary environment variables.

5. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

## Usage

- **Register/Login**: Create an account or log in to access your dashboard.
- **Import Playlists**: Connect your Spotify account and import playlists.
- **Add Photos**: Upload custom images for your songs.

# painted-playlists
