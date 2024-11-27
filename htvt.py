import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc

def calculate_and_plot():
    try:
        # Lấy thông số từ giao diện
        R_E = float(entry_R_E.get())  # Bán kính Trái Đất (km)
        h = float(entry_h.get())  # Chiều cao vệ tinh (km)
        P_tx = float(entry_P_tx.get())  # Công suất phát (W)
        f = float(entry_f.get())  # Tần số (GHz)
        theta = float(entry_theta.get())  # Góc ngẩng (độ)
        alpha = float(entry_alpha.get())  # Hệ số suy hao
        Ha = float(entry_Ha.get())  # Độ cao anten phát (m)
        H_rain = float(entry_Hrain.get())  # Độ cao mưa (m)
        L_tx = float(entry_L_tx.get())  # Suy hao truyền phát (dB)
        L_rx = float(entry_L_rx.get())  # Suy hao truyền thu (dB)
        eta = float(entry_eta.get())  # Hiệu suất anten
        D_tx = float(entry_D_tx.get())  # Đường kính anten phát (m)
        D_rx = float(entry_D_rx.get())  # Đường kính anten thu (m)

        # Tính toán cơ bản
        d = np.sqrt(R_E**2 + (R_E + h)**2 - 2 * R_E * (R_E + h) * np.cos(np.radians(theta)))
        Lfs = 92.44 + 20 * np.log10(d) + 20 * np.log10(f)
        Dr = (H_rain - Ha) / np.sin(np.radians(theta))
        Lrain = alpha * Dr
        L_total = Lfs + L_tx + Lrain + L_rx
        G_tx = eta * ((np.pi * D_tx) / (3e8 / (f * 1e9)))**2
        G_rx = eta * ((np.pi * D_rx) / (3e8 / (f * 1e9)))**2
        EIRP = 10 * np.log10(P_tx) + 10 * np.log10(G_tx) + L_tx
        P_rx = 10 * np.log10(P_tx) + 10 * np.log10(G_tx) + 10 * np.log10(G_rx) - L_total

        # Tính BER
        SNR_dB = np.arange(0, 30, 2)
        BER = 0.5 * erfc(np.sqrt(10**(SNR_dB / 10)))

        # Đồ thị
        fig, axs = plt.subplots(3, 2, figsize=(12, 10))

        # Đồ thị 1: SNR vs BER
        axs[0, 0].semilogy(SNR_dB, BER, 'b-', linewidth=2)
        axs[0, 0].set_title('Tỷ lệ lỗi bit (BER)', fontsize=10)
        axs[0, 0].set_xlabel('SNR (dB)', fontsize=9)
        axs[0, 0].set_ylabel('Tỷ lệ lỗi bit (BER)', fontsize=9)
        axs[0, 0].grid(True)

        # Đồ thị 2: Suy hao tín hiệu
        axs[0, 1].bar(['Lfs', 'Lrain', 'L_total'], [Lfs, Lrain, L_total], color=['blue', 'orange', 'green'])
        axs[0, 1].set_title('Suy hao tín hiệu', fontsize=10)
        axs[0, 1].set_ylabel('Suy hao (dB)', fontsize=9)
        axs[0, 1].grid(True)

        # Đồ thị 3: Góc xoay anten
        distances = np.linspace(0.1, h, 50)
        angles = np.degrees(np.arctan((distances + h) / R_E))
        axs[1, 0].plot(distances, angles, 'r-', linewidth=2)
        axs[1, 0].set_title('Góc xoay anten theo khoảng cách', fontsize=10)
        axs[1, 0].set_xlabel('Khoảng cách (km)', fontsize=9)
        axs[1, 0].set_ylabel('Góc xoay (độ)', fontsize=9)
        axs[1, 0].grid(True)

        # Đồ thị 4: Hiệu suất anten
        radii = np.linspace(0.1, D_tx, 50)
        efficiencies = eta * ((np.pi * radii) / (3e8 / (f * 1e9)))**2
        axs[1, 1].plot(radii, efficiencies, 'g-', linewidth=2)
        axs[1, 1].set_title('Hiệu suất anten theo bán kính', fontsize=10)
        axs[1, 1].set_xlabel('Bán kính anten (m)', fontsize=9)
        axs[1, 1].set_ylabel('Hiệu suất anten', fontsize=9)
        axs[1, 1].grid(True)

        # Đồ thị 5: Mô phỏng Trái Đất - vệ tinh
        earth = plt.Circle((0, 0), R_E, color='blue', alpha=0.3, label='Trái Đất')
        axs[2, 0].add_artist(earth)
        axs[2, 0].plot([0, d * np.cos(np.radians(theta))], [0, d * np.sin(np.radians(theta))], 'r-', label='Đường truyền')
        axs[2, 0].scatter([0, d * np.cos(np.radians(theta))], [0, d * np.sin(np.radians(theta))], color='black', label='Vệ tinh')
        axs[2, 0].set_xlim(-R_E * 1.2, R_E * 1.2)
        axs[2, 0].set_ylim(-R_E * 1.2, (R_E + h) * 1.2)
        axs[2, 0].set_title('Mô phỏng Trái Đất và vệ tinh', fontsize=10)
        axs[2, 0].set_aspect('equal', 'box')
        axs[2, 0].legend(fontsize=8)

        # Ô trống để cân bằng grid
        axs[2, 1].axis('off')

        # Điều chỉnh khoảng cách giữa các đồ thị
        plt.tight_layout()
        plt.show()

    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập đúng định dạng số!")

# Giao diện Tkinter
root = tk.Tk()
root.title("Mô phỏng vệ tinh")

# Các label và entry với giá trị mặc định
default_values = {
    "Bán kính Trái Đất (R_E):": "6371",
    "Chiều cao vệ tinh (h):": "500",
    "Công suất phát (P_tx):": "100",
    "Tần số (f):": "10",
    "Góc ngẩng (theta):": "45",
    "Hệ số suy hao (alpha):": "0.02",
    "Độ cao anten phát (Ha):": "10",
    "Độ cao mưa (H_rain):": "200",
    "Suy hao truyền phát (L_tx):": "2",
    "Suy hao truyền thu (L_rx):": "2",
    "Hiệu suất anten (eta):": "0.6",
    "Đường kính anten phát (D_tx):": "1",
    "Đường kính anten thu (D_rx):": "1"
}

entries = []

for i, (label, default) in enumerate(default_values.items()):
    tk.Label(root, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="w")
    entry = tk.Entry(root)
    entry.insert(0, default)  # Hiển thị giá trị mặc định
    entry.grid(row=i, column=1, padx=5, pady=5)
    entries.append(entry)

# Gán các entry
entry_R_E, entry_h, entry_P_tx, entry_f, entry_theta, entry_alpha, \
entry_Ha, entry_Hrain, entry_L_tx, entry_L_rx, entry_eta, entry_D_tx, entry_D_rx = entries

# Nút tính toán
btn_calculate = tk.Button(root, text="Tính toán và vẽ đồ thị", command=calculate_and_plot)
btn_calculate.grid(row=len(default_values), column=0, columnspan=2, pady=10)

root.mainloop()
