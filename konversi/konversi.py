from PIL import Image
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import shutil


ekspanduser = lambda dir: Path(dir).expanduser()
nama_berkas = lambda dir: Path(dir).stem

def resize_and_save_png(input_path, output_path, size):
    try:
        image = Image.open(input_path)
        resized_image = image.resize(size, Image.LANCZOS)
        
        # Membuat folder jika belum ada
        output_folder = Path(output_path).parent
        output_folder.mkdir(parents=True, exist_ok=True)
        
        resized_image.save(output_path, format='PNG')
        # print(f"Gambar berhasil diubah ukurannya ke {size} dan disimpan sebagai {output_path}")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def move_folders_to_hicolor(base_path, output_base_path):
    hicolor_path = output_base_path / 'icon' / 'hicolor'
    hicolor_path.mkdir(parents=True, exist_ok=True)
    
    # List semua folder ukuran
    size_folders = [folder for folder in base_path.iterdir() if folder.is_dir() and 'x' in folder.name]
    
    for folder in size_folders:
        target_folder = hicolor_path / folder.name
        shutil.move(str(folder), str(target_folder))  # Menggunakan shutil.move untuk memindahkan folder
        print(f"Folder {folder.name} dipindahkan ke {target_folder}")

def jalan_ubah_ukuran_png_multi(url, output_dir):
    input_path = ekspanduser(url)
    output_base_path = ekspanduser(output_dir)
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]  # Ukuran yang diinginkan (lebar, tinggi)

    with ProcessPoolExecutor() as executor:
        futures = []
        for size in sizes:
            folder_name = f"{size[0]}x{size[1]}"
            output_path = output_base_path / folder_name / f"{nama_berkas(url)}.png"
            futures.append(executor.submit(resize_and_save_png, input_path, output_path, size))
        
        for future in futures:
            future.result()  # Menunggu setiap future selesai dan menangani pengecualian jika ada
    
    # Memindahkan folder ukuran ke dalam icon/hicolor
    move_folders_to_hicolor(output_base_path, output_base_path)

# Contoh pemanggilan fungsi jalan_ubah_ukuran_png_multi
# if __name__ == "__main__":
#     url = "~/Gambar/hasil_kerja/kde-3.png"
#     output_dir = "~/Gambar/hasil"
#     jalan_ubah_ukuran_png_multi(url, output_dir)
