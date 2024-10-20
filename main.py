from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

# Inisialisasi driver Chrome menggunakan ChromeDriverManager agar lebih dinamis
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# rentang surah yang ingin di-scrape
surah_range = range(1, 115)  

# Membuka file CSV untuk menulis hasil scraping
with open('korpus_parallel.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Arabic", "Bahasa"])  # Header baru tanpa kolom Surah

    # Iterasi melalui setiap surah
    for surah in surah_range:
        # Membuat URL dinamis berdasarkan surah
        url = f'https://quran.kemenag.go.id/quran/per-ayat/surah/{surah}?from=1&to=300'
        
        # Buka halaman web yang ingin diambil teksnya
        driver.get(url)

        # Tunggu sampai elemen-elemen yang diinginkan muncul
        driver.implicitly_wait(10)

        # Scroll halaman ke bawah hingga semua elemen dimuat
        scroll_pause_time = 2  # Waktu jeda antar scroll (sesuaikan jika perlu)
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll ke bawah
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Tunggu beberapa detik untuk halaman memuat elemen baru
            time.sleep(scroll_pause_time)
            
            # Hitung tinggi halaman baru setelah scroll
            new_height = driver.execute_script("return document.body.scrollHeight")
            
            # Cek apakah sudah mencapai bagian paling bawah halaman
            if new_height == last_height:
                break
            
            last_height = new_height

        # Temukan semua elemen dengan class 'arabic' untuk teks Arab
        arabic_elements = driver.find_elements(By.CLASS_NAME, 'arabic')

        # Gunakan selektor CSS untuk hanya mengambil elemen dengan class 'surah-translate' tanpa class 'gold'
        translation_elements = driver.find_elements(By.CSS_SELECTOR, ".surah-translate:not(.gold)")

        # Iterasi melalui semua elemen yang ditemukan dan ambil teksnya
        arabic_texts = [element.text for element in arabic_elements]
        translation_texts = [element.text for element in translation_elements]

        # Simpan hasil scraping ke dalam file CSV tanpa kolom surah
        for arabic, translation in zip(arabic_texts, translation_texts):
            writer.writerow([arabic, translation])

# Tutup browser setelah selesai
driver.quit()

print("Hasil scraping telah disimpan dalam file 'korpus_parallel.csv'.")
