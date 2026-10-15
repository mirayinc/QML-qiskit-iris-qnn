# Kurulum ve güvenli inceleme

[Ana sayfa](../README.md)

## Önerilen başlangıç

Önce notebook'ları kayıtlı çıktılarıyla okuyun. Yerel uygulama için **04_qnn_aer_v2.ipynb** ile başlayın. Dosyalar öğrenme günlüğü olduğundan eski tanısal hücreler ve yeniden tanımlar içerir. Özellikle donanım dosyalarında doğrudan “Run All” kullanmak geçmiş deney sırasını tekrar üretmez.

## Qiskit 1 ortamı — yamalı sürüm

Python 3.12 için:

```bash
python -m venv .venv
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade 'pip>=26.2'
python -m pip install -r requirements.txt
python -m pip check
python scripts/validate_archive.py
python scripts/smoke_simulation.py
jupyter notebook
```

Güncel kurulumda **Qiskit 1.4.6** kullanılır. Geçmiş notebook çıktılarında Qiskit 1.2.4, Aer 0.16.0, NumPy 2.1.3 ve scikit-learn 1.7.1 görülür; güvenlik yaması eski çıktıları yeniden üretilmiş sonuçlar gibi değiştirmez. **Qiskit Machine Learning 0.8.4**, 10–11'in çıktılarında yazılıdır. Runtime 0.29.0, sağlanan bağımlılık dosyasından korunmuştur. `qiskit-algorithms==0.3.1`, açık import için eklenmiş ve kurulumda doğrulanmıştır. Bu dosya, eski ortamın eksiksiz bir lockfile'ı değildir; yardımcı paketlerin sürümleri tümüyle arşivde kayıtlı değildir.

Notebook içinde bulunan `!pip install` hücreleri tarihsel kayıttır. Hazırlanan ortamı kurduktan sonra bu hücreleri atlayın; notebook içinden paket güncellemek, seçilen sürüm birleşimini değiştirebilir.

## 07 için ayrı Qiskit 2 ortamı

```bash
python -m venv .venv-qiskit2
source .venv-qiskit2/bin/activate
# Windows PowerShell: .venv-qiskit2\Scripts\Activate.ps1
python -m pip install --upgrade 'pip>=26.2'
python -m pip install -r requirements-qiskit2.txt
jupyter notebook
```

Qiskit 1 ve Qiskit 2 bağımlılıklarını aynı ortama üst üste kurmayın. Bu dosya, 07'de kayıtlı Qiskit 2.1.2 / Aer 0.17.1 ve arşivde verilen Runtime 0.41.1 ayrımını korur. Donanım API uyumluluğu için güncel IBM dokümantasyonunu ve kendi hesap erişiminizi ayrıca kontrol edin. Güvenlik güncellemesinde bu ortamın kurulumu, import'ları ve 07'nin seçilmiş yerel Aer çıkarım hücreleri doğrulandı. IBM hizmetinde uçtan uca donanım yürütmesi doğrulanmadı.

## IBM hesabı ve kimlik bilgileri

Simülasyon ve doğrulama scriptleri IBM hesabı istemez. 05–09 ve 11 ise hizmet bağlantısı/hardware hücreleri içerir. Gerçek IBM anahtarını, instance CRN değerini, yerel hesap dosyasını veya bunları gösteren çıktıları repoya koymayın. Arşivdeki `BURAYA_...` / `YOUR_...` değerleri yer tutucudur.

Güncel hesap kurulumunu [IBM'nin yerel ortam rehberinden](https://quantum.cloud.ibm.com/docs/en/guides/local-environment) izleyin. Eski notebook'taki hesap kaydetme hücreleri güncel bir kurulum sözleşmesi değildir. Kimlik bilgilerini yerel hesap kaydı veya ortam değişkenleriyle yönetin; notebook içine yazmayın. Hesap dosyası şifreli bir kasa olarak varsayılmamalıdır.

Önceden yapılandırılmış hesap için arşivde kullanılan yükleme biçimi:

```python
from qiskit_ibm_runtime import QiskitRuntimeService
service = QiskitRuntimeService()
```

Bu çağrının çalışması tüm sonraki eski API hücrelerinin uyumlu olduğunu kanıtlamaz. Sabit cihaz adları değişebilir; erişilebilir cihazı hesabınızdan seçin. Donanım işleri kendi kullanım/kota koşullarınıza tabidir.

## Doğrulama ne yapar?

- `validate_archive.py`: 11 notebook'un şemasını ve Python hücrelerinin sözdizimini inceler; yerel bağlantıları, referans verisini ve belirli gizli bilgi kalıplarını kontrol eder. Kod hücrelerini yürütmez.
- `smoke_simulation.py`: 04'teki seçilmiş Aer kurulum/eğitim hücrelerini küçük veri üzerinde çalıştırır; bir epoch, gradyan, olasılık ve q0 okuma duyarlılığını sınar. IBM'ye bağlanmaz.
- GitHub Actions aynı kontrolleri tekrarlar. Bu kontroller bütün notebook'ların baştan sona veya gerçek cihazda yeniden üretildiği anlamına gelmez.

## Bağımlılık güvenliği taraması

Her ortamda `python -m pip install -r requirements-security.txt` ve ardından `python -m pip_audit --local --strict` çalıştırabilirsiniz. GitHub Actions iki ortamı da ayrı denetler; Qiskit 1 için 04'ün küçük eğitim akışını, Qiskit 2 için 07'nin yerel Aer çıkarımını kontrol eder. [Güvenlik yamasının kapsamı](../SECURITY.md).
