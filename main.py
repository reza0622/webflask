from flask import Flask, render_template, request #harus import Flask dari modul flask, template_rendered untuk memamanggil template html dll, request untuk mengambil data dari form

app = Flask(__name__) # inisialisasi objek Flask

@app.route("/") # decorator untuk menentukan route

# route ini akan mengembalikan halaman home
def home():
    web_title = "Halaman utama"
    return render_template('index.html', pesan= web_title) # #menggunakan template_rendered untuk memanggil file index.html yang ada di folder templates

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