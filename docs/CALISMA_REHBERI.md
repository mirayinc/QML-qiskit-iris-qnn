# Çalışma rehberi: Ne yapıldı, neden yapıldı?

[Ana sayfa](../README.md) · [Sonuçlar](SONUCLAR.md) · [Yöntem incelemesi](YONTEM_VE_SINIRLAR.md)

Bu rehber, dosya adlarını değil içerikteki gerçek modelleme akışını esas alır. Notebook başına eklenen ilk hücre yayına hazırlık notudur; devamındaki kodlar staj dönemindeki deneylerin gelişimini gösterir. Staj kurumu ve tarihleri arşivde doğrulanmadığı için eklenmemiştir.

## 1. Simülasyonda temel modeli kurma

| Dosya | Yapılan işlem | Neden? | Okuma notu |
|---|---|---|---|
| [01 — StatevectorSampler v1](../notebooks/01_simulation/01_qnn_statevectorsampler_v1.ipynb) | İlk 100 Iris gözlemi, dört RX kapısı, halka CX, RY parametreleri, q0 ölçümü, MSE, ileri sonlu fark ve eğitim döngüsü; SVM karşılaştırması | Veri → devre → olasılık → kayıp → parametre güncellemesi zincirini elle kurmak | Özellikler ölçeklenmez. StatevectorSampler sonlu shot kullanır. SVM sonucu bir klasik referanstır. |
| [02 — StatevectorSampler v2](../notebooks/01_simulation/02_qnn_statevectorsampler_v2.ipynb) | Benzer modelde gradyan ve eğitim kodunun yeniden düzenlenmesi | İlk uygulama üzerinden kod akışını geliştirmek | v2 adı, tüm mantık sorunlarının çözüldüğünü veya daha yüksek doğruluğu göstermez. |
| [03 — Aer v1](../notebooks/01_simulation/03_qnn_aer_v1.ipynb) | Eğitim verisinde fit edilen [0, π] ölçekleme ve Aer counts çıktılarından p(1) hesaplama | Açısal kodlamayı düzenlemek ve Aer yürütmesini öğrenmek | Kaydedilmiş `NameError`, eğitim geçmişi oluşmadan grafik çizme çağrısından gelir. |
| [04 — Aer v2](../notebooks/01_simulation/04_qnn_aer_v2.ipynb) | Parametreli devre şablonu, tek sefer transpile, her çağrıda parametre bağlama, merkezi sonlu fark ve karıştırılmış eğitim | Tekrarlanan devre derlemesini azaltmak ve gradyan yaklaşımını değiştirmek | Yerel inceleme için en uygun başlangıç. Son RY katmanındaki üç parametre ideal q0 okumasında etkisizdir; `theta_init` seçeneklerinin davranışı adlarının tersidir. |

Simülasyon başlangıçta kuyruk gerektirmeden kodlama ve eğitim akışını incelemeyi sağlar. Buradaki Aer kullanımı açık bir gürültü modeli içermediğinden fiziksel cihazın bütün hata kaynaklarını taklit etmez.

## 2. Gerçek IBM donanımını araştırma

| Dosya | Yapılan işlem | Neden? | Okuma notu |
|---|---|---|---|
| [05 — Donanımda eğitim/test](../notebooks/02_ibm_hardware/05_qnn_ibm_train_test.ipynb) | Cihaz seçimi, transpile, küçük batch, BCE ve SPSA; ardından daha derin ansatz denemesi | Eğitim döngüsünü gerçek cihaz üzerinde deneyerek kuyruk, shot ve sonuç formatı etkilerini görmek | Tek bir temiz eğitim akışı değildir: yeniden tanımlar, tanısal hücreler ve yarım kalan depth-2 denemesi vardır. |
| [06 — Aer eğitimi, IBM testi](../notebooks/02_ibm_hardware/06_qnn_aer_train_ibm_test.ipynb) | Parametreleri Aer ile eğitme, IBM'e bağlanmış devre gönderme, 8 örnekte test ve eşik taraması | Donanım üzerinde pahalı eğitim yerine yalnız çıkarımı denemek | %62,5 sabit eşik ve %75 aynı test üzerinde ayarlanmış eşik farklı niteliktedir. Daha sonraki denemeler kesilmiştir. |
| [07 — SamplerV2 ve tuning](../notebooks/02_ibm_hardware/07_qnn_aer_train_ibm_test_tuning.ipynb) | Qiskit 2 ortamında SamplerV2, 8 devrelik donanım testi, p(1) ve simülasyon karşılaştırması | Primitive sürüm değişimini ve sonuç okuma akışını araştırmak | Eşik sekiz test etiketinden seçilir. Bu seçim için ayrı doğrulama kümesi yoktur. |

`Sampler` ile `SamplerV2` gibi API adlarının bir arşivde birlikte bulunması, her dosyanın aynı ortamda çalışacağı anlamına gelmez. Güncel donanım yürütmesi için bu bölümün ayrıca uyarlanması gerekir.

## 3. Optimizasyon ve değerlendirme kapsamını değiştirme

| Dosya | Yapılan işlem | Neden? | Okuma notu |
|---|---|---|---|
| [08 — Fine-tuning v2](../notebooks/03_finetuning/08_finetuning_v2.ipynb) | Aer üzerinde MSE ve merkezi sonlu fark ile eğitim; IBM'de test kümesinin tamamını değerlendirme | Küçük alt küme denemesini 33 test gözlemine genişletmek ve eğitim ayarlarını araştırmak | Dosya adına rağmen IBM üzerinde yeniden eğitim iddiası yoktur. Kaydedilmiş donanım çıktısı 25/33'tür. |
| [09 — Fine-tuning v3 / GA](../notebooks/03_finetuning/09_finetuning_v3.ipynb) | Parametre vektörlerinden popülasyon, eğitim doğruluğuna dayalı fitness, elitizm, çaprazlama, mutasyon | Gradyan tahmini yerine türevsiz bir arama yaklaşımını denemek | Eski docstring'deki “Fitness: test accuracy” ifadesine karşın gerçek fitness eğitim kümesinde hesaplanır. Test doğruluğu yalnız izlenir. |

Bu denemeler GA'nın veya sonlu farkın üstünlüğünü kanıtlamaz. Aynı bölme, seed, shot bütçesi, ölçüm kuralı ve tekrar protokolüyle kontrollü karşılaştırma yapılmamıştır.

## 4. Hazır VQC bileşenleriyle çalışma

| Dosya | Yapılan işlem | Neden? | Okuma notu |
|---|---|---|---|
| [10 — VQC](../notebooks/04_vqc/10_vqc_aer.ipynb) | 150 gözlemle keşif, sonra iki sınıfa filtreleme; ZZFeatureMap, RealAmplitudes, SPSA ve cross-entropy | Kuantum sınıflandırıcıyı hazır bir arayüzle kurmak ve elle yazılan döngüyle farkını görmek | AerEstimator tanımlanır fakat VQC'ye verilmez; dosya adı Aer kullanımının kanıtı değildir. Ölçekleme bölmeden önce fit edilir. |
| [11 — VQC / IBM denemesi](../notebooks/04_vqc/11_vqc_ibm.ipynb) | VQC ağırlıklarını alıp cihaz için devre bağlama, tüm qubitleri ölçme, iki shot bütçesiyle test | Hazır sınıflandırıcının ağırlıklarını gerçek cihaza taşıma sorununu incelemek | VQC 0.8.4'ün sağdaki bit (`x % 2`) kararı yerine soldaki bit okunur; bu farklı bir karar kuralıdır. Sonuçlar doğrudan simülasyon/donanım performans farkı olarak kullanılamaz. |

## Bu çalışmaların öğrettiği noktalar

1. Veri ölçekleme ve bölme sırası, kuantum modelinde de değerlendirme güvenilirliğini etkiler.
2. Modelin devresi kadar **çıktının hangi kuralla sınıfa dönüştürüldüğü** de korunmalıdır.
3. Devreyi bir kez derlemek, eğitim sırasında tekrarlanan işi azaltır.
4. Shot sayısı, optimizer, rastgelelik ve cihaz koşulları sonuçlarla birlikte kaydedilmelidir.
5. Başarısız ve kesilmiş deneyler de yöntem seçiminin gerekçesini açıklayan çalışma kayıtlarıdır.
