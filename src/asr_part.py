from utils.load_openai_client import client

audio_folder = '../audios/'

def transcript_text(audio_file_name):
    audio_file= open(f"{audio_folder}{audio_file_name}", "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    print(transcription.text)

if __name__ == '__main__':
    transcript_text('dias.mp3')