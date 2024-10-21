# Voice Assistant Script

## Overview
This Python script is a voice-controlled assistant that interacts with users to perform file or folder searches on the system. It uses speech recognition and voice synthesis to provide a hands-free experience, allowing users to search for specific files or folders by simply speaking commands.

## Features

- **Voice Interaction**: The script listens to user commands and provides responses using speech synthesis, offering an interactive, voice-based experience.

- **System Language Detection**: The script detects the system’s default language and adapts the interaction accordingly, allowing multilingual support.

- **File and Folder Search**: The assistant can search for files or folders based on a keyword provided by the user, traversing the file system to locate matches.

- **Confirmation Requests**: Before taking actions, the script confirms the user's intent to ensure accuracy.

- **Search Filters**: Users can filter search results by type (e.g., folder, specific file type) or by modification date, giving them more control over the search process.

- **Error Handling**: The script includes multiple attempts for speech recognition and provides error messages in case of failure or internet connection issues.



## How It Works

- **Initialize the Assistant**: The assistant greets the user and asks if they want to search for a file or folder.

- **Voice Commands**: The user provides voice commands (e.g., "search for a document") which the script processes and converts to text using speech recognition.

- **Search Execution**: Based on the keyword, the assistant searches through the system files and folders, presenting the user with results.

- **Filtering and Confirmation**: The user can further refine the search results by file type or modification date. The assistant confirms any actions before proceeding.

- **Voice Feedback**: The script gives voice feedback throughout the interaction, guiding the user step by step.



## Dependencies
- **speech_recognition**: For converting speech to text.
- **pyttsx3**: For voice synthesis (text-to-speech).
- **locale**: For detecting system language.
- **os**: For traversing the file system.
- **time**, **datetime**: For handling time and date-based operations.

## Installation
To run this script, you'll need to install the required libraries:

```bash
pip install speechrecognition pyttsx3
```

## Usage
Run the script, and the assistant will guide you through voice commands to search for files or folders.
