# 📈🤖 FinPrompt (Beta)

> ⚠️ **DİKKAT:**
> Geliştirme geçici süreyle askıya alınmıştır.
> Uygulama sadece kendi OpenAI API anahtarınız ile çalışır. Ücretsiz API, sorgu limiti ve log mekanizması devre dışıdır.

**FinPrompt**, doğal dilde finansal veri sorgularınızı otomatik olarak Python koduna çevirip çalıştıran, kullanıcı dostu bir finansal analiz uygulamasıdır. Şu an beta aşamasında olup, **İş Yatırım** verileriyle çalışmaktadır.

---

## 🚀 Özellikler

- **Doğal Dil Sorguları:** Türkçe (veya İngilizce) cümlelerle hisse ve finansal veri talebinde bulunabilirsiniz.
- **Otomatik Kod Üretimi:** Sorgunuz, OpenAI GPT-4o ile otomatik olarak Python koduna çevrilir ve Streamlit arayüzünde çalıştırılır.
- **Kod ve Sonuç Tablosu:** Oluşturulan Python kodunu görebilir, çıktısını tablo halinde inceleyebilirsiniz.
- **Kullanıcı Dostu Arayüz:** Tüm kullanılabilir sütunlar ve örnek sorgular uygulama içinde gösterilir.
- **Veri Kaynağı ve Mod Seçimi:** Şimdilik sadece İş Yatırım veri kaynağı desteklenir. İki mod bulunur:
    - **Tarihsel Veriler**
    - **Finansal Tablolar** (3 tip tablo: Solo/SPK, Konsolide/UFRS, Solo/UFRS)
- **Kolay API Anahtarı Yönetimi:** Kendi OpenAI API anahtarınızı girebilir veya ücretsiz (sınırlı) modda kullanabilirsiniz.
- **Kullanım Limiti:** Ücretsiz modda, IP başına günde 25 sorgu hakkınız vardır. Limitler her gece 00:00'da sıfırlanır.
- **Hata Yönetimi ve Loglama:** Oluşan hatalar ve kullanıcı sorguları anonim olarak geliştiriciye iletilir.

---

## ⚠️ Gizlilik & Kullanım Limiti

- **Sorgular ve hata mesajları**, ürünün geliştirilmesi amacıyla anonim şekilde Supabase veritabanına kaydedilir.
- **API anahtarı girmeden** kullanırsanız, IP adresiniz üzerinden günlük sorgu limiti uygulanır (25 sorgu/gün).
- **IP adresiniz alınamazsa**, güvenlik nedeniyle ücretsiz erişim devre dışı kalır. (Local/test modunda bu kısıt devre dışıdır.)
- **API anahtarınızı girerseniz** tüm limitler kalkar ve sınırsız sorgu hakkınız olur.

---

## 🛠️ Kurulum

1. **Projeyi Klonlayın**

```bash
git clone https://github.com/kullanici/finprompt.git
cd finprompt
```

2. **Gerekli Kütüphaneleri Kurun**

```bash
pip install -r requirements.txt
```

3. **Ayar Dosyalarını Oluşturun**

`.streamlit/secrets.toml` dosyasını oluşturup aşağıdaki gibi doldurun:

```toml
OPENAI_API_KEY="openai-anahtarınız"
REDIS_HOST="redis-host"
REDIS_PORT="6379"
REDIS_PASSWORD="redis-parola"
REDIS_DB="0"
SUPABASE_URL="supabase-url"
SUPABASE_KEY="supabase-key"
```

Sadece OpenAI API anahtarı ile çalıştırmak isterseniz diğer alanları boş bırakabilirsiniz. Ancak bu durumda sadece kendi anahtarınızla sorgu yapabilir, ücretsiz modun limit/mekanizmasından ve hata loglamadan yararlanamazsınız.

4. **Uygulamayı Başlatın**

```bash
streamlit run app.py
```

---

## 👀 Kullanım

- Ana ekranda OpenAI API anahtarınızı girebilir veya ücretsiz modda devam edebilirsiniz.
- Veri kaynağı olarak "İş Yatırım" seçilidir. Mod olarak "Tarihsel Veriler" veya "Finansal Tablolar" arasında seçim yapabilirsiniz.
- Mod seçiminden sonra kullanılabilir sütunlar ve örnek sorgular uygulamada görünür.
- Sorgunuzu doğal dilde yazarak "Kodu Oluştur ve Sonuçları Getir" butonuna tıklayın.
- Hem üretilen Python kodunu hem de sonuç tablosunu görebilirsiniz.
- Kodda hata olursa hata mesajı ekranda gösterilir ve geliştiriciye iletilir.

---

## 📝 Örnek Sorgular

- 2024 yılı için AKBNK ve THYAO hisselerinin aylık ortalama kapanış verilerini göster
- SISE'nin Ocak-Mart 2025 kapanış fiyatlarını getir
- TUPRS hissesinin son 7 iş günündeki en düşük ve en yüksek değerlerini getir
- 2023 ve 2024 yılları için AKBNK ve THYAO'nun finansal tablolarını getir
- SISE'nin son 4 çeyrek finansal tablosu
- TUPRS'ın bu yıla ait tablolarını TRY ve USD cinsinden getir

---

## ⚙️ Teknik Detaylar

- Kod üretiminde OpenAI GPT-4o modeli kullanılır.
- Kodun çıktısı, `pandas` ve `requests` dışında ek paket gerektirmez.
- Tüm sütun kontrolleri ve filtrelemeler, ilgili veri modunda `COLUMN_DESCRIPTIONS` sözlüğü ile yapılır. (Fuzzy matching yoktur.)
- Tarihsel veri modunda: Tüm kod çıktısı, dayfirst formatında tarih ve uppercase hisse kodları ile gelir. Kodun sonunda bir `df` DataFrame'i bulunur.
- Finansal tablo modunda: İlgili tablo tipi ve döviz seçimine göre sütunlar ve sorgular oluşturulur, istenen dönemler ve son N çeyrek gibi talepler otomatik algılanır.
- Kod çıktısı arayüzde gösterilir ve çalıştırıldığında sonucu tablo halinde Streamlit'te sunar.
- Hata olması durumunda hata mesajı ve detaylı traceback otomatik olarak geliştiriciye Supabase ile loglanır.
- Ücretsiz modda, rate-limit Redis ile takip edilir. (IP başına günlük sorgu limiti.)

---

## ⚡ Bilinen Kısıtlamalar ve Sık Sorulan Sorular

- Hangi veri kaynakları destekleniyor?
  Şimdilik sadece İş Yatırım veri kaynağı destekleniyor. Farklı kaynaklar ilerleyen sürümlerde eklenebilir.

- API anahtarı olmadan kullanabilir miyim?
  Evet, ücretsiz modda IP başına günde 25 sorgu hakkınız olur. Ancak IP adresiniz alınamazsa ücretsiz mod çalışmaz. (Test modunda devre dışı kalır.)

- Kod çalışmazsa ne olur?
  Hata mesajı ekranda gösterilir ve hata otomatik olarak geliştiriciye iletilir.

- Veriler ve sorgularım kayıt ediliyor mu?
  Sadece sorgu cümlesi ve hata mesajları anonim olarak ürünün geliştirilmesi amacıyla Supabase üzerinde tutulur. Sonuç verileriniz veya kimlik bilgileriniz kaydedilmez.

- Kod veya tablo üretilemiyorsa?
  Sorgunuz finansal veriyle ilgili değilse veya anlamlı değilse sistem otomatik hata verir.

---

## 📬 Katkı ve Geri Bildirim

- Her türlü hata bildirimi veya geliştirme önerisi için issue açabilirsiniz veya pull request gönderebilirsiniz.
- Beta aşamasında olduğu için kullanım sırasında oluşan hatalar anonim olarak geliştiricilerle paylaşılır.

---

## 📄 Lisans

MIT Lisansı