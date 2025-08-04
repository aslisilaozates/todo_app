# To Do List Uygulaması

Python ile geliştirilmiş, JSON veri depolama kullanan modern bir To Do List uygulaması.

## Özellikler

-  **Görev Ekleme**: Başlık, açıklama ve öncelik ile görev ekleme
-  **Görev Listeleme**: Tüm, bekleyen veya tamamlanan görevleri listeleme
-  **Görev Tamamlama**: Görevleri tamamlandı olarak işaretleme
-  **Görev Silme**: Görevleri kalıcı olarak silme
-  **Görev Düzenleme**: Mevcut görevleri düzenleme
-  **İstatistikler**: Görev tamamlanma oranı ve öncelik dağılımı
-  **JSON Veri Depolama**: Görevler JSON dosyasında kalıcı olarak saklanır
-  **Öncelik Sistemi**: Düşük, orta, yüksek öncelik seviyeleri
-  **Zaman Takibi**: Görev oluşturma ve tamamlanma tarihleri
-  **Kullanıcı Dostu Arayüz**: Emoji'ler ve renkli çıktılar

## Kullanım

1. **Uygulamayı çalıştırın:**
   ```bash
   python todo_app.py
   ```

2. **Ana menüden seçim yapın:**
   - `1` - Yeni görev ekle
   - `2` - Tüm görevleri listele
   - `3` - Bekleyen görevleri listele
   - `4` - Tamamlanan görevleri listele
   - `5` - Görev tamamla
   - `6` - Görev sil
   - `7` - Görev düzenle
   - `8` - İstatistikler
   - `9` - Çıkış

## Teknolojiler

- **Python 3.x**: Ana programlama dili
- **JSON**: Veri depolama formatı
- **datetime**: Tarih ve saat işlemleri
- **os**: Dosya sistemi işlemleri

## Dosya Yapısı

```
todo_app/
├── todo_app.py          # Ana uygulama dosyası
├── tasks.json           # Görev verileri (otomatik oluşturulur)
└── README.md            # Bu dosya
```

## Veri Yapısı

Görevler JSON formatında şu yapıda saklanır:

```json
{
  "id": 1,
  "title": "Görev başlığı",
  "description": "Görev açıklaması",
  "priority": "orta",
  "status": "bekliyor",
  "created_at": "2024-08-04 00:00:00",
  "completed_at": null
}
```

## Özellikler Detayı

### Görev Ekleme
- Başlık zorunlu, açıklama opsiyonel
- Öncelik seviyeleri: düşük, orta, yüksek
- Otomatik ID atama ve tarih kaydetme

### Görev Listeleme
- Tüm görevleri görüntüleme
- Duruma göre filtreleme (bekliyor/tamamlandı)
- Öncelik ve durum ikonları ile görsel gösterim

### Görev Yönetimi
- Görev tamamlama (tarih kaydı ile)
- Görev silme (onay ile)
- Görev düzenleme (kısmi güncelleme)

### İstatistikler
- Toplam görev sayısı
- Tamamlanan/bekleyen görev sayısı
- Tamamlanma oranı
- Öncelik dağılımı

## Sistem Gereksinimleri

- Python 3.6 veya üzeri
- UTF-8 karakter desteği
- Dosya yazma izinleri

## Kurulum

1. Python'u yükleyin (https://python.org)
2. Proje klasörüne gidin
3. Uygulamayı çalıştırın:
   ```bash
   python todo_app.py
   ```

## Güvenlik

- JSON dosyası UTF-8 encoding ile kaydedilir
- Hatalı JSON dosyası durumunda otomatik yeniden oluşturma

- Dosya yazma hatalarına karşı koruma 
