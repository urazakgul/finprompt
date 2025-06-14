# 📈🤖 FinPrompt (Beta)

FinPrompt, **doğal dilde finansal veri sorgularını otomatik olarak Python koduna çevirip çalıştıran** kullanıcı dostu bir finansal analiz uygulamasıdır. Şu an beta aşamasında olup, **İş Yatırım** verileriyle çalışmaktadır.

---

## 🚀 Özellikler

- **Doğal Dil Sorguları:** Doğrudan Türkçe cümlelerle hisse ve finansal veri talebinde bulunabilirsiniz.
- **Otomatik Kod Üretimi:** Girilen sorgu OpenAI API ile Python koduna çevrilir ve sonuçlar otomatik olarak tabloya dökülür.
- **Kolay API Anahtarı Yönetimi:** Kendi OpenAI API anahtarınızı girebilir veya ücretsiz (sınırlı) modda kullanabilirsiniz.
- **Kullanıcı Dostu Arayüz:** Tüm kullanılabilir sütunlar ve örnek sorgular gösterilir.
- **Veri Kaynağı Seçimi:** Şimdilik sadece İş Yatırım kullanılmaktadır.
- **Kullanım Limiti:** Ücretsiz modda günde 25 sorgu hakkınız bulunur. Limitler her gece 00:00'da sıfırlanır.

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

Not: Sadece OpenAI API anahtarı ile çalıştırmak için diğer alanları boş bırakabilirsiniz ancak ücretsiz modda sorgu limiti devreye girer.

4. Uygulamayı Başlatın

```bash
streamlit run app.py
```

---

## 👀 Kullanım

- Ana ekranda API anahtarınızı girebilir veya ücretsiz modda devam edebilirsiniz.
- Veri Kaynağı olarak "İş Yatırım" seçilidir.
- "Kullanılabilir Sütunlar" bölümünden sorgulayabileceğiniz sütunları ve açıklamalarını görebilirsiniz.
- "Örnek Sorgular" kısmından nasıl sorgu yazabileceğinizle ilgili fikir edinebilirsiniz.
- Doğal dilde sorgunuzu yazarak "Kodu Oluştur ve Sonuçları Getir" butonuna tıklayın.
- Sonuçlar tablo olarak gösterilir; ister kodu görüntüleyin, ister sadece tabloyu inceleyin.

---

## 📝 Örnek Sorgular

- 2024 yılı için AKBNK ve THYAO hisselerinin aylık ortalama verilerini göster
- SISE'nin Ocak-Mart 2025 kapanış fiyatlarını getir
- TUPRS hissesinin son 7 iş günündeki en düşük ve en yüksek değerlerini getir

---

## ⚙️ Teknik Detaylar

- Kod üretiminde ChatGPT API (gpt-4o) kullanılır.
- Sütun eşleştirmede yalnızca `COLUMN_DESCRIPTIONS` sözlüğündeki başlıklar dikkate alınır. Fuzzy matching yapılmaz.
- Sonuçlar otomatik olarak bir DataFrame'e aktarılır.
- Sorgular ve hata mesajları, geliştiriciye iletilmek üzere anonim olarak Supabase'e loglanır.

---

## ⚡ Bilinen Kısıtlamalar

- Şu anda yalnızca İş Yatırım veri kaynağı destekleniyor.
- Ücretsiz modda günde 25 sorgu sınırı var.
- Üretilen kodun çalışabilmesi için verilen sorgunun anlamlı ve yeterli olması gerekir.
- Tüm veri alanlarını çekmek için "Kullanılabilir Sütunlar" kısmındaki başlıkları kullanın.

---

## 📬 Katkı ve Geri Bildirim

- Her türlü hata bildirimi veya geliştirme önerisi için issue açabilirsiniz ya da pull request gönderebilirsiniz.
- Beta aşamasında olduğundan, kullanım sırasında oluşan hatalar anonim olarak geliştiricilerle paylaşılır.

---

## 📄 Lisans

MIT Lisansı