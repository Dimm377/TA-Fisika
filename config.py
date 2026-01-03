"""
Configuration constants for the Spring Simulation App.
Centralizes all hardcoded values for easy maintenance.
"""

# ============================================================
# APP CONFIG
# ============================================================

APP_TITLE = "Simulasi Gaya Pegas"
APP_SUBTITLE = "Eksplorasi Hukum Hooke dan Dinamika Sistem Massa-Pegas"
APP_ICON = ""

# ============================================================
# SIMULATION DEFAULTS
# ============================================================

DEFAULT_DURATION_SECONDS = 10.0
DEFAULT_TIME_STEP = 0.001
MIN_DURATION = 1.0
MAX_DURATION = 30.0

ANIMATION_MAX_POINTS = 500
ANIMATION_FPS = 60

# ============================================================
# EXTERNAL FORCE DEFAULTS
# ============================================================

STEP_FORCE_AMPLITUDE = 10.0
STEP_FORCE_START_TIME = 1.0

HARMONIC_FORCE_AMPLITUDE = 10.0
HARMONIC_FORCE_OMEGA = 5.0

# ============================================================
# CUSTOM MODE INPUT LIMITS
# ============================================================

MASS_RANGE = (0.01, 1000.0, 1.0, 0.1)  # min, max, default, step
SPRING_CONSTANT_RANGE = (0.1, 100000.0, 100.0, 1.0)
DAMPING_RANGE = (0.0, 10000.0, 1.0, 0.1)
INITIAL_POSITION_RANGE = (-1.0, 1.0, 0.5, 0.01)

# ============================================================
# SIMULATION MODES
# ============================================================

MODE_PRESET = " Preset Real-Life"
MODE_CUSTOM = " Custom"
SIMULATION_MODES = [MODE_PRESET, MODE_CUSTOM]

# ============================================================
# EXTERNAL FORCE OPTIONS
# ============================================================

FORCE_NONE = "Tanpa Gaya"
FORCE_STEP = "Step Force"
FORCE_HARMONIC = "Harmonic Force"
EXTERNAL_FORCE_OPTIONS = [FORCE_NONE, FORCE_STEP, FORCE_HARMONIC]

# ============================================================
# TAB CONFIGURATION
# ============================================================

TAB_ANIMATION = " Animasi"
TAB_GRAPHS = " Grafik"
TAB_VALIDATION = " Validasi & FFT"
TAB_THEORY = " Teori"
TAB_CONCLUSION = " Kesimpulan"
TAB_EXPORT = " Ekspor"

TAB_NAMES = [
    TAB_ANIMATION,
    TAB_GRAPHS,
    TAB_VALIDATION,
    TAB_THEORY,
    TAB_CONCLUSION,
    TAB_EXPORT
]

# ============================================================
# DAMPING TYPE ICONS
# ============================================================

DAMPING_ICONS = {
    "Tanpa Redaman": "🟢",
    "Underdamped": "",
    "Critically Damped": "",
    "Overdamped": ""
}

# ============================================================
# CHART COLORS
# ============================================================

COLORS = {
    "position": "#3B82F6",
    "velocity": "#22C55E",
    "energy_kinetic": "#F59E0B",
    "energy_potential": "#8B5CF6",
    "energy_total": "#EC4899",
    "envelope": "#EF4444",
    "phase_space": "#A855F7",
    "start_marker": "#22C55E",
    "end_marker": "#EF4444"
}

# ============================================================
# STATISTICS CARD STYLES
# ============================================================

STAT_CARD_AMPLITUDE = {
    "bg_gradient": "linear-gradient(135deg, #1e3a5f, #0d2137)",
    "border_color": "#3b82f6",
    "text_color": "#60a5fa",
    "icon": ""
}

STAT_CARD_VELOCITY = {
    "bg_gradient": "linear-gradient(135deg, #1e3a2f, #0d2117)",
    "border_color": "#22c55e",
    "text_color": "#4ade80",
    "icon": ""
}

STAT_CARD_ENERGY = {
    "bg_gradient": "linear-gradient(135deg, #3a2f1e, #21170d)",
    "border_color": "#f59e0b",
    "text_color": "#fbbf24",
    "icon": ""
}

STAT_CARD_DISSIPATED = {
    "bg_gradient": "linear-gradient(135deg, #3a1e2f, #210d17)",
    "border_color": "#ec4899",
    "text_color": "#f472b6",
    "icon": ""
}
