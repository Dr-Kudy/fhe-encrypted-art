#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 FHE CRYPTO ART - DEMO LAUNCHER
Zama Creator Program

Hızlı demo için tüm-in-one launcher
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser
import threading
import time

class FHEArtLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_ui()
        self.web_process = None
        
    def setup_ui(self):
        """Launcher arayüzü"""
        self.root.title("🎨 FHE Crypto Art - Demo Launcher")
        self.root.geometry("600x500")
        self.root.configure(bg='#2C3E50')
        self.root.resizable(False, False)
        
        # Ana başlık
        header_frame = tk.Frame(self.root, bg='#34495E', height=100)
        header_frame.pack(fill=tk.X, pady=10, padx=10)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, 
                text="🔐 FHE ŞIFRELILI SANAT", 
                font=('Arial', 20, 'bold'), 
                fg='#ECF0F1', bg='#34495E').pack(pady=10)
        
        tk.Label(header_frame, 
                text="Zama Creator Program | Interactive Crypto Art Demo", 
                font=('Arial', 12), 
                fg='#BDC3C7', bg='#34495E').pack()
        
        # Demo seçenekleri
        self.setup_demo_options()
        
        # Sistem bilgisi
        self.setup_system_info()
        
        # Alt butonlar
        self.setup_bottom_buttons()
    
    def setup_demo_options(self):
        """Demo seçenekleri"""
        options_frame = tk.LabelFrame(self.root, text="🚀 Demo Seçenekleri", 
                                     fg='#ECF0F1', bg='#2C3E50', 
                                     font=('Arial', 14, 'bold'))
        options_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Buton stili
        btn_style = {
            'font': ('Arial', 12, 'bold'), 
            'bg': '#3498DB', 
            'fg': 'white',
            'activebackground': '#2980B9',
            'relief': tk.FLAT,
            'cursor': 'hand2',
            'pady': 15
        }
        
        # Desktop Demo
        desktop_frame = tk.Frame(options_frame, bg='#2C3E50')
        desktop_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(desktop_frame, text="🖥️ Desktop GUI Demo", 
                 command=self.launch_desktop_demo, **btn_style).pack(fill=tk.X, pady=2)
        
        tk.Label(desktop_frame, 
                text="• Tkinter tabanlı masaüstü uygulaması\n• Offline çalışır, kurulum gerektirmez", 
                font=('Arial', 10), fg='#95A5A6', bg='#2C3E50', 
                justify=tk.LEFT).pack(anchor=tk.W, padx=10)
        
        # Web Demo
        web_frame = tk.Frame(options_frame, bg='#2C3E50')
        web_frame.pack(fill=tk.X, padx=10, pady=5)
        
        web_btn_style = btn_style.copy()
        web_btn_style['bg'] = '#E74C3C'
        web_btn_style['activebackground'] = '#C0392B'
        
        tk.Button(web_frame, text="🌐 Web Demo (Flask)", 
                 command=self.launch_web_demo, **web_btn_style).pack(fill=tk.X, pady=2)
        
        tk.Label(web_frame, 
                text="• Modern web arayüzü, responsive design\n• Herhangi bir tarayıcıda çalışır", 
                font=('Arial', 10), fg='#95A5A6', bg='#2C3E50', 
                justify=tk.LEFT).pack(anchor=tk.W, padx=10)
        
        # Quick Test
        test_frame = tk.Frame(options_frame, bg='#2C3E50')
        test_frame.pack(fill=tk.X, padx=10, pady=5)
        
        test_btn_style = btn_style.copy()
        test_btn_style['bg'] = '#27AE60'
        test_btn_style['activebackground'] = '#229954'
        
        tk.Button(test_frame, text="🧪 Quick Test (Art Engine)", 
                 command=self.run_quick_test, **test_btn_style).pack(fill=tk.X, pady=2)
        
        tk.Label(test_frame, 
                text="• Sanat motorunu test eder, örnek görseller oluşturur\n• 30 saniye içinde tamamlanır", 
                font=('Arial', 10), fg='#95A5A6', bg='#2C3E50', 
                justify=tk.LEFT).pack(anchor=tk.W, padx=10)
    
    def setup_system_info(self):
        """Sistem bilgisi paneli"""
        info_frame = tk.LabelFrame(self.root, text="💻 Sistem Durumu", 
                                  fg='#ECF0F1', bg='#2C3E50', 
                                  font=('Arial', 12, 'bold'))
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Python versiyonu
        python_version = f"Python {sys.version.split()[0]}"
        self.python_status = tk.Label(info_frame, 
                                     text=f"✅ {python_version}", 
                                     font=('Arial', 10), 
                                     fg='#27AE60', bg='#2C3E50')
        self.python_status.pack(anchor=tk.W, padx=10, pady=2)
        
        # Kütüphane durumu
        self.check_dependencies()
    
    def check_dependencies(self):
        """Gerekli kütüphaneleri kontrol et"""
        dependencies = ['matplotlib', 'PIL', 'numpy', 'flask']
        
        for dep in dependencies:
            try:
                if dep == 'PIL':
                    import PIL
                else:
                    __import__(dep)
                status = "✅"
                color = "#27AE60"
            except ImportError:
                status = "❌"
                color = "#E74C3C"
            
            label = tk.Label(self.root, 
                           text=f"{status} {dep.capitalize()}", 
                           font=('Arial', 10), 
                           fg=color, bg='#2C3E50')
            label.pack(anchor=tk.W, padx=20)
    
    def setup_bottom_buttons(self):
        """Alt butonlar"""
        bottom_frame = tk.Frame(self.root, bg='#2C3E50')
        bottom_frame.pack(fill=tk.X, padx=10, pady=10)
        
        btn_style = {'font': ('Arial', 10), 'bg': '#95A5A6', 'fg': 'white', 'relief': tk.FLAT}
        
        tk.Button(bottom_frame, text="📖 README", 
                 command=self.show_readme, **btn_style).pack(side=tk.LEFT, padx=5)
        
        tk.Button(bottom_frame, text="🌐 Zama", 
                 command=lambda: webbrowser.open("https://zama.ai"), 
                 **btn_style).pack(side=tk.LEFT, padx=5)
        
        tk.Button(bottom_frame, text="📱 Social Share", 
                 command=self.social_share, **btn_style).pack(side=tk.LEFT, padx=5)
        
        tk.Button(bottom_frame, text="❌ Çıkış", 
                 command=self.safe_exit, **btn_style).pack(side=tk.RIGHT, padx=5)
    
    def launch_desktop_demo(self):
        """Desktop demo başlat"""
        self.show_loading("Desktop uygulaması başlatılıyor...")
        
        try:
            # Desktop uygulamasını başlat
            subprocess.Popen([sys.executable, 'art_app.py'], 
                           cwd=os.path.dirname(os.path.abspath(__file__)))
            
            messagebox.showinfo("Başarılı", 
                               "🖥️ Desktop uygulaması başlatıldı!\n\n"
                               "Yeni pencere açılması birkaç saniye sürebilir.")
            
        except FileNotFoundError:
            messagebox.showerror("Hata", 
                                "❌ art_app.py dosyası bulunamadı!\n\n"
                                "Tüm dosyaların aynı klasörde olduğundan emin olun.")
        except Exception as e:
            messagebox.showerror("Hata", f"Desktop uygulaması başlatılamadı:\n{str(e)}")
    
    def launch_web_demo(self):
        """Web demo başlat"""
        if self.web_process and self.web_process.poll() is None:
            messagebox.showinfo("Bilgi", 
                               "🌐 Web uygulaması zaten çalışıyor!\n\n"
                               "http://localhost:5000 adresini kontrol edin.")
            return
        
        self.show_loading("Web uygulaması başlatılıyor...")
        
        try:
            # Flask uygulamasını arka planda başlat
            self.web_process = subprocess.Popen(
                [sys.executable, 'web_art_generator.py'], 
                cwd=os.path.dirname(os.path.abspath(__file__)),
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            
            # 3 saniye bekle ve tarayıcıyı aç
            threading.Thread(target=self.open_browser_delayed, daemon=True).start()
            
            messagebox.showinfo("Başarılı", 
                               "🌐 Web uygulaması başlatıldı!\n\n"
                               "Tarayıcınız otomatik olarak açılacak.\n"
                               "Manuel: http://localhost:5000")
            
        except FileNotFoundError:
            messagebox.showerror("Hata", 
                                "❌ web_art_generator.py dosyası bulunamadı!")
        except Exception as e:
            messagebox.showerror("Hata", f"Web uygulaması başlatılamadı:\n{str(e)}")
    
    def open_browser_delayed(self):
        """Tarayıcıyı gecikmeli aç"""
        time.sleep(3)
        webbrowser.open("http://localhost:5000")
    
    def run_quick_test(self):
        """Hızlı test çalıştır"""
        self.show_loading("Test motoru çalışıyor...")
        
        def run_test():
            try:
                result = subprocess.run([sys.executable, 'fhe_art_engine.py'], 
                                      capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    self.root.after(0, lambda: messagebox.showinfo(
                        "Test Tamamlandı", 
                        "✅ Sanat motoru testi başarılı!\n\n"
                        f"📊 Çıktı:\n{result.stdout[:200]}...\n\n"
                        "Oluşturulan test dosyalarını kontrol edin."
                    ))
                else:
                    self.root.after(0, lambda: messagebox.showerror(
                        "Test Hatası", 
                        f"❌ Test başarısız:\n{result.stderr[:200]}"
                    ))
                    
            except subprocess.TimeoutExpired:
                self.root.after(0, lambda: messagebox.showwarning(
                    "Test Zaman Aşımı", 
                    "⏱️ Test 60 saniyede tamamlanamadı."
                ))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(
                    "Test Hatası", 
                    f"❌ Test çalıştırılamadı:\n{str(e)}"
                ))
        
        threading.Thread(target=run_test, daemon=True).start()
    
    def show_loading(self, message):
        """Loading mesajı göster"""
        loading = tk.Toplevel(self.root)
        loading.title("İşlem Devam Ediyor")
        loading.geometry("300x100")
        loading.configure(bg='#34495E')
        loading.transient(self.root)
        loading.grab_set()
        
        tk.Label(loading, text=message, 
                font=('Arial', 12), 
                fg='#ECF0F1', bg='#34495E').pack(pady=20)
        
        progress = ttk.Progressbar(loading, mode='indeterminate')
        progress.pack(pady=10, padx=20, fill=tk.X)
        progress.start()
        
        # 2 saniye sonra kapat
        loading.after(2000, loading.destroy)
    
    def show_readme(self):
        """README penceresini göster"""
        readme_window = tk.Toplevel(self.root)
        readme_window.title("📖 Proje Hakkında")
        readme_window.geometry("600x400")
        readme_window.configure(bg='#2C3E50')
        
        text_widget = tk.Text(readme_window, 
                             bg='#34495E', fg='#ECF0F1', 
                             font=('Arial', 11), wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        readme_content = """
🎨 FHE ŞIFRELILI SANAT PROJESİ
Zama Creator Program

Bu proje, Fully Homomorphic Encryption (FHE) teknolojisini 
kullanarak interaktif dijital sanat eserleri oluşturur.

✨ ÖZELLİKLER:
• 4 farklı sanat teması (Uzay, Soyut, Teknoloji, Kripto)
• FHE simülasyonu ile şifreli hesaplama
• Desktop ve Web arayüzü seçenekleri
• Gerçek zamanlı parça çözme animasyonları
• Yüksek kaliteli görsel export

🔐 FHE TEKNOLOJİSİ:
Her sanat eseri 16 parçaya bölünür ve şifrelenir. 
Kullanıcılar her etkileşimde bir parçanın şifresini çözer.

Bu, Zama'nın FHE teknolojisinin temel prensiplerini 
eğlenceli ve görsel bir şekilde gösterir.

🚀 HIZLI BAŞLANGIÇ:
1. Desktop Demo: Masaüstü uygulaması
2. Web Demo: Tarayıcı tabanlı arayüz  
3. Quick Test: Sanat motoru testi

📱 PAYLAŞ:
Sosyal medyada #ZamaCreatorProgram hashtag'i ile paylaşın!

Made with ❤️ for Zama Community
        """
        
        text_widget.insert(tk.END, readme_content)
        text_widget.config(state=tk.DISABLED)
    
    def social_share(self):
        """Sosyal medya paylaşım penceresini göster"""
        share_window = tk.Toplevel(self.root)
        share_window.title("📱 Sosyal Medya Paylaşımı")
        share_window.geometry("500x600")
        share_window.configure(bg='#2C3E50')
        
        # Başlık
        tk.Label(share_window, 
                text="📱 Projeyi Paylaş", 
                font=('Arial', 16, 'bold'), 
                fg='#ECF0F1', bg='#2C3E50').pack(pady=10)
        
        # Twitter paylaşım metni
        twitter_frame = tk.LabelFrame(share_window, text="🐦 Twitter/X", 
                                     fg='#ECF0F1', bg='#2C3E50', 
                                     font=('Arial', 12, 'bold'))
        twitter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        twitter_text = """🎨 Yepyeni bir #FHE projesi: Şifreli Dijital Sanat!

@zama_fhe teknolojisini kullanarak interaktif sanat eserleri oluşturdum. Her etkileşimde bir parça şifresi çözülüyor!

🔐 FHE şifreleme
🎨 Dinamik sanat  
⚡ Gerçek zamanlı etkileşim

#ZamaCreatorProgram #FHE #DigitalArt #Crypto

Demo: [GitHub linki]"""
        
        twitter_widget = tk.Text(twitter_frame, height=8, width=50,
                               bg='#34495E', fg='#ECF0F1',
                               font=('Arial', 10), wrap=tk.WORD)
        twitter_widget.pack(padx=5, pady=5)
        twitter_widget.insert(tk.END, twitter_text)
        
        tk.Button(twitter_frame, text="📋 Kopyala", 
                 command=lambda: self.copy_to_clipboard(twitter_text),
                 bg='#1DA1F2', fg='white', font=('Arial', 10)).pack(pady=5)
        
        # LinkedIn paylaşımı
        linkedin_frame = tk.LabelFrame(share_window, text="💼 LinkedIn", 
                                      fg='#ECF0F1', bg='#2C3E50', 
                                      font=('Arial', 12, 'bold'))
        linkedin_frame.pack(fill=tk.X, padx=10, pady=5)
        
        linkedin_text = """🚀 Zama Creator Program kapsamında geliştirdiğim yeni proje: FHE Şifreli Sanat!

Fully Homomorphic Encryption teknolojisini kullanarak, kullanıcıların sanat eserlerini parça parça keşfedebildiği interaktif bir uygulama oluşturdum.

✨ Özellikler:
• 4 farklı tema (Uzay, Soyut, Teknoloji, Kripto)  
• Desktop ve Web arayüzü
• Gerçek zamanlı şifreli hesaplama simülasyonu
• Modern UI/UX tasarım

Bu proje, blockchain ve kriptografi teknolojilerinin sanatla buluştuğu noktayı gösteriyor.

#ZamaCreatorProgram #FHE #Blockchain #DigitalArt #Python #Innovation"""
        
        linkedin_widget = tk.Text(linkedin_frame, height=8, width=50,
                                bg='#34495E', fg='#ECF0F1',
                                font=('Arial', 10), wrap=tk.WORD)
        linkedin_widget.pack(padx=5, pady=5)
        linkedin_widget.insert(tk.END, linkedin_text)
        
        tk.Button(linkedin_frame, text="📋 Kopyala", 
                 command=lambda: self.copy_to_clipboard(linkedin_text),
                 bg='#0077B5', fg='white', font=('Arial', 10)).pack(pady=5)
        
        # Hashtag'ler
        hashtag_frame = tk.Frame(share_window, bg='#2C3E50')
        hashtag_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(hashtag_frame, text="🏷️ Önerilen Hashtag'ler:", 
                font=('Arial', 12, 'bold'), 
                fg='#ECF0F1', bg='#2C3E50').pack(anchor=tk.W)
        
        hashtags = "#ZamaCreatorProgram #FHE #DigitalArt #Crypto #Blockchain #Python #Innovation #TechArt"
        tk.Label(hashtag_frame, text=hashtags, 
                font=('Arial', 10), 
                fg='#3498DB', bg='#2C3E50', 
                wraplength=400).pack(anchor=tk.W, padx=10)
    
    def copy_to_clipboard(self, text):
        """Metni panoya kopyala"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Başarılı", "📋 Metin panoya kopyalandı!")
    
    def safe_exit(self):
        """Güvenli çıkış"""
        if messagebox.askokcancel("Çıkış", "Uygulamadan çıkmak istediğinizden emin misiniz?"):
            # Web sunucusunu durdur
            if self.web_process and self.web_process.poll() is None:
                try:
                    self.web_process.terminate()
                except:
                    pass
            
            self.root.quit()
            self.root.destroy()
    
    def run(self):
        """Launcher'ı çalıştır"""
        # Pencere kapanma event'i
        self.root.protocol("WM_DELETE_WINDOW", self.safe_exit)
        
        # Ana loop
        self.root.mainloop()

# Ana çalıştırma fonksiyonu
def main():
    """Ana launcher fonksiyonu"""
    try:
        # ASCII Art Banner
        print("""
        
    ████████╗██╗  ██╗███████╗     ██████╗██████╗ ██╗   ██╗██████╗ ████████╗ ██████╗ 
    ██╔════╝██║  ██║██╔════╝    ██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔═══██╗
    █████╗  ███████║█████╗      ██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   ██║   ██║
    ██╔══╝  ██╔══██║██╔══╝      ██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ██║   ██║
    ██║     ██║  ██║███████╗    ╚██████╗██║  ██║   ██║   ██║        ██║   ╚██████╔╝
    ╚═╝     ╚═╝  ╚═╝╚══════╝     ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝    ╚═════╝ 
    
                               ██╗  ██╗██████╗ ████████╗
                               ██║ ██╔╝██╔══██╗╚══██╔══╝
                               █████╔╝ ██████╔╝   ██║   
                               ██╔═██╗ ██╔══██╗   ██║   
                               ██║  ██╗██║  ██║   ██║   
                               ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
                               
    ============================================================================
        🎨 FHE CRYPTO ART LAUNCHER - ZAMA CREATOR PROGRAM
    ============================================================================
        """)
        
        print("🚀 Demo Launcher başlatılıyor...")
        
        # Launcher'ı çalıştır
        launcher = FHEArtLauncher()
        launcher.run()
        
    except ImportError as e:
        print(f"❌ Gerekli kütüphane eksik: {e}")
        print("📥 Lütfen 'pip install tkinter' komutunu çalıştırın")
        input("Devam etmek için Enter'a basın...")
    except Exception as e:
        print(f"❌ Launcher başlatılamadı: {e}")
        input("Devam etmek için Enter'a basın...")

# Komut satırından çalıştırma
if __name__ == "__main__":
    main()

# ================================
# BONUS: requirements-dev.txt (Geliştiriciler için)
# ================================
"""
# Ana gereksinimler
matplotlib>=3.7.0
pillow>=10.0.0
numpy>=1.24.0
flask>=2.3.0

# Geliştirme araçları
pytest>=7.0.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.0.0

# Paketleme
setuptools>=68.0.0
wheel>=0.40.0
twine>=4.0.0

# Dokümantasyon
sphinx>=7.0.0
sphinx-rtd-theme>=1.3.0

# Test kapsamı
pytest-cov>=4.0.0
coverage>=7.0.0

# Web geliştirme (opsiyonel)
gunicorn>=20.1.0
flask-cors>=4.0.0
waitress>=2.1.0
"""

# ================================
# BONUS: Dockerfile (Container için)
# ================================
"""
FROM python:3.11-slim

LABEL maintainer="Zama Creator"
LABEL description="FHE Crypto Art - Interactive Digital Art with Encryption"

# Sistem paketlerini yükle
RUN apt-get update && apt-get install -y \
    tk-dev \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

# Çalışma dizinini ayarla
WORKDIR /app

# Requirements dosyasını kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Port açık
EXPOSE 5000

# Sağlık kontrolü
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:5000/ || exit 1

# Varsayılan komut
CMD ["python", "web_art_generator.py"]

# Kullanım:
# docker build -t fhe-crypto-art .
# docker run -p 5000:5000 fhe-crypto-art
"""

# ================================
# BONUS: GitHub Actions CI/CD
# ================================
"""
# .github/workflows/test.yml
name: FHE Crypto Art Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install system dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y python3-tk
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        python -m pytest tests/ -v --cov=./ --cov-report=xml
    
    - name: Test art engine
      run: |
        python fhe_art_engine.py
        
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
"""