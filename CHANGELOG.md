# Değişiklik kaydı

## 2026-10-15 — Qiskit güvenlik yaması

- Varsayılan Qiskit sürümü 1.2.4'ten **1.4.6**'ya yükseltildi; CVE-2025-2000 ve CVE-2025-1403 bildirimlerindeki etkilenen sürüm aralığından çıkıldı.
- Kurulumda `pip>=26.2` güncellemesi eklendi.
- `pip-audit` ve iki ortamı ayrı kuran CI matrisi eklendi; bilinen açık bulunduğunda kontrol başarısız olur.
- GitHub Actions referansları tam SHA'ya sabitlendi, checkout kimlik bilgisinin saklanması kapatıldı.
- 07 notebook'unun yerel Aer kodu için Qiskit 2 uyumluluk kontrolü ve SECURITY.md eklendi.
- Geçmiş notebook kodları ve deney çıktıları değiştirilmedi.

## 2026-10-15 — Public portföy yayınına hazırlık

Sağlanan `qiskit-iris-qnn.zip` temel alındı. Geçmişte yapılmış çalışmaları temsil etmek için eski tarihlere commit eklenmedi; yayın commitleri içerik grupları halinde oluşturuldu.

### Eklenenler

- Türkçe ana README ve İngilizce tanıtım.
- Her notebook'un başına amaç, gerekçe ve önemli sınırlılık notu.
- Deney rehberi, geçmiş sonuçların kapsamlı açıklaması, yöntem incelemesi ve kurulum rehberi.
- Kaynak arşiv/notebook SHA-256 kayıtları; yerel doğrulama ve simülasyon smoke kontrolü; otomatik GitHub kontrolü.

### Düzeltilen açıklamalar

- VQC eğitimleri üç sınıflı değil iki sınıflı olarak tanımlandı.
- StatevectorSampler, Aer, varsayılan VQC sampler'ı ve fiziksel gürültü ayrıldı.
- Test üzerinde eşik seçimi, ölçekleme sızıntısı, son parametre katmanının duyarlılığı ve VQC karar kuralı uyuşmazlığı açıklandı.
- GA kodunda fitness'ın eğitim doğruluğu olduğu belirtildi.
- QML sürümü varsayım yerine notebook çıktısındaki 0.8.4 ile sabitlendi; doğrudan kullanılan `qiskit-algorithms` bağımlılığı eklendi.
- MIT lisansındaki `YOUR NAME` yer tutucusu Miray İnci Başaran olarak dolduruldu.

### Paylaşım temizliği

- Notebook çıktılarına gömülü yerel geçici yollar ve iş kimlikleri temizlendi.
- Gereksiz hücre/platform metadata'sı ve desteklenmeyen zengin çıktı türleri çıkarıldı; PNG/devre/grafik ve metin sonuçları korundu.
- Bir markdown hücresine kopyalanmış arayüz kalıntısı çıkarıldı. Tarihsel teknik açıklamaların hatalı bölümleri baştaki not ve yöntem belgesinde düzeltildi.
- Kimlik bilgileri ve yerel ortam dosyaları için `.gitignore` genişletildi. Kaynakta çoğunlukla yer tutucular vardı; 08 ve 09'un kayıtlı hesap çıktılarında bulunan gerçek anahtar değerleri yayından önce çıkarıldı.

### Korunanlar ve sınırlar

Deney algoritmaları, sayısal model çıktıları, hata/yarıda kesilme kayıtları ve sürüm klasörleri korunmuştur. İstisna olarak 08–09'daki hesap kayıtlarını yazdıran iki hücre güvenlik için değiştirilmiş ve bu iki hücrenin eski çıktısı tamamen kaldırılmıştır. Dokümantasyon, bu çıktıları düzeltilmiş kodla yeniden üretilmiş gibi sunmaz. Yeni bir IBM donanım işi çalıştırılmamıştır. Staj kurumu, süre veya doğrulanmamış iş etkisi eklenmemiştir.
