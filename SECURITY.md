# Güvenlik durumu ve güvenli kurulum

## 15 Ekim 2026 güncellemesi

Varsayılan ortamda `qiskit==1.2.4`, yamalı **`qiskit==1.4.6`** sürümüyle değiştirildi. Eski sürüm aşağıdaki iki bildirimin etkilenen sürüm aralığındaydı:

| Bildirim | Risk | İlgili düzeltme |
|---|---|---|
| [CVE-2025-2000](https://github.com/Qiskit/qiskit/security/advisories/GHSA-6m2c-76ff-6vrf) | Kötü amaçlı eski QPY yüklenirken kod çalıştırma | Qiskit 1.4.2 ve sonrası; bu repo 1.4.6 kullanır |
| [CVE-2025-1403](https://github.com/Qiskit/qiskit/security/advisories/GHSA-fpmr-m242-xm7x) | Bozuk SymEngine içeriğiyle işlem çökmesi | QPY 13 yolu Qiskit 1.3 ile eklendi; eski QPY 10–12 dosyalarının riskleri ayrıca dikkate alınmalıdır |

Notebook'larda QPY yükleme çağrısı bulunmamıştır. Güvenilmeyen QPY veya pickle dosyalarını açmayın; sürüm güncellemesi her eski dosya biçiminin güvenli olduğu anlamına gelmez. Kaydedilmiş notebook çıktılarındaki 1.2.4 sürümü geçmiş deneyin bilgisidir; güncel kurulum talimatı değildir.

`requirements-qiskit2.txt` içindeki Qiskit 2.1.2 ortamı ayrı tutulur. Her iki ortam GitHub Actions'ta kurulup uyumluluk ve bilinen bağımlılık açıkları açısından kontrol edilir. Yeni bir açık saptanırsa güvenlik adımı başarısız olur; açıklar taramadan hariç tutulmaz.

## Yerel doğrulama

Yeni bir sanal ortamda:

```bash
python -m pip install --upgrade 'pip>=26.2'
python -m pip install -r requirements.txt -r requirements-security.txt
python -m pip check
python -m pip_audit --local --strict
python scripts/validate_archive.py
python scripts/smoke_simulation.py
```

Qiskit 2 için ayrı sanal ortamda `requirements.txt` yerine `requirements-qiskit2.txt`, son komut yerine `python scripts/smoke_qiskit2.py` kullanın. `pip` güncellemesi, denetim sırasında kurulum aracının eski sürümünde görülen açıkların yeni ortamda taşınmasını önler.

Tarama, denetim anında bilinen paket açıklarını kontrol eder; tüm notebook'ların veya güncel IBM hizmetinin kapsamlı güvenlik incelemesi değildir. IBM hesap bilgilerine erişilmez ve donanım işi gönderilmez.

## Kimlik bilgileri

Anahtarları, CRN değerlerini veya `saved_accounts()` çıktısının tamamını commit etmeyin. Orijinal ZIP'teki eski anahtar public repo ve ilk altı commit'in erişilebilir geçmişinde bulunmadı. Bu kontrol anahtarın IBM tarafında iptal edildiğini göstermez; anahtarın sahibi iptal işlemini kendi hesabından tamamlamalıdır.

CI yalnız okuma yetkisi kullanır, IBM sırrı gerektirmez ve checkout kimlik bilgisini kalıcı olarak saklamaz. Kullanılan GitHub Actions referansları doğrulanmış tam commit SHA'larına sabitlenmiştir.
