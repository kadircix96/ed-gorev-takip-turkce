# 🚀 Elite Dangerous Mission & Cargo Tracker HUD

Elite Dangerous oyuncuları için geliştirilmiş, şeffaf, oyun penceresinin üstünde durabilen (Always on Top) ve anlık olarak görev ve kargo takibi yapan hafif bir HUD aracıdır. Oyun loglarını (`Journal` ve `Cargo.json`) anlık okuyarak çalışır.

## Güncellemeler
* **v1.0.1:** Bir gün önce eklenmiş olan görevler gözümüyordu, düzeltildi.

## 🌟 Özellikler
* **Anlık Görev Takibi:** Alınan teslimat ve bağış görevlerini otomatik listeler.
* **Akıllı İhtiyaç Listesi:** Tüm görevler için gereken toplam mal miktarını hesaplar.
* **Canlı Market Kontrolü:** Bulunduğunuz istasyonun marketinde ihtiyaç duyduğunuz mallardan stok varsa anında uyarır `🏪 [MARKETTE VAR: X]`.
* **Kargo Durumu:** Geminizin anlık kargo doluluğunu ve kapasitesini gösterir.
* **Oyun İçi Kullanım:** Şeffaf arkaplanı sayesinde oyun ekranını kapatmaz, ekranda sol tık ile istenilen yere sürüklenebilir.

## 📸 Ekran Görüntüleri
**Hud Görünümü** ![HUD Görünümü](1.png)

**Market Görünümü** ![Market Görünümü](2.png)

**Donate görevlerinin commodities markette gözükmeme çözümü** ![Donate Görünmeme Sorunu Çözümü](3.png)

**Eksik materyallerin belirtilmesi, kaç adet almanız gerektiği belirtilir.** ![Eksik Materyalin Belirtilmesi Bkz: Advanced Medicines](4.png)

---

## 📥 Nasıl Kurulur ve Kullanılır?

### Seçenek 1: Direkt Çalıştırma (Tavsiye Edilen)
En kolay ve hızlı yöntemdir. Hiçbir program kurmanıza gerek yoktur.
1. Sağ taraftaki **Releases** bölümünden (veya [buraya tıklayarak](#)) `mission.exe` dosyasını indirin.
2. Dosyaya çift tıklayıp çalıştırın ve oyuna girin!

### Seçenek 2: Kaynak Kodundan Çalıştırma (Python Gerekli)
Eğer .exe kullanmak istemiyor ve doğrudan açık kaynak kodunu çalıştırmak istiyorsanız bu adımları izleyin:

**Adım 1: Python Kurulumu (Eğer yüklü değilse)**
1. [Python'un resmi sitesine](https://www.python.org/downloads/) gidin ve en güncel sürümü indirin.
2. ⚠️ **ÇOK ÖNEMLİ:** İndirdiğiniz kurulum dosyasını açtığınızda, ilk ekranda alt tarafta bulunan **"Add Python.exe to PATH"** (veya benzeri) kutucuğunu **kesinlikle işaretleyin**. İşaretlemezseniz script çalışmaz. Ardından "Install Now" diyerek kurun.

**Adım 2: Dosyaları İndirme**
1. Bu sayfanın sağ üst köşesindeki yeşil **`<> Code`** butonuna tıklayın.
2. **"Download ZIP"** seçeneğini seçerek dosyaları bilgisayarınıza indirin ve klasöre çıkartın.

**Adım 3: Çalıştırma**
1. Klasörün içindeki `baslat.bat` dosyasına çift tıklayın.
2. Bu dosya, uygulamanın çalışması için gereken eksik kütüphaneleri (PyQt6) bilgisayarınıza otomatik olarak kuracak ve uygulamayı başlatacaktır.

---

## ⚠️ Virüs Tarama (False Positive) Hakkında Önemli Not
`mission.exe` dosyası, Python kodunun herkes tarafından tek tıkla kolayca kullanılabilmesi için **PyInstaller** kütüphanesi kullanılarak derlenmiştir. PyInstaller, tüm Python altyapısını tek bir `.exe` dosyasına sıkıştırdığı için, Windows Defender ve VirusTotal üzerinde bazı sezgisel (heuristic) yapay zeka motorları (örn: *Wacatac.B!ml*) tarafından **yanlış alarm (False Positive)** üretebilir.

Bu durum, PyInstaller kullanan neredeyse tüm açık kaynak projelerde yaşanan zararsız ve bilinen bir teknik sorundur. Şeffaflık adına VirusTotal tarama sonuçlarını aşağıya bırakıyorum:

🛡️ **VirusTotal Tarama Sonuçları:** [Buraya Tıklayarak İnceleyebilirsiniz](https://www.virustotal.com/gui/file/e2c187de98bc219f13d8195e88c34195d718ee2c0ff7bf6b1733d010198916a7/detection)

Güvenmeyen veya şüphe duyan kullanıcılar doğrudan `.py` uzantılı açık kaynak kodunu inceleyebilir ve yukarıdaki **Seçenek 2** adımlarını uygulayarak kendi bilgisayarlarında güvenle çalıştırabilirler.

## 🛠️ Geliştirici İçin
Kodu kendiniz derlemek isterseniz, klasör içindeki `exe_yap.bat` dosyasını çalıştırarak bağımlılıkları yükleyip kendi temiz `.exe` dosyanızı otomatik olarak oluşturabilirsiniz.
