from flask import Flask, render_template, jsonify, request, send_file
import base64
from io import BytesIO
import json
import os
import threading
import time
from datetime import datetime
from fhe_art_engine import FHEArtGenerator

# Flask uygulaması
app = Flask(__name__)
app.secret_key = 'fhe-crypto-art-zama-2024'

# Global değişkenler
art_generators = {}  # Session bazlı art generator'lar
session_data = {}    # Session verileri

def get_session_id():
    """Basit session ID oluştur"""
    return request.headers.get('X-Session-ID', 'default-session')

def get_art_generator(session_id):
    """Session için art generator al/oluştur"""
    if session_id not in art_generators:
        art_generators[session_id] = FHEArtGenerator()
        session_data[session_id] = {
            'created': datetime.now(),
            'encrypted_pieces': [],
            'stats': {'revealed': 0, 'total': 0}
        }
    return art_generators[session_id]

# Templates oluştur (uygulama başlarken)
def create_templates():
    """Templates klasörünü ve HTML dosyalarını oluştur"""
    os.makedirs('templates', exist_ok=True)
    
    html_content = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎨 FHE Şifreli Sanat Galerisi - Zama Creator Program</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #2c3e50, #34495e);
            color: #ecf0f1;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: rgba(52, 73, 94, 0.8);
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        .main-content {
            display: grid;
            grid-template-columns: 1fr 300px;
            gap: 30px;
            margin-bottom: 30px;
        }
        
        .art-section {
            background: rgba(52, 73, 94, 0.6);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
        }
        
        .art-display {
            margin: 20px 0;
            border: 3px solid #3498db;
            border-radius: 10px;
            overflow: hidden;
            background: #2c3e50;
        }
        
        .art-image {
            width: 100%;
            height: auto;
            display: block;
        }
        
        .controls {
            background: rgba(52, 73, 94, 0.8);
            border-radius: 15px;
            padding: 20px;
        }
        
        .control-group {
            margin-bottom: 20px;
        }
        
        .control-group h3 {
            margin-bottom: 10px;
            color: #3498db;
            border-bottom: 2px solid #3498db;
            padding-bottom: 5px;
        }
        
        .theme-buttons {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 15px;
        }
        
        .btn {
            padding: 12px 15px;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        
        .btn-theme {
            background: #95a5a6;
            color: white;
        }
        
        .btn-theme.active {
            background: #3498db;
        }
        
        .btn-primary {
            background: #3498db;
            color: white;
        }
        
        .btn-danger {
            background: #e74c3c;
            color: white;
        }
        
        .btn-success {
            background: #27ae60;
            color: white;
        }
        
        .btn-warning {
            background: #f39c12;
            color: white;
        }
        
        .btn-block {
            width: 100%;
            margin-bottom: 10px;
        }
        
        .stats {
            background: rgba(44, 62, 80, 0.8);
            border-radius: 10px;
            padding: 15px;
        }
        
        .stat-item {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            padding: 5px 0;
            border-bottom: 1px solid #34495e;
        }
        
        .stat-value {
            color: #3498db;
            font-weight: bold;
        }
        
        .progress-section {
            background: rgba(52, 73, 94, 0.8);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
        }
        
        .progress-bar {
            width: 100%;
            height: 30px;
            background: #34495e;
            border-radius: 15px;
            overflow: hidden;
            margin: 15px 0;
            box-shadow: inset 0 2px 5px rgba(0,0,0,0.3);
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #e74c3c, #f39c12, #27ae60);
            border-radius: 15px;
            transition: width 0.5s ease;
            width: 0%;
            position: relative;
        }
        
        .progress-fill::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.2) 50%, transparent 70%);
            animation: shimmer 2s infinite;
        }
        
        @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        
        .fhe-info {
            background: rgba(44, 62, 80, 0.9);
            border-radius: 10px;
            padding: 15px;
            margin-top: 15px;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            border-left: 4px solid #3498db;
        }
        
        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
        }
        
        .spinner {
            border: 4px solid #34495e;
            border-top: 4px solid #3498db;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .message {
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            font-weight: bold;
        }
        
        .message.success {
            background: rgba(39, 174, 96, 0.8);
            border: 1px solid #27ae60;
        }
        
        .message.error {
            background: rgba(231, 76, 60, 0.8);
            border: 1px solid #e74c3c;
        }
        
        .message.info {
            background: rgba(52, 152, 219, 0.8);
            border: 1px solid #3498db;
        }
        
        /* ZAMA ÖZEL STİLLER */
        .zama-themes {
            background: linear-gradient(135deg, #FFD700, #FFC107);
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            border: 3px solid #FFB300;
            box-shadow: 0 8px 20px rgba(255, 215, 0, 0.4);
        }
        
        .zama-themes h4 {
            color: #1A1A1A;
            font-weight: bold;
            margin-bottom: 15px;
            text-shadow: 1px 1px 2px rgba(255,255,255,0.7);
        }
        
        .btn-theme-zama {
            background: linear-gradient(135deg, #FFD700, #FFB300);
            color: #1A1A1A;
            font-weight: bold;
            border: 2px solid #FF8F00;
            box-shadow: 0 4px 8px rgba(255, 193, 7, 0.3);
            text-shadow: 1px 1px 2px rgba(255,255,255,0.7);
            transition: all 0.3s ease;
        }
        
        .btn-theme-zama:hover {
            background: linear-gradient(135deg, #FFE082, #FFD700);
            transform: translateY(-3px);
            box-shadow: 0 8px 16px rgba(255, 193, 7, 0.5);
        }
        
        .btn-theme-zama.active {
            background: linear-gradient(135deg, #FF8F00, #FFB300);
            color: white;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.7);
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(255, 143, 0, 0.6);
        }
        
        .zama-glow {
            background: linear-gradient(135deg, #FFD700, #FF8F00);
            color: #1A1A1A;
            font-weight: bold;
            text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
            animation: zama-pulse 2s infinite;
            border: 3px solid #FFB300;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        @keyframes zama-pulse {
            0% { 
                box-shadow: 0 0 0 0 rgba(255, 215, 0, 0.7);
                transform: scale(1);
            }
            50% { 
                box-shadow: 0 0 0 15px rgba(255, 215, 0, 0.3);
                transform: scale(1.02);
            }
            100% { 
                box-shadow: 0 0 0 0 rgba(255, 215, 0, 0);
                transform: scale(1);
            }
        }
        
        @keyframes sparkle-fade {
            0% { opacity: 1; transform: translateY(0) scale(1) rotate(0deg); }
            100% { opacity: 0; transform: translateY(-100px) scale(0.5) rotate(180deg); }
        }
        
        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
            }
            
            .header h1 {
                font-size: 1.8rem;
            }
            
            .theme-buttons {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔐 FHE Şifreli Sanat Galerisi</h1>
            <p>Zama Creator Program | Her etkileşim bir parçanın şifresini çözer</p>
        </div>
        
        <div class="main-content">
            <div class="art-section">
                <h2>🎨 Şifreli Sanat Eseri</h2>
                <div id="loading" class="loading">
                    <div class="spinner"></div>
                    <p>Sanat eseri oluşturuluyor...</p>
                </div>
                <div class="art-display">
                    <img id="artImage" class="art-image" src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAwIiBoZWlnaHQ9IjYwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjMmMzZTUwIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIyNCIgZmlsbD0iIzk1YTVhNiIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPvCfkZMgU2FuYXQgZXNlcmluaXogYnVyYWRhIGfDtnJ1bnTDvGxlbmVjZWs8L3RleHQ+PC9zdmc+" alt="Sanat Eseri">
                </div>
                <div id="themeInfo">
                    <p><strong>Tema:</strong> <span id="currentTheme">Henüz seçilmedi</span></p>
                </div>
                <div id="messages"></div>
            </div>
            
            <div class="controls">
                <div class="control-group">
                    <h3>🎨 Tema Seçimi</h3>
                    
                    <!-- Zama Özel Temalar -->
                    <div class="theme-category zama-themes">
                        <h4>⭐ ZAMA ÖZEL TEMALARI</h4>
                        <div class="theme-buttons">
                            <button class="btn btn-theme-zama active" data-theme="zama_classic">🟨 Klasik</button>
                            <button class="btn btn-theme-zama" data-theme="zama_minimal">🔒 Minimal</button>
                            <button class="btn btn-theme-zama" data-theme="zama_geometric">📦 Geometrik</button>
                            <button class="btn btn-theme-zama" data-theme="zama_vision">🌟 Vizyon</button>
                        </div>
                    </div>
                    
                    <!-- Klasik Temalar -->
                    <div class="theme-category">
                        <h4 style="margin-bottom: 10px;">📚 Klasik Temalar</h4>
                        <div class="theme-buttons">
                            <button class="btn btn-theme" data-theme="space">🚀 Uzay</button>
                            <button class="btn btn-theme" data-theme="abstract">🎨 Soyut</button>
                            <button class="btn btn-theme" data-theme="tech">💻 Teknoloji</button>
                            <button class="btn btn-theme" data-theme="crypto">₿ Kripto</button>
                        </div>
                    </div>
                    
                    <button id="generateBtn" class="btn btn-primary btn-block zama-glow">🎲 Zama Sanatı Oluştur</button>
                </div>
                
                <div class="control-group">
                    <h3>🔓 FHE İşlemleri</h3>
                    <button id="revealOneBtn" class="btn btn-primary btn-block">🔓 Bir Parça Çöz</button>
                    <button id="revealFiveBtn" class="btn btn-danger btn-block">⚡ 5 Parça Çöz</button>
                    <button id="autoRevealBtn" class="btn btn-warning btn-block">🤖 Otomatik Çözme</button>
                </div>
                
                <div class="control-group">
                    <h3>💾 İşlemler</h3>
                    <button id="downloadBtn" class="btn btn-success btn-block">📥 Eseri İndir</button>
                    <button id="resetBtn" class="btn btn-danger btn-block">🔄 Sıfırla</button>
                </div>
                
                <div class="control-group">
                    <h3>📊 İstatistikler</h3>
                    <div class="stats">
                        <div class="stat-item">
                            <span>Toplam Parça:</span>
                            <span id="totalPieces" class="stat-value">0</span>
                        </div>
                        <div class="stat-item">
                            <span>Çözülmüş:</span>
                            <span id="revealedPieces" class="stat-value">0</span>
                        </div>
                        <div class="stat-item">
                            <span>Gizli:</span>
                            <span id="hiddenPieces" class="stat-value">0</span>
                        </div>
                        <div class="stat-item">
                            <span>Şifre Anahtarı:</span>
                            <span id="encryptionKey" class="stat-value">-</span>
                        </div>
                    </div>
                </div>
                
                <div class="fhe-info" id="fheInfo">
                    🔐 FHE (Fully Homomorphic Encryption) ile şifreli hesaplama hazır!
                    <br><br>
                    Zama teknolojisi sayesinde verileriniz şifreli kalarak işleniyor.
                </div>
            </div>
        </div>
        
        <div class="progress-section">
            <h3>📈 Çözülme İlerlemesi</h3>
            <div class="progress-bar">
                <div id="progressFill" class="progress-fill"></div>
            </div>
            <p id="progressText">0/0 parça çözüldü (0%)</p>
        </div>
    </div>
    
    <script>
        // Global değişkenler
        let selectedTheme = 'zama_classic';
        let autoRevealInterval = null;
        let sessionId = 'session-' + Date.now();
        
        // API çağrısı yap
        async function apiCall(endpoint, method = 'GET', data = null) {
            try {
                const options = {
                    method: method,
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Session-ID': sessionId
                    }
                };
                
                if (data) {
                    options.body = JSON.stringify(data);
                }
                
                const response = await fetch(`/api/${endpoint}`, options);
                return await response.json();
            } catch (error) {
                console.error('API Error:', error);
                return { success: false, error: error.message };
            }
        }
        
        // Yardımcı fonksiyonlar
        function showMessage(message, type = 'info') {
            const messagesDiv = document.getElementById('messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}`;
            messageDiv.textContent = message;
            messagesDiv.appendChild(messageDiv);
            setTimeout(() => messageDiv.remove(), 5000);
        }
        
        function showLoading(show = true) {
            document.getElementById('loading').style.display = show ? 'block' : 'none';
        }
        
        function updateStats(stats) {
            document.getElementById('totalPieces').textContent = stats.total || 0;
            document.getElementById('revealedPieces').textContent = stats.revealed || 0;
            document.getElementById('hiddenPieces').textContent = (stats.total - stats.revealed) || 0;
            document.getElementById('encryptionKey').textContent = stats.encryption_key || '-';
            
            const percentage = stats.total ? Math.round((stats.revealed / stats.total) * 100) : 0;
            document.getElementById('progressFill').style.width = percentage + '%';
            document.getElementById('progressText').textContent = 
                `${stats.revealed || 0}/${stats.total || 0} parça çözüldü (${percentage}%)`;
            
            if (stats.theme) {
                let themeDisplay = stats.theme.replace('_', ' ');
                themeDisplay = themeDisplay.charAt(0).toUpperCase() + themeDisplay.slice(1);
                document.getElementById('currentTheme').textContent = themeDisplay;
            }
        }
        
        function updateFHEInfo(message) {
            document.getElementById('fheInfo').innerHTML = 
                `🔐 ${message}<br><br>Timestamp: ${new Date().toLocaleTimeString()}`;
        }
        
        function updateArtImage(imageData) {
            document.getElementById('artImage').src = imageData;
        }
        
        function triggerZamaEffects() {
            const sparkles = ['✨', '🌟', '⭐', '💫'];
            for (let i = 0; i < 5; i++) {
                setTimeout(() => {
                    const sparkle = document.createElement('div');
                    sparkle.textContent = sparkles[Math.floor(Math.random() * sparkles.length)];
                    sparkle.style.position = 'fixed';
                    sparkle.style.left = Math.random() * window.innerWidth + 'px';
                    sparkle.style.top = Math.random() * window.innerHeight + 'px';
                    sparkle.style.fontSize = '24px';
                    sparkle.style.pointerEvents = 'none';
                    sparkle.style.zIndex = '9999';
                    sparkle.style.animation = 'sparkle-fade 2s ease-out forwards';
                    document.body.appendChild(sparkle);
                    setTimeout(() => sparkle.remove(), 2000);
                }, i * 200);
            }
            updateFHEInfo('🌟 Zama teması seçildi! FHE teknolojisinin gücünü hissedeceksiniz...');
        }
        
        // Ana fonksiyonlar
        async function generateArt() {
            showLoading(true);
            updateFHEInfo('Yeni sanat eseri oluşturuluyor...');
            
            const result = await apiCall('generate_art', 'POST', { theme: selectedTheme });
            showLoading(false);
            
            if (result.success) {
                updateArtImage(result.image);
                updateStats(result.stats);
                if (selectedTheme.startsWith('zama_')) {
                    updateFHEInfo(`🌟 ${result.stats.theme.replace('_', ' ').toUpperCase()} sanat eseri oluşturuldu! Zama FHE şifreleme aktif.`);
                    showMessage(`🎨 ${result.message} ✨ Zama'nın gücüyle şifrelendi!`, 'success');
                } else {
                    updateFHEInfo(`${selectedTheme} temalı sanat eseri oluşturuldu! FHE şifreleme aktif.`);
                    showMessage(result.message, 'success');
                }
            } else {
                showMessage(result.error || 'Sanat oluşturulurken hata oluştu!', 'error');
            }
        }
        
        async function revealOnePiece() {
            updateFHEInfo('FHE ile parça şifresi çözülüyor...');
            const result = await apiCall('reveal_piece', 'POST');
            
            if (result.success) {
                updateArtImage(result.image);
                updateStats(result.stats);
                updateFHEInfo(`Parça #${result.revealed_piece.id} şifresi çözüldü! Pozisyon: (${result.revealed_piece.position[0]}, ${result.revealed_piece.position[1]})`);
                showMessage(result.message, 'success');
                
                if (result.completed) {
                    showMessage('🎉 Tebrikler! Tüm parçaların şifresi çözüldü!', 'success');
                    updateFHEInfo('✅ FHE işlemi tamamlandı! Tüm parçalar çözüldü.');
                    if (selectedTheme.startsWith('zama_')) {
                        setTimeout(() => showMessage('🌟 Zama FHE teknolojisiyle mükemmel bir deneyim yaşadınız!', 'info'), 1000);
                    }
                }
            } else {
                showMessage(result.error || 'Parça çözülürken hata oluştu!', 'error');
                if (result.completed) updateFHEInfo('ℹ️ Tüm parçalar zaten çözülmüş durumda.');
            }
        }
        
        async function revealMultiplePieces() {
            updateFHEInfo('⚡ Toplu FHE işlemi başlatılıyor...');
            const result = await apiCall('reveal_multiple', 'POST', { count: 5 });
            
            if (result.success) {
                updateArtImage(result.image);
                updateStats(result.stats);
                updateFHEInfo('⚡ Toplu FHE işlemi tamamlandı!');
                showMessage(result.message, 'success');
                if (result.completed) showMessage('🎉 Tebrikler! Tüm parçaların şifresi çözüldü!', 'success');
            } else {
                showMessage(result.error || 'Toplu çözme hatası!', 'error');
            }
        }
        
        function toggleAutoReveal() {
            const btn = document.getElementById('autoRevealBtn');
            if (autoRevealInterval) {
                clearInterval(autoRevealInterval);
                autoRevealInterval = null;
                btn.textContent = '🤖 Otomatik Çözme';
                btn.classList.remove('active');
                updateFHEInfo('⏸️ Otomatik FHE çözme durduruldu.');
            } else {
                autoRevealInterval = setInterval(revealOnePiece, 3000);
                btn.textContent = '⏸️ Durdur';
                btn.classList.add('active');
                updateFHEInfo('🤖 Otomatik FHE çözme başlatıldı! Her 3 saniyede bir parça...');
            }
        }
        
        async function downloadArt() {
            updateFHEInfo('💾 Sanat eseri indiriliyor...');
            try {
                const response = await fetch('/api/download_art', { headers: { 'X-Session-ID': sessionId } });
                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.style.display = 'none';
                    a.href = url;
                    a.download = `fhe_art_${selectedTheme}_${Date.now()}.png`;
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                    showMessage('✅ Sanat eseri başarıyla indirildi!', 'success');
                    updateFHEInfo('💾 Sanat eseri başarıyla kaydedildi.');
                } else {
                    showMessage('❌ İndirme hatası!', 'error');
                }
            } catch (error) {
                showMessage('❌ İndirme hatası: ' + error.message, 'error');
            }
        }
        
        async function resetSession() {
            if (confirm('🔄 Session sıfırlanacak ve tüm veriler silinecek. Emin misiniz?')) {
                if (autoRevealInterval) {
                    clearInterval(autoRevealInterval);
                    autoRevealInterval = null;
                    document.getElementById('autoRevealBtn').textContent = '🤖 Otomatik Çözme';
                }
                
                const result = await apiCall('reset_session', 'POST');
                if (result.success) {
                    updateArtImage('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAwIiBoZWlnaHQ9IjYwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjMmMzZTUwIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIyNCIgZmlsbD0iIzk1YTVhNiIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPvCfkZMgU2FuYXQgZXNlcmluaXogYnVyYWRhIGfDtnJ1bnTDvGxlbmVjZWs8L3RleHQ+PC9zdmc+');
                    updateStats({ total: 0, revealed: 0, encryption_key: '-' });
                    updateFHEInfo('🔄 Session sıfırlandı. Yeni sanat eseri oluşturabilirsiniz.');
                    document.getElementById('currentTheme').textContent = 'Henüz seçilmedi';
                    document.getElementById('messages').innerHTML = '';
                    showMessage('✅ Session başarıyla sıfırlandı!', 'success');
                } else {
                    showMessage('❌ Sıfırlama hatası!', 'error');
                }
            }
        }
        
        // Event listener'ları ayarla
        document.addEventListener('DOMContentLoaded', function() {
            // Zama tema butonları
            document.querySelectorAll('.btn-theme-zama').forEach(btn => {
                btn.addEventListener('click', function() {
                    document.querySelectorAll('.btn-theme, .btn-theme-zama').forEach(b => b.classList.remove('active'));
                    this.classList.add('active');
                    selectedTheme = this.getAttribute('data-theme');
                    triggerZamaEffects();
                });
            });
            
            // Klasik tema butonları
            document.querySelectorAll('.btn-theme').forEach(btn => {
                btn.addEventListener('click', function() {
                    document.querySelectorAll('.btn-theme, .btn-theme-zama').forEach(b => b.classList.remove('active'));
                    this.classList.add('active');
                    selectedTheme = this.getAttribute('data-theme');
                });
            });
            
            // İlk tema seçimi
            document.querySelector('.btn-theme-zama[data-theme="zama_classic"]').classList.add('active');
            
            // Buton event listener'ları
            document.getElementById('generateBtn').addEventListener('click', generateArt);
            document.getElementById('revealOneBtn').addEventListener('click', revealOnePiece);
            document.getElementById('revealFiveBtn').addEventListener('click', revealMultiplePieces);
            document.getElementById('autoRevealBtn').addEventListener('click', toggleAutoReveal);
            document.getElementById('downloadBtn').addEventListener('click', downloadArt);
            document.getElementById('resetBtn').addEventListener('click', resetSession);
            
            // Başlangıç mesajı
            updateFHEInfo('Zama FHE teknolojisi hazır! Bir tema seçip sanat eserinizi oluşturun.');
        });
    </script>
</body>
</html>
    '''
    
    with open('templates/art_gallery.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

@app.route('/')
def index():
    """Ana sayfa"""
    return render_template('art_gallery.html')

@app.route('/api/generate_art', methods=['POST'])
def generate_art():
    """Yeni sanat eseri oluştur"""
    try:
        session_id = get_session_id()
        art_gen = get_art_generator(session_id)
        
        data = request.get_json()
        theme = data.get('theme', 'zama_classic')
        
        # Sanat oluştur
        art_gen.reset_encryption()
        art_path = art_gen.generate_base_art(theme)
        
        # Parçalara ayır
        encrypted_pieces = art_gen.encrypt_art_pieces(art_path)
        
        # Session data güncelle
        session_data[session_id]['encrypted_pieces'] = encrypted_pieces
        session_data[session_id]['stats'] = {
            'revealed': 0,
            'total': len(encrypted_pieces),
            'theme': theme,
            'encryption_key': art_gen.encryption_key
        }
        
        # İlk progress görüntüsü
        progress_img = art_gen.generate_progress_image(encrypted_pieces)
        
        # Base64'e çevir
        img_buffer = BytesIO()
        progress_img.save(img_buffer, format='PNG')
        img_data = base64.b64encode(img_buffer.getvalue()).decode()
        
        # Tema ismi düzelt
        theme_display = theme.replace('_', ' ').title()
        if 'Zama' in theme_display:
            theme_display = theme_display.replace('Zama', 'Zama')
        
        return jsonify({
            'success': True,
            'message': f'{theme_display} temalı sanat eseri oluşturuldu!',
            'image': f"data:image/png;base64,{img_data}",
            'stats': session_data[session_id]['stats'],
            'total_pieces': len(encrypted_pieces)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/reveal_piece', methods=['POST'])
def reveal_piece():
    """Rastgele bir parça çöz"""
    try:
        session_id = get_session_id()
        
        if session_id not in session_data:
            return jsonify({
                'success': False,
                'error': 'Önce bir sanat eseri oluşturun!'
            }), 400
        
        art_gen = art_generators[session_id]
        encrypted_pieces = session_data[session_id]['encrypted_pieces']
        stats = session_data[session_id]['stats']
        
        # Çözülmemiş parça bul
        hidden_pieces = [i for i, p in enumerate(encrypted_pieces) 
                        if not p['is_revealed']]
        
        if not hidden_pieces:
            return jsonify({
                'success': False,
                'error': 'Tüm parçalar zaten çözülmüş!',
                'completed': True
            })
        
        # Rastgele parça seç ve çöz
        import random
        piece_index = random.choice(hidden_pieces)
        success = art_gen.reveal_piece(encrypted_pieces, piece_index)
        
        if success:
            stats['revealed'] += 1
            
            # Güncel görüntü oluştur
            progress_img = art_gen.generate_progress_image(encrypted_pieces)
            
            # Base64'e çevir
            img_buffer = BytesIO()
            progress_img.save(img_buffer, format='PNG')
            img_data = base64.b64encode(img_buffer.getvalue()).decode()
            
            # Parça bilgisi
            revealed_piece = encrypted_pieces[piece_index]
            
            return jsonify({
                'success': True,
                'message': f"Parça #{revealed_piece['piece_id']:02d} çözüldü!",
                'image': f"data:image/png;base64,{img_data}",
                'stats': stats,
                'revealed_piece': {
                    'id': revealed_piece['piece_id'],
                    'position': revealed_piece['position']
                },
                'completed': stats['revealed'] >= stats['total']
            })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/reveal_multiple', methods=['POST'])
def reveal_multiple():
    """Birden fazla parça çöz"""
    try:
        session_id = get_session_id()
        data = request.get_json()
        count = min(data.get('count', 5), 10)
        
        results = []
        for i in range(count):
            result = reveal_piece()
            if result[1] == 200:
                result_data = json.loads(result[0].data)
                if not result_data['success']:
                    break
                results.append(result_data)
            else:
                break
        
        if results:
            final_result = results[-1]
            final_result['message'] = f"{len(results)} parça çözüldü!"
            return jsonify(final_result)
        else:
            return jsonify({
                'success': False,
                'error': 'Hiçbir parça çözülemedi!'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/get_stats', methods=['GET'])
def get_stats():
    """Mevcut istatistikleri al"""
    try:
        session_id = get_session_id()
        
        if session_id not in session_data:
            return jsonify({
                'success': False,
                'error': 'Aktif session bulunamadı!'
            })
        
        stats = session_data[session_id]['stats']
        return jsonify({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/download_art', methods=['GET'])
def download_art():
    """Sanat eserini indir"""
    try:
        session_id = get_session_id()
        
        if session_id not in session_data:
            return jsonify({
                'success': False,
                'error': 'Aktif session bulunamadı!'
            }), 400
        
        art_gen = art_generators[session_id]
        encrypted_pieces = session_data[session_id]['encrypted_pieces']
        stats = session_data[session_id]['stats']
        
        # Yüksek çözünürlüklü görüntü oluştur
        progress_img = art_gen.generate_progress_image(encrypted_pieces, (1200, 1200))
        
        # Temporary file oluştur
        temp_filename = f"fhe_art_{stats.get('theme', 'unknown')}_{stats['revealed']}of{stats['total']}.png"
        temp_path = os.path.join('temp', temp_filename)
        
        # Temp klasörü oluştur
        os.makedirs('temp', exist_ok=True)
        
        progress_img.save(temp_path)
        
        return send_file(temp_path, 
                        as_attachment=True, 
                        download_name=temp_filename,
                        mimetype='image/png')
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/reset_session', methods=['POST'])
def reset_session():
    """Session'ı sıfırla"""
    try:
        session_id = get_session_id()
        
        if session_id in art_generators:
            del art_generators[session_id]
        if session_id in session_data:
            del session_data[session_id]
        
        return jsonify({
            'success': True,
            'message': 'Session sıfırlandı!'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Cleanup fonksiyonu
def cleanup_temp_files():
    """Geçici dosyaları temizle"""
    import glob
    temp_files = glob.glob('temp/*.png') + glob.glob('*.png')
    for file in temp_files:
        try:
            if os.path.exists(file) and file != 'icon.png':
                os.remove(file)
        except:
            pass

# Uygulama başlatma
if __name__ == '__main__':
    import atexit
    atexit.register(cleanup_temp_files)
    
    # Templates oluştur
    create_templates()
    
    print("🎨 FHE Sanat Web Uygulaması Başlatılıyor...")
    print("📱 Tarayıcınızda http://localhost:5000 adresini açın")
    print("🔐 Zama Creator Program | FHE Şifreli Sanat Galerisi")
    print("🌟 Varsayılan tema: Zama Classic")
    
    # Debug modda çalıştır
    app.run(debug=True, host='0.0.0.0', port=5000)