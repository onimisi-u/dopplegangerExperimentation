import assemblyai as aai
import cv2
import os

""" # Replace with your API token
aai.settings.api_key = f"85342ce1568c4f69ba290e6b22cd877a"

# URL of the file to transcribe
FILE_URL = "https://imxze2im7tagxmrw.public.blob.vercel-storage.com/second_video-Mjo26HqmS7KzJM1enyIIJaXTlcpnfp.mov"

# You can also transcribe a local file by passing in a file path
# FILE_URL = './path/to/file.mp3'

transcriber = aai.Transcriber()
transcript = transcriber.transcribe(FILE_URL)

print(transcript.words) """

# LIMITATION: if the confidence is too low, it can get the word wrong

transcriptWords = [
    {"text": 'Hello,', "start": 1210, "end": 1614, "confidence": 0.9458},
    {"text": 'Abracadabra', "start": 1732, "end": 3150, "confidence": 0.32111},
    {"text": 'I', "start": 3730, "end": 4094, "confidence": 1.0},
    {"text": 'see', "start": 4132, "end": 4334, "confidence": 0.99999},
    {"text": "you're", "start": 4548, "end": 4874, "confidence": 0.61134},
    {"text": 'working', "start": 4922, "end": 5278, "confidence": 0.99996},
    {"text": 'at', "start": 5364, "end": 5806, "confidence": 0.83},
    {"text": 'Company', "start": 5908, "end": 6560, "confidence": 0.9884},
    {"text": 'I', "start": 7090, "end": 7454, "confidence": 1.0},
    {"text": 'think', "start": 7492, "end": 7694, "confidence": 0.99998},
    {"text": 'that', "start": 7732, "end": 7934, "confidence": 0.99841},
    {"text": 'vidyard', "start": 7972, "end": 8506, "confidence": 0.13243},
    {"text": 'would', "start": 8538, "end": 8638, "confidence": 0.66355},
    {"text": 'be', "start": 8644, "end": 8862, "confidence": 0.99945},
    {"text": 'a', "start": 8916, "end": 9182, "confidence": 1.0},
    {"text": 'great', "start": 9236, "end": 9742, "confidence": 0.99998},
    {"text": 'solution', "start": 9876, "end": 10750, "confidence": 0.99181},
    {"text": 'for', "start": 11090, "end": 11790, "confidence": 0.99996},
    {"text": 'your', "start": 11940, "end": 12542, "confidence": 0.9998},
    {"text": 'Purpose', "start": 12676, "end": 13500, "confidence": 0.98515}
]

# Function to split the video without modifying audio
def split_video(video_path, start_time, end_time, output_path):
    print(f"Splitting video from {start_time} to {end_time} seconds.")

    """ # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get the frame rate of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Calculate start and end frames
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)

    # Set the starting frame of the video
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (int(cap.get(3)), int(cap.get(4))))

    for frame_num in range(start_frame, end_frame):
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release() """

    # Use FFmpeg to copy audio from the original video to the output video segment
    os.system(f'ffmpeg -i "{video_path}" -ss {start_time} -t {end_time - start_time} -c:v copy -c:a copy "{output_path}_with_audio.mp4"')

def get_time_ranges(transcript_words, target_words):
    time_ranges = []
    for i in range(len(transcript_words) - 1):
        if transcript_words[i + 1]['text'] in target_words:
            time_range = (transcript_words[i]['start'], transcript_words[i]['end'])
            time_ranges.append(time_range)
    return time_ranges

# Your transcript data
transcript = transcriptWords

# Define the words to isolate
words_to_isolate = ["Abracadabra", "Company", "Purpose"]

# Video path
video_path = 'second_video.mov'

# Check if the file exists
if os.path.exists(video_path):
    print(f"The file {video_path} exists.")
else:
    print(f"The file {video_path} does not exist.")

# Iterate through the transcript to split the video for the defined words
for word in transcript:
    if word['text'] in words_to_isolate:
        start_time = word['start'] / 1000  # Convert to seconds
        end_time = word['end'] / 1000  # Convert to seconds
        output_path = f'segment_{word["text"]}.mp4'  # Output file named after the word
        # split_video(video_path, start_time, end_time, output_path)

# Get the time ranges for the words to isolate
target_words = ["Abracadabra", "Company", "Purpose"]
time_ranges = get_time_ranges(transcriptWords, target_words)
print(time_ranges)