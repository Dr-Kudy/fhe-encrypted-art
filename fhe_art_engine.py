import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw
import random
import os

class FHEArtGenerator:
    def __init__(self):
        self.art_pieces = []
        self.encryption_key = random.randint(1000, 9999)
    
    def generate_base_art(self, theme="zama_classic"):
        fig, ax = plt.subplots(figsize=(10, 10))
    
        if theme == "zama_classic":
            self._create_zama_classic_art(ax)
        elif theme == "zama_minimal":
            self._create_zama_minimal_art(ax)
        elif theme == "zama_geometric":
            self._create_zama_geometric_art(ax)
        elif theme == "zama_vision":
            self._create_zama_vision_art(ax)
        else:
            self._create_zama_classic_art(ax)
        
        plt.axis('off')
        plt.tight_layout()
        plt.savefig('base_art.png', dpi=150, bbox_inches='tight', 
                   facecolor='white', transparent=False, pad_inches=0)
        plt.close()
        return 'base_art.png'
    
    def _create_zama_classic_art(self, ax):
        ax.set_facecolor('#FFD700')
        
        # Basit ZAMA logosu
        ax.text(0.5, 0.5, 'ZAMA', fontsize=60, fontweight='bold',
               ha='center', va='center', color='black')
        
        # Kilit simgeleri
        lock_positions = [(0.2, 0.7), (0.8, 0.7), (0.2, 0.3), (0.8, 0.3)]
        for x, y in lock_positions:
            # Basit kilit
            lock = plt.Rectangle((x-0.05, y-0.05), 0.1, 0.08,
                               facecolor='black', edgecolor='white', linewidth=2)
            ax.add_patch(lock)
            
            # Kilit kulpu
            handle = plt.Circle((x, y+0.03), 0.03, fill=False, 
                              edgecolor='white', linewidth=3)
            ax.add_patch(handle)
    
    def _create_zama_minimal_art(self, ax):
        ax.set_facecolor('#FFEB3B')
        
        # Merkezi kilit (emoji yerine basit şekil)
        lock = plt.Rectangle((0.45, 0.45), 0.1, 0.1,
                           facecolor='black', edgecolor='white', linewidth=3)
        ax.add_patch(lock)
        
        # ZAMA yazısı
        ax.text(0.5, 0.3, 'ZAMA FHE', fontsize=30, fontweight='bold',
               ha='center', va='center', color='black')

    def _create_zama_geometric_art(self, ax):
        ax.set_facecolor('#FFD54F')
        
        # Merkezi Zama küpü
        self._draw_central_zama_cube(ax, (0.5, 0.5), 0.18)
        
        # Çevresinde FHE elementleri
        self._draw_surrounding_fhe_elements(ax)
        
        # Parlama efektleri
        self._add_sparkle_effects(ax)

    def _create_zama_vision_art(self, ax):
        ax.set_facecolor('#FFC107')
        
        # Futuristik ağ
        self._draw_fhe_network(ax)
        
        # Dağıtık şifreleme
        self._draw_distributed_encryption(ax)
        
        # Teknoloji ızgara deseni
        self._draw_tech_grid_pattern(ax)

    def _draw_central_zama_cube(self, ax, center, size):
        x, y = center
        
        # İzometrik küp
        top_points = [(x-size/2, y), (x, y+size/2), 
                     (x+size/2, y), (x, y-size/2)]
        top_face = plt.Polygon(top_points, facecolor='#FFE082', 
                             edgecolor='black', linewidth=2)
        ax.add_patch(top_face)
        
        # Sol yüz
        left_points = [(x-size/2, y), (x, y-size/2),
                      (x, y-size*1.2), (x-size/2, y-size*0.7)]
        left_face = plt.Polygon(left_points, facecolor='#FFCC02', 
                              edgecolor='black', linewidth=2)
        ax.add_patch(left_face)
        
        # Sağ yüz
        right_points = [(x, y-size/2), (x+size/2, y),
                       (x+size/2, y-size*0.7), (x, y-size*1.2)]
        right_face = plt.Polygon(right_points, facecolor='#FFB300', 
                               edgecolor='black', linewidth=2)
        ax.add_patch(right_face)
        
        # ZAMA logosu
        ax.text(x-size/8, y-size/4, 'Z', fontsize=int(size*80), 
               fontweight='bold', color='black')

    def _draw_surrounding_fhe_elements(self, ax):
        positions = [(0.2, 0.8), (0.8, 0.8), (0.2, 0.2), (0.8, 0.2)]
        symbols = ['Enc()', 'f()', 'Dec()', 'FHE']
        
        for i, pos in enumerate(positions):
            x, y = pos
            
            # Arka plan kutusu
            box = plt.Rectangle((x-0.05, y-0.03), 0.1, 0.06,
                               facecolor='white', edgecolor='#FFD700', linewidth=2)
            ax.add_patch(box)
            
            # Simge metni
            ax.text(x, y, symbols[i], fontsize=12, fontweight='bold',
                   ha='center', va='center', color='#424242')

    def _add_sparkle_effects(self, ax):
        sparkle_positions = [(0.15, 0.85), (0.85, 0.85), 
                           (0.15, 0.15), (0.85, 0.15)]
        
        for pos in sparkle_positions:
            x, y = pos
            
            # Ana yıldız
            ax.plot(x, y, '*', color='white', markersize=18, alpha=0.9)
            ax.plot(x, y, '*', color='#FFD700', markersize=12)

    def _draw_fhe_network(self, ax):
        # Merkezi hub
        hub = plt.Circle((0.5, 0.5), 0.08, facecolor='#FFD700', 
                        edgecolor='black', linewidth=3)
        ax.add_patch(hub)
        ax.text(0.5, 0.5, 'FHE', fontsize=14, fontweight='bold',
               ha='center', va='center', color='black')
        
        # Çevresinde bağlantı noktaları
        angles = np.linspace(0, 2*np.pi, 8, endpoint=False)
        for angle in angles:
            x_node = 0.5 + 0.25 * np.cos(angle)
            y_node = 0.5 + 0.25 * np.sin(angle)
            
            # Bağlantı çizgisi
            ax.plot([0.5, x_node], [0.5, y_node], 
                   color='#FFD700', linewidth=2, alpha=0.8)
            
            # Düğüm
            node = plt.Circle((x_node, y_node), 0.03, 
                            facecolor='white', edgecolor='#FFD700', linewidth=2)
            ax.add_patch(node)

    def _draw_distributed_encryption(self, ax):
        for _ in range(15):
            x = random.uniform(0.1, 0.9)
            y = random.uniform(0.1, 0.9)
            
            # Şifreli blok
            block = plt.Rectangle((x-0.025, y-0.015), 0.05, 0.03,
                                facecolor='#424242', edgecolor='#FFD700', linewidth=1)
            ax.add_patch(block)
            
            # Şifre simgesi
            cipher_symbol = plt.Circle((x, y), 0.008, facecolor='#FFD700')
            ax.add_patch(cipher_symbol)

    def _draw_tech_grid_pattern(self, ax):
        # İnce ızgara çizgileri
        for i in range(0, 10):
            x_pos = i * 0.1
            y_pos = i * 0.1
            
            # Dikey çizgiler
            ax.plot([x_pos, x_pos], [0, 1], color='white', 
                   linewidth=0.5, alpha=0.3)
            
            # Yatay çizgiler
            ax.plot([0, 1], [y_pos, y_pos], color='white', 
                   linewidth=0.5, alpha=0.3)

    def encrypt_art_pieces(self, image_path, pieces=16):
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Art file not found: {image_path}")
            
        img = Image.open(image_path)
        width, height = img.size
        
        piece_width = width // 4
        piece_height = height // 4
        
        encrypted_pieces = []
        
        for i in range(4):
            for j in range(4):
                left = j * piece_width
                upper = i * piece_height
                right = (j + 1) * piece_width
                lower = (i + 1) * piece_height
                
                piece = img.crop((left, upper, right, lower))
                
                encrypted_data = self._encrypt_image_data(piece)
                encrypted_pieces.append({
                    'position': (i, j),
                    'encrypted_data': encrypted_data,
                    'original_piece': piece,
                    'is_revealed': False,
                    'piece_id': len(encrypted_pieces)
                })
                
        return encrypted_pieces
    
    def _encrypt_image_data(self, image_piece):
        arr = np.array(image_piece)
        encrypted = ((arr.astype(int) ^ self.encryption_key) + self.encryption_key) % 256
        return encrypted.astype(np.uint8)
    
    def reveal_piece(self, encrypted_pieces, piece_index):
        if 0 <= piece_index < len(encrypted_pieces):
            if not encrypted_pieces[piece_index]['is_revealed']:
                encrypted_pieces[piece_index]['is_revealed'] = True
                return True
        return False
    
    def generate_progress_image(self, encrypted_pieces, original_size=(800, 800)):
        img = Image.new('RGB', original_size, color='black')
        draw = ImageDraw.Draw(img)
        
        piece_width = original_size[0] // 4
        piece_height = original_size[1] // 4
        
        for piece in encrypted_pieces:
            i, j = piece['position']
            left = j * piece_width
            upper = i * piece_height
            right = (j + 1) * piece_width
            lower = (i + 1) * piece_height
            
            if piece['is_revealed']:
                if 'original_piece' in piece:
                    resized_piece = piece['original_piece'].resize((piece_width, piece_height))
                    img.paste(resized_piece, (left, upper))
                else:
                    color = self._get_piece_color(piece['piece_id'])
                    draw.rectangle([left, upper, right, lower], 
                                  fill=color, outline='white', width=2)
            else:
                draw.rectangle([left, upper, right, lower], 
                              fill='#2c3e50', outline='#34495e', width=2)
                
                center_x = left + piece_width // 2
                center_y = upper + piece_height // 2
                
                lock_size = min(piece_width, piece_height) // 4
                draw.rectangle([center_x - lock_size//2, center_y - lock_size//3,
                              center_x + lock_size//2, center_y + lock_size//3],
                              fill='#7f8c8d', outline='#95a5a6', width=2)
                
                draw.text((center_x, center_y + lock_size), 
                         f"#{piece['piece_id']:02d}", 
                         fill='#bdc3c7', anchor='mm')
        
        draw.text((10, original_size[1] - 30), 
                 "🔐 FHE Crypto Art - Zama Creator Program", 
                 fill='#7f8c8d')
        
        return img
    
    def _get_piece_color(self, piece_id):
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', 
                 '#FECA57', '#FF9FF3', '#54A0FF', '#5F27CD']
        return colors[piece_id % len(colors)]
    
    def get_encryption_stats(self, encrypted_pieces):
        total_pieces = len(encrypted_pieces)
        revealed_pieces = sum(1 for piece in encrypted_pieces if piece['is_revealed'])
        
        return {
            'total_pieces': total_pieces,
            'revealed_pieces': revealed_pieces,
            'hidden_pieces': total_pieces - revealed_pieces,
            'completion_percentage': (revealed_pieces / total_pieces) * 100,
            'encryption_key': self.encryption_key
        }
    
    def reset_encryption(self):
        """Şifreleme anahtarını sıfırla"""
        self.encryption_key = random.randint(1000, 9999)
        print(f"🔑 Yeni şifreleme anahtarı: {self.encryption_key}")

# Test fonksiyonu
def test_fhe_art():
    print("🎨 FHE Sanat Motoru Test Ediliyor...")
    
    generator = FHEArtGenerator()
    
    print("✨ Zama Classic teması oluşturuluyor...")
    art_path = generator.generate_base_art('zama_classic')
    print(f"💾 {art_path} oluşturuldu!")
    
    print("✨ Zama Minimal teması oluşturuluyor...")
    art_path2 = generator.generate_base_art('zama_minimal')
    print(f"💾 {art_path2} oluşturuldu!")
    
    print("✅ Test tamamlandı!")

if __name__ == "__main__":
    test_fhe_art()