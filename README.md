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

3. Masuk ke Classifier sebelum ke Filter
 - CNN
 - kNN
 - SVM

4. Filter menggunakan Predictor dengan Elman atau LSTM RNN
 - Berdasarkan dari persentase Benign atau Malicious dari paket, jika kecenderungan mencapai diatas 80% Benign, maka paket akan di loloskan, dengan Range Prediksi sebanyak 50 step, jika kecenderungan mencapai diatas 80% Malicious, maka paket akan dihentikan, dengan Range Prediksi sebanyak 50 step

5. Dari data kecenderungan Benign akan di ekstraksi fitur PCRE dengan rule : 
 - PCRE hanya mendeteksi non ASCII char, PCRE yang di ekstraksi merupakan salah satu dari jenis paket yang paling sering menghasilkan Prediksi Negative

6. PCRE digunakan sebagai rule yang dihasilkan oleh NN, dimana dari NN diperoleh database yang berisi list packet yang terdapat benign, dan list packet yang normal
Kemudian dilihat diff nya satu persatu, jika terdapat kesamaan, maka itu dianggap packet Background, tetapi jika terdapat pada Packet Malicious namun tidak pada Packet Benign, maka snip itu dianggap code Malicious. Begitupula sebaliknya, jika terdapat pada Packet Benign namun tidak pada Packet Malicious, maka snip itu dikategorikan kode Benign

7. Dari ketiga perbedaan itu, di kumpulkan dan dipisahkan ke tabel masing-masing, kemudian dari tabel masing-masing akan di cari kesamaan dengan snip yang sudah ada, dengan memanfaatkan Regex dengan Word Boundary dengan Boundary Limiter 0x00, 0x0a, 0x0d, 0x90, 0x20, atau 0x00 NULL, 0x0a (LF), 0x0d (CR), 0x90 (NOP), 0x20 (SPC) 

8. Dari perbedaan yang dicari perbyte kemudian akan dihasilkan jika pada delimiter tersebut terdapat 1 atau lebih kesamaan yang sering terjadi (lebih dari 3 kali) maka akan di buat regex nya, dan akan masuk ke dalam tabel regex Malicious

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

4. Testing sebelum dipakai di snort, pcaptest.c

```console
pcaptest [options] file.pcap
options:
 - s (1 untuk negative, 2 untuk positif) 
```

5. Untuk di Snort spp_nnota.c

```c
# Memanfaatkan database yang telah diolah untuk diperoleh hasilnya live
gunanya adalah untuk memfilter data jaringan, dengan data neural
# Skenario 1 : Data masuk di sampling jarang-jarang dan di prediksi berdasarkan hasil dari LSTM, atau Elman RNN
```

6. Untuk di Snort Web Interface | Nanti setelah ujian

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
