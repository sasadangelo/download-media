import argparse
import subprocess
import os
from faster_whisper import WhisperModel


def is_valid_youtube_url(url):
    return url and ("youtube.com" in url or "youtu.be" in url)


def download_audio(url, output_file):
    try:
        subprocess.run(
            [
                "yt-dlp",
                "-x",
                "--audio-format",
                "mp3",
                "-o",
                output_file,
                url,
            ],
            check=True,
        )
        print(f"Audio scaricato con successo: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Errore durante il download dell'audio: {e}")


def download_video(url, output_file):
    try:
        subprocess.run(
            [
                "yt-dlp",
                "-f",
                "bestvideo+bestaudio/best",
                "-o",
                output_file,
                url,
            ],
            check=True,
        )
        print(f"Video scaricato con successo: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Errore durante il download del video: {e}")


def transcribe_audio(
    input_file, output_file, lang="it", model_name="base", delete_audio=False
):
    try:
        # Converte in WAV compatibile Whisper se non è WAV
        if not input_file.lower().endswith(".wav"):
            wav_file = os.path.splitext(input_file)[0] + "_whisper.wav"
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-i",
                    input_file,
                    "-ar",
                    "16000",
                    "-ac",
                    "1",
                    wav_file,
                ],
                check=True,
            )
            audio_to_transcribe = wav_file
        else:
            audio_to_transcribe = input_file

        # Carica modello Whisper
        model = WhisperModel(model_name)
        segments, _ = model.transcribe(audio_to_transcribe, language=lang)

        # Scrive la trascrizione
        with open(output_file, "w", encoding="utf-8") as f:
            for segment in segments:
                f.write(segment.text + " ")

        print(f"Trascrizione salvata in: {output_file}")

        # Rimuove file temporaneo se richiesto
        if delete_audio and audio_to_transcribe != input_file:
            os.remove(audio_to_transcribe)
            print(f"File temporaneo rimosso: {audio_to_transcribe}")

    except Exception as e:
        print(f"Errore durante la trascrizione: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Scarica audio, video o trascrivi audio usando yt-dlp e Whisper."
    )
    parser.add_argument("-u", "--url", help="URL del video di YouTube")
    parser.add_argument("-i", "--input", help="File audio locale per trascrizione")
    parser.add_argument(
        "-a", "--audio", help="Scarica solo l'audio in mp3", action="store_true"
    )
    parser.add_argument(
        "-c",
        "--captions",
        help="Trascrivi l'audio in un file di testo",
        action="store_true",
    )
    parser.add_argument("-o", "--output", help="Nome del file in output")
    parser.add_argument(
        "-l", "--lang", help="Lingua della trascrizione (default: it)", default="it"
    )
    parser.add_argument(
        "-m",
        "--model",
        help="Modello Whisper da usare (tiny/base/small/medium/large)",
        default="base",
    )
    parser.add_argument(
        "--delete-audio",
        help="Rimuove file audio temporanei dopo la trascrizione",
        action="store_true",
    )
    args = parser.parse_args()

    # Gestione download
    if args.audio:
        if not is_valid_youtube_url(args.url):
            print("URL non valido per il download audio.")
            return
        output_file = args.output if args.output else "audio.%(ext)s"
        download_audio(args.url, output_file)
    elif args.url and not args.captions:
        output_file = args.output if args.output else "video.%(ext)s"
        download_video(args.url, output_file)

    # Gestione trascrizione
    if args.captions:
        if args.input:
            input_file = args.input
        elif args.audio:
            input_file = args.output if args.output else "audio.%(ext)s"
        else:
            print(
                "Per la trascrizione serve un file locale (-i) o un audio scaricato (-a)."
            )
            return

        output_file = args.output if args.output else "captions.txt"
        transcribe_audio(
            input_file=input_file,
            output_file=output_file,
            lang=args.lang,
            model_name=args.model,
            delete_audio=args.delete_audio,
        )


if __name__ == "__main__":
    main()
