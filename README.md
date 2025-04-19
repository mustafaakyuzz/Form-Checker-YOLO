# Mini Spor Asistanı – YOLO, OpenCV, MediaPipe ile Form Kontrol

Bu proje, vücut geliştirme hareketlerinin doğruluğunu değerlendirmek için geliştirilmiş bir görüntü işleme tabanlı **Mini Spor Asistanı**dır. Kullanıcıdan alınan videolar üzerinde çalışır; hareketleri tanır, açıları hesaplar ve **doğru form**da yapılmış tekrarları sayar.

## Projenin Özellikleri

-  Videodan görüntü çıkarma ve etiketleme
-  YOLO ile obje tanıma eğitimi (şınav pozisyonları)
-  MediaPipe Pose ile açı hesaplama (omuz, dirsek, kalça)
-  Form analizi ve tekrar sayacı
-  OpenCV ile video işleme ve görselleştirme

## Kullanılan Teknolojiler

- YOLOv8 : Hareketlerin Tespiti ve Sınıflandırılması.
- OpenCV : Videoyu açma, boundingbox alma ve üzerindeki yazıların yerini rengini ve fontunu belirlemede kullanıldı.
- MediaPipe Pose : Vücut üzerinde gerekli noktalara erişim için kullanıldı.
- Google Colab : YOLO Modelinin eğitilmesi için kullanıldı
- LabelImg : Görüntü Etiketleme İçin Kullanıldı

## Projenin Amacı

Spor yaparken en sık karşılaşılan sorunlardan biri, hareketin yanlış formda yapılmasıdır. Bu proje, özellikle şınav hareketinin:
- Doğru yapılıp yapılmadığını analiz eder.
- Vücut açılarını kontrol eder (örneğin dirsek 70° altı → iniş, 150° üzeri → kalkış).
- "Correct Form" olarak değerlendirilen her tekrarı sayar.
- Hareketin devam ettiği ya da yanlış yapıldığı durumlarda uyarı verir.

### Doğru Form Kriterleri

- **Dirsek Açısı**
  - `< 70°` → İniş pozisyonu
  - `> 150°` → Kalkış pozisyonu
- **Kalça Açısı**
  - `155° - 180°` → Vücut dikliği kontrolü

---

### OpenCV Kullanımı

-  Video oynatma ve frame işleme  
-  Bounding box çizimi  
-  Açıların ve form durumunun ekrana yazdırılması  
-  `'q'` tuşu ile çıkış veya video sonunda otomatik kapanma

---

### Sonuç ve Geliştirme Önerileri

Bu proje ile görüntü işleme temelli basit bir spor asistanı oluşturulmuştur.

#### Geliştirme Potansiyeli:
- Diğer egzersiz hareketleri (plank, squat, mekik vb.) için genişletme  
- Farklı açılardan çekilmiş videolarla daha kapsamlı analiz  
- Gerçek zamanlı çalışan mobil uygulama haline getirme

## Medium Hesabımı İnceleyin
Detaylı proje açıklaması için Medium Hesabımı : https://medium.com/@akyuzmustafa03 inceleyebilirsiniz.

