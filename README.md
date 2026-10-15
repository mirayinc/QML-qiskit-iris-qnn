# Iris Üzerinde Kuantum Makine Öğrenmesi

**Qiskit ile QNN ve VQC deneyleri · Staj çalışmaları portföyü**  
Miray İnci Başaran · [English](README_EN.md) · [MIT](LICENSE)

Bu repo, staj dönemimde Iris çiçek veri seti üzerinde yürüttüğüm kuantum makine öğrenmesi çalışmalarını bir araya getirir. Kendi eğitim döngüsü olan basit bir QNN kurma, simülatörde eğitme, IBM Quantum donanımında deneme ve farklı optimizasyon yöntemlerini araştırma sürecini gösterir.

**Temel soru:** Klasik veriyi kuantum devresine nasıl kodlayabilir, devre parametrelerini nasıl eğitebilir ve simülasyondaki modeli gerçek donanıma nasıl taşıyabiliriz?

Bu bir **öğrenme ve deney arşividir**. Başarılı sonuçlarla birlikte düşük doğruluklar, yarım kalan denemeler ve yöntem sınırlılıkları da belgelenmiştir. Kuantum üstünlüğü veya üretime hazır bir model iddiası taşımaz.

## Ne yaptım, neden yaptım?

| Çalışma | Amaç |
|---|---|
| Iris verisini hazırlama ve eğitim/test ayırma | Küçük, bilinen bir problemde model akışını anlamak |
| RX kapılarıyla veri kodlama | Dört sayısal özelliği dört qubit üzerinde temsil etmek |
| CX bağlantıları ve RY parametreleriyle QNN | Veri kodlama, öğrenilebilir devre ve ölçüm ilişkisini kurmak |
| MSE, sonlu fark ve klasik parametre güncellemeleri | Hazır bir modelin arkasındaki eğitim döngüsünü elle kurmak |
| StatevectorSampler ve Aer deneyleri | Donanım kuyruğuna girmeden devre ve eğitim mantığını incelemek |
| IBM donanımında eğitim / simülasyondan donanıma aktarım | Shot, kuyruk, derleme ve sonuç okuma sorunlarını gözlemlemek |
| SPSA ve genetik algoritma denemeleri | Farklı parametre arama yöntemlerini araştırmak |
| Hazır VQC arayüzü | Elle kurulan yaklaşımı Qiskit Machine Learning bileşenleriyle karşılaştırmak |

## Veri ve kapsam

- Veri: `sklearn.datasets.load_iris()`; dört çiçek ölçümü.
- Tüm notebook’lardaki **sınıflandırıcı eğitimi iki sınıflıdır**: Setosa ve Versicolor, 100 gözlem.
- Eğitim/test: 67 / 33 gözlem. Bazı donanım denemeleri yalnız 8 test gözlemini kullanır.
- VQC dosyalarının ilk keşif grafikleri 150 gözlemi ve üç sınıfı gösterir; ardından modelleme verisi iki sınıfa filtrelenir.
- `data/iris.csv` inceleme amaçlı referans kopyadır; notebook’lar CSV’yi okumaz.

## Deneylerin sırası

| Aşama | Dosyalar | İçerik |
|---|---|---|
| 1. Simülasyon | [01–04](notebooks/01_simulation) | StatevectorSampler, Aer, ölçekleme, eğitim döngüsü ve parametreli devre |
| 2. IBM donanımı | [05–07](notebooks/02_ibm_hardware) | Donanımda SPSA, Aer eğitimi → IBM testi, SamplerV2 |
| 3. İyileştirme denemeleri | [08–09](notebooks/03_finetuning) | Merkezi sonlu fark ve genetik algoritma; 33 örnekte donanım değerlendirmesi |
| 4. Hazır sınıflandırıcı | [10–11](notebooks/04_vqc) | VQC, ZZFeatureMap, RealAmplitudes, SPSA ve donanım aktarımı |

Her dosyanın ne yaptığı ve hangi gerekçeyle eklendiği: **[Çalışma rehberi](docs/CALISMA_REHBERI.md)**.

## Sonuçları nasıl okumalı?

Arşivde Aer QNN ikinci sürümünün kayıtlı test doğruluğu **%87,9 (29/33)**; 08 ve 09 dosyalarının donanım çıktısı **%75,8 (25/33)** olarak görünür. İlk notebook’taki klasik SVM karşılaştırması **%100 (33/33)** verir. Bunlar farklı koşullarda kaydedilmiş tarihsel çıktılardır; ortak protokolle üretilmiş bir performans sıralaması değildir.

Özellikle şu ayrımlar önemlidir:

- StatevectorSampler durum vektörü kullanır, ancak bu notebook’larda sonuçlar sonlu shot ile örneklenir; ölçüm çıktıları shotsız ve deterministik değildir.
- Aer deneylerinde açık bir gürültü modeli yoktur. Sonlu shot örneklemesi, fiziksel cihaz gürültüsüyle aynı şey değildir.
- 06–07’de aynı test alt kümesinde eşik seçilmiştir; ayarlanmış doğruluk bağımsız test başarısı sayılmaz.
- 10–11’de ölçekleme eğitim/test ayrımından önce yapılmıştır. 10’da oluşturulan AerEstimator, VQC’ye bağlanmamıştır.
- 11’de VQC 0.8.4 eğitimi sağdaki bit (`x % 2`), donanım kodu soldaki bit kuralını kullanır. Bu sonuçlar aynı modelin adil simülasyon/donanım karşılaştırması değildir.

Tam kayıtlar: **[Sonuçlar](docs/SONUCLAR.md)** · Gerekçeler ve geliştirme adımları: **[Yöntem ve sınırlılıklar](docs/YONTEM_VE_SINIRLAR.md)**.

## İnceleme ve çalıştırma

Kodları okumak için kurulum gerekmez; notebook’lar GitHub’da geçmiş çıktılarıyla görüntülenebilir. Yerelde başlamak için **04 numaralı Aer notebook’unu** öneririm.

```bash
git clone https://github.com/mirayinc/qiskit-iris-qnn.git
cd qiskit-iris-qnn
python -m venv .venv
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade 'pip>=26.2'
python -m pip install -r requirements.txt
python scripts/validate_archive.py
python scripts/smoke_simulation.py
jupyter notebook
```

Python 3.12 ile yerel kontroller yapılmıştır. 07 için ayrı Qiskit 2 ortamı gerekir. Donanım notebook’ları eski API’ler ve etkileşimli denemeler içerir; tamamının güncel IBM hizmetinde baştan sona çalışacağı garanti edilmez. Donanım hücreleri kendi hesabınız üzerinden gerçek işler gönderir ve kota/kullanım tüketebilir. **[Kurulum, hesap güvenliği ve sürümler](docs/KURULUM.md)**.

## Güvenlik güncellemesi

Güncel kurulum **Qiskit 1.4.6** kullanır; notebook çıktılarındaki 1.2.4 geçmiş deney kaydıdır. Qiskit 1 ve Qiskit 2 ortamları her commit'te ayrı kurulup `pip-audit` ile taranır. **[Güvenlik notları ve yerel tarama](SECURITY.md)**.

## Bu repoda gösterilen beceriler

Python, NumPy, scikit-learn, Jupyter, kuantum devre tasarımı, açısal veri kodlama, model eğitimi, sayısal optimizasyon, görselleştirme, IBM Runtime sonuçlarının incelenmesi ve deneylerin eleştirel değerlendirilmesi.

Yayına hazırlıkta notebook’lara okuma notları eklendi, açıklamalar kodla eşleştirildi, yerel yol/iş kimliği gibi gereksiz çıktılar temizlendi ve bağımlılıklar düzenlendi. Deney kodunun geçmiş sürümleri korunmuştur. **[Değişiklik kaydı](CHANGELOG.md)** · **[Doğrulama kapsamı](docs/DOGRULAMA.md)**.
