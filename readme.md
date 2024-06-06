# Facial Emotion Recognition 

Bu proje, FER-2013 veri seti kullanılarak yüz ifadelerinin tanınması için bir model oluşturmayı amaçlamaktadır.

## Proje Açıklaması

Bu projede, FER-2013 veri seti kullanılarak bir derin öğrenme modeli eğitilmiş ve bu model ile yüz ifadeleri tanınmıştır. Projenin temel amacı, yüz ifadelerinin doğru bir şekilde tanınmasını sağlamaktır.

## Veri Setine Erişim

Proje için kullanılan veri setine aşağıdaki Kaggle bağlantılarından ulaşabilirsiniz:
- [Original Model with FER-2013 Dataset](https://www.kaggle.com/code/imano00/original-model-with-fer-2013-dataset/input)
- [Dataset3 Modified](https://www.kaggle.com/datasets/imano00/dataset3modified)

## Modele Erişim

Projede eğitilen ve kullanılan modele aşağıdaki Google Drive bağlantısından ulaşabilirsiniz:
- [Model Dosyaları](https://drive.google.com/drive/folders/1cgHWzb6Xnhqrb9WWG7mAhU1u7FubQOtD?usp=sharing)

Model indirildikten sonra `app` klasörü içine atılmalıdır.

## Kurulum Talimatları

Gerekli kütüphaneler `requirements.txt` dosyasında belirtilmiştir. Kütüphaneleri indirmek için aşağıdaki adımları takip edebilirsiniz:

1. Proje dizinine gidin:
    ```bash
    cd proje-dizini
    ```

2. Gerekli kütüphaneleri indirin:
    ```bash
    pip install -r requirements.txt
    ```

## Kullanım Talimatları

### Resimden Tespit

`app.py` dosyası ile resimden yüz tespiti ve duygu tahmini yapan bir uygulama geliştirilmiştir. Uygulamayı çalıştırmak için:

1. Model dosyasını `app` klasörü içine yerleştirin.
2. Uygulamayı çalıştırın:
    ```bash
    python app.py
    ```

### Gerçek Zamanlı Tespit

`real_time_recognition.py` dosyasında, kullanıcının web kamerasından yüz tespiti ve duygu tahmini yapılmaktadır. Gerçek zamanlı tespiti başlatmak için:

1. Model dosyasını `app` klasörü içine yerleştirin.
2. Gerçek zamanlı tespiti çalıştırın:
    ```bash
    python real_time_recognition.py
    ```
