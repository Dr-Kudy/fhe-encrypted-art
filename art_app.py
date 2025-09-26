import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from PIL import Image, ImageTk
from fhe_art_engine import FHEArtGenerator
import random
import threading
import time
import os

class FHEArtApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 FHE Şifreli Sanat Galerisi - Zama Creator Program")
        self.root.geometry("1200x900")
        self.root.configure(bg='#2C3E50')
        
        # Pencereyi merkeze al
        self.center_window()
        
        # Ana değişkenler
        self.art_generator = FHEArtGenerator()
        self.encrypted_pieces = []
        self.revealed_count = 0
        self.total_pieces = 16
        self.current_theme = "space"
        self.animation_active = False
        
        self.setup_ui()
        self.generate_new_art()
    
    def center_window(self):
        """Pencereyi ekranın ortasına yerleştir"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (900 // 2)
        self.root.geometry(f"1200x900+{x}+{y}")
    
    def setup_ui(self):
        """Ana arayüzü oluştur"""
        # Ana başlık
        self.setup_header()
        
        # İçerik alanı (sol: sanat, sağ: kontroller)
        content_frame = tk.Frame(self.root, bg='#2C3E50')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Sol panel - Sanat eseri
        left_frame = tk.Frame(content_frame, bg='#2C3E50')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.setup_art_display(left_frame)
        
        # Sağ panel - Kontroller
        right_frame = tk.Frame(content_frame, bg='#34495E', width=300)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(20, 0))
        right_frame.pack_propagate(False)
        
        self.setup_control_panel(right_frame)
        
        # Alt panel - İlerleme
        self.setup_bottom_panel()
    
    def setup_header(self):
        """Üst başlık bölümü"""
        header_frame = tk.Frame(self.root, bg='#34495E', height=80)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Ana başlık
        title_label = tk.Label(header_frame, 
                              text="🔐 FHE Şifreli Sanat Galerisi", 
                              font=('Arial', 24, 'bold'), 
                              fg='#ECF0F1', bg='#34495E')
        title_label.pack(pady=10)
        
        # Alt başlık
        subtitle_label = tk.Label(header_frame, 
                                 text="Zama Creator Program | Her etkileşim bir parçanın şifresini çözer", 
                                 font=('Arial', 12), 
                                 fg='#BDC3C7', bg='#34495E')
        subtitle_label.pack()
    
    def setup_art_display(self, parent):
        """Sanat eseri görüntü alanı"""
        art_frame = tk.Frame(parent, bg='#2C3E50')
        art_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sanat eseri başlığı
        art_title = tk.Label(art_frame, 
                            text="🎨 Şifreli Sanat Eseri", 
                            font=('Arial', 16, 'bold'), 
                            fg='#ECF0F1', bg='#2C3E50')
        art_title.pack(pady=(0, 10))
        
        # Sanat eseri görüntüsü için frame
        self.art_display_frame = tk.Frame(art_frame, bg='#34495E', relief=tk.RAISED, bd=2)
        self.art_display_frame.pack(padx=10, pady=10)
        
        self.art_label = tk.Label(self.art_display_frame, bg='#34495E')
        self.art_label.pack(padx=10, pady=10)
        
        # Tema bilgisi
        self.theme_label = tk.Label(art_frame, 
                                   text=f"Tema: {self.current_theme.capitalize()}", 
                                   font=('Arial', 12), 
                                   fg='#95A5A6', bg='#2C3E50')
        self.theme_label.pack()
    
    def setup_control_panel(self, parent):
        """Sağ taraftaki kontrol paneli"""
        # Panel başlığı
        control_title = tk.Label(parent, 
                                text="⚙️ Kontrol Paneli", 
                                font=('Arial', 16, 'bold'), 
                                fg='#ECF0F1', bg='#34495E')
        control_title.pack(pady=15)
        
        # Tema seçimi
        self.setup_theme_selection(parent)
        
        # Ana butonlar
        self.setup_main_buttons(parent)
        
        # FHE bilgi paneli
        self.setup_fhe_info(parent)
        
        # İstatistikler
        self.setup_stats_panel(parent)
    
    def setup_theme_selection(self, parent):
        """Tema seçim bölümü"""
        theme_frame = tk.LabelFrame(parent, text="🎨 Tema Seçimi", 
                                   fg='#ECF0F1', bg='#34495E', 
                                   font=('Arial', 12, 'bold'))
        theme_frame.pack(fill=tk.X, padx=10, pady=10)
        
        themes = [
            ("🚀 Uzay", "space"),
            ("🎨 Soyut", "abstract"), 
            ("💻 Teknoloji", "tech"),
            ("₿ Kripto", "crypto")
        ]
        
        self.theme_var = tk.StringVar(value="space")
        
        for text, value in themes:
            rb = tk.Radiobutton(theme_frame, text=text, value=value,
                               variable=self.theme_var, fg='#ECF0F1', 
                               bg='#34495E', selectcolor='#3498DB',
                               font=('Arial', 10), activebackground='#34495E')
            rb.pack(anchor=tk.W, padx=10, pady=2)
    
    def setup_main_buttons(self, parent):
        """Ana işlem butonları"""
        button_frame = tk.Frame(parent, bg='#34495E')
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Buton stili
        btn_style = {
            'font': ('Arial', 11, 'bold'), 
            'bg': '#3498DB', 
            'fg': 'white',
            'activebackground': '#2980B9',
            'activeforeground': 'white',
            'relief': tk.FLAT,
            'cursor': 'hand2'
        }
        
        # Yeni sanat oluştur
        tk.Button(button_frame, text="🎲 Yeni Sanat Oluştur", 
                 command=self.generate_new_art_with_theme, 
                 **btn_style).pack(fill=tk.X, pady=2)
        
        # Tek parça çöz
        tk.Button(button_frame, text="🔓 Bir Parça Çöz", 
                 command=self.reveal_random_piece, 
                 **btn_style).pack(fill=tk.X, pady=2)
        
        # Çoklu parça çöz
        multi_btn_style = btn_style.copy()
        multi_btn_style['bg'] = '#E74C3C'
        multi_btn_style['activebackground'] = '#C0392B'
        
        tk.Button(button_frame, text="⚡ 5 Parça Çöz", 
                 command=self.reveal_multiple_pieces, 
                 **multi_btn_style).pack(fill=tk.X, pady=2)
        
        # Otomatik çözme
        auto_btn_style = btn_style.copy()
        auto_btn_style['bg'] = '#9B59B6'
        auto_btn_style['activebackground'] = '#8E44AD'
        
        tk.Button(button_frame, text="🤖 Otomatik Çözme", 
                 command=self.toggle_auto_reveal, 
                 **auto_btn_style).pack(fill=tk.X, pady=2)
        
        # Kaydet
        save_btn_style = btn_style.copy()
        save_btn_style['bg'] = '#27AE60'
        save_btn_style['activebackground'] = '#229954'
        
        tk.Button(button_frame, text="💾 Eseri Kaydet", 
                 command=self.save_artwork, 
                 **save_btn_style).pack(fill=tk.X, pady=2)
    
    def setup_fhe_info(self, parent):
        """FHE bilgi paneli"""
        fhe_frame = tk.LabelFrame(parent, text="🔐 FHE Bilgisi", 
                                 fg='#ECF0F1', bg='#34495E', 
                                 font=('Arial', 12, 'bold'))
        fhe_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.fhe_info_text = tk.Text(fhe_frame, height=4, width=30,
                                    bg='#2C3E50', fg='#ECF0F1',
                                    font=('Consolas', 9), wrap=tk.WORD)
        self.fhe_info_text.pack(padx=5, pady=5)
        
        # Başlangıç metni
        self.update_fhe_info("FHE ile şifreli hesaplama başlatılıyor...")
    
    def setup_stats_panel(self, parent):
        """İstatistik paneli"""
        stats_frame = tk.LabelFrame(parent, text="📊 İstatistikler", 
                                   fg='#ECF0F1', bg='#34495E', 
                                   font=('Arial', 12, 'bold'))
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.stats_labels = {}
        stats_data = [
            ("Toplam Parça:", "total"),
            ("Çözülmüş:", "revealed"),
            ("Gizli:", "hidden"),
            ("Şifre Anahtarı:", "key")
        ]
        
        for label_text, key in stats_data:
            frame = tk.Frame(stats_frame, bg='#34495E')
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            tk.Label(frame, text=label_text, fg='#BDC3C7', bg='#34495E',
                    font=('Arial', 10)).pack(side=tk.LEFT)
            
            self.stats_labels[key] = tk.Label(frame, text="0", fg='#3498DB', 
                                            bg='#34495E', font=('Arial', 10, 'bold'))
            self.stats_labels[key].pack(side=tk.RIGHT)
    
    def setup_bottom_panel(self):
        """Alt panel - ilerleme çubuğu"""
        bottom_frame = tk.Frame(self.root, bg='#34495E', height=100)
        bottom_frame.pack(fill=tk.X, side=tk.BOTTOM)
        bottom_frame.pack_propagate(False)
        
        # İlerleme başlığı
        self.progress_label = tk.Label(bottom_frame, 
                                      text="Şifre Çözülmüş: 0/16 parça", 
                                      font=('Arial', 14, 'bold'), 
                                      fg='#ECF0F1', bg='#34495E')
        self.progress_label.pack(pady=10)
        
        # İlerleme çubuğu
        progress_container = tk.Frame(bottom_frame, bg='#34495E')
        progress_container.pack(pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_container, 
                                           variable=self.progress_var,
                                           maximum=100, length=400,
                                           mode='determinate')
        self.progress_bar.pack()
        
        # Progress yüzdesi
        self.progress_percent_label = tk.Label(bottom_frame, 
                                             text="0%", 
                                             font=('Arial', 12), 
                                             fg='#3498DB', bg='#34495E')
        self.progress_percent_label.pack()
    
    def generate_new_art_with_theme(self):
        """Seçilen tema ile yeni sanat oluştur"""
        selected_theme = self.theme_var.get()
        self.current_theme = selected_theme
        self.generate_new_art()
    
    def generate_new_art(self):
        """Yeni sanat eseri oluştur"""
        try:
            # Loading animasyonu başlat
            self.show_loading("Sanat eseri oluşturuluyor...")
            
            # Thread'de sanat oluştur (UI donmasını engellemek için)
            threading.Thread(target=self._generate_art_thread, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Hata", f"Sanat oluşturulurken hata: {str(e)}")
    
    def _generate_art_thread(self):
        """Sanat oluşturma thread'i"""
        try:
            # Yeni encryption key
            self.art_generator.reset_encryption()
            
            # Sanat oluştur
            art_path = self.art_generator.generate_base_art(self.current_theme)
            
            # Parçalara ayır
            self.encrypted_pieces = self.art_generator.encrypt_art_pieces(art_path)
            self.revealed_count = 0
            
            # UI'yi güncelle (ana thread'de)
            self.root.after(0, self._update_ui_after_generation)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Hata", str(e)))
    
    def _update_ui_after_generation(self):
        """Sanat oluşturulduktan sonra UI'yi güncelle"""
        self.update_art_display()
        self.update_progress()
        self.update_stats()
        self.update_fhe_info(f"Yeni {self.current_theme} sanat eseri oluşturuldu!\nFHE şifreleme aktif.")
        self.theme_label.config(text=f"Tema: {self.current_theme.capitalize()}")
        
        messagebox.showinfo("Başarılı", 
                           f"🎨 {self.current_theme.capitalize()} temalı sanat eseri oluşturuldu!\n"
                           f"🔐 {self.total_pieces} parça FHE ile şifrelendi.")
    
    def show_loading(self, message):
        """Loading mesajı göster"""
        self.update_fhe_info(f"⏳ {message}\nLütfen bekleyin...")
    
    def reveal_random_piece(self):
        """Rastgele bir parçanın şifresini çöz"""
        if self.revealed_count >= self.total_pieces:
            messagebox.showinfo("Tamamlandı!", 
                               "🎉 Tüm parçaların şifresi çözüldü!\n"
                               "Yeni bir sanat eseri oluşturabilirsiniz.")
            return
        
        # Şifresi çözülmemiş parçaları bul
        hidden_pieces = [i for i, p in enumerate(self.encrypted_pieces) 
                        if not p['is_revealed']]
        
        if hidden_pieces:
            piece_index = random.choice(hidden_pieces)
            success = self.art_generator.reveal_piece(self.encrypted_pieces, piece_index)
            
            if success:
                self.revealed_count += 1
                self.update_art_display()
                self.update_progress()
                self.update_stats()
                
                # FHE mesajları
                piece_info = self.encrypted_pieces[piece_index]
                self.update_fhe_info(
                    f"Parça #{piece_info['piece_id']:02d} şifresi çözüldü!\n"
                    f"Pozisyon: ({piece_info['position'][0]}, {piece_info['position'][1]})\n"
                    f"FHE işlemi başarılı."
                )
                
                # Özel mesajlar
                if self.revealed_count == self.total_pieces:
                    self.show_completion_message()
                elif self.revealed_count % 4 == 0:
                    self.show_fhe_milestone_message()
    
    def reveal_multiple_pieces(self):
        """Birden fazla parça çöz"""
        pieces_to_reveal = min(5, self.total_pieces - self.revealed_count)
        
        if pieces_to_reveal == 0:
            messagebox.showinfo("Bilgi", "Tüm parçalar zaten çözülmüş!")
            return
        
        self.update_fhe_info("⚡ Toplu FHE işlemi başlatılıyor...")
        
        # Animasyonlu çözme
        for i in range(pieces_to_reveal):
            self.root.after(i * 300, self.reveal_random_piece)
    
    def toggle_auto_reveal(self):
        """Otomatik çözmeyi başlat/durdur"""
        if not self.animation_active:
            self.animation_active = True
            self.auto_reveal_pieces()
            self.update_fhe_info("🤖 Otomatik FHE çözme başlatıldı...")
        else:
            self.animation_active = False
            self.update_fhe_info("⏸️ Otomatik çözme durduruldu.")
    
    def auto_reveal_pieces(self):
        """Otomatik parça çözme"""
        if self.animation_active and self.revealed_count < self.total_pieces:
            self.reveal_random_piece()
            # 2 saniye sonra tekrar çağır
            self.root.after(2000, self.auto_reveal_pieces)
        else:
            self.animation_active = False
    
    def show_fhe_milestone_message(self):
        """FHE kilometre taşı mesajları"""
        messages = [
            "🔐 FHE ile güvenli hesaplama devam ediyor!",
            "⚡ Zama teknolojisinin gücünü görüyorsunuz!",
            "🛡️ Verileriniz şifreli kalarak işleniyor!",
            "🎯 Fully Homomorphic Encryption çalışıyor!",
            "💡 Gizliliği koruyarak hesaplama yapılıyor!"
        ]
        messagebox.showinfo("FHE Teknolojisi", random.choice(messages))
    
    def show_completion_message(self):
        """Tamamlanma mesajı"""
        completion_text = (
            "🎉 TEBRIKLER! 🎉\n\n"
            "Sanat eserinizin tüm parçalarının şifresi çözüldü!\n\n"
            "🔐 FHE (Fully Homomorphic Encryption) teknolojisi sayesinde "
            "her parça güvenli bir şekilde çözüldi.\n\n"
            "💡 Bu, Zama'nın geleceğin gizlilik teknolojisini gösteriyor!"
        )
        messagebox.showinfo("Görev Tamamlandı!", completion_text)
    
    def update_art_display(self):
        """Sanat eserini güncelle"""
        if not self.encrypted_pieces:
            return
            
        try:
            progress_img = self.art_generator.generate_progress_image(self.encrypted_pieces)
            # Görüntüyü uygun boyuta getir
            display_size = (600, 600)
            progress_img = progress_img.resize(display_size, Image.Resampling.LANCZOS)
            
            self.art_photo = ImageTk.PhotoImage(progress_img)
            self.art_label.configure(image=self.art_photo)
        except Exception as e:
            print(f"Görüntü güncellenirken hata: {e}")
    
    def update_progress(self):
        """İlerlemeyi güncelle"""
        if self.total_pieces == 0:
            return
            
        progress_percent = (self.revealed_count / self.total_pieces) * 100
        
        # Progress bar güncelle
        self.progress_var.set(progress_percent)
        
        # Labels güncelle
        self.progress_label.configure(
            text=f"Şifre Çözülmüş: {self.revealed_count}/{self.total_pieces} parça"
        )
        self.progress_percent_label.configure(text=f"{progress_percent:.1f}%")
    
    def update_stats(self):
        """İstatistikleri güncelle"""
        if not hasattr(self, 'stats_labels'):
            return
            
        stats = self.art_generator.get_encryption_stats(self.encrypted_pieces)
        
        self.stats_labels['total'].config(text=str(stats['total_pieces']))
        self.stats_labels['revealed'].config(text=str(stats['revealed_pieces']))
        self.stats_labels['hidden'].config(text=str(stats['hidden_pieces']))
        self.stats_labels['key'].config(text=str(stats['encryption_key']))
    
    def update_fhe_info(self, message):
        """FHE bilgi panelini güncelle"""
        if hasattr(self, 'fhe_info_text'):
            self.fhe_info_text.delete(1.0, tk.END)
            self.fhe_info_text.insert(1.0, message)
    
    def save_artwork(self):
        """Sanat eserini kaydet"""
        if not self.encrypted_pieces:
            messagebox.showwarning("Uyarı", "Kaydedilecek sanat eseri bulunamadı!")
            return
        
        try:
            # Dosya adı oluştur
            filename = f"fhe_art_{self.current_theme}_{self.revealed_count}of{self.total_pieces}.png"
            
            # Dosya kaydetme dialog'u
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                initialvalue=filename,
                title="Sanat Eserini Kaydet"
            )
            
            if file_path:
                progress_img = self.art_generator.generate_progress_image(self.encrypted_pieces, (1200, 1200))
                progress_img.save(file_path, quality=95)
                
                messagebox.showinfo("Başarılı", 
                                   f"🎨 Sanat eseri başarıyla kaydedildi:\n{file_path}\n\n"
                                   f"📊 İçerik: {self.revealed_count}/{self.total_pieces} parça çözülmüş")
        except Exception as e:
            messagebox.showerror("Hata", f"Kaydetme hatası: {str(e)}")

# Ana uygulama çalıştırıcı
def main():
    """Ana uygulama fonksiyonu"""
    try:
        root = tk.Tk()
        
        # Uygulama ikonu (eğer varsa)
        try:
            root.iconbitmap("icon.ico")  # Opsiyonel
        except:
            pass
        
        # Uygulama başlat
        app = FHEArtApp(root)
        
        # Pencere kapatma event'i
        def on_closing():
            if messagebox.askokcancel("Çıkış", "Uygulamadan çıkmak istediğinizden emin misiniz?"):
                root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Ana loop
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Kritik Hata", f"Uygulama başlatılamadı: {str(e)}")

# Hızlı test fonksiyonu
def quick_test():
    """Hızlı test için basit pencere"""
    root = tk.Tk()
    root.title("FHE Art Test")
    root.geometry("400x300")
    
    def test_art_engine():
        from fhe_art_engine import test_fhe_art
        test_fhe_art()
        messagebox.showinfo("Test", "Sanat motoru testi tamamlandı!")
    
    tk.Button(root, text="Sanat Motoru Test Et", 
             command=test_art_engine, 
             font=('Arial', 14), bg='#3498DB', fg='white').pack(pady=20)
    
    tk.Button(root, text="Ana Uygulamayı Başlat", 
             command=lambda: [root.destroy(), main()], 
             font=('Arial', 14), bg='#E74C3C', fg='white').pack(pady=20)
    
    tk.Label(root, text="🎨 FHE Sanat Uygulaması\nTest ve Başlatma", 
            font=('Arial', 16), justify=tk.CENTER).pack(pady=40)
    
    root.mainloop()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        quick_test()
    else:
        main()