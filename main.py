import argparse
import os
from pytube import YouTube

def is_valid_youtube_url(url):
    return "youtube.com" in url

def download_audio(url, output_file):
    try:
        youtube = YouTube(url)
        # Ottieni la migliore qualità audio
        audio_stream = youtube.streams.get_audio_only()
        audio_stream.download(output_path=".", filename=output_file)
        # Stampare informazioni sulla qualità dell'audio
        print(f"Qualità audio: {audio_stream.abr} kbps - {audio_stream.mime_type}")
        print("Audio scaricato con successo!")
    except Exception as e:
        print(f"Errore durante il download dell'audio: {e}")

def download_video(url, output_file):
    try:
        youtube = YouTube(url)
        video_stream = youtube.streams.filter(file_extension="mp4", progressive=True).get_highest_resolution()
        video_stream.download(output_path=".", filename=output_file)
        # Stampare informazioni sulla risoluzione video
        print(f"Risoluzione video: {video_stream.resolution}")
        print("Video scaricato con successo!")
    except Exception as e:
        print(f"Errore durante il download del video: {e}")

def main():
    parser = argparse.ArgumentParser(description="Scarica audio o video da un URL di YouTube.")
    parser.add_argument("-u", "--url", help="URL del video di YouTube", required=True)
    parser.add_argument("-a", "--audio", help="Scarica solo l'audio in un file .mp4", action="store_true")
    parser.add_argument("-o", "--output", help="Nome del file in output (default: audio.mp3 per audio, video.mp4 per video)")
    args = parser.parse_args()

    url = args.url

    if not is_valid_youtube_url(url):
        print("URL non supportato. Assicurati che sia un URL valido di YouTube.")
        return

    output_file = args.output if args.output else "audio.mp3" if args.audio else "video.mp4"

    if args.audio:
        download_audio(url, output_file)
    else:
        download_video(url, output_file)

if __name__ == "__main__":
    main()
