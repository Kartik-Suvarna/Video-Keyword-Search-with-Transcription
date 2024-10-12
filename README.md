# Video Keyword Search with Transcription

This script processes video files by extracting their audio, transcribing the speech to text, and searching for a user-specified keyword within the transcription. If the keyword is found, the corresponding video is moved to a destination folder. It also supports resetting all videos back to the source folder without reprocessing.

## Table of Contents
- [Installation](#installation)
- [How It Works](#how-it-works)
- [Features](#features)
- [Command Line Usage](#command-line-usage)
- [Folder Structure](#folder-structure)
- [Code Workflow](#code-workflow)
- [Troubleshooting](#troubleshooting)

## Installation

### Prerequisites
- Python 3.x
- The following Python libraries must be installed:
  - `moviepy`
  - `speech_recognition`
  - `pydub` (optional, required for advanced audio manipulation)

### Installing Dependencies
To install the required libraries, run the following command:

```bash
pip install moviepy SpeechRecognition pydub
```

## How It Works

The script performs the following tasks:

1. **Audio Extraction**: For each `.mp4` video in the source folder (`videos`), the audio is extracted as a `.wav` file using `moviepy`.
2. **Transcription**: The extracted audio is transcribed to text using Google's Speech Recognition API (`speech_recognition` library).
3. **Keyword Search**: The user is prompted to enter a keyword. The transcription is then searched for the keyword.
4. **Move Videos**: If the keyword is found in the transcription, the video is moved from the source folder (`videos`) to the destination folder (`dest`).
5. **Reset Functionality**: The script can also reset all videos back to the source folder without reprocessing them.
6. **Handling Large Audio Files**: The audio files are processed in smaller chunks to prevent overloading the transcription service, ensuring full transcription even for long videos.

## Features

- **Audio Extraction**: Converts video files to audio for transcription.
- **Dynamic Audio Chunking**: Processes long audio files in manageable chunks to avoid service limitations.
- **Transcription Caching**: If a transcription already exists for a video, it will be reused rather than re-transcribed.
- **Keyword Prompt**: You can enter a different keyword for each script run.
- **Reset Option**: Moves all videos back to the source folder when the `--reset` flag is used, without asking for a keyword.
- **Error Handling**: Handles common errors such as request limits or unknown speech in chunks.

## Command Line Usage

### Run the Script

To run the script and perform the full process (audio extraction, transcription, keyword search), simply use:
```bash
python your_script.py
```

You will be prompted to enter a keyword to search for within the transcriptions:
```bash 
You will be prompted to enter a keyword to search for within the transcriptions:
```
The script will then:

- Extract audio from each video.
- Transcribe the audio to text.
- Search for the keyword in the transcription.
- Move videos that contain the keyword to the `dest` folder.

### Reset Videos to the Source Folder

To reset and move all videos back from the `dest` folder to the `videos` folder, use the `--reset` flag:
```bash
python your_script.py --reset
```

This will move all videos from `dest` back to `videos` without performing any transcription or keyword search.

## Folder Structure

The following folder structure is expected:

project_root/
│
├── videos/              # Source folder containing all the video files (.mp4)
│   ├── video1.mp4      # Sample video for testing purposes
│   ├── video2.mp4      # Sample video for testing purposes
│   └── ...              # Additional sample videos can be added here
│
├── dest/                # Destination folder for videos where keyword is found
│   └── (empty initially)
│
├── transcriptions/      # Folder for storing transcriptions (.txt)
│   └── (generated automatically)
│
└── your_script.py       # The Python script (this script)

The script will create the `transcriptions` folder if it does not already exist.

**Note**: Sample videos have been added to the `videos` folder for testing purposes. These videos are intended to demonstrate the functionality of the script and can be modified or replaced with your own video files.

## Code Workflow

1. **Initialization**: The script ensures the `videos`, `dest`, and `transcriptions` folders exist.
2. **Audio Extraction**: For each `.mp4` file in the `videos` folder, the script extracts the audio track and saves it as a `.wav` file.
3. **Transcription**:
    - The audio is split into chunks (default max chunk size is 60 seconds) to avoid overloading the transcription service.
    - Each chunk is sent to Google's Speech Recognition API for transcription.
    - If transcription fails for a chunk (e.g., poor audio quality), the chunk is skipped.
4. **Keyword Search**:
    - The script prompts the user for a keyword.
    - The keyword is searched within the transcription for each video.
    - If the keyword is found, the video is moved to the `dest` folder.
5. **Reset Option**: If the `--reset` flag is passed, all videos are moved from `dest` back to the `videos` folder without performing transcription or keyword search.

## Troubleshooting

### Transcription Service Errors

If you see errors related to transcription:

- Ensure you have a stable internet connection.
- Check if the audio quality is good enough for speech recognition.
- Reduce the chunk size if the videos are long to avoid timeouts.

### Missing `videos` or `dest` Folder

Ensure that both the `videos` and `dest` folders exist in your project directory. The script will create the `transcriptions` folder automatically if it does not exist.
