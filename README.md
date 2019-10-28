# FinalProject

file :
* pcap : untuk desain preprocessor untuk digunakan sebagai simulasi packet dissector pada Snort
* web : desain antarmuka snort berbasis web

untuk compile snort manual dibutuhkan
1. dumbnet
2. daq


## Struktur Tabel Database
Tabel berikut ini hanya berubah saat melakukan Training Data, sedangkan pada saat Filtering Data maka tabel ini hanya akan diakses sebagai rule saja.
1. Benign Data (id, data, 3byte content...)
2. Background Data (id, data, 3byte content...)
3. Malicious Data (id, data, 3byte content...)
4. Benign Regex (id, data, 3byte content...)
5. Background Regex (id, data, 3byte content...)
6. Malicious Regex (id, data, 3byte content...)

Alert dan tabel lain diakses secara terpisah dan mengeluarkan log secara simultan dengan NN Database
Tabel yang diusulkan : ACID (Analysis Console for Intrusion Databases)
yang hanya menampilkan Alert dan Lain-lain secara umum


## Batasan masalah
1. Snort murni

2. Webgui hanya untuk nenepreprocessor (buat sendiri)

3. Masuk ke Classifier sebelum ke Filter dengan Convolutional Neural Network

4. Filter menggunakan Predictor dengan Elman atau LSTM RNN
 - Berdasarkan dari persentase Benign atau Malicious dari paket, jika kecenderungan mencapai diatas 80% Benign, maka paket akan di loloskan, dengan Range Prediksi sebanyak 50 step, jika kecenderungan mencapai diatas 80% Malicious, maka paket akan dihentikan, dengan Range Prediksi sebanyak 50 step

5. Dari data kecenderungan Benign akan di ekstraksi fitur PCRE dengan rule : 
 - PCRE hanya mendeteksi non ASCII char, PCRE yang di ekstraksi merupakan salah satu dari jenis paket yang paling sering menghasilkan Prediksi Negative

6. PCRE digunakan sebagai pattern matching untuk header tertentu sebelum di defrag dan akan dimasukkan dalam CNN sebagai bentuk aslinya (seperti saat belum di enkapsulasi)

7. Dari ketiga perbedaan itu, di kumpulkan dan dipisahkan ke tabel masing-masing, kemudian dari tabel masing-masing akan di cari kesamaan dengan snip yang sudah ada, dengan memanfaatkan Regex dengan Word Boundary dengan Boundary Limiter 0x00, 0x0a, 0x0d, 0x90, 0x20, atau 0x00 NULL, 0x0a (LF), 0x0d (CR), 0x90 (NOP), 0x20 (SPC). Beberapa ketentuan ini masih opsional. Dan untuk kepastian data PCRE yang diperoleh adalah memaksimalkan penggunaan PCRE hanya untuk pemisahan dan pengkategorian paket berdasarkan header saja. (Bisa dikembangkan ke packet konten untuk penelitian selanjutnya yang berkelanjutan) 

8. Dari perbedaan yang dicari perbyte kemudian akan dihasilkan jika pada delimiter tersebut terdapat 1 atau lebih kesamaan yang sering terjadi (lebih dari 3 kali) maka akan di buat regex nya, dan akan masuk ke dalam tabel regex Malicious. (Ini skenario sederhana bagaiman PCRE yang terdeteksi dalam suatu file dapat memisahkan Pola Malicious dan pola Benign)

## Intro Command

1. Training External, untuk ekstraksi dataset

```console
pcapread [options] [namafile.pcap]
options:
 -n jumlahoutput
 -p Mendifinisikan prefix, contoh: payload -> payload.001.log
 -g gambar, akan mengeluarkan: payload.001.bmp
 -v verbose
```

2. Untuk memulai training dataset

```console
pcaptrain [options] [prefix dari .log]
options:
 -e epoch disini untuk epochs LSTM nya
 -c pcaptrain.conf
 -p Mendefinisikan prefix, contoh: paytrain -> paytrain.001.hdf5
 -v verbose
 -t target (Normal (1), Background(0), Malicious(-1))
```
Opsi ini untuk sementara tidak dipakai karena memaksimalkan penggunaan keras sebagai metode training model

3. Untuk pcaptrain.conf

```console
# Ini config untuk program pcaptrain
[database]
database namadatabase
user root
password passworddatabase

# Database harus berisi tabel dengan nama
# benign, malicious, background

[CNN]
learning rate = 0.5
hidden layer = 5
activation = {RELU,SIGMOID,RELU,SIGMOID,RELU}
optimizer = Adam # Adam atau SGD
epochs = 10
-....-....-.-

# kNN belum dibuat
[kNN]
default
-....-....-.-

[SVM]
default
-....-....-.-

pakai CNN # perintah pakai untuk menseleksi selector

```
Untuk opsi ini tidak dibuat karena memaksimalkan penggunaan keras sebagai model trainer dan tester. Sehingga konfigurasinya menggunakan flask dalam bentuk web.
Hal-hal yang di parameterkan adalah MTU
dan yang ditampilkan ketika model di load adalah ukuran MTU itu sendiri.

4. Testing sebelum dipakai di snort, pcaptest.c

```console
pcaptest [options] file.pcap
options:
 - s (1 untuk negative, 2 untuk positif) 
```
Untuk testing ini menggunakan flask juga karena yang digunakan adalah prediktornya

5. Untuk di Snort spp\_nnota.c

```c
# Memanfaatkan database yang telah diolah untuk diperoleh hasilnya live
gunanya adalah untuk memfilter data jaringan, dengan data neural
# Skenario 1 : Data masuk di sampling jarang-jarang dan di prediksi berdasarkan hasil dari LSTM, atau Elman RNN
```

Beberapa konten dari file ini belum di ubah
6. Untuk di Snort Web Interface

```console
Grafik persentase Normal / Malicious
50 grafik bitmap jaringan MTU 1500
LSTM Net config
LSTM Net on action
[ ]
byte stream dengan format PCRE
```

## Buat makefile nya

```makefile
make:pcapread.c pcaptrain.c pcaptest.c
	gcc -lpcap -g pcapread.c -o pcapread.c
	\ gcc -lpcap -g pcaptrain.c -o pcaptrain.c
	\ gcc -lpcap -g pcaptest.c -o pcaptest.c
```

# Sistem Terbagi menjadi dua
1. LSTM Profiler
2. CNN Predictor

# Cara Penggunaan
1. Pertama-tama compile seluruh program yang ada di src
2. Compile program yang ada di src/bitmap/raw2bmp.c
3. Lakukan pcapread -r untuk baca file, atau pcapread -i untuk baca interface
4. Dari data yang keluar yang banyak itu, raw2bmp input output agar keluar data bitmapnya
5. Dari data bitmap yang diperoleh baca di Jupyter Notebook
6. Buat classifier untuk data yang diperoleh dan simpan hasil trainingnya dalam bentuk pickle
7. Hasil training dalam bentuk pickle buka dengan pcaptest untuk melakukan testing dengan pcaptest -r datatest.pcap -f filepickle
8. Jika diperoleh nilanya bagus, gunakan data filepickle untuk diolah dalam spp\_example di snort yang memfilter data SnortPacket-\>payload untuk kemudian di tetapkan sebagai rule untuk intrusi yang ada dari file pcap itu
9. Untuk web interface snort, snort hanya akan menampilkan alert saja.
10. Sedang untuk interface Malware Classifier, berada di Jupyter Notebook
