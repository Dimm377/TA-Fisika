"""
🔬 Simulasi Gaya Pegas - Hooke's Law
====================================

Aplikasi Streamlit interaktif untuk simulasi sistem massa-pegas.

Features:
- Mode Preset (real-life examples)
- Mode Custom (user-defined parameters)
- Animasi pegas real-time
- Visualisasi posisi, kecepatan, energi
- Penjelasan fisika lengkap

Jalankan:
    streamlit run app.py

Author: Dimas
Tugas Akhir Fisika Komputasi
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_agg import FigureCanvasAgg

from spring_physics import (
    SpringParameters, 
    PRESETS,
    DampingType,
    solve_spring_system,
    no_force,
    step_force,
    harmonic_force,
    impulse_force,
    PHYSICS_EXPLANATION,
    # Premium features
    validate_numerical_solution,
    frequency_analysis,
    resonance_analysis,
    generate_conclusions,
    export_to_csv
)
from spring_visualization import (
    create_static_plots,
    create_spring_animation_figure,
    draw_spring,
    COLORS
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Simulasi Gaya Pegas",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>
    /* ============================================
       RESPONSIVE & INTERACTIVE UI STYLES
       ============================================ */
    
    /* Root variables for theming */
    :root {
        --primary: #3B82F6;
        --primary-light: #60A5FA;
        --secondary: #22C55E;
        --accent: #8B5CF6;
        --danger: #EF4444;
        --warning: #F59E0B;
        --bg-primary: #0E1117;
        --bg-secondary: #1E2329;
        --bg-card: #262B33;
        --border: #374151;
        --text: #E5E7EB;
        --text-muted: #9CA3AF;
        --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Base responsive container */
    .main .block-container {
        padding: 1.5rem 2rem;
        max-width: 1600px;
        transition: var(--transition);
    }
    
    /* Responsive breakpoints */
    @media (max-width: 1200px) {
        .main .block-container {
            padding: 1rem 1.5rem;
        }
    }
    
    @media (max-width: 768px) {
        .main .block-container {
            padding: 0.75rem 1rem;
        }
    }
    
    /* Header with animation */
    .main-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #0d1b2a 100%);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(59, 130, 246, 0.3);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.6s ease-out;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(59, 130, 246, 0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    .main-header h1 {
        background: linear-gradient(90deg, #60A5FA, #34D399, #A78BFA);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        position: relative;
        animation: gradientShift 3s ease infinite;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% center; }
        50% { background-position: 100% center; }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.5; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.05); }
    }
    
    /* Interactive cards with hover effects */
    .info-card {
        background: linear-gradient(145deg, var(--bg-secondary), var(--bg-card));
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid var(--border);
        margin-bottom: 1rem;
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }
    
    .info-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent);
        transition: left 0.5s ease;
    }
    
    .info-card:hover {
        border-color: var(--primary-light);
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(59, 130, 246, 0.15);
    }
    
    .info-card:hover::after {
        left: 100%;
    }
    
    .info-card h3 {
        color: var(--primary-light);
        margin-top: 0;
    }
    
    /* Preset card with glass effect */
    .preset-card {
        background: rgba(30, 35, 41, 0.8);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1.25rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: var(--transition);
        cursor: pointer;
    }
    
    .preset-card:hover {
        border-color: var(--primary);
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 15px 35px rgba(59, 130, 246, 0.2);
        background: rgba(30, 35, 41, 0.95);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1117 0%, #161b22 100%);
        border-right: 1px solid var(--border);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
    }
    
    /* Metrics with animation */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        transition: var(--transition);
    }
    
    [data-testid="metric-container"] {
        background: linear-gradient(145deg, var(--bg-secondary), var(--bg-card));
        border-radius: 12px;
        padding: 1rem !important;
        border: 1px solid var(--border);
        transition: var(--transition);
    }
    
    [data-testid="metric-container"]:hover {
        border-color: var(--primary);
        transform: scale(1.02);
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: var(--bg-secondary);
        padding: 8px;
        border-radius: 12px;
        border: 1px solid var(--border);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 20px;
        transition: var(--transition);
        font-weight: 500;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(59, 130, 246, 0.1);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary), #2563EB) !important;
        color: white !important;
    }
    
    /* Buttons with ripple effect */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary), #2563EB);
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Sliders */
    .stSlider > div > div > div > div {
        background: var(--primary) !important;
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: 10px;
        transition: var(--transition);
    }
    
    .stSelectbox > div > div:hover {
        border-color: var(--primary);
    }
    
    /* Number inputs */
    .stNumberInput > div > div > input {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: 8px;
        transition: var(--transition);
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: var(--bg-secondary);
        border-radius: 10px;
        transition: var(--transition);
    }
    
    .streamlit-expanderHeader:hover {
        background: var(--bg-card);
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, var(--secondary), #16A34A);
        width: 100%;
    }
    
    .stDownloadButton > button:hover {
        box-shadow: 0 8px 25px rgba(34, 197, 94, 0.3);
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid var(--border);
    }
    
    /* Alert boxes */
    .stAlert {
        border-radius: 12px;
        border-left-width: 4px;
    }
    
    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }
    
    /* Loading animation for content */
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-primary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary);
    }
    
    /* Tooltip styling */
    [data-tooltip] {
        position: relative;
    }
    
    [data-tooltip]:hover::after {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        background: var(--bg-card);
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 12px;
        white-space: nowrap;
        z-index: 1000;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="main-header">
    <h1>🔬 Simulasi Gaya Pegas</h1>
    <p style="color: #94A3B8; margin-top: 0.5rem;">
        Eksplorasi Hukum Hooke dan Dinamika Sistem Massa-Pegas
    </p>
</div>
""", unsafe_allow_html=True)


# Sidebar dihapus - semua kontrol dipindah ke main content untuk responsif mobile


# ============================================================
# MAIN CONTENT
# ============================================================

# Mobile-friendly settings in main area
with st.expander("⚙️ **Pengaturan Simulasi** (Klik untuk buka/tutup)", expanded=True):
    mode = st.radio(
        "Mode Simulasi:",
        ["📦 Preset Real-Life", "🔧 Custom"],
        horizontal=True,
        key="main_mode"
    )
    
    if mode == "📦 Preset Real-Life":
        preset_names = list(PRESETS.keys())
        preset_labels = [PRESETS[k].name for k in preset_names]
        
        selected_label = st.selectbox(
            "🎯 Pilih Contoh Sistem:",
            preset_labels,
            key="main_preset"
        )
        
        selected_key = preset_names[preset_labels.index(selected_label)]
        params = PRESETS[selected_key]
        st.success(f"📋 {params.description}")
        
        # Show parameters
        pc1, pc2, pc3, pc4 = st.columns(4)
        pc1.metric("m", f"{params.m} kg")
        pc2.metric("k", f"{params.k} N/m")
        pc3.metric("c", f"{params.c} Ns/m")
        pc4.metric("ζ", f"{params.zeta:.3f}")
        
    else:  # Custom mode
        cc1, cc2 = st.columns(2)
        with cc1:
            m = st.number_input("Massa (kg)", 0.01, 1000.0, 1.0, 0.1, key="main_m")
            k = st.number_input("Konstanta k (N/m)", 0.1, 100000.0, 100.0, 1.0, key="main_k")
        with cc2:
            c = st.number_input("Redaman (Ns/m)", 0.0, 10000.0, 1.0, 0.1, key="main_c")
            x0 = st.number_input("Posisi awal x₀ (m)", -1.0, 1.0, 0.5, 0.01, key="main_x0")
        
        params = SpringParameters(m=m, k=k, c=c, x0=x0, v0=0.0, name="Custom")
    
    # Time and force settings
    tc1, tc2 = st.columns(2)
    with tc1:
        t_max = st.slider("⏱️ Durasi (s)", 1.0, 30.0, 10.0, 0.5, key="main_tmax")
    with tc2:
        force_type = st.selectbox(
            "🌊 Gaya Eksternal:",
            ["Tanpa Gaya", "Step Force", "Harmonic Force"],
            key="main_force"
        )
    
    F_ext = None
    if force_type == "Step Force":
        F_ext = step_force(10.0, 1.0)
        st.caption("Step Force: 10N mulai dari t=1s")
    elif force_type == "Harmonic Force":
        F_ext = harmonic_force(10.0, 5.0)
        st.caption("Harmonic Force: 10N @ ω=5 rad/s")

# Solve the system
solution = solve_spring_system(params, (0, t_max), dt=0.001, F_ext=F_ext)

# Display system info
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Frekuensi Natural", f"{params.omega_n:.2f} rad/s")
with col2:
    st.metric("Periode", f"{params.period:.3f} s" if params.period < float('inf') else "∞")
with col3:
    st.metric("Rasio Redaman ζ", f"{params.zeta:.3f}")
with col4:
    damping_icon = {"Tanpa Redaman": "🟢", "Underdamped": "🔵", 
                    "Critically Damped": "🟡", "Overdamped": "🔴"}
    st.metric("Tipe Redaman", f"{damping_icon.get(params.damping_type.value, '')} {params.damping_type.value[:10]}")
with col5:
    energy_loss = (solution['E_total'][0] - solution['E_total'][-1]) / solution['E_total'][0] * 100
    st.metric("Energi Hilang", f"{energy_loss:.1f}%")

st.markdown("---")

# Tabs - 6 tabs untuk analisis lengkap
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🎬 Animasi", 
    "📊 Grafik", 
    "🔬 Validasi & FFT", 
    "📚 Teori", 
    "🎯 Kesimpulan",
    "📥 Ekspor"
])

with tab1:
    st.markdown("### 🎬 Animasi Sistem Massa-Pegas")
    st.caption("Animasi berjalan smooth 60 FPS langsung di browser. Klik Play untuk memulai!")
    
    # Prepare data for JavaScript
    t_data = solution['t']
    x_data = solution['x']
    v_data = solution['v']
    E_data = solution['E_total']
    
    # Sample data for performance (max 500 points)
    sample_step = max(1, len(t_data) // 500)
    t_js = t_data[::sample_step].tolist()
    x_js = x_data[::sample_step].tolist()
    v_js = v_data[::sample_step].tolist()
    E_js = E_data[::sample_step].tolist()
    
    x_max = max(abs(x_data.max()), abs(x_data.min()), 0.3)
    
    # HTML5 Canvas Animation - Enhanced Visual with Responsive Design
    animation_html = f"""
    <style>
        @media (max-width: 600px) {{
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr) !important;
            }}
            .stats-grid .stat-value {{
                font-size: 16px !important;
            }}
            .spring-title {{
                font-size: 14px !important;
            }}
        }}
    </style>
    <div style="background: linear-gradient(180deg, #1a1f2e 0%, #0d1117 100%); border-radius: 16px; padding: 25px; border: 1px solid #30363d; box-shadow: 0 8px 32px rgba(0,0,0,0.3);">
        <div style="text-align: center; margin-bottom: 15px;">
            <span class="spring-title" style="color: #58a6ff; font-size: 18px; font-weight: bold;">🔬 {params.name}</span>
        </div>
        
        <div id="springCanvasContainer" style="width: 100%; max-width: 100%; overflow: hidden;">
            <canvas id="springCanvas" style="display: block; margin: 0 auto; border-radius: 12px; width: 100%; max-width: 700px;"></canvas>
        </div>
        
        <div style="display: flex; justify-content: center; gap: 12px; margin-top: 20px; flex-wrap: wrap;">
            <button id="playBtn" onclick="togglePlay()" style="
                background: linear-gradient(135deg, #238636, #2ea043);
                color: white; border: none; padding: 14px 35px; border-radius: 10px;
                font-size: 16px; cursor: pointer; font-weight: bold;
                transition: all 0.3s; box-shadow: 0 4px 20px rgba(35,134,54,0.4);
                display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 20px;">▶️</span> Play
            </button>
            <button onclick="resetAnim()" style="
                background: linear-gradient(135deg, #21262d, #30363d);
                color: #c9d1d9; border: 1px solid #30363d; padding: 14px 25px;
                border-radius: 10px; font-size: 14px; cursor: pointer;
                transition: all 0.3s; display: flex; align-items: center; gap: 6px;">
                <span>🔄</span> Reset
            </button>
            <select id="speedSelect" onchange="changeSpeed()" style="
                background: linear-gradient(135deg, #21262d, #30363d);
                color: #c9d1d9; border: 1px solid #30363d; padding: 14px 20px;
                border-radius: 10px; font-size: 14px; cursor: pointer;">
                <option value="0.25">🐢 0.25x</option>
                <option value="0.5">🚶 0.5x</option>
                <option value="1" selected>🏃 1x</option>
                <option value="2">🚀 2x</option>
                <option value="4">⚡ 4x</option>
            </select>
        </div>
        
        <div style="margin: 20px 10px 10px;">
            <input type="range" id="frameSlider" min="0" max="{len(t_js)-1}" value="0" 
                   style="width: 100%; height: 8px; accent-color: #58a6ff; cursor: pointer;" 
                   oninput="seekFrame(this.value)">
            <div style="display: flex; justify-content: space-between; color: #8b949e; font-size: 11px; margin-top: 5px;">
                <span>0.00s</span>
                <span id="currentTimeLabel" style="color: #58a6ff; font-weight: bold;">t = 0.000 s</span>
                <span>{t_js[-1]:.2f}s</span>
            </div>
        </div>
        
        <div class="stats-grid" style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-top: 15px;">
            <div style="background: linear-gradient(135deg, #161b22, #0d1117); padding: 18px 12px; border-radius: 12px; text-align: center; border: 1px solid #21262d;">
                <div style="color: #8b949e; font-size: 11px; text-transform: uppercase; letter-spacing: 1px;">⏱️ Waktu</div>
                <div id="timeVal" class="stat-value" style="color: #f0f6fc; font-size: 22px; font-weight: bold; margin-top: 8px; font-family: 'Courier New', monospace;">0.000 s</div>
            </div>
            <div style="background: linear-gradient(135deg, #161b22, #0d1117); padding: 18px 12px; border-radius: 12px; text-align: center; border: 1px solid #21262d;">
                <div style="color: #8b949e; font-size: 11px; text-transform: uppercase; letter-spacing: 1px;">📍 Posisi</div>
                <div id="posVal" class="stat-value" style="color: #58a6ff; font-size: 22px; font-weight: bold; margin-top: 8px; font-family: 'Courier New', monospace;">0.0000 m</div>
            </div>
            <div style="background: linear-gradient(135deg, #161b22, #0d1117); padding: 18px 12px; border-radius: 12px; text-align: center; border: 1px solid #21262d;">
                <div style="color: #8b949e; font-size: 11px; text-transform: uppercase; letter-spacing: 1px;">🏃 Kecepatan</div>
                <div id="velVal" class="stat-value" style="color: #3fb950; font-size: 22px; font-weight: bold; margin-top: 8px; font-family: 'Courier New', monospace;">0.000 m/s</div>
            </div>
            <div style="background: linear-gradient(135deg, #161b22, #0d1117); padding: 18px 12px; border-radius: 12px; text-align: center; border: 1px solid #21262d;">
                <div style="color: #8b949e; font-size: 11px; text-transform: uppercase; letter-spacing: 1px;">⚡ Energi</div>
                <div id="energyVal" class="stat-value" style="color: #f85149; font-size: 22px; font-weight: bold; margin-top: 8px; font-family: 'Courier New', monospace;">0.0000 J</div>
            </div>
        </div>
    </div>
    
    <script>
        const canvas = document.getElementById('springCanvas');
        const ctx = canvas.getContext('2d');
        
        // Responsive canvas setup - VERTIKAL (tinggi lebih dari lebar)
        const BASE_WIDTH = 400;
        const BASE_HEIGHT = 450;
        
        function resizeCanvas() {{
            const container = document.getElementById('springCanvasContainer');
            const containerWidth = container.offsetWidth;
            const width = Math.min(BASE_WIDTH, containerWidth);
            const height = (width / BASE_WIDTH) * BASE_HEIGHT;
            
            canvas.width = width;
            canvas.height = height;
            canvas.style.width = width + 'px';
            canvas.style.height = height + 'px';
        }}
        resizeCanvas();
        window.addEventListener('resize', function() {{
            resizeCanvas();
            draw();
        }});
        
        // Data from Python
        const tData = {t_js};
        const xData = {x_js};
        const vData = {v_js};
        const EData = {E_js};
        const xMax = {x_max};
        const totalFrames = tData.length;
        
        let frameIdx = 0;
        let isPlaying = false;
        let speed = 1;
        let lastTime = 0;
        let animationId = null;
        
        // Fungsi menggambar pegas VERTIKAL yang lebih natural (heliks 3D)
        function drawSpringVertical(startY, endY, centerX, numCoils = 10) {{
            const scale = canvas.width / BASE_WIDTH;
            const springLen = endY - startY;
            if (springLen < 30 * scale) return;
            
            const coilHeight = (springLen - 20 * scale) / numCoils;
            const coilWidth = 20 * scale;  // Lebar coil
            
            // Gambar batang penghubung atas
            ctx.strokeStyle = '#6b7280';
            ctx.lineWidth = 3 * scale;
            ctx.beginPath();
            ctx.moveTo(centerX, startY);
            ctx.lineTo(centerX, startY + 10 * scale);
            ctx.stroke();
            
            // Gambar setiap coil dengan efek 3D
            for (let i = 0; i < numCoils; i++) {{
                const coilY = startY + 10 * scale + i * coilHeight;
                const nextCoilY = coilY + coilHeight;
                
                // Bagian belakang coil (lebih gelap - shadow)
                ctx.strokeStyle = '#1e40af';
                ctx.lineWidth = 4 * scale;
                ctx.beginPath();
                ctx.moveTo(centerX - coilWidth/2, coilY);
                ctx.quadraticCurveTo(centerX - coilWidth, coilY + coilHeight/2, centerX - coilWidth/2, nextCoilY);
                ctx.stroke();
                
                // Bagian depan coil (lebih terang - highlight)
                const gradCoil = ctx.createLinearGradient(centerX, coilY, centerX + coilWidth, coilY);
                gradCoil.addColorStop(0, '#3b82f6');
                gradCoil.addColorStop(0.5, '#93c5fd');
                gradCoil.addColorStop(1, '#3b82f6');
                
                ctx.strokeStyle = gradCoil;
                ctx.lineWidth = 5 * scale;
                ctx.beginPath();
                ctx.moveTo(centerX - coilWidth/2, coilY);
                ctx.quadraticCurveTo(centerX + coilWidth, coilY + coilHeight/2, centerX - coilWidth/2, nextCoilY);
                ctx.stroke();
                
                // Garis penghubung kanan (edge coil)
                ctx.strokeStyle = '#60a5fa';
                ctx.lineWidth = 3 * scale;
                ctx.beginPath();
                ctx.moveTo(centerX + coilWidth/2, coilY + coilHeight/4);
                ctx.lineTo(centerX + coilWidth/2, coilY + coilHeight * 3/4);
                ctx.stroke();
            }}
            
            // Gambar batang penghubung bawah
            ctx.strokeStyle = '#6b7280';
            ctx.lineWidth = 3 * scale;
            ctx.beginPath();
            ctx.moveTo(centerX, endY - 10 * scale);
            ctx.lineTo(centerX, endY);
            ctx.stroke();
        }}
        
        function draw() {{
            const scaleX = canvas.width / BASE_WIDTH;
            const scaleY = canvas.height / BASE_HEIGHT;
            const scale = Math.min(scaleX, scaleY);
            
            // Clear with gradient background
            const bgGrad = ctx.createLinearGradient(0, 0, 0, canvas.height);
            bgGrad.addColorStop(0, '#0d1117');
            bgGrad.addColorStop(1, '#161b22');
            ctx.fillStyle = bgGrad;
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            const x = xData[frameIdx];
            const t = tData[frameIdx];
            const v = vData[frameIdx];
            const E = EData[frameIdx];
            
            // ============================================
            // CEILING (Langit-langit/Penopang di atas)
            // ============================================
            const ceilingGrad = ctx.createLinearGradient(0, 0, 0, 35 * scaleY);
            ceilingGrad.addColorStop(0, '#4b5563');
            ceilingGrad.addColorStop(1, '#374151');
            ctx.fillStyle = ceilingGrad;
            ctx.fillRect(0, 0, canvas.width, 30 * scaleY);
            
            // Ceiling pattern
            ctx.strokeStyle = '#6b7280';
            ctx.lineWidth = 1;
            for (let i = 0; i < 6; i++) {{
                ctx.beginPath();
                ctx.moveTo(i * 80 * scaleX, 15 * scaleY);
                ctx.lineTo((i + 0.5) * 80 * scaleX, 28 * scaleY);
                ctx.stroke();
            }}
            
            // Hook/Mount point
            const hookX = canvas.width / 2;
            ctx.fillStyle = '#1f2937';
            ctx.beginPath();
            ctx.arc(hookX, 30 * scaleY, 8 * scale, 0, Math.PI * 2);
            ctx.fill();
            ctx.strokeStyle = '#4b5563';
            ctx.lineWidth = 2 * scale;
            ctx.stroke();
            
            // ============================================
            // EQUILIBRIUM LINE (Garis Kesetimbangan)
            // ============================================
            const equilibriumY = 200 * scaleY;
            ctx.strokeStyle = '#3fb950';
            ctx.lineWidth = 2 * scale;
            ctx.setLineDash([8 * scale, 4 * scale]);
            ctx.beginPath();
            ctx.moveTo(hookX - 60 * scaleX, equilibriumY);
            ctx.lineTo(hookX + 60 * scaleX, equilibriumY);
            ctx.stroke();
            ctx.setLineDash([]);
            
            // Label y = 0
            ctx.fillStyle = '#3fb950';
            ctx.font = 'bold ' + Math.max(10, 12 * scale) + 'px Arial';
            ctx.textAlign = 'left';
            ctx.fillText('y = 0', hookX + 70 * scaleX, equilibriumY + 4 * scaleY);
            
            // ============================================
            // CALCULATE MASS POSITION (Posisi Massa)
            // ============================================
            // Posisi massa berdasarkan displacement x (positif = ke bawah)
            const massY = equilibriumY + (x / xMax) * 100 * scaleY;
            
            // ============================================
            // DRAW SPRING (Gambar Pegas Vertikal)
            // ============================================
            drawSpringVertical(35 * scaleY, massY - 25 * scaleY, hookX);
            
            // ============================================
            // DRAW MASS (Gambar Massa - Blue gradient seperti sebelumnya)
            // ============================================
            const massWidth = 56 * scaleX;
            const massHeight = 50 * scaleY;
            
            // Mass shadow
            ctx.fillStyle = 'rgba(0,0,0,0.3)';
            ctx.beginPath();
            ctx.ellipse(hookX + 4 * scaleX, massY + massHeight/2 + 8 * scaleY, massWidth/2, 6 * scaleY, 0, 0, Math.PI * 2);
            ctx.fill();
            
            // Mass body (blue gradient - sama seperti sebelumnya)
            const massGrad = ctx.createLinearGradient(hookX - massWidth/2, massY - massHeight/2, hookX + massWidth/2, massY + massHeight/2);
            massGrad.addColorStop(0, '#60a5fa');
            massGrad.addColorStop(0.3, '#3b82f6');
            massGrad.addColorStop(0.7, '#2563eb');
            massGrad.addColorStop(1, '#1d4ed8');
            
            ctx.fillStyle = massGrad;
            ctx.beginPath();
            ctx.roundRect(hookX - massWidth/2, massY - massHeight/2, massWidth, massHeight, 10 * scale);
            ctx.fill();
            
            // Mass border glow (biru seperti sebelumnya)
            ctx.strokeStyle = '#93c5fd';
            ctx.lineWidth = 3 * scale;
            ctx.stroke();
            
            // Mass label with glow (putih dengan shadow)
            ctx.shadowColor = '#60a5fa';
            ctx.shadowBlur = 10 * scale;
            ctx.fillStyle = 'white';
            ctx.font = 'bold ' + Math.max(14, 22 * scale) + 'px Arial';
            ctx.textAlign = 'center';
            ctx.fillText('m', hookX, massY + 8 * scaleY);
            ctx.shadowBlur = 0;
            
            // Position indicator (di bawah massa)
            ctx.fillStyle = '#c9d1d9';
            ctx.font = Math.max(10, 13 * scale) + 'px Arial';
            ctx.fillText('y = ' + x.toFixed(4) + ' m', hookX, massY + massHeight/2 + 25 * scaleY);
            
            // ============================================
            // INFO PANEL (Top Right)
            // ============================================
            const panelX = canvas.width - 130 * scaleX;
            ctx.fillStyle = 'rgba(22, 27, 34, 0.9)';
            ctx.beginPath();
            ctx.roundRect(panelX, 45 * scaleY, 120 * scaleX, 85 * scaleY, 8 * scale);
            ctx.fill();
            ctx.strokeStyle = '#30363d';
            ctx.lineWidth = 1;
            ctx.stroke();
            
            ctx.textAlign = 'left';
            ctx.font = 'bold ' + Math.max(9, 13 * scale) + 'px Courier New';
            ctx.fillStyle = '#f0f6fc';
            ctx.fillText('t = ' + t.toFixed(3) + 's', panelX + 8 * scaleX, 65 * scaleY);
            
            ctx.font = Math.max(8, 11 * scale) + 'px Courier New';
            ctx.fillStyle = '#60a5fa';
            ctx.fillText('y = ' + x.toFixed(3) + 'm', panelX + 8 * scaleX, 82 * scaleY);
            
            ctx.fillStyle = '#3fb950';
            ctx.fillText('v = ' + v.toFixed(3) + 'm/s', panelX + 8 * scaleX, 99 * scaleY);
            
            ctx.fillStyle = '#f59e0b';
            ctx.fillText('E = ' + E.toFixed(3) + 'J', panelX + 8 * scaleX, 116 * scaleY);
            
            // ============================================
            // PROGRESS BAR
            // ============================================
            const progress = frameIdx / (totalFrames - 1);
            const barY = canvas.height - 20 * scaleY;
            ctx.fillStyle = '#21262d';
            ctx.beginPath();
            ctx.roundRect(20 * scaleX, barY, canvas.width - 40 * scaleX, 8 * scaleY, 4 * scale);
            ctx.fill();
            
            const progressGrad = ctx.createLinearGradient(20 * scaleX, 0, canvas.width - 20 * scaleX, 0);
            progressGrad.addColorStop(0, '#1d4ed8');
            progressGrad.addColorStop(0.5, '#3b82f6');
            progressGrad.addColorStop(1, '#60a5fa');
            ctx.fillStyle = progressGrad;
            ctx.beginPath();
            ctx.roundRect(20 * scaleX, barY, (canvas.width - 40 * scaleX) * progress, 8 * scaleY, 4 * scale);
            ctx.fill();
            
            // Update HTML
            document.getElementById('timeVal').textContent = t.toFixed(3) + ' s';
            document.getElementById('posVal').textContent = x.toFixed(4) + ' m';
            document.getElementById('velVal').textContent = v.toFixed(3) + ' m/s';
            document.getElementById('energyVal').textContent = E.toFixed(4) + ' J';
            document.getElementById('frameSlider').value = frameIdx;
            document.getElementById('currentTimeLabel').textContent = 't = ' + t.toFixed(3) + ' s';
        }}
        
        function animate(currentTime) {{
            if (!isPlaying) return;
            
            const deltaTime = currentTime - lastTime;
            if (deltaTime > 16 / speed) {{
                frameIdx++;
                if (frameIdx >= totalFrames) frameIdx = 0;
                draw();
                lastTime = currentTime;
            }}
            
            animationId = requestAnimationFrame(animate);
        }}
        
        function togglePlay() {{
            isPlaying = !isPlaying;
            const btn = document.getElementById('playBtn');
            
            if (isPlaying) {{
                btn.innerHTML = '<span style="font-size: 20px;">⏸️</span> Pause';
                btn.style.background = 'linear-gradient(135deg, #da3633, #f85149)';
                btn.style.boxShadow = '0 4px 20px rgba(248,81,73,0.4)';
                lastTime = performance.now();
                animate(lastTime);
            }} else {{
                btn.innerHTML = '<span style="font-size: 20px;">▶️</span> Play';
                btn.style.background = 'linear-gradient(135deg, #238636, #2ea043)';
                btn.style.boxShadow = '0 4px 20px rgba(35,134,54,0.4)';
                if (animationId) cancelAnimationFrame(animationId);
            }}
        }}
        
        function resetAnim() {{
            frameIdx = 0;
            draw();
        }}
        
        function changeSpeed() {{
            speed = parseFloat(document.getElementById('speedSelect').value);
        }}
        
        function seekFrame(val) {{
            frameIdx = parseInt(val);
            if (!isPlaying) draw();
        }}
        
        // Initial draw
        draw();
    </script>
    """
    
    import streamlit.components.v1 as components
    components.html(animation_html, height=650)

with tab2:
    st.markdown("### 📊 Grafik Analisis Interaktif")
    st.caption("Grafik interaktif dengan zoom, pan, dan hover. Double-click untuk reset view.")
    
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    
    t = solution['t']
    x = solution['x']
    v = solution['v']
    
    # Create interactive subplot figure with better spacing for mobile
    fig_interactive = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Posisi vs Waktu', 
            'Kecepatan vs Waktu',
            'Phase Space',
            'Energi vs Waktu'
        ),
        vertical_spacing=0.18,
        horizontal_spacing=0.12
    )
    
    # 1. Position plot with envelope
    fig_interactive.add_trace(
        go.Scatter(
            x=t, y=x, mode='lines', name='Posisi',
            line=dict(color='#3B82F6', width=2),
            hovertemplate='t=%{x:.2f}s<br>x=%{y:.3f}m<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Add envelope for underdamped systems
    if params.zeta < 1 and params.zeta > 0:
        alpha = params.zeta * params.omega_n
        envelope_upper = params.x0 * np.exp(-alpha * t)
        envelope_lower = -params.x0 * np.exp(-alpha * t)
        fig_interactive.add_trace(
            go.Scatter(x=t, y=envelope_upper, mode='lines', name='Envelope',
                      line=dict(color='#EF4444', width=1, dash='dash'),
                      hoverinfo='skip'),
            row=1, col=1
        )
        fig_interactive.add_trace(
            go.Scatter(x=t, y=envelope_lower, mode='lines', name='Envelope',
                      line=dict(color='#EF4444', width=1, dash='dash'),
                      showlegend=False, hoverinfo='skip'),
            row=1, col=1
        )
    
    # 2. Velocity plot
    fig_interactive.add_trace(
        go.Scatter(
            x=t, y=v, mode='lines', name='Kecepatan',
            line=dict(color='#22C55E', width=2),
            hovertemplate='t=%{x:.2f}s<br>v=%{y:.3f}m/s<extra></extra>'
        ),
        row=1, col=2
    )
    
    # 3. Phase space - simplified without colorbar for better responsiveness
    fig_interactive.add_trace(
        go.Scatter(
            x=x, y=v, mode='lines', name='Phase Space',
            line=dict(color='#A855F7', width=2),
            hovertemplate='x=%{x:.3f}m<br>v=%{y:.3f}m/s<extra></extra>'
        ),
        row=2, col=1
    )
    
    # Add starting point marker
    fig_interactive.add_trace(
        go.Scatter(
            x=[x[0]], y=[v[0]], mode='markers', name='Start',
            marker=dict(color='#22C55E', size=10, symbol='circle'),
            hovertemplate='START<extra></extra>'
        ),
        row=2, col=1
    )
    
    # Add ending point marker
    fig_interactive.add_trace(
        go.Scatter(
            x=[x[-1]], y=[v[-1]], mode='markers', name='End',
            marker=dict(color='#EF4444', size=10, symbol='x'),
            hovertemplate='END<extra></extra>'
        ),
        row=2, col=1
    )
    
    # 4. Energy plot
    fig_interactive.add_trace(
        go.Scatter(
            x=t, y=solution['KE'], mode='lines', name='KE',
            line=dict(color='#F59E0B', width=2),
            hovertemplate='KE=%{y:.3f}J<extra></extra>'
        ),
        row=2, col=2
    )
    fig_interactive.add_trace(
        go.Scatter(
            x=t, y=solution['PE'], mode='lines', name='PE',
            line=dict(color='#8B5CF6', width=2),
            hovertemplate='PE=%{y:.3f}J<extra></extra>'
        ),
        row=2, col=2
    )
    fig_interactive.add_trace(
        go.Scatter(
            x=t, y=solution['E_total'], mode='lines', name='Total',
            line=dict(color='#EC4899', width=2, dash='dash'),
            hovertemplate='E=%{y:.3f}J<extra></extra>'
        ),
        row=2, col=2
    )
    
    # Update layout for dark theme - optimized for responsiveness
    fig_interactive.update_layout(
        height=600,
        template='plotly_dark',
        paper_bgcolor='#0E1117',
        plot_bgcolor='#1E2329',
        font=dict(color='#E5E7EB', size=10),
        showlegend=False,  # Hide legend to save space on mobile
        margin=dict(t=50, b=50, l=50, r=20),
        hoverlabel=dict(
            bgcolor='#1E2329',
            font_size=11,
            font_family='monospace'
        )
    )
    
    # Update axes with shorter labels
    for i in range(1, 3):
        for j in range(1, 3):
            fig_interactive.update_xaxes(
                showgrid=True, gridwidth=1, gridcolor='#374151',
                zeroline=True, zerolinecolor='#4B5563',
                tickfont=dict(size=9),
                row=i, col=j
            )
            fig_interactive.update_yaxes(
                showgrid=True, gridwidth=1, gridcolor='#374151',
                zeroline=True, zerolinecolor='#4B5563',
                tickfont=dict(size=9),
                row=i, col=j
            )
    
    fig_interactive.update_xaxes(title_text='t (s)', row=1, col=1)
    fig_interactive.update_xaxes(title_text='t (s)', row=1, col=2)
    fig_interactive.update_xaxes(title_text='x (m)', row=2, col=1)
    fig_interactive.update_xaxes(title_text='t (s)', row=2, col=2)
    
    fig_interactive.update_yaxes(title_text='x (m)', row=1, col=1)
    fig_interactive.update_yaxes(title_text='v (m/s)', row=1, col=2)
    fig_interactive.update_yaxes(title_text='v (m/s)', row=2, col=1)
    fig_interactive.update_yaxes(title_text='E (J)', row=2, col=2)
    
    st.plotly_chart(fig_interactive, use_container_width=True)
    
    st.markdown("---")
    
    # Animated Phase Space
    st.markdown("### 🌀 Animasi Phase Space")
    st.caption("Lihat evolusi sistem dalam ruang fase dengan trail yang memudar")
    
    # Sample for animation performance
    sample_step = max(1, len(t) // 200)
    t_anim = t[::sample_step]
    x_anim = x[::sample_step]
    v_anim = v[::sample_step]
    
    # Create animated phase space HTML with responsive design
    phase_anim_html = f"""
    <div style="background: linear-gradient(180deg, #1a1f2e, #0d1117); border-radius: 12px; padding: 20px; border: 1px solid #30363d;">
        <div id="phaseCanvasContainer" style="width: 100%; max-width: 100%; overflow: hidden;">
            <canvas id="phaseCanvas" style="display: block; margin: 0 auto; width: 100%; max-width: 600px; height: auto;"></canvas>
        </div>
        <div style="display: flex; justify-content: center; gap: 12px; margin-top: 15px; flex-wrap: wrap;">
            <button id="phasePlayBtn" onclick="togglePhase()" style="
                background: linear-gradient(135deg, #238636, #2ea043);
                color: white; border: none; padding: 10px 25px; border-radius: 8px;
                font-size: 14px; cursor: pointer; font-weight: bold;">
                ▶️ Play
            </button>
            <button onclick="resetPhase()" style="
                background: #30363d; color: #c9d1d9; border: none; padding: 10px 20px;
                border-radius: 8px; font-size: 14px; cursor: pointer;">
                🔄 Reset
            </button>
            <select id="trailLength" onchange="updateTrail()" style="
                background: #30363d; color: #c9d1d9; border: none; padding: 10px 15px;
                border-radius: 8px; font-size: 14px; cursor: pointer;">
                <option value="20">Trail: Short</option>
                <option value="50" selected>Trail: Medium</option>
                <option value="100">Trail: Long</option>
                <option value="{len(x_anim)}">Trail: Full</option>
            </select>
        </div>
    </div>
    
    <script>
        const pCanvas = document.getElementById('phaseCanvas');
        const pCtx = pCanvas.getContext('2d');
        
        // Set canvas resolution based on container
        function resizePhaseCanvas() {{
            const container = document.getElementById('phaseCanvasContainer');
            const containerWidth = container.offsetWidth;
            const aspectRatio = 500 / 600; // height / width
            const width = Math.min(600, containerWidth);
            const height = width * aspectRatio;
            
            pCanvas.width = width;
            pCanvas.height = height;
            pCanvas.style.width = width + 'px';
            pCanvas.style.height = height + 'px';
        }}
        resizePhaseCanvas();
        window.addEventListener('resize', function() {{
            resizePhaseCanvas();
            drawPhase();
        }});
        
        const xData = {x_anim.tolist()};
        const vData = {v_anim.tolist()};
        const tData = {t_anim.tolist()};
        const totalPoints = xData.length;
        
        const xMin = {x_anim.min()}, xMax = {x_anim.max()};
        const vMin = {v_anim.min()}, vMax = {v_anim.max()};
        
        let currentIdx = 0;
        let isPlaying = false;
        let trailLength = 50;
        let animId = null;
        
        function mapX(x) {{
            const scale = pCanvas.width / 600;
            return (80 + (x - xMin) / (xMax - xMin) * 440) * scale;
        }}
        function mapV(v) {{
            const scale = pCanvas.height / 500;
            return (450 - (v - vMin) / (vMax - vMin) * 380) * scale;
        }}
        
        function drawPhase() {{
            const scaleX = pCanvas.width / 600;
            const scaleY = pCanvas.height / 500;
            
            // Background
            pCtx.fillStyle = '#0d1117';
            pCtx.fillRect(0, 0, pCanvas.width, pCanvas.height);
            
            // Grid
            pCtx.strokeStyle = '#21262d';
            pCtx.lineWidth = 1;
            for (let i = 0; i <= 5; i++) {{
                let px = (80 + i * 88) * scaleX;
                let py = (70 + i * 76) * scaleY;
                pCtx.beginPath();
                pCtx.moveTo(px, 70 * scaleY); pCtx.lineTo(px, 450 * scaleY);
                pCtx.moveTo(80 * scaleX, py); pCtx.lineTo(520 * scaleX, py);
                pCtx.stroke();
            }}
            
            // Axes
            pCtx.strokeStyle = '#4b5563';
            pCtx.lineWidth = 2;
            pCtx.beginPath();
            pCtx.moveTo(80 * scaleX, 450 * scaleY); pCtx.lineTo(520 * scaleX, 450 * scaleY);
            pCtx.moveTo(80 * scaleX, 70 * scaleY); pCtx.lineTo(80 * scaleX, 450 * scaleY);
            pCtx.stroke();
            
            // Zero lines
            pCtx.strokeStyle = '#22c55e';
            pCtx.lineWidth = 1;
            pCtx.setLineDash([5, 5]);
            let zeroX = mapX(0);
            let zeroV = mapV(0);
            pCtx.beginPath();
            pCtx.moveTo(zeroX, 70 * scaleY); pCtx.lineTo(zeroX, 450 * scaleY);
            pCtx.moveTo(80 * scaleX, zeroV); pCtx.lineTo(520 * scaleX, zeroV);
            pCtx.stroke();
            pCtx.setLineDash([]);
            
            // Labels - scale font size
            const fontSize = Math.max(10, 14 * Math.min(scaleX, scaleY));
            pCtx.fillStyle = '#e5e7eb';
            pCtx.font = fontSize + 'px Arial';
            pCtx.textAlign = 'center';
            pCtx.fillText('Posisi x (m)', 300 * scaleX, 485 * scaleY);
            pCtx.save();
            pCtx.translate(25 * scaleX, 260 * scaleY);
            pCtx.rotate(-Math.PI / 2);
            pCtx.fillText('Kecepatan v (m/s)', 0, 0);
            pCtx.restore();
            
            // Title
            pCtx.font = 'bold ' + Math.max(12, 16 * Math.min(scaleX, scaleY)) + 'px Arial';
            pCtx.fillText('🌀 Phase Space Trajectory', 300 * scaleX, 40 * scaleY);
            
            // Time display
            pCtx.font = Math.max(10, 14 * Math.min(scaleX, scaleY)) + 'px monospace';
            pCtx.fillStyle = '#60a5fa';
            pCtx.textAlign = 'right';
            pCtx.fillText('t = ' + tData[currentIdx].toFixed(3) + ' s', 520 * scaleX, 40 * scaleY);
            
            const scaleMin = Math.min(scaleX, scaleY);
            
            // Draw trail
            const startIdx = Math.max(0, currentIdx - trailLength);
            for (let i = startIdx; i < currentIdx; i++) {{
                const alpha = (i - startIdx) / (currentIdx - startIdx);
                const hue = 200 + alpha * 60;
                pCtx.strokeStyle = 'hsla(' + hue + ', 80%, 60%, ' + alpha * 0.8 + ')';
                pCtx.lineWidth = (2 + alpha * 2) * scaleMin;
                pCtx.beginPath();
                pCtx.moveTo(mapX(xData[i]), mapV(vData[i]));
                pCtx.lineTo(mapX(xData[i+1]), mapV(vData[i+1]));
                pCtx.stroke();
            }}
            
            // Current point with glow
            pCtx.shadowColor = '#60a5fa';
            pCtx.shadowBlur = 15 * scaleMin;
            pCtx.fillStyle = '#60a5fa';
            pCtx.beginPath();
            pCtx.arc(mapX(xData[currentIdx]), mapV(vData[currentIdx]), 8 * scaleMin, 0, Math.PI * 2);
            pCtx.fill();
            pCtx.shadowBlur = 0;
            
            // Current values - positioned relative to canvas size
            pCtx.fillStyle = '#e5e7eb';
            pCtx.font = Math.max(10, 12 * scaleMin) + 'px monospace';
            pCtx.textAlign = 'left';
            // Position info box in top-right area
            const infoX = pCanvas.width - 10;
            pCtx.textAlign = 'right';
            pCtx.fillText('x = ' + xData[currentIdx].toFixed(4) + ' m', infoX, 70 * scaleY);
            pCtx.fillText('v = ' + vData[currentIdx].toFixed(4) + ' m/s', infoX, 90 * scaleY);
        }}
        
        function animate() {{
            if (!isPlaying) return;
            currentIdx++;
            if (currentIdx >= totalPoints) currentIdx = 0;
            drawPhase();
            animId = requestAnimationFrame(animate);
        }}
        
        function togglePhase() {{
            isPlaying = !isPlaying;
            const btn = document.getElementById('phasePlayBtn');
            if (isPlaying) {{
                btn.innerHTML = '⏸️ Pause';
                btn.style.background = 'linear-gradient(135deg, #da3633, #f85149)';
                animate();
            }} else {{
                btn.innerHTML = '▶️ Play';
                btn.style.background = 'linear-gradient(135deg, #238636, #2ea043)';
                if (animId) cancelAnimationFrame(animId);
            }}
        }}
        
        function resetPhase() {{
            currentIdx = 0;
            drawPhase();
        }}
        
        function updateTrail() {{
            trailLength = parseInt(document.getElementById('trailLength').value);
            if (!isPlaying) drawPhase();
        }}
        
        drawPhase();
    </script>
    """
    
    import streamlit.components.v1 as components
    components.html(phase_anim_html, height=600)
    
    st.markdown("---")
    
    # Statistics
    st.markdown("### 📈 Statistik Simulasi")
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e3a5f, #0d2137); padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #3b82f6;">
            <div style="color: #9ca3af; font-size: 11px;">📍 Amplitudo</div>
            <div style="color: #60a5fa; font-size: 20px; font-weight: bold;">{:.4f} m</div>
        </div>
        """.format((x.max() - x.min())/2), unsafe_allow_html=True)
    
    with stat_col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e3a2f, #0d2117); padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #22c55e;">
            <div style="color: #9ca3af; font-size: 11px;">🏃 Vmax</div>
            <div style="color: #4ade80; font-size: 20px; font-weight: bold;">{:.4f} m/s</div>
        </div>
        """.format(abs(v).max()), unsafe_allow_html=True)
    
    with stat_col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #3a2f1e, #21170d); padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #f59e0b;">
            <div style="color: #9ca3af; font-size: 11px;">⚡ E₀</div>
            <div style="color: #fbbf24; font-size: 20px; font-weight: bold;">{:.4f} J</div>
        </div>
        """.format(solution['E_total'][0]), unsafe_allow_html=True)
    
    with stat_col4:
        energy_loss = (solution['E_total'][0] - solution['E_total'][-1]) / solution['E_total'][0] * 100
        st.markdown("""
        <div style="background: linear-gradient(135deg, #3a1e2f, #210d17); padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #ec4899;">
            <div style="color: #9ca3af; font-size: 11px;">📉 Dissipated</div>
            <div style="color: #f472b6; font-size: 20px; font-weight: bold;">{:.1f}%</div>
        </div>
        """.format(energy_loss), unsafe_allow_html=True)

with tab3:
    st.markdown("### 🔬 Validasi Numerik & Analisis Frekuensi")
    st.caption("Memvalidasi akurasi solusi numerik dan menganalisis spektrum frekuensi")
    
    # Validasi numerik
    st.markdown("#### 📐 Validasi vs Solusi Analitik")
    
    validation = validate_numerical_solution(solution)
    
    val_col1, val_col2, val_col3, val_col4 = st.columns(4)
    val_col1.metric("Max Error", f"{validation['max_error']:.2e} m")
    val_col2.metric("RMS Error", f"{validation['rms_error']:.2e} m")
    val_col3.metric("Korelasi", f"{validation['correlation']:.6f}")
    val_col4.metric("Status", "✅ Akurat" if validation['is_accurate'] else "⚠️ Perlu review")
    
    # Plot perbandingan
    fig_val, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4), facecolor='#0E1117')
    for ax in [ax1, ax2]:
        ax.set_facecolor('#1E2329')
        ax.tick_params(colors='#E5E7EB')
        ax.grid(True, alpha=0.3, color='#374151')
        for spine in ax.spines.values():
            spine.set_color('#374151')
    
    t = solution['t']
    ax1.plot(t, solution['x'], 'b-', label='Numerik (odeint)', linewidth=1.5)
    ax1.plot(t, validation['x_analytical'], 'r--', label='Analitik', linewidth=1.5, alpha=0.8)
    ax1.set_xlabel('Waktu (s)', color='#E5E7EB')
    ax1.set_ylabel('Posisi (m)', color='#E5E7EB')
    ax1.set_title('Perbandingan Solusi', color='#E5E7EB')
    ax1.legend(facecolor='#1E2329', edgecolor='#374151')
    
    error = solution['x'] - validation['x_analytical']
    ax2.plot(t, error * 1000, 'orange', linewidth=1)  # Convert to mm
    ax2.axhline(y=0, color='#22C55E', linestyle='--', alpha=0.5)
    ax2.set_xlabel('Waktu (s)', color='#E5E7EB')
    ax2.set_ylabel('Error (mm)', color='#E5E7EB')
    ax2.set_title('Error Numerik', color='#E5E7EB')
    ax2.fill_between(t, error * 1000, alpha=0.3, color='orange')
    
    plt.tight_layout()
    st.pyplot(fig_val)
    plt.close()
    
    st.markdown("---")
    
    # FFT Analysis
    st.markdown("#### 📊 Analisis Frekuensi (FFT)")
    
    fft_result = frequency_analysis(solution)
    
    fft_col1, fft_col2, fft_col3 = st.columns(3)
    fft_col1.metric("Frekuensi Dominan", f"{fft_result['dominant_freq']:.4f} Hz")
    fft_col2.metric("Frekuensi Teoritis", f"{fft_result['theoretical_freq']:.4f} Hz")
    fft_col3.metric("Perbedaan", f"{fft_result['freq_error']:.2f} %")
    
    # FFT plot
    fig_fft, ax = plt.subplots(figsize=(10, 4), facecolor='#0E1117')
    ax.set_facecolor('#1E2329')
    ax.tick_params(colors='#E5E7EB')
    ax.grid(True, alpha=0.3, color='#374151')
    for spine in ax.spines.values():
        spine.set_color('#374151')
    
    # Only show relevant frequency range
    freq_mask = fft_result['frequencies'] < 10 * fft_result['theoretical_freq'] if fft_result['theoretical_freq'] > 0 else fft_result['frequencies'] < 10
    ax.plot(fft_result['frequencies'][freq_mask], fft_result['amplitudes'][freq_mask], 'cyan', linewidth=1.5)
    ax.fill_between(fft_result['frequencies'][freq_mask], fft_result['amplitudes'][freq_mask], alpha=0.3, color='cyan')
    
    # Mark dominant frequency
    ax.axvline(x=fft_result['dominant_freq'], color='#EF4444', linestyle='--', label=f"Dominan: {fft_result['dominant_freq']:.3f} Hz")
    if fft_result['theoretical_freq'] > 0:
        ax.axvline(x=fft_result['theoretical_freq'], color='#22C55E', linestyle=':', label=f"Teoritis: {fft_result['theoretical_freq']:.3f} Hz")
    
    ax.set_xlabel('Frekuensi (Hz)', color='#E5E7EB')
    ax.set_ylabel('Amplitudo', color='#E5E7EB')
    ax.set_title('Spektrum Frekuensi (FFT)', color='#E5E7EB')
    ax.legend(facecolor='#1E2329', edgecolor='#374151')
    
    plt.tight_layout()
    st.pyplot(fig_fft)
    plt.close()
    
    st.markdown("---")
    
    # Resonance analysis
    st.markdown("#### 🎯 Kurva Resonansi")
    
    resonance = resonance_analysis(params)
    
    res_col1, res_col2, res_col3 = st.columns(3)
    res_col1.metric("Frekuensi Resonansi", f"{resonance['resonance_omega']:.4f} rad/s" if resonance['resonance_omega'] > 0 else "N/A")
    res_col2.metric("Quality Factor (Q)", f"{resonance['Q_factor']:.2f}" if resonance['Q_factor'] < 1e6 else "∞")
    res_col3.metric("Bandwidth 3dB", f"{resonance['bandwidth']:.4f} rad/s")
    
    # Resonance plot
    fig_res, ax = plt.subplots(figsize=(10, 4), facecolor='#0E1117')
    ax.set_facecolor('#1E2329')
    ax.tick_params(colors='#E5E7EB')
    ax.grid(True, alpha=0.3, color='#374151')
    for spine in ax.spines.values():
        spine.set_color('#374151')
    
    ax.plot(resonance['omega'], resonance['amplitude'], 'lime', linewidth=2)
    ax.fill_between(resonance['omega'], resonance['amplitude'], alpha=0.2, color='lime')
    ax.axvline(x=params.omega_n, color='#EF4444', linestyle='--', alpha=0.7, label=f'ωₙ = {params.omega_n:.2f}')
    if resonance['resonance_omega'] > 0:
        ax.axvline(x=resonance['resonance_omega'], color='#F59E0B', linestyle=':', label=f'ω_res = {resonance["resonance_omega"]:.2f}')
    
    ax.set_xlabel('ω (rad/s)', color='#E5E7EB')
    ax.set_ylabel('|H(ω)| (normalized)', color='#E5E7EB')
    ax.set_title('Kurva Respons Frekuensi', color='#E5E7EB')
    ax.legend(facecolor='#1E2329', edgecolor='#374151')
    
    plt.tight_layout()
    st.pyplot(fig_res)
    plt.close()

with tab4:
    st.markdown(PHYSICS_EXPLANATION)
    
    st.markdown("---")
    st.markdown("### 🔍 Analisis Sistem Saat Ini")
    
    analysis_col1, analysis_col2 = st.columns(2)
    
    with analysis_col1:
        st.markdown(f"""
        **Parameter Sistem:**
        - Massa: **{params.m}** kg
        - Konstanta pegas: **{params.k}** N/m
        - Koefisien redaman: **{params.c}** Ns/m
        
        **Karakteristik:**
        - Frekuensi natural: **{params.omega_n:.3f}** rad/s
        - Periode: **{params.period:.3f}** s
        - Rasio redaman ζ: **{params.zeta:.4f}**
        """)
    
    with analysis_col2:
        dtype = params.damping_type
        if dtype == DampingType.UNDAMPED:
            st.success("🟢 **Sistem Tanpa Redaman**\n\nSistem akan berosilasi terus tanpa kehilangan energi.")
        elif dtype == DampingType.UNDERDAMPED:
            st.info("🔵 **Sistem Underdamped**\n\nSistem berosilasi dengan amplitudo yang menurun eksponensial.")
        elif dtype == DampingType.CRITICALLY_DAMPED:
            st.warning("🟡 **Sistem Critically Damped**\n\nSistem kembali ke equilibrium secepat mungkin tanpa osilasi.")
        else:
            st.error("🔴 **Sistem Overdamped**\n\nSistem kembali ke equilibrium dengan lambat tanpa osilasi.")

with tab5:
    st.markdown("### 🎯 Kesimpulan Analisis Otomatis")
    st.caption("Kesimpulan ilmiah yang dihasilkan secara otomatis berdasarkan hasil simulasi")
    
    # Generate conclusions
    validation = validate_numerical_solution(solution)
    fft_result = frequency_analysis(solution)
    conclusions = generate_conclusions(solution, validation, fft_result)
    
    st.markdown(conclusions)
    
    # Summary metrics in cards
    st.markdown("---")
    st.markdown("### 📊 Ringkasan Hasil")
    
    summ_col1, summ_col2, summ_col3 = st.columns(3)
    
    with summ_col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e3a5f, #0d2137); padding: 20px; border-radius: 12px; border: 1px solid #3b82f6;">
            <h4 style="color: #60a5fa; margin: 0 0 10px 0;">📐 Akurasi Numerik</h4>
            <p style="color: #e5e7eb; margin: 0;">
                Korelasi: <strong>{:.6f}</strong><br>
                RMS Error: <strong>{:.2e} m</strong>
            </p>
        </div>
        """.format(validation['correlation'], validation['rms_error']), unsafe_allow_html=True)
    
    with summ_col2:
        energy_loss = (solution['E_total'][0] - solution['E_total'][-1]) / solution['E_total'][0] * 100
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e3a2f, #0d2117); padding: 20px; border-radius: 12px; border: 1px solid #22c55e;">
            <h4 style="color: #4ade80; margin: 0 0 10px 0;">⚡ Energi</h4>
            <p style="color: #e5e7eb; margin: 0;">
                Awal: <strong>{:.4f} J</strong><br>
                Terdisipasi: <strong>{:.1f}%</strong>
            </p>
        </div>
        """.format(solution['E_total'][0], energy_loss), unsafe_allow_html=True)
    
    with summ_col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #3a1e3f, #210d21); padding: 20px; border-radius: 12px; border: 1px solid #a855f7;">
            <h4 style="color: #c084fc; margin: 0 0 10px 0;">🎵 Frekuensi</h4>
            <p style="color: #e5e7eb; margin: 0;">
                Dominan: <strong>{:.4f} Hz</strong><br>
                Error: <strong>{:.2f}%</strong>
            </p>
        </div>
        """.format(fft_result['dominant_freq'], fft_result['freq_error']), unsafe_allow_html=True)

with tab6:
    st.markdown("### 📥 Ekspor Data Simulasi")
    st.caption("Unduh hasil simulasi dalam berbagai format")
    
    export_col1, export_col2 = st.columns(2)
    
    with export_col1:
        st.markdown("#### 📊 Data CSV")
        st.info("Format CSV dapat dibuka di Excel, Google Sheets, atau software analisis data lainnya.")
        
        csv_data = export_to_csv(solution)
        st.download_button(
            label="📥 Download Data (CSV)",
            data=csv_data,
            file_name=f"simulasi_pegas_{params.name.replace(' ', '_').lower()}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        # Preview
        st.markdown("**Preview data:**")
        import pandas as pd
        df_preview = pd.DataFrame({
            't(s)': solution['t'][:5],
            'x(m)': solution['x'][:5],
            'v(m/s)': solution['v'][:5],
            'E(J)': solution['E_total'][:5]
        })
        st.dataframe(df_preview, use_container_width=True)
    
    with export_col2:
        st.markdown("#### 📝 Laporan Markdown")
        st.info("Format Markdown ideal untuk dokumentasi dan laporan akademik.")
        
        # Generate full report
        validation = validate_numerical_solution(solution)
        fft_result = frequency_analysis(solution)
        conclusions_md = generate_conclusions(solution, validation, fft_result)
        
        report_text = f"""# Simulasi Gaya Pegas - {params.name}

## 1. Parameter Sistem
| Parameter | Nilai | Satuan |
|-----------|-------|--------|
| Massa (m) | {params.m} | kg |
| Konstanta pegas (k) | {params.k} | N/m |
| Koefisien redaman (c) | {params.c} | Ns/m |
| Posisi awal (x₀) | {params.x0} | m |
| Kecepatan awal (v₀) | {params.v0} | m/s |

## 2. Karakteristik Sistem
| Parameter | Nilai |
|-----------|-------|
| Frekuensi natural (ωₙ) | {params.omega_n:.4f} rad/s |
| Frekuensi natural (f) | {params.omega_n / (2*np.pi):.4f} Hz |
| Rasio redaman (ζ) | {params.zeta:.4f} |
| Periode (T) | {params.period:.4f} s |
| Tipe redaman | {params.damping_type.value} |

## 3. Hasil Simulasi
| Metrik | Nilai |
|--------|-------|
| Durasi simulasi | {t_max} s |
| Posisi maksimum | {solution['x'].max():.6f} m |
| Posisi minimum | {solution['x'].min():.6f} m |
| Kecepatan maksimum | {solution['v'].max():.6f} m/s |
| Energi awal | {solution['E_total'][0]:.6f} J |
| Energi akhir | {solution['E_total'][-1]:.6f} J |
| Energi terdisipasi | {solution['E_dissipated'][-1]:.6f} J |

## 4. Validasi Numerik
| Metrik | Nilai |
|--------|-------|
| RMS Error | {validation['rms_error']:.2e} m |
| Korelasi | {validation['correlation']:.6f} |
| Status | {"Akurat" if validation['is_accurate'] else "Perlu review"} |

## 5. Analisis Frekuensi
| Metrik | Nilai |
|--------|-------|
| Frekuensi dominan (FFT) | {fft_result['dominant_freq']:.4f} Hz |
| Frekuensi teoritis | {fft_result['theoretical_freq']:.4f} Hz |
| Perbedaan | {fft_result['freq_error']:.2f}% |

{conclusions_md}

---
*Laporan dibuat oleh Simulasi Gaya Pegas - Tugas Akhir Fisika Komputasi*
"""
        
        st.download_button(
            label="📥 Download Laporan (Markdown)",
            data=report_text,
            file_name=f"laporan_pegas_{params.name.replace(' ', '_').lower()}.md",
            mime="text/markdown",
            use_container_width=True
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; padding: 1rem;">
    <p>🔬 <strong>Simulasi Gaya Pegas - Hooke's Law</strong></p>
    <p>Tugas Akhir Fisika Komputasi | Dimas</p>
    <p style="font-size: 0.8rem;">
        Solver: scipy.integrate.odeint | Visualisasi: matplotlib
    </p>
</div>
""", unsafe_allow_html=True)
