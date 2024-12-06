import yt_dlp
import os
import re
import random
import subprocess

def reencoding(file_input, file_output):
    try:
        # Perintah FFmpeg untuk re-encoding dengan pengaturan kualitas tinggi
        command = [
            "ffmpeg",
            "-i", file_input,  # File input
            "-c:v", "libx264",  # Codec video H.264
            "-crf", "18",  # Kualitas tinggi
            "-pix_fmt", "yuv420p",  # Format warna untuk kompatibilitas
            "-c:a", "aac",  # Codec audio AAC
            file_output  # File output
        ]

        # Jalankan perintah
        subprocess.run(command, check=True)
        print(f"File baru disimpan sebagai: {file_output}")
    except subprocess.CalledProcessError as e:
        print(f"Terjadi kesalahan saat menjalankan FFmpeg: {e}")
    except Exception as e:
        print(f"Kesalahan umum: {e}")

def unduh_video():
    # Minta input URL video
    url = input("Masukkan URL video yang ingin diunduh: ")

    # Konfigurasi untuk memilih resolusi terbaik
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",  # Pilih video dan audio dengan kualitas terbaik
        "outtmpl": "%(title)s.%(ext)s",  # Nama file keluaran akan mengikuti judul video
    }

    try:
        # Mengunduh video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            title = info_dict.get('title', 'Video')
            ext = info_dict.get('ext', 'mp4')
            print(f"\n\n{info_dict}\n\n")
            
            filename = f"{title}.{ext}"
            filename1 = f"{title}_Baru.{ext}"
            os.rename(filename, filename1)
            reencoding(filename1, filename)
            os.remove(filename1)

            print(f"Video berhasil diunduh dan diproses ulang.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    unduh_video()
