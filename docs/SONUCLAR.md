# Kaydedilmiş deney sonuçları

[Ana sayfa](../README.md) · [Yöntem ve sınırlılıklar](YONTEM_VE_SINIRLAR.md)

Bu sayfadaki sayılar, sağlanan ZIP içindeki notebook çıktılarından alınmıştır. Yayına hazırlık sırasında bu deneylerin tamamı yeniden çalıştırılmamıştır. Aynı dosyada birden fazla çalışma ve farklı değerlendirme kapsamları bulunabilir. Tablo bir model sıralaması değildir.

## Simülasyon kayıtları

| Dosya / çıktı | Eğitim doğruluğu | Test doğruluğu | Kapsam ve yorum |
|---|---:|---:|---|
| [01](../notebooks/01_simulation/01_qnn_statevectorsampler_v1.ipynb) — `Final ... Accuracy` | %77,6 | %84,8 | 33 test örneği; StatevectorSampler ile örnekleme |
| [01](../notebooks/01_simulation/01_qnn_statevectorsampler_v1.ipynb) — klasik SVM | — | %100,0 | Aynı dosyadaki 33 örneklik klasik referans |
| [02](../notebooks/01_simulation/02_qnn_statevectorsampler_v2.ipynb) — `Final ... Accuracy` | %79,1 | %81,8 | 33 test örneği |
| [03](../notebooks/01_simulation/03_qnn_aer_v1.ipynb) — `Final ... Accuracy` | %88,1 | %84,8 | 33 örnek; ayrıca daha önceki bir hücrede `NameError` kaydı vardır |
| [04](../notebooks/01_simulation/04_qnn_aer_v2.ipynb) — son değerler | %80,6 | %87,9 | 29/33; ayrı yeniden çalıştırma/tekrar ortalaması değildir |
| [07](../notebooks/02_ibm_hardware/07_qnn_aer_train_ibm_test_tuning.ipynb) — `Epoch 09` | %79,1 | %81,8 | Son epoch; test doğruluğu eğitim boyunca izlenir |
| [09](../notebooks/03_finetuning/09_finetuning_v3.ipynb) — `Gen 29` | %85,1 | %75,8 | Son nesil; önceki nesillerde farklı test skorları vardır |
| [10](../notebooks/04_vqc/10_vqc_aer.ipynb) — VQC | %85,1 | %78,8 | İki sınıf; bölmeden önce ölçekleme ve varsayılan sampler |
| [11](../notebooks/04_vqc/11_vqc_ibm.ipynb) — VQC eğitim çıktısı | %85,1 | %84,8 | İki sınıf; bölmeden önce ölçekleme |

## Donanım kayıtları

| Dosya / değerlendirme | Örnek | Kaydedilmiş doğruluk | Yorum |
|---|---:|---:|---|
| [05](../notebooks/02_ibm_hardware/05_qnn_ibm_train_test.ipynb) — ilk final test | 33 | %51,5 | Aynı dosyadaki başka eğitim denemelerinden ayrı bir kayıt |
| [05](../notebooks/02_ibm_hardware/05_qnn_ibm_train_test.ipynb) — Fast SPSA final, eşik 0,5 | 33 | %24,2 | Düşük sonuç korunmuştur; tek başına gürültüye atfedilmez |
| [05](../notebooks/02_ibm_hardware/05_qnn_ibm_train_test.ipynb) — eğitim verisinden seçilmiş eşik 0,3 | 33 | %51,5 | Eşik eğitim verisinden seçilmiştir; 06–07'deki test üzerinde eşik aramasıyla karıştırılmamalıdır |
| [06](../notebooks/02_ibm_hardware/06_qnn_aer_train_ibm_test.ipynb) — eşik 0,5, 256 shot | 8 | %62,5 (5/8) | Küçük test alt kümesi |
| [06](../notebooks/02_ibm_hardware/06_qnn_aer_train_ibm_test.ipynb) — seçilen eşik 0,45 | 8 | %75,0 (6/8) | Aynı sekiz test etiketiyle eşik seçilmiştir; bağımsız test skoru değildir |
| [07](../notebooks/02_ibm_hardware/07_qnn_aer_train_ibm_test_tuning.ipynb) — eşik 0,5, 1024 shot | 8 | %62,5 (5/8) | SamplerV2 çıktısı |
| [07](../notebooks/02_ibm_hardware/07_qnn_aer_train_ibm_test_tuning.ipynb) — seçilen eşik 0,42 | 8 | %75,0 (6/8) | Aynı test alt kümesinde eşik seçilmiştir |
| [08](../notebooks/03_finetuning/08_finetuning_v2.ipynb) — eşik 0,5, 256 shot | 33 | %75,8 (25/33) | Tam test kümesi; ayrı doğrulama tekrarı yok |
| [09](../notebooks/03_finetuning/09_finetuning_v3.ipynb) — eşik 0,5, 256 shot | 33 | %75,8 (25/33) | GA ağırlıklarıyla kaydedilmiş değerlendirme |
| [11](../notebooks/04_vqc/11_vqc_ibm.ipynb) — eşik 0,5, 256 shot | 33 | %33,3 (11/33) | Eğitimdeki VQC 0.8.4 `x % 2` (sağdaki bit) kuralından farklı bir bit marjinali okunur |
| [11](../notebooks/04_vqc/11_vqc_ibm.ipynb) — eşik 0,5, 2048 shot | 33 | %42,4 (14/33) | Aynı karar kuralı sorunu; artış bir tekrarlı deney sonucu değildir |

## Bu sonuçlardan ne çıkarılabilir?

Çalışma kayıtları, simülasyon kurma ve donanıma aktarım sürecini gösterir. Donanımda başarılı bir iş gönderilmesi, modelin doğru karar kuralıyla değerlendirildiği anlamına gelmez. Sekiz örneklik değerlendirmede tek bir doğru tahmin, doğruluğu 12,5 yüzde puan değiştirir.

Ölçekleme sızıntısı, test üzerinde eşik seçimi, farklı ansatz/optimizer/shot ayarları ve eksik tekrarlar nedeniyle burada yöntem üstünlüğü veya güvenilir bir genelleme karşılaştırması yapılamaz. Daha sağlam bir deney için aynı protokol altında ayrı doğrulama kümesi, tekrarlı seed çalışmaları ve klasik referanslarla karşılaştırma gerekir.
