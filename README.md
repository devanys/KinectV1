# Panduan Instalasi Kinect v1 dengan Library OpenNI dan PrimeSense

README ini merupakan panduan langkah demi langkah untuk menginstal dan mengatur Kinect v1 dengan library OpenNI dan PrimeSense.

## system requirements

- Sensor Kinect v1
- Port USB
- Sistem operasi Windows, macOS, atau Linux
- Koneksi internet untuk mengunduh file yang diperlukan

## Unduh dan Instal OpenNI

1. **Unduh OpenNI**:
   - Buka situs web OpenNI atau repository GitHub untuk mengunduh versi terbaru OpenNI.
   - Unduh versi yang sesuai untuk sistem operasi Anda.
   - Jika mengunakan PyPi pada terminal dapat mengunakan (pip install openni-python)
     
2. **Instal OpenNI**:
   - Ekstrak file yang telah diunduh ke direktori pilihan Anda.
   - Buka terminal atau command prompt dan navigasikan ke direktori yang telah diekstrak.
   - Jalankan installer:
     - Pada Windows: `msiexec /i OpenNI-Win32-<versi>.msi`
     - Pada macOS: Gunakan installer `.pkg` yang disediakan.
     - Pada Linux: Jalankan skrip instalasi menggunakan `sudo ./install.sh`.


## Unduh dan Instal PrimeSense

1. **Unduh PrimeSense**:
   - Buka situs web PrimeSense NITE atau repository GitHub untuk mengunduh versi terbaru driver PrimeSense.
   - Unduh versi yang sesuai untuk sistem operasi Anda.
   - Jika mengunakan PyPi pada terminal dapat mengunakan (pip install primesense)
2. **Instal PrimeSense**:
   - Ekstrak file yang telah diunduh ke direktori pilihan Anda.
   - Buka terminal atau command prompt dan navigasikan ke direktori yang telah diekstrak.
   - Jalankan installer:
     - Pada Windows: `msiexec /i PrimeSense-NITE-Win32-<versi>.msi`
     - Pada macOS: Gunakan installer `.pkg` yang disediakan.
     - Pada Linux: Jalankan skrip instalasi menggunakan `sudo ./install.sh`.

3. **Setel Variabel Lingkungan**:
   - Tambahkan binary PrimeSense ke PATH sistem Anda:
     - Pada Windows: Tambahkan `C:\Program Files\PrimeSense\NITE\Bin` ke variabel lingkungan PATH Anda.
     - Pada macOS/Linux: Tambahkan direktori bin PrimeSense ke PATH di `.bash_profile` atau `.bashrc`.

## Menghubungkan Kinect v1

1. **Hubungkan Sensor Kinect v1**:
   - Sambungkan Kinect v1 ke stopkontak menggunakan adaptor daya yang tersedia.
   - Hubungkan Kinect v1 ke komputer melalui port USB.
   - install kinect SDK

2. **Verifikasi Koneksi**:
   - Pastikan sensor dikenali oleh sistem operasi. Pada Windows, memeriksa Device Manager untuk sensor Kinect.
