from flask import Flask, render_template, request #harus import Flask dari modul flask, template_rendered untuk memamanggil template html dll, request untuk mengambil data dari form
from bs4 import BeautifulSoup #import BeautifulSoup dari modul bs4 untuk scraping web berita
import requests #import requests untuk melakukan request ke web berita

app = Flask(__name__) # inisialisasi objek Flask

#filter berita
def filter_berita(media_berita):
    nama_elemen = ''  # elemen yang akan dicari
    nama_class = ''  # class yang akan dicari
    
    if media_berita == 'kompas':
        nama_elemen = 'h1'
        nama_class = 'hlTitle'
    elif media_berita == 'tribunNews':
        nama_elemen = 'div'
        nama_class = 'hltitle'
    elif media_berita == 'cnnIndonesia':
        nama_elemen = 'h2'
        nama_class = 'text-sm'
        
    return [nama_elemen, nama_class]  # mengembalikan elemen dan class yang sesuai dengan media berita

# Scraping Web Berita
def berita(media_berita, url):
    #url = "https://www.cnnindonesia.com/" # URL yang akan di-scrape
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers) # melakukan request ke URL dengan headers
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # filter berita berdasarkan media
    filter = filter_berita(media_berita)
    nama_elemen = filter[0]  # elemen yang akan dicari
    nama_class = filter[1]  # class yang akan dicari
    
    headlines = soup.find_all(nama_elemen, nama_class) # mencari semua elemen h3 dengan class article__title
    
    if headlines:
        hasil = [h.text.strip() for h in headlines]
        return hasil  # mengembalikan list
    else:
        return "Tidak ditemukan headline pada halaman."


@app.route("/") # decorator untuk menentukan route

# route ini akan mengembalikan halaman home
def home():
    kompas = berita('kompas', "https://www.kompas.com/") # scraping berita dari kompas
    tribunNews = berita('tribunNews', "https://www.tribunnews.com/") # scraping berita dari tribunNews
    cnnIndonesia = berita('cnnIndonesia', "https://www.cnnindonesia.com/")
    web_title = "Dihalaman Berita"
    return render_template('index.html', pesan= web_title, kompas=kompas, tribunNews=tribunNews, cnnIndonesia=cnnIndonesia) # #menggunakan template_rendered untuk memanggil file index.html yang ada di folder templates

    # return f"<p>Hallo, kamu berada di {web_title}!</p><br> <a href='/about'>About</a>" #gunakan f untuk dapat memanggil variabel dalam string

#route ini akan mengembalikan halaman about
@app.route("/about")
def about():
    web_title = "Halaman about"
    return render_template('about.html', web_title= web_title) #menggunakan template_rendered untuk memanggil file about.html yang ada di folder templates

#route untuk menghitung usia
@app.route("/usia", methods=['GET', 'POST']) #method post untuk mengirim data dari form
def cek_usia():
    if request.method == 'POST':
        # ambil data dari form
        nama = request.form.get('nama')
        tahun_lahir = int(request.form.get('tahun_lahir'))
        tahun_sekarang = 2025 # misalkan tahun sekarang adalah 2025
        usia = tahun_sekarang - tahun_lahir
        return render_template('cek_usia.html', nama=nama, usia=usia)
    return render_template('cek_usia.html', nama=None, usia=None)

# route untuk menghitung index massa tubuh
@app.route("/imt", methods=['GET', 'POST'])
def cek_imt():
    if request.method == 'POST':
        # ambil data dari form
        nama = request.form.get('nama')
        tinggi = float(request.form.get('tinggi')) / 100 # konversi tinggi ke meter
        berat = float(request.form.get('berat')) # berat dalam kilogram
        imt = berat / (tinggi * tinggi) # menghitung IMT
        # menentukan kategori IMT
        if imt < 17.0:
            kategori = "Sangat Kurus"
            img = "skurus.png"
        elif 17.0 <= imt < 18.4:
            kategori = "Kurus"
            img = "kurus.png"
        elif 18.4 <= imt < 25.0:
            kategori = "Normal (Ideal)"
            img = "normal.jpg"
        elif 25.1 <= imt < 27.0:
            kategori = "Gemuk"
            img = "gemuk.jpg"
        else:
            kategori = "Obesitas"
            img = "obesitas.png"
        return render_template('cek_imt.html', nama=nama, imt=imt, kategori=kategori, img=img)
    return render_template('cek_imt.html', nama=None, imt=None, kategori=None)
