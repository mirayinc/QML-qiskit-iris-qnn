# Yöntem incelemesi ve geliştirme gerekçeleri

[Ana sayfa](../README.md) · [Çalışma rehberi](CALISMA_REHBERI.md) · [Sonuçlar](SONUCLAR.md)

Bu inceleme deney kodunun neden belirli sonuçları sınırlı biçimde desteklediğini açıklar. Tarihsel kod sessizce düzeltilip eski çıktılar yeni kodun sonucu gibi sunulmamıştır. Bu belgede önerilen değişiklikler, uygulanıp yeniden deney yapılmış özellikler değildir.

## Kullanılan yöntem

Manuel QNN'de her çiçek özelliği bir qubit'e RX dönüşüyle kodlanır. Halka CX kapıları qubit'ler arasında etkileşim kurar; RY açıları eğitilebilir parametrelerdir. q0 ölçümünden alınan `1` sayısı toplam shot sayısına bölünerek p(1) kestirilir. Sabit eşikli durumda p(1) ≥ 0,5, sınıf 1 olarak yorumlanır.

MSE ve BCE, tahmin olasılığı ile etiket arasındaki hatayı ölçmek için denenir. Sonlu fark, parametreyi küçük miktarda değiştirerek sayısal gradyan tahmini yapar. SPSA rastgele ortak pertürbasyonlarla iki yöndeki kayıpları kullanır; bu uygulamalarda izleme için ek kayıp/değerlendirme çağrıları da vardır. GA ise parametre popülasyonunu eğitim doğruluğuna göre seçer, çaprazlar ve mutasyona uğratır.

Hazır VQC akışında feature map ve ansatz birlikte eğitilir. `VQC`, QNN ile ilişkisiz başka bir model ailesi değildir; sınıflandırma için bir QNN'yi yüksek seviyeli arayüzle kullanır.

## Bulgu → etkisi → sonraki adım

| Bulgu | Sonuca etkisi | Gerekli geliştirme |
|---|---|---|
| 10–11'in eğitim hücresi `y == 0` veya `y == 1` maskesi kullanır | Eski README'deki üç sınıflı VQC açıklaması kodla uyuşmaz | Dokümantasyon iki sınıflı olarak düzeltildi; gerçek üç sınıf deneyi için model yeniden kurulmalı |
| 10–11'de `MinMaxScaler().fit_transform(X)` bölmeden önce çalışır | Test kümesinin min/max bilgisi eğitim dönüşümüne taşınır | Önce böl; scaler'ı yalnız eğitim kümesinde fit et; deneyleri yeniden çalıştır |
| 06–07'de eşik, ölçülen test alt kümesinin etiketleriyle seçilir | Eşik sonrası doğruluk iyimser bir keşif skorudur | Eşiği ayrı doğrulama kümesinde seç, testte sabitle |
| 10–11'de AerEstimator oluşturulsa da VQC'ye verilmez | `shots=2048` ayarının VQC eğitimine uygulandığı söylenemez | VQC'nin kullandığı sampler'ı açıkça belirt; eğitim ve değerlendirmeyi aynı primitive üzerinden kur |
| 11'de VQC 0.8.4 sağdaki bit (`x % 2`), donanım kodu soldaki bit marjinali kullanır | Eğitimde optimize edilen hedefle donanımda değerlendirilen hedef farklıdır | Aynı `x % 2` yorumunu donanım counts çıktısında uygula veya aynı sampler/interpret ile VQC tahmini kullan |
| 11'de soldaki bit “ilk qubit” diye tanımlanır | Standart ölçüm eşlemesinde q0 sağdaki bittir | Classical register ve bit sırasını açıkça eşle; eğitimde kullanılan yorum fonksiyonunu aynen koru |
| 04'te `theta_init="random"` ones, `"ones"` rastgele başlangıç üretir | Etiketler ile gerçek başlangıç ters düşer | Yeni deneyde başlangıç dallarını düzelt; geçmiş skorları yeni kodun sonucu gibi kullanma |
| Tek katmanlı manuel ansatz'ta CX halkasından sonra yalnız yerel RY kapıları ve q0 ölçümü vardır | Ölçülmeyen q1–q3 üzerindeki son rotasyonlar ideal q0 marjinalini değiştirmez; bazı parametreler etkisizdir | Öğrenilebilir katmanların ardından yeniden etkileşim/başka okuma tasarla ve duyarlılığı kontrol et |
| StatevectorSampler sonucu counts üzerinden, sonlu shot ile okunur | “Shotsız, deterministik çıktı” açıklaması bu koda uymaz | Tam olasılık isteniyorsa `Statevector.probabilities` gibi bir yol kullan; örnekleme ile tam olasılığı ayır |
| Aer'de açık noise model yoktur | Simülasyondaki rastgelelik fiziksel cihaz gürültüsü sayılmaz | İdeal, shot örneklemeli ve kalibre gürültülü deneyleri ayrı tanımla |
| Birçok dosyada test skoru her epoch/nesilde izlenir | Sonraki elle model seçimlerinde test bilgisi kullanılabilir | Model seçimini doğrulama kümesine taşı; test kümesini en sona sakla |
| 05–06'da fonksiyon yeniden tanımları ve kesilmiş işler vardır | Baştan sona tek çalıştırma ile geçmiş çıktılar yeniden üretilemeyebilir | Üretim/araştırma sürümünde tek eğitim ve tek sonuç okuma yolu oluştur |
| Tek split, küçük test kümeleri, tutarlı tekrar protokolü yoktur | Skor farkları yöntem üstünlüğü veya kuantum avantajı göstermez | Aynı veri/ölçekleme protokolüyle seed tekrarları, belirsizlik ve SVM/lojistik regresyon referansları ekle |

## Sürüme bağlı VQC karar kuralı

Kurulan **Qiskit Machine Learning 0.8.4** kaynak kodunda `VQC._get_interpret(2)` fonksiyonu `x % 2` döndürür. Bu, standart bit sıralamasında en sağdaki bitin sınıfı belirlemesidir; bütün bitlerdeki 1 sayısının parity'siyle karıştırılmamalıdır. Notebook 11 ise en soldaki biti okur. Güncel dokümantasyondaki genel “parity” ifadesi yerine bu arşivin gerçek sürümü esas alınmıştır.

## Son RY katmanının özel sınırlılığı

Bu bulgu, dört özelliğin devrede hiç etkisi olmadığı anlamına gelmez. Önceki CX halkası girdi özelliklerini q0 okumasına taşıyabilir. Sorun **son yerel parametre katmanındadır**: q0 dışındaki qubit'lere uygulanan birimsel dönüşümler, daha sonra başka etkileşim yoksa q0'ın indirgenmiş durumunu değiştirmez. Bu nedenle dört RY parametresi tanımlamak tek başına dört etkili öğrenilebilir parametre sağlamaz. 05'te ayrıca denenen depth-2 yapısı ayrı incelenmelidir.

## Teknik kaynaklar

Kaynaklar yöntem kavramlarını destekler; notebook içindeki geçmiş sayılar için kanıt notebook çıktılarıdır.

- [IBM: StatevectorSampler (Qiskit 1.1 API)](https://quantum.cloud.ibm.com/docs/en/api/qiskit/1.1/qiskit.primitives.StatevectorSampler) — sonlu shot ile örnekleme arayüzü.
- [Qiskit Machine Learning: VQC](https://qiskit-community.github.io/qiskit-machine-learning/stubs/qiskit_machine_learning.algorithms.VQC.html) — sampler ve interpret ilişkisi. Yayındaki kontroller ayrıca kurulan 0.8.4 kaynak kodu üzerinden yapıldı.
- [IBM: Bit ordering](https://quantum.cloud.ibm.com/docs/en/guides/bit-ordering) — klasik bit dizilerinin yorumu.
- [scikit-learn: Common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html) — veri sızıntısı ve yalnız eğitim verisinde fit etme ilkesi.
