import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from pathlib import Path

# Doc du lieu tu file CSV
FILE_CSV = "abc-7(1).csv"

df = pd.read_csv(FILE_CSV, header=None)
data = df.apply(pd.to_numeric, errors="coerce")

# Lay gia dong cua (cot thu 7)
close = data.iloc[:, 6].dropna().to_numpy(dtype=float)

if len(close) != 365:
    raise ValueError("Du lieu phai co dung 365 ngay!")

# Thiet lap cac thong so
INITIAL_REFERENCE = 10000
FPS = 12
FRAME_STEP = 2

days = np.arange(1, len(close) + 1)

# Tinh gia tham chieu, gia san va gia tran
reference = np.empty(len(close))
reference[0] = INITIAL_REFERENCE
reference[1:] = close[:-1]

floor_price = reference * 0.90
ceiling_price = reference * 1.10

# Xac dinh mau sac theo gia co phieu
def price_color(i):
    if np.isclose(close[i], floor_price[i]):
        return "blue"
    elif np.isclose(close[i], ceiling_price[i]):
        return "purple"
    elif np.isclose(close[i], reference[i]):
        return "gold"
    elif close[i] < reference[i]:
        return "red"
    else:
        return "green"


# Khoi tao bieu do
fig, ax = plt.subplots(figsize=(12, 6))

ax.set_title(
    "MO PHONG BIEN DONG GIA CO PHIEU ABC-7",
    fontsize=16,
    fontweight="bold"
)

ax.set_xlabel("Ngay giao dich")
ax.set_ylabel("Gia dong cua")

ax.set_xlim(1, 365)

ax.set_ylim(
    min(close.min(), floor_price.min()) * 0.95,
    max(close.max(), ceiling_price.max()) * 1.05
)

ax.grid(True, alpha=0.3)

# Tao duong bieu dien gia
line, = ax.plot([], [], color="black", linewidth=2)

points = ax.scatter([], [], s=25)

# Duong gia tham chieu, gia san, gia tran
ref_line = ax.axhline(
    INITIAL_REFERENCE,
    color="gold",
    linestyle="--",
    label="Gia tham chieu"
)

floor_line = ax.axhline(
    INITIAL_REFERENCE * 0.9,
    color="blue",
    linestyle=":",
    label="Gia san"
)

ceiling_line = ax.axhline(
    INITIAL_REFERENCE * 1.1,
    color="purple",
    linestyle=":",
    label="Gia tran"
)

# Hien thi thong tin tren bieu do
info = ax.text(
    0.02, 0.95, "",
    transform=ax.transAxes,
    fontsize=10,
    verticalalignment="top",
    bbox=dict(
        boxstyle="round",
        facecolor="white",
        alpha=0.9
    )
)

ax.legend(loc="lower right")


# Ham cap nhat tung khung hinh
def update(frame):

    i = int(frame)

    x = days[:i + 1]
    y = close[:i + 1]

    line.set_data(x, y)

    points.set_offsets(
        np.column_stack((x, y))
    )

    points.set_color(
        [price_color(j) for j in range(i + 1)]
    )

    # Cap nhat cac muc gia
    ref_line.set_ydata(
        [reference[i], reference[i]]
    )

    floor_line.set_ydata(
        [floor_price[i], floor_price[i]]
    )

    ceiling_line.set_ydata(
        [ceiling_price[i], ceiling_price[i]]
    )

    # Xac dinh trang thai gia
    if np.isclose(close[i], floor_price[i]):
        status = "CHAM GIA SAN"

    elif np.isclose(close[i], ceiling_price[i]):
        status = "CHAM GIA TRAN"

    elif np.isclose(close[i], reference[i]):
        status = "BANG GIA THAM CHIEU"

    elif close[i] < reference[i]:
        status = "DUOI GIA THAM CHIEU"

    else:
        status = "TREN GIA THAM CHIEU"

    # Cap nhat thong tin
    info.set_text(
        f"Ngay: {i + 1}/365\n"
        f"Gia dong cua: {close[i]:,.2f}\n"
        f"Gia tham chieu: {reference[i]:,.2f}\n"
        f"Gia san: {floor_price[i]:,.2f}\n"
        f"Gia tran: {ceiling_price[i]:,.2f}\n"
        f"Trang thai: {status}"
    )

    return (
        line,
        points,
        ref_line,
        floor_line,
        ceiling_line,
        info
    )


# Tao cac khung hinh animation
frames = list(range(0, len(close), FRAME_STEP))

if frames[-1] != len(close) - 1:
    frames.append(len(close) - 1)

animation = FuncAnimation(
    fig,
    update,
    frames=frames,
    interval=1000 / FPS,
    blit=False,
    repeat=False
)


# Xuat video MP4
output_dir = Path("ket_qua_animation")
output_dir.mkdir(exist_ok=True)

writer = FFMpegWriter(
    fps=FPS,
    bitrate=1600
)

animation.save(
    output_dir / "animation_gia_co_phieu.mp4",
    writer=writer,
    dpi=100
)

print("DA TAO VIDEO ANIMATION THANH CONG!")

plt.close(fig)