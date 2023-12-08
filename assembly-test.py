import assemblyai as aai
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
    {"text": 'Purpose', "start": 12676, "end": 13500, "confidence": 0.98515},
]

def slice_transcript_by_keywords(transcriptWords, keywords):
    slices = []
    start_index = 0

    for i, word in enumerate(transcriptWords):
        if word['text'] in keywords:
            if i > start_index:
                slices.append(transcriptWords[start_index:i])
            start_index = i + 1

    if start_index < len(transcriptWords) and start_index != len(transcriptWords) - 1:
        slices.append(transcriptWords[start_index:])

    return slices

def get_start_end_times_of_slices(slices):
    start_times = []
    end_times = []

    for slice in slices:
        if slice:
            start_times.append(slice[0]['start'])
            end_times.append(slice[-1]['end'])

    return start_times, end_times

# Your transcript data
transcript = transcriptWords

# Define the words to isolate
keywords = ["Abracadabra", "Company", "Purpose"]

# Video path
video_path = 'second_video.mov'

# Directory to save the output segments
output_directory = 'output_segments'

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

slices = slice_transcript_by_keywords(transcriptWords, keywords)

start_times, end_times = get_start_end_times_of_slices(slices)

for i, (start_time, end_time) in enumerate(zip(start_times, end_times)):
    print(f"Slice {i + 1}:")
    print(f"Start Time: {start_time}")
    print(f"End Time: {end_time}")
    print("\n")
    output_segment = os.path.join(output_directory, f'original_segment{i}.mp4')
    os.system(f'ffmpeg -ss {start_time/1000} -t {(end_time/1000) - (start_time/1000)} -i "{video_path}" -c:v copy -c:a copy "{output_segment}"')

"""
NEXT STEPS:
- Once you have the segments that are not keywords, you need to create segments that are keywords in sieve
- Once you have all the clips, you need standardize the clips to have the same encoding.
    - You can do this by running the following command, run this command for all the video files:
    - ffmpeg -i clip-1.mp4 -c:v libx264 -profile:v main -c:a aac -ac 2 -b:a 128k clip-1-converted.mp4
- Once you have all the clips, you can add them to a text file called segments.txt
- Once you have the segments.txt file, you need to run the following command:
    - ffmpeg -f concat -safe 0 -i segments.txt -c copy output.mp4
    - This will create a new video called output.mp4 that is the final video
"""