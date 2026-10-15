# Yayına hazırlık doğrulaması

**Tarih:** 15 Ekim 2026 · **Ortam:** Linux, Python 3.12.14

Bu kontroller public portföy düzenlemesini doğrular. Geçmiş deneylerin tamamının yeniden çalıştırıldığı iddia edilmez.

| Kontrol | Sonuç | Kapsam |
|---|---|---|
| Temiz sanal ortamda `requirements.txt` kurulumu | Geçti | Qiskit 1.2.4, Aer 0.16.0, QML 0.8.4, Runtime 0.29.0 ve tanımlı bağımlılıklar |
| `python -m pip check` | Geçti | Paket bağımlılıkları arasında bildirilmiş çelişki yok |
| Notebook şeması | Geçti | 11 notebook, nbformat doğrulaması |
| Python sözdizimi | Geçti | 256 kod hücresi; iki kurulum/magic hücresi AST kontrolü dışında |
| Kodun korunması | Geçti | ZIP ile karşılaştırmada 254 kod hücresi aynı; 08–09'daki iki hesap yazdırma hücresi güvenlik için değiştirildi |
| Referans veri | Geçti | CSV içindeki 150 gözlemin özellik, etiket ve tür adları `load_iris()` ile aynı |
| Yerel dokümantasyon bağlantıları | Geçti | Markdown ve notebook girişlerindeki göreli bağlantıların hedefleri var |
| Belirli kimlik bilgisi kalıpları | Geçti | 08 ve 09'un token içeren iki hesap çıktısı kaldırıldı ve ilgili hücreler güvenli hale getirildi. Son taramada kimlik bilgisi değerleri yer tutucu/redaksiyon olarak doğrulandı; kalıp taraması mutlak garanti değildir. |
| Küçük Aer çalışma kontrolü | Geçti | 04'ten seçilmiş devre/eğitim hücreleri, 4 eğitim + 4 test örneği ve 1 epoch; parametre bağlama, olasılık ve gradyan kontrolleri |
| q0 parametre duyarlılığı | Geçti | Tam durum vektörüyle son RY katmanındaki q1–q3 açılarının q0 marjinalini değiştirmediği doğrulandı |
| VQC karar kuralı | Geçti | Kurulan QML 0.8.4'ün varsayılan `x % 2` kuralı ile 11'in soldaki bit kuralının farklı olduğu doğrulandı |

## Yayın öncesi güvenlik düzeltmesi

Otomatik yayın incelemesi, 08–09 notebook'larının `saved_accounts()` hesap çıktısında token bulunduğunu saptayıp ilgili yüklemeyi engelledi. İlk yerel tarama yalnız `token=...` biçimini kapsadığı için sözlük biçimindeki `'token': '...'` değerini kaçırmıştı. İki hesap çıktısı tamamen kaldırıldı; bunları üreten hücreler yalnız hesap adlarını yazdıracak şekilde değiştirildi; tarama hem atama hem sözlük/JSON alanlarını ve tüm metinsel çıktı türlerini kapsayacak şekilde genişletildi. Temizlenmiş dosyalar yeniden doğrulandı.

## Bilerek korunmuş tarihsel sorunlar

Dört kayıtlı hata çıktısı vardır: 03'te bir `NameError`, 05'te bir ve 06'da iki `KeyboardInterrupt`. Bunlar yayına hazırlık kontrollerinin hatası değildir; geçmiş deneylerin parçası olarak korunmuştur.

04'te `theta_init` etiketlerinin davranışı ters, 10–11'de ölçekleme sızıntısı ve 11'de karar kuralı uyuşmazlığı vardır. Bu sorunlar düzeltilmiş gibi sunulmadı; [yöntem incelemesinde](YONTEM_VE_SINIRLAR.md) açıklandı.

## Doğrulanmayanlar

- Notebook'ların tamamının temiz kernel ile baştan sona aynı çıktıları üretmesi.
- Geçmiş doğrulukların aynı seed/cihaz koşullarında tekrarı veya istatistiksel anlamlılığı.
- Güncel IBM hizmetinde donanım notebook'larının uyumluluğu; yeni donanım işi gönderilmedi.
- Ayrı Qiskit 2 ortamının kurulumu ve 07'nin uçtan uca çalışması.

GitHub Actions tanımı aynı yerel kontrolleri yeni commitlerde çalıştırmak için eklendi. Otomatik koşunun durumu GitHub'daki **Actions** bölümünden görülebilir; bu belge bağımsız yerel kontrollerin kaydıdır.
