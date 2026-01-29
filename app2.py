import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from scipy.special import lambertw


# =========================================================
# МОДЕЛЬ IRR (АНАЛИТИЧЕСКАЯ, АНАЛОГ WOLFRAM ProductLog)
# =========================================================
def IRR(
    Mvn,        # стоимость внедрения системы обслуживания РВД, руб
    Tvosst,     # время восстановления после отказа РВД, час
    Msod,       # годовая стоимость содержания системы, руб/год
    Cp,         # часовая стоимость простоя техники, руб
    Kteh,       # количество обслуживаемой техники, ед.
    Ktg,        # закладываемый КТГ из-за РВД (доля)
    Tpl,        # плановое время работы в год, час
    Tvosstso,   # время восстановления при внедрении системы, час
    Y           # время с начала проекта, лет
):
    A = (
        Msod * Tvosst
        - Cp * Kteh * Ktg * Tpl * Tvosst
        + Cp * Kteh * Ktg * Tpl * Tvosstso
    )

    W = lambertw(
        (A * Y / (Mvn * Tvosst)) * np.exp((A * Y) / (Mvn * Tvosst))
    )

    irr = (
        -Msod * Tvosst * Y
        + Cp * Kteh * Ktg * Tpl * Tvosst * Y
        - Cp * Kteh * Ktg * Tpl * Tvosstso * Y
        + Mvn * Tvosst * W.real
    ) / (Mvn * Tvosst * Y)

    return irr


# =========================================================
# НАСТРОЙКИ СТРАНИЦЫ
# =========================================================
st.set_page_config(
    page_title="IRR проекта (РВД)",
    layout="wide"
)

st.title("Интерактивный расчёт IRR проекта внедрения системы обслуживания РВД")


# =========================================================
# БАЗОВЫЙ СЦЕНАРИЙ
# =========================================================
BASE = {
    "Mvn": 20_000_000,
    "Tvosstso": 2.0,
    "Kteh": 100,
    "Tpl": 5_000,
    "Tvosst": 12.0,
    "Msod": 1_000_000,
    "Cp": 50_000,
    "Ktg": 0.10
}

for key, value in BASE.items():
    if key not in st.session_state:
        st.session
