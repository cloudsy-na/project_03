from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime
import time

# List untuk menampung hasil sementara
result = []

# Header untuk permintaan HTTP
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Direktori file
master_dir = "C:\\Users\\andriawan\\Documents\\My Task\\Python\\GRAINGER\\"
link_dir = master_dir + "link\\"

# Membaca daftar URL dari file teks
with open(link_dir + "list_links.txt", 'r+', encoding='utf-8') as f:
    linkProd = [line for line in f.read().splitlines()]

# Membuat nama file CSV dengan timestamp
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
csv_filename = f"product_images_{timestamp}.csv"

# Membuka file CSV untuk menulis data
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['link', 'image']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Menulis header ke file CSV
    writer.writeheader()

    # Loop melalui setiap URL
    for url in linkProd:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        try:
            # Mengambil semua elemen gambar dengan selector tertentu
            thumbnail_images = soup.select('.J9d-PS img')
            for img in thumbnail_images:
                result.append(img.get('src'))
                time.sleep(3)  # Menambahkan jeda untuk menghindari pemblokiran oleh server

            # Membuat dictionary hasil dengan link dan gambar
            dict_result = {'link': url, 'image': ', '.join(result) if result else 'null'}
            result = []  # Reset list result untuk iterasi berikutnya

        except AttributeError:
            continue

        # Menulis hasil ke file CSV
        writer.writerow(dict_result)
        print(dict_result)
