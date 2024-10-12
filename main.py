import os
import shutil
import sys
import moviepy.editor as mp
import speech_recognition as sr

# Define paths
source_folder = 'videos'
destination_folder = 'dest'
transcription_folder = 'transcriptions'  # Folder to save transcriptions

# Ensure the transcription folder exists
if not os.path.exists(transcription_folder):
    os.makedirs(transcription_folder)

# Function to move all videos from dest back to videos folder
def reset_videos():
    print("Moving all videos from dest back to videos folder...")
    for file_name in os.listdir(destination_folder):
        if file_name.endswith(".mp4"):
            shutil.move(os.path.join(destination_folder, file_name), os.path.join(source_folder, file_name))
            print(f"Moved {file_name} back to {source_folder}")
    print("Reset complete.")

# Function to extract audio from video using moviepy
def extract_audio(video_path, audio_path):
    try:
        print(f"Extracting audio from {video_path}")
        video_clip = mp.VideoFileClip(video_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(audio_path, codec='pcm_s16le')
        audio_clip.close()
        video_clip.close()
        print(f"Audio extracted to {audio_path}")
    except Exception as e:
        print(f"Error extracting audio from {video_path}: {str(e)}")

# Function to transcribe audio using SpeechRecognition with dynamic chunk size
def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    transcription = ""
    
    try:
        with sr.AudioFile(audio_path) as source:
            audio_duration = source.DURATION
            
            # Set maximum chunk size to 60 seconds (this helps avoid API limits)
            chunk_size = 60 if audio_duration > 60 else audio_duration
            
            for start_time in range(0, int(audio_duration), int(chunk_size)):
                print(f"Transcribing from {start_time} to {min(start_time + chunk_size, audio_duration)} seconds...")
                
                # Transcribe the chunk
                try:
                    audio_chunk = recognizer.record(source, offset=start_time, duration=chunk_size)
                    chunk_transcription = recognizer.recognize_google(audio_chunk)
                    transcription += chunk_transcription + " "
                except sr.UnknownValueError:
                    print(f"Unable to transcribe audio chunk from {start_time} to {start_time + chunk_size}. Skipping...")
                except sr.RequestError:
                    print(f"Error with transcription service. Skipping chunk from {start_time} to {start_time + chunk_size}.")
                except Exception as e:
                    print(f"General error during transcription from {start_time} to {start_time + chunk_size}: {str(e)}")
    
    except Exception as e:
        print(f"Error during transcription: {str(e)}")
    
    return transcription

# Function to save transcription to a text file
def save_transcription(file_name, transcription):
    transcription_file = os.path.join(transcription_folder, f"{os.path.splitext(file_name)[0]}.txt")
    with open(transcription_file, 'w') as file:
        file.write(transcription)

# Function to load transcription for a video
def load_transcription(file_name):
    transcription_file = os.path.join(transcription_folder, f"{os.path.splitext(file_name)[0]}.txt")
    if os.path.exists(transcription_file):
        with open(transcription_file, 'r') as file:
            return file.read()
    return None

# Function to search transcriptions for a keyword
def search_transcriptions(keyword):
    print(f"Searching transcriptions for keyword: '{keyword}'")
    for transcription_file in os.listdir(transcription_folder):
        file_path = os.path.join(transcription_folder, transcription_file)
        with open(file_path, 'r') as file:
            transcription = file.read()
            if keyword.lower() in transcription.lower():
                print(f"Keyword '{keyword}' found in {transcription_file}")

# Main logic
if __name__ == "__main__":
    # Check if the "--reset" parameter is passed
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        reset_videos()
        sys.exit(0)  # Exit after reset to prevent further execution

    # Prompt the user for a keyword to search for
    search_keyword = input("Enter the keyword to search for in transcriptions: ")

    # Process all videos in the source folder
    for file_name in os.listdir(source_folder):
        if file_name.endswith(".mp4"):
            video_path = os.path.join(source_folder, file_name)
            audio_path = os.path.join(source_folder, f"{os.path.splitext(file_name)[0]}.wav")
            
            # Check if transcription already exists
            transcription = load_transcription(file_name)
            
            # If transcription doesn't exist, extract audio and transcribe it
            if transcription is None:
                extract_audio(video_path, audio_path)
                transcription = transcribe_audio(audio_path)
                save_transcription(file_name, transcription)
            
            # Check if the user-provided keyword exists in the transcription
            if search_keyword.lower() in transcription.lower():
                # Move the video to the destination folder
                shutil.move(video_path, os.path.join(destination_folder, file_name))
                print(f'Moved {file_name} to {destination_folder}')
            else:
                print(f'Keyword "{search_keyword}" not found in {file_name}')
            
            # Clean up the audio file after processing
            if os.path.exists(audio_path):
                os.remove(audio_path)
                print(f"Cleaned up {audio_path}")

    # Search for the provided keyword in the saved transcriptions
    search_transcriptions(search_keyword)
