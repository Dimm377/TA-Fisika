"""
 Simulasi Gaya Pegas - Hooke's Law
====================================
VERSI INTERAKTIF: Drag & Drop + Auto Physics

Fitur:
- Drag beban untuk set simpangan awal
- Release untuk mulai osilasi otomatis
- Slider untuk durasi
- Preset real-life

Jalankan:
    streamlit run app.py
"""

import streamlit as st
import numpy as np
import os

from physics_config.spring_physics import (
    PRESETS,
    DampingType,
    solve_spring_system,
    PHYSICS_EXPLANATION,
)
from physics_config.config import (
    DEFAULT_DURATION_SECONDS, MIN_DURATION, MAX_DURATION,
    DAMPING_ICONS,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Simulasi Gaya Pegas",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================


def load_css(css_file: str = "styles/styles.css") -> str:
    css_path = os.path.join(os.path.dirname(__file__), css_file)
    with open(css_path, "r") as f:
        return f.read()


st.markdown(f"<style>{load_css()}</style>", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="main-header">
    <h1> Simulasi Gaya Pegas</h1>
    <p style="color: #94A3B8; margin-top: 0.5rem;">
        Hukum Hooke - Tarik beban untuk memulai!
    </p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# PENGATURAN SIMULASI
# ============================================================

with st.expander("️ **Pilih Sistem** (Klik untuk buka/tutup)", expanded=True):
    preset_names = list(PRESETS.keys())
    preset_labels = [PRESETS[k].name for k in preset_names]

    selected_label = st.selectbox(
        " Pilih Contoh Sistem:",
        preset_labels,
        key="main_preset"
    )

    selected_key = preset_names[preset_labels.index(selected_label)]
    params = PRESETS[selected_key]
    st.success(f" {params.description}")

    col_mass, col_spring, col_damping, col_zeta = st.columns(4)
    col_mass.metric("Massa (m)", f"{params.m} kg")
    col_spring.metric("Konstanta (k)", f"{params.k} N/m")
    col_damping.metric("Redaman (c)", f"{params.c} Ns/m")
    col_zeta.metric("Rasio ζ", f"{params.zeta:.3f}")

    simulation_duration = st.slider(
        "⏱️ Durasi Simulasi (detik)",
        MIN_DURATION, MAX_DURATION, DEFAULT_DURATION_SECONDS, 0.5,
        key="main_tmax"
    )

# Display system info
st.markdown("---")
metric_freq, metric_period, metric_zeta, metric_damping_type = st.columns(4)

with metric_freq:
    st.metric("Frekuensi Natural", f"{params.omega_n:.2f} rad/s")
with metric_period:
    st.metric("Periode", f"{params.period:.3f} s" if params.period < float('inf') else "∞")
with metric_zeta:
    st.metric("Rasio Redaman ζ", f"{params.zeta:.3f}")
with metric_damping_type:
    damping_type_icon = DAMPING_ICONS.get(params.damping_type.value, '')
    st.metric("Tipe Redaman", f"{damping_type_icon} {params.damping_type.value}")

st.markdown("---")

# ============================================================
# TABS
# ============================================================

tab_interactive, tab_autoplay, tab_graphs, tab_theory = st.tabs([" Interaktif", "▶️ Auto-Play", " Grafik", " Teori"])

# ============================================================
# TAB 1: ANIMASI INTERAKTIF DENGAN DRAG
# ============================================================

with tab_interactive:
    st.markdown("###  Simulasi Interaktif")
    st.caption("🖱️ **Tarik beban** ke bawah/atas, lalu **lepas** untuk melihat osilasi!")

    # Interactive HTML5 Canvas with DRAG support and real-time physics
    interactive_html = f"""
    <style>
        @media (max-width: 600px) {{
            .stats-grid {{ grid-template-columns: repeat(2, 1fr) !important; }}
            .stats-grid .stat-value {{ font-size: 16px !important; }}
        }}
        #springCanvas {{ cursor: grab; }}
        #springCanvas.dragging {{ cursor: grabbing; }}
    </style>
    <div style="background: linear-gradient(180deg, #1a1f2e 0%, #0d1117 100%); border-radius: 16px; padding: 25px; border: 1px solid #30363d;">
        <div style="text-align: center; margin-bottom: 15px;">
            <span style="color: #58a6ff; font-size: 18px; font-weight: bold;"> {params.name}</span>
            <span id="modeLabel" style="color: #3fb950; font-size: 14px; margin-left: 15px;">🟢 Siap - Tarik beban!</span>
        </div>

        <div id="springCanvasContainer" style="width: 100%; overflow: hidden;">
            <canvas id="springCanvas" style="display: block; margin: 0 auto; border-radius: 12px; max-width: 700px;"></canvas>
        </div>

        <div style="display: flex; justify-content: center; gap: 12px; margin-top: 20px; flex-wrap: wrap;">
            <button id="resetBtn" onclick="resetSimulation()" style="
                background: linear-gradient(135deg, #f59e0b, #d97706);
                color: white; border: none; padding: 14px 30px; border-radius: 10px;
                font-size: 16px; cursor: pointer; font-weight: bold;">
                 Reset
            </button>
            <select id="dampingSelect" onchange="changeDamping()" style="
                background: #30363d; color: #c9d1d9; border: none; padding: 14px 20px;
                border-radius: 10px; font-size: 14px; cursor: pointer;">
                <option value="0">Tanpa Redaman</option>
                <option value="{params.c}" selected>Default ({params.c})</option>
                <option value="{params.c * 2}">Tinggi ({params.c * 2})</option>
            </select>
        </div>

        <div class="stats-grid" style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-top: 20px;">
            <div style="background: #161b22; padding: 18px 12px; border-radius: 12px; text-align: center; border: 1px solid #21262d;">
                <div style="color: #8b949e; font-size: 11px;"> Simpangan</div>
                <div id="posVal" class="stat-value" style="color: #58a6ff; font-size: 22px; font-weight: bold; margin-top: 8px;">0.000 m</div>
            </div>
            <div style="background: #161b22; padding: 18px 12px; border-radius: 12px; text-align: center; border: 1px solid #21262d;">
                <div style="color: #8b949e; font-size: 11px;"> Kecepatan</div>
                <div id="velVal" class="stat-value" style="color: #3fb950; font-size: 22px; font-weight: bold; margin-top: 8px;">0.000 m/s</div>
            </div>
            <div style="background: #161b22; padding: 18px 12px; border-radius: 12px; text-align: center; border: 1px solid #21262d;">
                <div style="color: #8b949e; font-size: 11px;"> Gaya (F)</div>
                <div id="forceVal" class="stat-value" style="color: #f85149; font-size: 22px; font-weight: bold; margin-top: 8px;">0.00 N</div>
            </div>
            <div style="background: #161b22; padding: 18px 12px; border-radius: 12px; text-align: center; border: 1px solid #21262d;">
                <div style="color: #8b949e; font-size: 11px;"> Energi</div>
                <div id="energyVal" class="stat-value" style="color: #a855f7; font-size: 22px; font-weight: bold; margin-top: 8px;">0.000 J</div>
            </div>
        </div>

        <!-- Energy Bars -->
        <div style="margin-top: 20px; padding: 15px; background: #0d1117; border-radius: 12px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="color: #f59e0b; font-size: 12px;">Energi Kinetik (Ek)</span>
                <span id="ekVal" style="color: #f59e0b; font-size: 12px;">0.000 J</span>
            </div>
            <div style="height: 20px; background: #21262d; border-radius: 6px; overflow: hidden; margin-bottom: 12px;">
                <div id="ekBar" style="height: 100%; width: 0%; background: linear-gradient(90deg, #f59e0b, #f97316); transition: width 0.1s;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="color: #a78bfa; font-size: 12px;">Energi Potensial (Ep)</span>
                <span id="epVal" style="color: #a78bfa; font-size: 12px;">0.000 J</span>
            </div>
            <div style="height: 20px; background: #21262d; border-radius: 6px; overflow: hidden;">
                <div id="epBar" style="height: 100%; width: 0%; background: linear-gradient(90deg, #8b5cf6, #a78bfa); transition: width 0.1s;"></div>
            </div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('springCanvas');
        const ctx = canvas.getContext('2d');

        // Canvas size
        const BASE_WIDTH = 400;
        const BASE_HEIGHT = 500;

        function resizeCanvas() {{
            const container = document.getElementById('springCanvasContainer');
            const width = Math.min(BASE_WIDTH, container.offsetWidth);
            const height = (width / BASE_WIDTH) * BASE_HEIGHT;
            canvas.width = width;
            canvas.height = height;
        }}
        resizeCanvas();
        window.addEventListener('resize', () => {{ resizeCanvas(); draw(); }});

        // Physics parameters from Python
        const k = {params.k};          // N/m
        const m = {params.m};          // kg
        let c = {params.c};            // Ns/m (damping)
        const restLength = 150;
        const scaleFactor = 100;

        // State
        let position = 0;              // meters (displacement from equilibrium)
        let velocity = 0;              // m/s
        let isDragging = false;
        let isSimulating = false;

        const anchorX = () => canvas.width / 2;
        const anchorY = 50;
        const equilibriumY = () => anchorY + restLength;
        const massRadius = 35;

        // Convert position (meters) to pixel Y
        function posToY(pos) {{
            return equilibriumY() + pos * scaleFactor;
        }}

        // Convert pixel Y to position (meters)
        function yToPos(y) {{
            return (y - equilibriumY()) / scaleFactor;
        }}

        // Physics: Hooke's Law
        function calculateForce() {{
            return -k * position;  // F = -kx
        }}

        function calculateEnergies() {{
            const Ek = 0.5 * m * velocity * velocity;
            const Ep = 0.5 * k * position * position;
            return {{ Ek, Ep, total: Ek + Ep }};
        }}

        // Physics update (Euler integration)
        function updatePhysics() {{
            if (!isSimulating) return;

            const dt = 0.016;  // ~60fps

            // Hooke's Law: F = -kx
            const springForce = -k * position;

            // Damping: F = -cv
            const dampingForce = -c * velocity;

            // Net force
            const netForce = springForce + dampingForce;

            // Acceleration: a = F/m
            const acceleration = netForce / m;

            // Update velocity and position
            velocity += acceleration * dt;
            position += velocity * dt;
        }}

        // Draw spring coils
        function drawSpring(startY, endY) {{
            const scale = canvas.width / BASE_WIDTH;
            const springLen = endY - startY;
            if (springLen < 30) return;

            const numCoils = 12;
            const coilHeight = (springLen - 20) / numCoils;
            const coilWidth = 22 * scale;
            const x = anchorX();

            ctx.strokeStyle = '#6b7280';
            ctx.lineWidth = 3 * scale;
            ctx.beginPath();
            ctx.moveTo(x, startY);
            ctx.lineTo(x, startY + 10);
            ctx.stroke();

            for (let i = 0; i < numCoils; i++) {{
                const y1 = startY + 10 + i * coilHeight;
                const y2 = y1 + coilHeight;

                // Color based on stretch
                const stretch = (springLen - 100) / 200;
                const r = Math.min(255, 59 + stretch * 180);
                const g = Math.max(68, 130 - stretch * 62);
                const b = Math.max(68, 246 - stretch * 178);
                ctx.strokeStyle = `rgb(${{r}},${{g}},${{b}})`;
                ctx.lineWidth = 4 * scale;

                const dir = (i % 2 === 0) ? 1 : -1;
                ctx.beginPath();
                ctx.moveTo(x, y1);
                ctx.lineTo(x + dir * coilWidth, y1 + coilHeight * 0.5);
                ctx.lineTo(x, y2);
                ctx.stroke();
            }}

            ctx.strokeStyle = '#6b7280';
            ctx.lineWidth = 3 * scale;
            ctx.beginPath();
            ctx.moveTo(x, endY - 10);
            ctx.lineTo(x, endY);
            ctx.stroke();
        }}

        // Draw force vector
        function drawForceVector() {{
            const force = calculateForce();
            if (Math.abs(force) < 0.5) return;

            const scale = canvas.width / BASE_WIDTH;
            const massY = posToY(position);
            const arrowLen = Math.min(80, Math.abs(force) / k * 100) * scale;

            const startY = massY + (force > 0 ? -massRadius - 10 : massRadius + 10);
            const endY = startY + (force > 0 ? -arrowLen : arrowLen);

            ctx.strokeStyle = '#f85149';
            ctx.lineWidth = 4 * scale;
            ctx.beginPath();
            ctx.moveTo(anchorX(), startY);
            ctx.lineTo(anchorX(), endY);
            ctx.stroke();

            // Arrow head
            ctx.fillStyle = '#f85149';
            ctx.beginPath();
            const headSize = 10 * scale;
            if (force > 0) {{
                ctx.moveTo(anchorX(), endY - headSize);
                ctx.lineTo(anchorX() - headSize/2, endY);
                ctx.lineTo(anchorX() + headSize/2, endY);
            }} else {{
                ctx.moveTo(anchorX(), endY + headSize);
                ctx.lineTo(anchorX() - headSize/2, endY);
                ctx.lineTo(anchorX() + headSize/2, endY);
            }}
            ctx.fill();

            // Force label
            ctx.font = '14px Arial';
            ctx.fillStyle = '#f85149';
            ctx.textAlign = 'left';
            ctx.fillText('F=' + force.toFixed(1) + 'N', anchorX() + 50, (startY + endY) / 2);
        }}

        function draw() {{
            const scale = canvas.width / BASE_WIDTH;

            // Background
            const bgGrad = ctx.createLinearGradient(0, 0, 0, canvas.height);
            bgGrad.addColorStop(0, '#0d1117');
            bgGrad.addColorStop(1, '#161b22');
            ctx.fillStyle = bgGrad;
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Grid
            ctx.strokeStyle = '#21262d';
            ctx.lineWidth = 1;
            for (let i = 0; i < canvas.width; i += 30) ctx.beginPath(), ctx.moveTo(i, 0), ctx.lineTo(i, canvas.height), ctx.stroke();
            for (let i = 0; i < canvas.height; i += 30) ctx.beginPath(), ctx.moveTo(0, i), ctx.lineTo(canvas.width, i), ctx.stroke();

            // Ceiling
            ctx.fillStyle = '#4b5563';
            ctx.fillRect(anchorX() - 60, 20, 120, 20);
            ctx.fillStyle = '#6b7280';
            ctx.beginPath();
            ctx.arc(anchorX(), anchorY, 10, 0, Math.PI * 2);
            ctx.fill();

            // Equilibrium line
            ctx.strokeStyle = '#3fb950';
            ctx.lineWidth = 2;
            ctx.setLineDash([8, 4]);
            ctx.beginPath();
            ctx.moveTo(anchorX() - 80, equilibriumY());
            ctx.lineTo(anchorX() + 80, equilibriumY());
            ctx.stroke();
            ctx.setLineDash([]);

            ctx.fillStyle = '#3fb950';
            ctx.font = '12px Arial';
            ctx.textAlign = 'left';
            ctx.fillText('y = 0', anchorX() + 90, equilibriumY() + 4);

            // Mass Y position
            const massY = posToY(position);

            // Spring
            drawSpring(anchorY + 10, massY - massRadius);

            // Force vector
            drawForceVector();

            // Mass (draggable indicator)
            const massWidth = 56;
            const massHeight = 50;

            if (isDragging) {{
                ctx.fillStyle = 'rgba(96, 165, 250, 0.3)';
                ctx.beginPath();
                ctx.roundRect(anchorX() - massWidth/2 - 10, massY - massHeight/2 - 10, massWidth + 20, massHeight + 20, 15);
                ctx.fill();
            }}

            // Mass body (rounded rectangle)
            const massGrad = ctx.createLinearGradient(anchorX() - massWidth/2, massY - massHeight/2, anchorX() + massWidth/2, massY + massHeight/2);
            massGrad.addColorStop(0, '#60a5fa');
            massGrad.addColorStop(0.3, '#3b82f6');
            massGrad.addColorStop(0.7, '#2563eb');
            massGrad.addColorStop(1, '#1d4ed8');
            ctx.fillStyle = massGrad;
            ctx.beginPath();
            ctx.roundRect(anchorX() - massWidth/2, massY - massHeight/2, massWidth, massHeight, 10);
            ctx.fill();

            // Border glow when dragging
            ctx.strokeStyle = isDragging ? '#60a5fa' : '#93c5fd';
            ctx.lineWidth = isDragging ? 4 : 3;
            ctx.stroke();

            ctx.fillStyle = 'white';
            ctx.font = 'bold 18px Arial';
            ctx.textAlign = 'center';
            ctx.fillText('m', anchorX(), massY + 6);

            ctx.fillStyle = '#c9d1d9';
            ctx.font = '12px Arial';
            ctx.fillText('{params.m} kg', anchorX(), massY + massRadius + 20);

            // Update displays
            const energies = calculateEnergies();
            const force = calculateForce();

            document.getElementById('posVal').textContent = position.toFixed(3) + ' m';
            document.getElementById('velVal').textContent = velocity.toFixed(3) + ' m/s';
            document.getElementById('forceVal').textContent = force.toFixed(2) + ' N';
            document.getElementById('energyVal').textContent = energies.total.toFixed(3) + ' J';

            document.getElementById('ekVal').textContent = energies.Ek.toFixed(3) + ' J';
            document.getElementById('epVal').textContent = energies.Ep.toFixed(3) + ' J';

            const maxE = Math.max(energies.total, 0.001);
            document.getElementById('ekBar').style.width = (energies.Ek / maxE * 100) + '%';
            document.getElementById('epBar').style.width = (energies.Ep / maxE * 100) + '%';

            // Mode label
            const modeLabel = document.getElementById('modeLabel');
            if (isDragging) {{
                modeLabel.textContent = '🟡 Menarik...';
                modeLabel.style.color = '#f59e0b';
            }} else if (isSimulating) {{
                modeLabel.textContent = '🔴 Berosilasi';
                modeLabel.style.color = '#f85149';
            }} else {{
                modeLabel.textContent = '🟢 Siap - Tarik beban!';
                modeLabel.style.color = '#3fb950';
            }}
        }}

        // Animation loop
        function animate() {{
            updatePhysics();
            draw();
            requestAnimationFrame(animate);
        }}

        // Mouse/Touch interaction
        function getMousePos(e) {{
            const rect = canvas.getBoundingClientRect();
            const x = (e.clientX || e.touches[0].clientX) - rect.left;
            const y = (e.clientY || e.touches[0].clientY) - rect.top;
            return {{ x, y }};
        }}

        function isOnMass(pos) {{
            const massY = posToY(position);
            const massWidth = 56;
            const massHeight = 50;
            const dx = Math.abs(pos.x - anchorX());
            const dy = Math.abs(pos.y - massY);
            return dx < massWidth/2 + 20 && dy < massHeight/2 + 20;
        }}

        canvas.addEventListener('mousedown', (e) => {{
            const pos = getMousePos(e);
            if (isOnMass(pos)) {{
                isDragging = true;
                isSimulating = false;
                velocity = 0;
                canvas.classList.add('dragging');
            }}
        }});

        canvas.addEventListener('mousemove', (e) => {{
            if (isDragging) {{
                const pos = getMousePos(e);
                const newY = Math.max(anchorY + 80, Math.min(canvas.height - massRadius - 20, pos.y));
                position = yToPos(newY);
            }}
        }});

        canvas.addEventListener('mouseup', () => {{
            if (isDragging) {{
                isDragging = false;
                isSimulating = true;  // Start physics!
                canvas.classList.remove('dragging');
            }}
        }});

        canvas.addEventListener('mouseleave', () => {{
            if (isDragging) {{
                isDragging = false;
                isSimulating = true;
                canvas.classList.remove('dragging');
            }}
        }});

        // Touch support
        canvas.addEventListener('touchstart', (e) => {{
            e.preventDefault();
            const pos = getMousePos(e);
            if (isOnMass(pos)) {{
                isDragging = true;
                isSimulating = false;
                velocity = 0;
            }}
        }});

        canvas.addEventListener('touchmove', (e) => {{
            e.preventDefault();
            if (isDragging) {{
                const pos = getMousePos(e);
                const newY = Math.max(anchorY + 80, Math.min(canvas.height - massRadius - 20, pos.y));
                position = yToPos(newY);
            }}
        }});

        canvas.addEventListener('touchend', () => {{
            if (isDragging) {{
                isDragging = false;
                isSimulating = true;
            }}
        }});

        // Controls
        function resetSimulation() {{
            position = 0;
            velocity = 0;
            isSimulating = false;
        }}

        function changeDamping() {{
            c = parseFloat(document.getElementById('dampingSelect').value);
        }}

        // Start animation
        animate();
    </script>
    """

    import streamlit.components.v1 as components
    components.html(interactive_html, height=800)

# ============================================================
# TAB 2: AUTO-PLAY ANIMATION (simplified working version)
# ============================================================

with tab_autoplay:
    st.markdown("### ▶️ Animasi Auto-Play")
    st.caption("Animasi berdasarkan preset yang dipilih. Klik Play untuk mulai!")

    # Solve the system
    solution_auto = solve_spring_system(params, (0, simulation_duration), time_step=0.001)

    # Sample data for animation
    from physics_config.config import ANIMATION_MAX_POINTS
    step = max(1, len(solution_auto['t']) // ANIMATION_MAX_POINTS)
    t_js = solution_auto['t'][::step].tolist()
    x_js = solution_auto['x'][::step].tolist()
    v_js = solution_auto['v'][::step].tolist()
    e_js = solution_auto['E_total'][::step].tolist()
    x_max = max(abs(min(x_js)), abs(max(x_js)), 0.1)

    # Simple working HTML animation
    simple_html = f"""
    <div style="background:#0d1117; padding:20px; border-radius:16px; border:1px solid #30363d;">
        <div style="text-align:center; margin-bottom:15px;">
            <span style="color:#58a6ff; font-size:18px; font-weight:bold;"> {params.name}</span>
        </div>

        <canvas id="simCanvas" width="400" height="400" style="display:block; margin:0 auto; background:#161b22; border-radius:12px;"></canvas>

        <div style="display:flex; justify-content:center; gap:12px; margin:20px 0; flex-wrap:wrap;">
            <button id="playPauseBtn" onclick="togglePlay()" style="background:linear-gradient(135deg,#238636,#2ea043); color:white; border:none; padding:12px 30px; border-radius:8px; font-size:16px; cursor:pointer; font-weight:bold;">▶️ Play</button>
            <button onclick="resetAnim()" style="background:#30363d; color:#c9d1d9; border:none; padding:12px 20px; border-radius:8px; cursor:pointer;"> Reset</button>
            <select id="speedSel" onchange="speed=parseFloat(this.value)" style="background:#30363d; color:#c9d1d9; border:none; padding:12px; border-radius:8px;">
                <option value="0.5">0.5x</option>
                <option value="1" selected>1x</option>
                <option value="2">2x</option>
            </select>
        </div>

        <div style="margin:0 10px;">
            <input type="range" id="timeSlider" min="0" max="{len(t_js) - 1}" value="0" style="width:100%; accent-color:#58a6ff;" oninput="seekTo(this.value)">
            <div style="display:flex; justify-content:space-between; color:#8b949e; font-size:12px; margin-top:5px;">
                <span>0.00s</span>
                <span id="timeLabel" style="color:#58a6ff; font-weight:bold;">t = 0.000 s</span>
                <span>{t_js[-1]:.2f}s</span>
            </div>
        </div>

        <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:10px; margin-top:20px;">
            <div style="background:#161b22; padding:15px; border-radius:10px; text-align:center; border:1px solid #21262d;">
                <div style="color:#8b949e; font-size:11px;">⏱️ Waktu</div>
                <div id="statTime" style="color:#f0f6fc; font-size:20px; font-weight:bold; margin-top:6px;">0.000 s</div>
            </div>
            <div style="background:#161b22; padding:15px; border-radius:10px; text-align:center; border:1px solid #21262d;">
                <div style="color:#8b949e; font-size:11px;"> Posisi</div>
                <div id="statPos" style="color:#58a6ff; font-size:20px; font-weight:bold; margin-top:6px;">0.000 m</div>
            </div>
            <div style="background:#161b22; padding:15px; border-radius:10px; text-align:center; border:1px solid #21262d;">
                <div style="color:#8b949e; font-size:11px;"> Kecepatan</div>
                <div id="statVel" style="color:#3fb950; font-size:20px; font-weight:bold; margin-top:6px;">0.000 m/s</div>
            </div>
            <div style="background:#161b22; padding:15px; border-radius:10px; text-align:center; border:1px solid #21262d;">
                <div style="color:#8b949e; font-size:11px;"> Energi</div>
                <div id="statEnergy" style="color:#a855f7; font-size:20px; font-weight:bold; margin-top:6px;">0.000 J</div>
            </div>
        </div>
    </div>

    <script>
    (function() {{
        const canvas = document.getElementById('simCanvas');
        const ctx = canvas.getContext('2d');
        const W = canvas.width, H = canvas.height;

        const tData = {t_js};
        const xData = {x_js};
        const vData = {v_js};
        const eData = {e_js};
        const xMax = {x_max};
        const totalFrames = tData.length;

        let frame = 0, playing = false, animId = null, lastT = 0;
        window.speed = 1;  // Exposed to global for HTML onchange event

        const anchorY = 40, restLen = 140, massW = 50, massH = 45;
        const equilibriumY = anchorY + restLen;

        function drawSpring(x1, y1, x2, y2, coils=12) {{
            const len = y2 - y1;
            if (len < 20) return;
            const coilH = len / coils, coilW = 20;
            ctx.strokeStyle = '#6b7280';
            ctx.lineWidth = 3;
            ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x1, y1+10); ctx.stroke();

            for (let i = 0; i < coils; i++) {{
                const yy = y1 + 10 + i * coilH;
                const stretch = Math.min(1, Math.max(0, (len - 80) / 160));
                ctx.strokeStyle = `rgb(${{59+180*stretch}},${{130-62*stretch}},${{246-178*stretch}})`;
                ctx.lineWidth = 4;
                const dir = (i % 2 === 0) ? 1 : -1;
                ctx.beginPath();
                ctx.moveTo(x1, yy);
                ctx.lineTo(x1 + dir * coilW, yy + coilH/2);
                ctx.lineTo(x1, yy + coilH);
                ctx.stroke();
            }}
        }}

        function draw() {{
            ctx.fillStyle = '#0d1117';
            ctx.fillRect(0, 0, W, H);

            // Grid
            ctx.strokeStyle = '#21262d';
            ctx.lineWidth = 1;
            for (let i = 0; i < W; i += 30) {{ ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, H); ctx.stroke(); }}
            for (let i = 0; i < H; i += 30) {{ ctx.beginPath(); ctx.moveTo(0, i); ctx.lineTo(W, i); ctx.stroke(); }}

            // Ceiling
            ctx.fillStyle = '#4b5563';
            ctx.fillRect(W/2 - 50, 15, 100, 18);
            ctx.fillStyle = '#6b7280';
            ctx.beginPath(); ctx.arc(W/2, anchorY, 8, 0, Math.PI*2); ctx.fill();

            // Equilibrium line
            ctx.strokeStyle = '#3fb950';
            ctx.setLineDash([8, 4]);
            ctx.beginPath(); ctx.moveTo(W/2-70, equilibriumY); ctx.lineTo(W/2+70, equilibriumY); ctx.stroke();
            ctx.setLineDash([]);
            ctx.fillStyle = '#3fb950'; ctx.font = '12px Arial'; ctx.textAlign = 'left';
            ctx.fillText('y = 0', W/2 + 80, equilibriumY + 4);

            // Get current data
            const x = xData[frame] || 0;
            const t = tData[frame] || 0;
            const v = vData[frame] || 0;
            const e = eData[frame] || 0;

            // Calculate mass position (scale displacement to pixels)
            const displacementPx = (x / xMax) * 80;
            const massY = equilibriumY + displacementPx;

            // Draw spring
            drawSpring(W/2, anchorY + 10, W/2, massY - massH/2);

            // Draw mass
            const grad = ctx.createLinearGradient(W/2-massW/2, massY-massH/2, W/2+massW/2, massY+massH/2);
            grad.addColorStop(0, '#60a5fa'); grad.addColorStop(0.5, '#3b82f6'); grad.addColorStop(1, '#1d4ed8');
            ctx.fillStyle = grad;
            ctx.beginPath();
            ctx.roundRect(W/2-massW/2, massY-massH/2, massW, massH, 8);
            ctx.fill();
            ctx.strokeStyle = '#93c5fd'; ctx.lineWidth = 2; ctx.stroke();

            ctx.fillStyle = 'white'; ctx.font = 'bold 16px Arial'; ctx.textAlign = 'center';
            ctx.fillText('m', W/2, massY + 5);

            ctx.fillStyle = '#c9d1d9'; ctx.font = '11px Arial';
            ctx.fillText('y = ' + x.toFixed(4) + ' m', W/2, massY + massH/2 + 18);

            // Update stats
            document.getElementById('statTime').textContent = t.toFixed(3) + ' s';
            document.getElementById('statPos').textContent = x.toFixed(4) + ' m';
            document.getElementById('statVel').textContent = v.toFixed(3) + ' m/s';
            document.getElementById('statEnergy').textContent = e.toFixed(4) + ' J';
            document.getElementById('timeSlider').value = frame;
            document.getElementById('timeLabel').textContent = 't = ' + t.toFixed(3) + ' s';
        }}

        function animate(ts) {{
            if (!playing) return;
            if (ts - lastT > 16 / window.speed) {{
                frame = (frame + 1) % totalFrames;
                draw();
                lastT = ts;
            }}
            animId = requestAnimationFrame(animate);
        }}

        window.togglePlay = function() {{
            playing = !playing;
            const btn = document.getElementById('playPauseBtn');
            if (playing) {{
                btn.innerHTML = '⏸️ Pause';
                btn.style.background = 'linear-gradient(135deg,#da3633,#f85149)';
                lastT = performance.now();
                animate(lastT);
            }} else {{
                btn.innerHTML = '▶️ Play';
                btn.style.background = 'linear-gradient(135deg,#238636,#2ea043)';
                if (animId) cancelAnimationFrame(animId);
            }}
        }};

        window.resetAnim = function() {{ frame = 0; draw(); }};
        window.seekTo = function(val) {{ frame = parseInt(val); if (!playing) draw(); }};

        // Initial draw
        draw();
    }})();
    </script>
    """

    import streamlit.components.v1 as components
    components.html(simple_html, height=750)

# ============================================================
# TAB 3: GRAFIK
# ============================================================

with tab_graphs:
    st.markdown("###  Grafik Analisis")
    st.caption("Grafik berdasarkan preset - tarik beban di tab Simulasi untuk demo live!")

    # Solve for preset (for static graphs)
    solution = solve_spring_system(params, (0, simulation_duration), time_step=0.001)

    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    t = solution['t']
    x = solution['x']
    v = solution['v']

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Posisi vs Waktu', 'Kecepatan vs Waktu', 'Phase Space', 'Energi vs Waktu'),
        vertical_spacing=0.15,
        horizontal_spacing=0.1
    )

    fig.add_trace(go.Scatter(x=t, y=x, mode='lines', name='Posisi',
                             line=dict(color='#3B82F6', width=2)), row=1, col=1)

    if 0 < params.zeta < 1:
        alpha = params.zeta * params.omega_n
        envelope = params.x0 * np.exp(-alpha * t)
        fig.add_trace(go.Scatter(x=t, y=envelope, mode='lines',
                                 line=dict(color='#EF4444', width=1, dash='dash'), showlegend=False), row=1, col=1)
        fig.add_trace(go.Scatter(x=t, y=-envelope, mode='lines',
                                 line=dict(color='#EF4444', width=1, dash='dash'), showlegend=False), row=1, col=1)

    fig.add_trace(go.Scatter(x=t, y=v, mode='lines', name='Kecepatan',
                             line=dict(color='#22C55E', width=2)), row=1, col=2)
    fig.add_trace(go.Scatter(x=x, y=v, mode='lines', name='Phase Space',
                             line=dict(color='#A855F7', width=2)), row=2, col=1)
    fig.add_trace(go.Scatter(x=[x[0]], y=[v[0]], mode='markers',
                             marker=dict(color='#22C55E', size=10)), row=2, col=1)
    fig.add_trace(go.Scatter(x=[x[-1]], y=[v[-1]], mode='markers',
                             marker=dict(color='#EF4444', size=10, symbol='x')), row=2, col=1)
    fig.add_trace(go.Scatter(x=t, y=solution['KE'], mode='lines', name='KE',
                             line=dict(color='#F59E0B', width=2)), row=2, col=2)
    fig.add_trace(go.Scatter(x=t, y=solution['PE'], mode='lines', name='PE',
                             line=dict(color='#8B5CF6', width=2)), row=2, col=2)
    fig.add_trace(go.Scatter(x=t, y=solution['E_total'], mode='lines', name='Total',
                             line=dict(color='#EC4899', width=2, dash='dash')), row=2, col=2)

    fig.update_layout(
        height=600,
        template='plotly_dark',
        paper_bgcolor='#0E1117',
        plot_bgcolor='#1E2329',
        showlegend=False,
        margin=dict(t=50, b=50, l=50, r=30)
    )

    fig.update_xaxes(title_text='t (s)', row=1, col=1)
    fig.update_xaxes(title_text='t (s)', row=1, col=2)
    fig.update_xaxes(title_text='x (m)', row=2, col=1)
    fig.update_xaxes(title_text='t (s)', row=2, col=2)
    fig.update_yaxes(title_text='x (m)', row=1, col=1)
    fig.update_yaxes(title_text='v (m/s)', row=1, col=2)
    fig.update_yaxes(title_text='v (m/s)', row=2, col=1)
    fig.update_yaxes(title_text='E (J)', row=2, col=2)

    st.plotly_chart(fig, width='stretch')

    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Amplitudo Max", f"{abs(x).max():.4f} m")
    col2.metric("Kecepatan Max", f"{abs(v).max():.4f} m/s")
    col3.metric("Energi Awal", f"{solution['E_total'][0]:.4f} J")
    energy_loss = (solution['E_total'][0] - solution['E_total'][-1]) / solution['E_total'][0] * 100
    col4.metric("Energi Hilang", f"{energy_loss:.1f}%")

# ============================================================
# TAB 3: TEORI
# ============================================================

with tab_theory:
    st.markdown(PHYSICS_EXPLANATION)

    st.markdown("---")
    st.markdown("###  Sistem Saat Ini")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        **Parameter:**
        - Massa: **{params.m}** kg
        - Konstanta pegas: **{params.k}** N/m
        - Koefisien redaman: **{params.c}** Ns/m

        **Karakteristik:**
        - ωₙ = **{params.omega_n:.3f}** rad/s
        - ζ = **{params.zeta:.4f}**
        - T = **{params.period:.3f}** s
        """)

    with col2:
        dtype = params.damping_type
        if dtype == DampingType.UNDAMPED:
            st.success("🟢 **Tanpa Redaman**\n\nOsilasi terus tanpa berhenti.")
        elif dtype == DampingType.UNDERDAMPED:
            st.info(" **Underdamped**\n\nOsilasi teredam, amplitudo menurun.")
        elif dtype == DampingType.CRITICALLY_DAMPED:
            st.warning("🟡 **Critically Damped**\n\nKembali tercepat tanpa osilasi.")
        else:
            st.error(" **Overdamped**\n\nKembali lambat tanpa osilasi.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; padding: 1rem;">
    <p> <strong>Simulasi Gaya Pegas - Hooke's Law</strong></p>
    <p>Tugas Akhir Fisika - Dimas, Daffa, Dharma</p>
</div>
""", unsafe_allow_html=True)
