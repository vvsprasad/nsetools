# # Load the CSV file
# import pandas as pd

# file_path = './strategy/fbd_buy/atr.csv'
# df = pd.read_csv(file_path)
# df.columns = df.columns.str.strip()

# df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
# df['High'] = pd.to_numeric(df['High'], errors='coerce')
# df['Low'] = pd.to_numeric(df['Low'], errors='coerce')
# df['prev. close'] = pd.to_numeric(df['prev. close'].str.replace(',', ''), errors='coerce')

# # Check for and handle missing values (NaNs)
# # Option 1: Fill NaNs with the previous value (forward fill)
# df.fillna(method='ffill', inplace=True)

# print(df['prev. close'])

# # Calculate True Range (TR)
# df['TR1'] = df['High'] - df['Low']
# df['TR2'] = abs(df['High'] - df['prev. close'])
# df['TR3'] = abs(df['Low'] - df['prev. close'])
# df['True Range'] = df[['TR1', 'TR2', 'TR3']].max(axis=1)

# # Calculate ATR with a 14-period window
# df['ATR'] = df['True Range'].rolling(window=14, min_periods=1).mean()

# # Display the DataFrame with True Range and ATR
# df[['Date', 'High', 'Low', 'Close', 'True Range', 'ATR']]
# print(df)


# import cv2
# # Load the video
# video = cv2.VideoCapture('C:/Users/Sree/Downloads/98893ef2-aae5-4d4d-bb2c-9aba2ddba2cd.mp4')

# frame_count = 0
# while True:
#     ret, frame = video.read()
#     if not ret:
#         break
#     print(f'Frame {frame_count} is being written'.format(frame_count))  
#     cv2.imwrite(f'frame_{frame_count}.jpg', frame)
#     frame_count += 1

# video.release()
# cv2.destroyAllWindows()

import nltk
import speech_recognition as sr
from moviepy.editor import VideoFileClip
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# Step 1: Extract Audio from Video
def extract_audio_from_video(video_path, audio_output_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_output_path)
    print(f"Audio extracted and saved to {audio_output_path}")

# Step 2: Transcribe Audio to Text
def transcribe_audio_to_text(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            transcript = recognizer.recognize_google(audio_data)
            print("Transcription completed successfully.")
            return transcript
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return ""

# Step 3: Summarize the Transcription using Sumy
def summarize_text(transcribed_text):
    nltk.download('punkt_tab')
    if transcribed_text:
        parser = PlaintextParser.from_string(transcribed_text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, 2)  # Summarize to 2 sentences
        print("Summary generated successfully.")
        return ' '.join(str(sentence) for sentence in summary)
    else:
        print("No transcription available to summarize.")
        return ""

# Step 4: Generate Analysis Report
def generate_analysis_report(video_path, transcript_summary):
    report_content = f"""
    Video Analysis Report
    ---------------------
    Video File: {video_path}

    Transcript Summary:
    {transcript_summary}

    """

    report_path = "C:/Users/Sree/Downloads/final/analysis_report.txt"
    with open(report_path, "w") as f:
        f.write(report_content)
    print(f"Analysis report generated and saved to {report_path}")

# Main Function to Execute All Steps
def analyze_video(video_path):
    audio_output_path = "C:/Users/Sree/Downloads/final/extracted_audio.wav"
    extract_audio_from_video(video_path, audio_output_path)
    
    transcript = transcribe_audio_to_text(audio_output_path)
    if transcript:
        with open("C:/Users/Sree/Downloads/final/transcript.txt", "w") as f:
            f.write(transcript)
        print("Transcript saved to transcript.txt")
    
    summary = summarize_text(transcript)
    if summary:
        with open("C:/Users/Sree/Downloads/final/summary.txt", "w") as f:
            f.write(summary)
        print("Summary saved to summary.txt")
    
    generate_analysis_report(video_path, summary)

# Specify the video file path
video_file_path = 'C:/Users/Sree/Downloads/98893ef2-aae5-4d4d-bb2c-9aba2ddba2cd.mp4'

# Run the analysis
analyze_video(video_file_path)
