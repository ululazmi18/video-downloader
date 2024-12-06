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
            "-b:a", "256k",  # Bitrate audio
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
            file_path = os.path.join(os.getcwd(), filename)

            # Ambil bagian sebelum tanda '#'
            title = re.split(r'#', title)[0]

            # Ganti spasi dengan garis bawah dan hapus karakter selain huruf, angka, dan garis bawah
            title = re.sub(r'[^a-zA-Z0-9_]', ' ', title).strip()
            title = re.sub(r'\s+', '_', title)

            # Pastikan judul tidak kosong
            if not title:  # Jika judul kosong setelah pemotongan, gunakan 'Video' sebagai fallback
                title = 'Video'

            filenamebaru = f"{title}_Baru.{ext}"

            # Periksa apakah nama file sudah ada, jika ada tambahkan nomor acak 3 digit
            if os.path.exists(filenamebaru):
                random_number = random.randint(100, 999)
                filenamebaru = f"{title}_Baru_{random_number}.{ext}"

            # Simpan file ke jalur lengkap
            file_path_baru = os.path.join(os.getcwd(), filenamebaru)
            
            os.rename(file_path, file_path_baru)
            
            file_output = filenamebaru.replace("_Baru", "").strip()
            
            reencoding(filenamebaru, file_output)
            
            os.remove(file_path_baru)

            print(f"Video berhasil diunduh dan diproses ulang. Hasil disimpan di: {file_output}")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    unduh_video()
