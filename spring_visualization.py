"""
 Visualisasi dan Animasi Pegas
================================

Modul ini menyediakan:
- Animasi pegas real-time dengan matplotlib
- Grafik posisi, kecepatan, energi
- Fungsi untuk generate GIF animasi
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle, FancyBboxPatch
from matplotlib.lines import Line2D
import io
import base64
from typing import Optional


# Style settings
plt.style.use('dark_background')
COLORS = {
    'spring': '#60A5FA',
    'mass': '#3B82F6',
    'wall': '#64748B',
    'ground': '#475569',
    'equilibrium': '#22C55E',
    'position': '#3B82F6',
    'velocity': '#22C55E',
    'energy_total': '#EF4444',
    'energy_kinetic': '#F59E0B',
    'energy_potential': '#8B5CF6',
    'text': '#E5E7EB',
    'grid': '#374151'
}


def draw_spring(ax, x_start: float, x_end: float, y: float = 0.5,
                n_coils: int = 10, amplitude: float = 0.08) -> Line2D:
    """
    Gambar pegas heliks antara dua titik
    """
    # Generate spring points
    n_points = n_coils * 20 + 1
    t = np.linspace(0, n_coils * 2 * np.pi, n_points)
    
    # Spring coordinates
    spring_length = x_end - x_start
    x = x_start + (t / (n_coils * 2 * np.pi)) * spring_length
    y_spring = y + amplitude * np.sin(t)
    
    # Flatten ends
    flat_points = 5
    y_spring[:flat_points] = y
    y_spring[-flat_points:] = y
    
    line, = ax.plot(x, y_spring, color=COLORS['spring'], linewidth=2.5, solid_capstyle='round')
    return line


def create_spring_animation_figure(solution: dict, x_scale: float = 1.0) -> tuple:
    """
    Buat figure untuk animasi pegas
    
    Returns:
    --------
    fig, ax_anim, ax_pos, ax_energy, elements
    """
    fig = plt.figure(figsize=(12, 8), facecolor='#0E1117')
    
    # Layout: Animation on top, graphs below
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1], hspace=0.3, wspace=0.25)
    
    ax_anim = fig.add_subplot(gs[0, :])  # Animation spans full width
    ax_pos = fig.add_subplot(gs[1, 0])   # Position plot
    ax_energy = fig.add_subplot(gs[1, 1])  # Energy plot
    
    # Style axes
    for ax in [ax_anim, ax_pos, ax_energy]:
        ax.set_facecolor('#1E2329')
        ax.tick_params(colors=COLORS['text'])
        for spine in ax.spines.values():
            spine.set_color(COLORS['grid'])
    
    # ===== ANIMATION AXIS =====
    x_data = solution['x']
    x_max = max(abs(x_data.max()), abs(x_data.min()), 0.3) * x_scale
    
    ax_anim.set_xlim(-0.5, 2.5)
    ax_anim.set_ylim(-0.3, 1.3)
    ax_anim.set_aspect('equal')
    ax_anim.axis('off')
    ax_anim.set_title(' Animasi Sistem Massa-Pegas', color=COLORS['text'], fontsize=14, fontweight='bold')
    
    # Wall
    wall = FancyBboxPatch((-0.4, 0.2), 0.15, 0.6, 
                          boxstyle="round,pad=0.02",
                          facecolor=COLORS['wall'], 
                          edgecolor='#94A3B8', linewidth=2)
    ax_anim.add_patch(wall)
    
    # Ground
    ax_anim.axhline(y=0.2, xmin=0, xmax=1, color=COLORS['ground'], linewidth=2)
    
    # Equilibrium marker
    ax_anim.axvline(x=1.0, ymin=0.05, ymax=0.25, color=COLORS['equilibrium'], 
                    linestyle='--', linewidth=2, alpha=0.7)
    ax_anim.text(1.0, 0.05, 'x=0', color=COLORS['equilibrium'], 
                 ha='center', fontsize=10, fontweight='bold')
    
    # Initial spring
    x_init = x_data[0]
    mass_x = 1.0 + x_init / x_max * 0.8
    spring_line = draw_spring(ax_anim, -0.25, mass_x - 0.15, y=0.5)
    
    # Mass
    mass_size = 0.25
    mass_rect = FancyBboxPatch((mass_x - mass_size/2, 0.5 - mass_size/2), 
                                mass_size, mass_size,
                                boxstyle="round,pad=0.02",
                                facecolor=COLORS['mass'], 
                                edgecolor='#60A5FA', linewidth=2)
    ax_anim.add_patch(mass_rect)
    
    # Mass label
    mass_text = ax_anim.text(mass_x, 0.5, 'm', color='white', 
                             ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Position text
    pos_text = ax_anim.text(mass_x, 0.12, f'x = {x_init:.3f} m', 
                            color=COLORS['text'], ha='center', fontsize=11)
    
    # Time text
    time_text = ax_anim.text(2.2, 1.1, 't = 0.00 s', 
                             color=COLORS['text'], ha='right', fontsize=12)
    
    # ===== POSITION PLOT =====
    t_data = solution['t']
    ax_pos.plot(t_data, x_data, color=COLORS['position'], linewidth=1.5, label='Posisi x(t)')
    ax_pos.axhline(y=0, color=COLORS['equilibrium'], linestyle='--', alpha=0.5)
    pos_marker, = ax_pos.plot([0], [x_data[0]], 'o', color=COLORS['position'], markersize=8)
    ax_pos.set_xlabel('Waktu (s)', color=COLORS['text'])
    ax_pos.set_ylabel('Posisi (m)', color=COLORS['text'])
    ax_pos.set_title(' Posisi vs Waktu', color=COLORS['text'], fontsize=11)
    ax_pos.grid(True, alpha=0.3, color=COLORS['grid'])
    ax_pos.legend(loc='upper right', facecolor='#1E2329', edgecolor=COLORS['grid'])
    
    # ===== ENERGY PLOT =====
    KE = solution['KE']
    PE = solution['PE']
    E_total = solution['E_total']
    
    ax_energy.plot(t_data, E_total, color=COLORS['energy_total'], linewidth=2, label='Total')
    ax_energy.plot(t_data, KE, color=COLORS['energy_kinetic'], linewidth=1.5, label='Kinetik', alpha=0.8)
    ax_energy.plot(t_data, PE, color=COLORS['energy_potential'], linewidth=1.5, label='Potensial', alpha=0.8)
    energy_marker, = ax_energy.plot([0], [E_total[0]], 'o', color=COLORS['energy_total'], markersize=8)
    ax_energy.set_xlabel('Waktu (s)', color=COLORS['text'])
    ax_energy.set_ylabel('Energi (J)', color=COLORS['text'])
    ax_energy.set_title(' Energi vs Waktu', color=COLORS['text'], fontsize=11)
    ax_energy.grid(True, alpha=0.3, color=COLORS['grid'])
    ax_energy.legend(loc='upper right', facecolor='#1E2329', edgecolor=COLORS['grid'])
    
    plt.tight_layout()
    
    elements = {
        'spring_line': spring_line,
        'mass_rect': mass_rect,
        'mass_text': mass_text,
        'pos_text': pos_text,
        'time_text': time_text,
        'pos_marker': pos_marker,
        'energy_marker': energy_marker,
        'x_max': x_max
    }
    
    return fig, ax_anim, ax_pos, ax_energy, elements


def create_animation(solution: dict, fps: int = 30, 
                     speed_multiplier: float = 1.0) -> animation.FuncAnimation:
    """
    Buat animasi matplotlib dari solusi
    
    Parameters:
    -----------
    solution : dict - Hasil dari solve_spring_system
    fps : int - Frame per second
    speed_multiplier : float - Pengali kecepatan animasi
    
    Returns:
    --------
    matplotlib.animation.FuncAnimation
    """
    fig, ax_anim, ax_pos, ax_energy, elements = create_spring_animation_figure(solution)
    
    t_data = solution['t']
    x_data = solution['x']
    E_total = solution['E_total']
    x_max = elements['x_max']
    
    # Calculate frame indices
    dt = t_data[1] - t_data[0]
    frame_skip = max(1, int(speed_multiplier / dt / fps))
    frame_indices = list(range(0, len(t_data), frame_skip))
    
    def update(frame_idx):
        i = frame_indices[frame_idx]
        t = t_data[i]
        x = x_data[i]
        
        # Update mass position
        mass_x = 1.0 + x / x_max * 0.8
        mass_size = 0.25
        elements['mass_rect'].set_xy((mass_x - mass_size/2, 0.5 - mass_size/2))
        elements['mass_text'].set_position((mass_x, 0.5))
        
        # Update spring
        elements['spring_line'].remove()
        elements['spring_line'] = draw_spring(ax_anim, -0.25, mass_x - 0.15, y=0.5)
        
        # Update texts
        elements['pos_text'].set_position((mass_x, 0.12))
        elements['pos_text'].set_text(f'x = {x:.3f} m')
        elements['time_text'].set_text(f't = {t:.2f} s')
        
        # Update markers
        elements['pos_marker'].set_data([t], [x])
        elements['energy_marker'].set_data([t], [E_total[i]])
        
        return [elements['mass_rect'], elements['mass_text'], 
                elements['spring_line'], elements['pos_text'], 
                elements['time_text'], elements['pos_marker'],
                elements['energy_marker']]
    
    anim = animation.FuncAnimation(
        fig, update, frames=len(frame_indices),
        interval=1000/fps, blit=False, repeat=True
    )
    
    return anim, fig


def create_static_plots(solution: dict) -> plt.Figure:
    """
    Buat grafik statis untuk analisis
    
    Returns figure dengan 4 subplot:
    - Posisi vs waktu
    - Kecepatan vs waktu
    - Phase space (v vs x)
    - Energi vs waktu
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), facecolor='#0E1117')
    
    t = solution['t']
    x = solution['x']
    v = solution['v']
    KE = solution['KE']
    PE = solution['PE']
    E_total = solution['E_total']
    params = solution['params']
    
    for ax in axes.flat:
        ax.set_facecolor('#1E2329')
        ax.tick_params(colors=COLORS['text'])
        ax.grid(True, alpha=0.3, color=COLORS['grid'])
        for spine in ax.spines.values():
            spine.set_color(COLORS['grid'])
    
    # Position
    axes[0, 0].plot(t, x, color=COLORS['position'], linewidth=1.5)
    axes[0, 0].axhline(y=0, color=COLORS['equilibrium'], linestyle='--', alpha=0.5)
    axes[0, 0].set_xlabel('Waktu (s)', color=COLORS['text'])
    axes[0, 0].set_ylabel('Posisi (m)', color=COLORS['text'])
    axes[0, 0].set_title(' Posisi x(t)', color=COLORS['text'], fontweight='bold')
    
    # Velocity
    axes[0, 1].plot(t, v, color=COLORS['velocity'], linewidth=1.5)
    axes[0, 1].axhline(y=0, color=COLORS['grid'], linestyle='--', alpha=0.5)
    axes[0, 1].set_xlabel('Waktu (s)', color=COLORS['text'])
    axes[0, 1].set_ylabel('Kecepatan (m/s)', color=COLORS['text'])
    axes[0, 1].set_title(' Kecepatan v(t)', color=COLORS['text'], fontweight='bold')
    
    # Phase space
    axes[1, 0].plot(x, v, color=COLORS['position'], linewidth=1.5)
    axes[1, 0].plot(x[0], v[0], 'go', markersize=10, label='Start')
    axes[1, 0].plot(x[-1], v[-1], 'rx', markersize=10, label='End')
    axes[1, 0].axhline(y=0, color=COLORS['grid'], linestyle='--', alpha=0.5)
    axes[1, 0].axvline(x=0, color=COLORS['grid'], linestyle='--', alpha=0.5)
    axes[1, 0].set_xlabel('Posisi (m)', color=COLORS['text'])
    axes[1, 0].set_ylabel('Kecepatan (m/s)', color=COLORS['text'])
    axes[1, 0].set_title(' Phase Space', color=COLORS['text'], fontweight='bold')
    axes[1, 0].legend(facecolor='#1E2329', edgecolor=COLORS['grid'])
    
    # Energy
    axes[1, 1].plot(t, E_total, color=COLORS['energy_total'], linewidth=2, label='Total')
    axes[1, 1].plot(t, KE, color=COLORS['energy_kinetic'], linewidth=1.5, label='Kinetik', alpha=0.8)
    axes[1, 1].plot(t, PE, color=COLORS['energy_potential'], linewidth=1.5, label='Potensial', alpha=0.8)
    axes[1, 1].axhline(y=E_total[0], color=COLORS['text'], linestyle=':', alpha=0.5, label='E₀')
    axes[1, 1].set_xlabel('Waktu (s)', color=COLORS['text'])
    axes[1, 1].set_ylabel('Energi (J)', color=COLORS['text'])
    axes[1, 1].set_title(' Energi', color=COLORS['text'], fontweight='bold')
    axes[1, 1].legend(loc='upper right', facecolor='#1E2329', edgecolor=COLORS['grid'])
    
    # Add info box
    info_text = (f"m = {params.m} kg | k = {params.k} N/m | c = {params.c} Ns/m\n"
                 f"ωₙ = {params.omega_n:.2f} rad/s | ζ = {params.zeta:.3f} | T = {params.period:.3f} s")
    fig.text(0.5, 0.02, info_text, ha='center', color=COLORS['text'], fontsize=10,
             bbox=dict(boxstyle='round', facecolor='#1E2329', edgecolor=COLORS['grid']))
    
    plt.tight_layout(rect=[0, 0.05, 1, 1])
    
    return fig


def fig_to_base64(fig: plt.Figure) -> str:
    """Convert matplotlib figure to base64 string for Streamlit"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor=fig.get_facecolor())
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode()
