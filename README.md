# GDSE Discord Bot

This repository contains the code for a Discord bot that provides various functionalities including reminders, polls, and music playback. The bot also integrates with the Gemini API to generate responses to user messages.

## Files

### `DISCORD BOT.py`

This is the main file for the Discord bot. It includes the setup, event handlers, and commands for the bot.

#### Key Components

- **Imports and Setup**
  - Imports necessary libraries and modules.
  - Loads environment variables from a `.env` file.
  - Sets up the bot with specific intents.

- **Global Variables**
  - `reminders`: Dictionary to track reminders.
  - `yt_dl_options`, `ytdl`, `ffmpeg_options`: Configuration for YouTube downloader and FFmpeg.
  - `voice_clients`: Dictionary to track voice clients.

- **Bot Events**
  - `on_ready`: Triggered when the bot is ready.
  - `on_member_join`: Welcomes new members.
  - `on_member_remove`: Notifies when a member leaves.

- **Commands**
  - `poll`: Creates a poll with up to 10 options.
  - `remind`: Sets a reminder for a specified date and time.
  - `cancel_reminder`: Cancels an active reminder.
  - `join`: Joins the voice channel the user is in.
  - `leave`: Leaves the voice channel.
  - `play`: Plays a song from a YouTube URL.
  - `pause`: Pauses the currently playing song.
  - `resume`: Resumes the paused song.
  - `stop`: Stops the song and leaves the voice channel.
  - `clearall`: Clears all messages in the channel.

- **On Message Event**
  - Handles incoming messages and processes commands.
  - Generates responses using the `get_response` function from `responce.py`.
  - For private chat with bot use '?'.

### `responce.py`

This file contains the function to generate responses using the Gemini API.

#### Key Components

- **Imports and Setup**
  - Imports necessary libraries and modules.
  - Loads environment variables from a `.env` file.
  - Configures the Gemini API with the provided API key.

- **Functions**
  - `get_response`: Generates a response based on user input using the Gemini API.
