import tkinter as tk
from tkinter import messagebox
import numpy as np
from scipy.special import erfc
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def calculate():
    error_messages = []
    try:
        # Lấy giá trị từ các trường nhập liệu
        a = float(entry_lat.get())  # Vĩ độ
        b = float(entry_lon.get())  # Kinh độ
        P_tx = float(entry_power.get())  # Công suất (W)

        if not (-90 <= a <= 90): 
            error_messages.append("Vĩ độ phải trong khoảng từ -90 đến 90 độ.") 
        if not (-180 <= b <= 180): 
            error_messages.append("Kinh độ phải trong khoảng từ -180 đến 180 độ.") 
        if P_tx <= 0: 
            error_messages.append("Công suất phải là giá trị dương.") 
        if error_messages: 
            raise ValueError("\n".join(error_messages))

        # Hằng số
        R_E = 6378  # Bán kính Trái Đất (km)
        h = 35786   # Khoảng cách từ Trái Đất đến vệ tinh (km)
        f = 6       # Tần số (GHz)
        R_bit = 8e6  # Tốc độ bit (8 Mbps)
        Ha = 0.1     # Mực nước biển (km)
        H_rain = 5   # suy hao do mưa (km)
        alpha = 3    # Hệ số nhiễu do mưa (dB/km) ở VNVN
        eta = 0.6    # Hiệu suất anten
        D_tx = 13    # Đường kính anten truyền (m)
        D_rx = 4     # Đường kính anten nhận (m)
        L_tx = 1     # Mất mát truyền (dB)
        L_rx = 1     # Mất mát nhận (dB)
        T = 290      # Nhiệt độ (K)
        k = 1.38e-23 # Hằng số Boltzmann (J/K)
        M = np.random.choice([2, 4, 8]) # Mô-đun là giá trị ngẫu nhiên
    
        # băng thông
        B = R_bit / np.log2(M)        

        # Tính toán cosine của góc
        phi_cos = np.cos(np.radians(a)) * np.cos(np.radians(b - 132))

        # Tính khoảng cách d (km)
        d = np.sqrt(R_E**2 + (R_E + h)**2 - 2 * R_E * (R_E + h) * phi_cos)

        # Góc ngẩng (theta)
        theta = 55  # Góc ngẩng tính bằng độ

        # Mất mát đường truyền tự do (Lfs)
        Lfs = 92.44 + 20 * np.log10(d) + 20 * np.log10(f)

        # Tính khoảng cách mưa hiệu quả (Dr)
        Dr = (H_rain - Ha) / np.sin(np.radians(theta))

        # Tính mất mát mưa (Lrain)
        Lrain = alpha * Dr

        # Tổng mất mát (L_total)
        L_total = Lfs + L_tx + Lrain + L_rx

        # Lợi ích anten
        G_tx = eta * ((np.pi * D_tx) / (3e8 / (f * 1e9)))**2
        G_rx = eta * ((np.pi * D_rx) / (3e8 / (f * 1e9)))**2

        # EIRP (Công suất phát sóng hiệu dụng toàn hướng)
        EIRP = 10 * np.log10(P_tx) + 10 * np.log10(G_tx) + L_tx

        # Công suất nhận tại vệ tinh (P_rx)
        P_rx = 10 * np.log10(P_tx) + 10 * np.log10(G_tx) + 10 * np.log10(G_rx) - L_total

        # Công suất nhiễu (Pn)
        P_N = 10 * np.log10(k * T* B)

        # Tỷ lệ mang trên nhiễu (C/N) và tỷ lệ mang trên mật độ nhiễu (C/N0)
        C_N = P_rx - P_N
        C_N0 = C_N + 10 * np.log10(R_bit / np.log2(M))

        # E_b/N_0 (Tỷ lệ năng lượng trên bit so với mật độ nhiễu)
        E_b_N_0 = 10 * np.log10(C_N0) + 10 * np.log10(R_bit)

        # Hiển thị kết quả lên giao diện
        result_text = f"""
        Kênh truyền M = {M} 
        Khoảng cách từ trạm Hà Nội tới vệ tinh (d) = {d:.4f} km
        Góc ngẩng (theta) = {theta:.4f} deg
        Tăng ích anten phát G_tx = {10 * np.log10(G_tx):.4f} dB
        Tăng ích anten thu G_rx = {10 * np.log10(G_rx):.4f} dB
        Công suất bức xạ đẳng hướng tương đương (EIRP) = {EIRP:.4f} dBW 
        Công suất nhận từ vệ tinh (P_rx) = {P_rx:.4f} dBW
        Công suất (Pn) = {P_N:.4f} dBW
        Tổng tỉ lệ tín hiệu trên nhiễu (C/N) = {C_N:.4f} dB-Hz
        Tổng tỉ lệ tín hiệu trên mật độ nhiễu (C/N0) = {C_N0:.4f} dB-Hz
        Tỉ số năng lượng của bit/một tạp âm (E_b/N_0) = {E_b_N_0:.4f} dB
        Suy hao không gian tự do Lfs = {Lfs:.4f} dB
        Khoảng cách hiệu dụng của máy Dr = {Dr:.4f} km
        Suy hao mưa Lrain = {Lrain:.4f} dB
        Tổng suy hao L = {L_total:.4f} dB
        """
        label_result.config(text=result_text)

        # Gọi các hàm vẽ đồ thị
        plot_planet_antenna(R_E, h, theta)
        plot_signal_noise()  
        plot_signal_noise_ratio(C_N, C_N0)  
        plot_signal_loss(Lfs, L_tx, L_rx, Lrain, L_total)  
        #plot_bit_error_rate(C_N)  
        plot_combined_BER()

    except ValueError as ve :
        messagebox.showerror("Lỗi", str(ve))

# Hàm vẽ đồ thị hành tinh và anten
def plot_planet_antenna(R_E, h, theta): 
    fig, ax = plt.subplots() #khởi tạo biểu đồ và trục
    # Tạo dữ liệu quỹ đạo của Trái đất và vệ tinh 
    theta_vals = np.linspace(0, 2 * np.pi, 100)  #0 -> 2pi
    #tọa độ x, y của quỹ đạo trái đất
    earth_orbit_x = R_E * np.cos(theta_vals) 
    earth_orbit_y = R_E * np.sin(theta_vals) 
    #tọa độ x, y của vệ tinh
    satellite_orbit_x = (R_E + h) * np.cos(theta_vals) 
    satellite_orbit_y = (R_E + h) * np.sin(theta_vals) 
    
    # Vẽ Trái đất và quỹ đạo vệ tinh 
    ax.plot(earth_orbit_x, earth_orbit_y, 'g', label="Trái đất", linewidth=2) 
    ax.plot(satellite_orbit_x, satellite_orbit_y, 'b--', label="Quỹ đạo vệ tinh", linewidth=2) 
    # Vẽ góc ngẩng 
    x_angle = [R_E, (R_E + h) * np.cos(np.radians(theta))] 
    y_angle = [0, (R_E + h) * np.sin(np.radians(theta))] 
    #x-angle, y_angle là tọa độ của đường thẳng từ trái đất đến vệ tinh -> góc ngẩng

    ax.plot(x_angle, y_angle, 'r', label="Góc ngẩng", linewidth=2) 
    # Thiết lập các thông số đồ thị 
    ax.set_xlabel("X (km)", fontsize=12) 
    ax.set_ylabel("Y (km)", fontsize=12) 
    ax.set_title("Anten và Góc Xoay", fontsize=14) 
    ax.axis('equal') # tỉ lệ 2 trục = nhaunhau
    ax.grid(True) #đồ thị có lướilưới
    ax.legend(loc='best', fontsize=10) #Thêm chú thích với kích thước phông chữ 10 và đặt vị trí tốt nhất.
    ax.tick_params(axis='both', which='major', labelsize=12) #Thiết lập thông số cho các vạch chia trên trục.

    top = tk.Toplevel(root) #tạo cửa sổ con mới
    top.title("Hành tinh và Anten") 
    canvas = FigureCanvasTkAgg(fig, master=top) 
    canvas.draw()
    canvas.get_tk_widget().pack()

# Hàm vẽ đồ thị tín hiệu, nhiễu và kênh truyền (AWGN)
def plot_signal_noise():
    t = np.arange(0, 1e-3, 1e-6)  # mảng thời gian
    signal = np.sin(2 * np.pi * 1e6 * t)  # Tín hiệu 1 MHz hình sin

    # Nhiễu Gaussian (AWGN)
    noise = np.random.normal(0, 0.5, len(t))  # Nhiễu Gauss có mean = 0 và std = 0.5

    # Kênh truyền (cộng nhiễu vào tín hiệu)
    noisy_signal = signal + noise  # Tín hiệu cộng nhiễu

    fig, axs = plt.subplots(3, 1, figsize=(10, 10))  # 3 hàng 1 cột
    axs[0].plot(t, signal, 'b-', linewidth=1.5, label="Tín hiệu gốc")
    axs[0].set_title('Tín hiệu', fontsize=14)
    axs[0].set_xlabel('Thời gian (s)', fontsize=12)
    axs[0].set_ylabel('Biên độ', fontsize=12)
    axs[0].grid(True)
    axs[0].legend()

    axs[1].plot(t, noise, 'r-', linewidth=1.5, label="Nhiễu Gauss")
    axs[1].set_title('Nhiễu Gaussian', fontsize=14)
    axs[1].set_xlabel('Thời gian (s)', fontsize=12)
    axs[1].set_ylabel('Biên độ', fontsize=12)
    axs[1].grid(True)
    axs[1].legend()

    axs[2].plot(t, noisy_signal, 'g-', linewidth=1.5, label="Tín hiệu + Nhiễu")
    axs[2].set_title('Tín hiệu sau khi truyền qua kênh (AWGN)', fontsize=14)
    axs[2].set_xlabel('Thời gian (s)', fontsize=12)
    axs[2].set_ylabel('Biên độ', fontsize=12)
    axs[2].grid(True)
    axs[2].legend()

    plt.tight_layout()  # tránh chồng lấn
    top = tk.Toplevel(root)
    top.title("Tín hiệu, Nhiễu và Kênh Truyền")
    canvas = FigureCanvasTkAgg(fig, master=top)
    canvas.draw()
    canvas.get_tk_widget().pack()


# Hàm vẽ đồ thị tỉ lệ tín hiệu/nhiễu (C/N0)
def plot_signal_noise_ratio(C_N, C_N0):
    fig, ax = plt.subplots(figsize=(10, 6)) 
    ax.bar(['C/N', 'C/N0'], [C_N, C_N0], color=[(0.2, 0.6, 0.8)]) 
    ax.set_ylabel('Tỷ lệ tín hiệu (dB Hz)', fontsize=12) 
    ax.set_title('Tỷ lệ tín hiệu (C/N và C/N0)', fontsize=14) 
    ax.grid(True) 

    top = tk.Toplevel(root) 
    top.title("Tỷ lệ tín hiệu (C/N và C/N0)") 
    canvas = FigureCanvasTkAgg(fig, master=top) 
    canvas.draw()
    canvas.get_tk_widget().pack()

# Hàm vẽ đồ thị suy hao tín hiệu
def plot_signal_loss(Lfs, L_tx, L_rx, Lrain, L_total):
    fig, ax = plt.subplots(figsize=(10, 6)) 
    ax.bar(['Lfs', 'L_tx', 'L_rx', 'Lrain', 'Tổng suy hao'], [Lfs, L_tx, L_rx, Lrain, L_total], color=[(0.8, 0.2, 0.2)]) 
    ax.set_ylabel('Suy hao (dB)', fontsize=12) 
    ax.set_title('Suy hao', fontsize=14) 
    ax.grid(True) 
    
    top = tk.Toplevel(root) 
    top.title("Suy hao") 
    canvas = FigureCanvasTkAgg(fig, master=top) 
    canvas.draw() 
    canvas.get_tk_widget().pack()

# Hàm vẽ đồ thị tỷ lệ lỗi bit (BER)
def plot_bit_error_rate(C_N):
    if C_N > 0:  
        SNR_dB = np.linspace(0, 50, 100)  # Tạo một dãy SNR từ 0 đến 550 dB với 100 giá trị
        BER = 0.5 * erfc(np.sqrt(10**(SNR_dB / 10)))  # Công thức lý thuyết cho BPSK BER

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.semilogy(SNR_dB, BER, 'b-', linewidth=2)  #trục y logarit
        ax.set_title('Tỷ lệ lỗi bit (BER) đối với các giá trị SNR', fontsize=14)
        ax.set_xlabel('SNR (dB)', fontsize=12)
        ax.set_ylabel('Tỷ lệ lỗi bit (BER)', fontsize=12)
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)

        top = tk.Toplevel(root)
        top.title("Bit Error Rate (BER)")
        canvas = FigureCanvasTkAgg(fig, master=top)
        canvas.draw()
        canvas.get_tk_widget().pack()
    else:
        messagebox.showwarning("Cảnh báo", "C_N phải là một giá trị hợp lệ và dương.")

# Hàm vẽ đồ thị tỷ lệ lỗi bit (BER) lý thuyết
def plot_bit_error_rate_theory():
    SNR_dB = np.linspace(0, 20, 50)  # Tạo một dãy SNR từ 0 đến 20 dB
    BER_theory = 0.5 * erfc(np.sqrt(10**(SNR_dB / 10)))  # Công thức lý thuyết cho BPSK BER
    return SNR_dB, BER_theory
# Hàm mô phỏng kênh truyền với nhiễu Gaussian và tính BER thực tế
def simulate_BER_with_noise(SNR_dB, num_bits=10000):
    noise_std = np.sqrt(1 / (2 * 10**(SNR_dB / 10)))  # Độ lệch chuẩn của nhiễu Gaussian
    # Sinh ra tín hiệu BPSK (0 -> -1, 1 -> 1)
    transmitted_bits = np.random.randint(0, 2, num_bits) * 2 - 1  # Tạo mảng bit (-1 và 1)
    # Thêm nhiễu Gaussian vào tín hiệu
    noise = np.random.normal(0, noise_std, num_bits)
    received_signal = transmitted_bits + noise  # Tín hiệu nhận được sau khi thêm nhiễu
    # Phục hồi bit từ tín hiệu nhận được
    received_bits = (received_signal >= 0).astype(int)  # Bit 1 nếu tín hiệu >= 0, ngược lại bit 0
    # Tính số bit bị lỗi
    errors = np.sum(transmitted_bits != (received_bits * 2 - 1))  # Số lỗi bit
    BER = errors / num_bits  # Tỷ lệ lỗi bit thực tế
    return BER
# Hàm vẽ đồ thị BER lý thuyết và thực tế
def plot_combined_BER():
    SNR_dB = np.linspace(0, 20, 100)    # Tạo một dãy SNR từ 0 đến 20 dB với 100 giá trị
    # Tính toán BER lý thuyết
    SNR_theory, BER_theory = plot_bit_error_rate_theory()
    # Tính toán BER thực tế cho từng giá trị SNR
    BER_simulated = [simulate_BER_with_noise(snr) for snr in SNR_dB]
    # Vẽ đồ thị
    fig, ax = plt.subplots(figsize=(10, 6))
    # Vẽ đồ thị lý thuyết
    ax.semilogy(SNR_theory, BER_theory, 'b-', linewidth=2, label="BER lý thuyết")
    # Vẽ đồ thị thực tế
    ax.semilogy(SNR_dB, BER_simulated, 'r-', linewidth=2, label="BER thực tế")
    # Tùy chỉnh đồ thị
    ax.set_title('Tỷ lệ lỗi bit (BER) lý thuyết và thực tế theo SNR', fontsize=14)
    ax.set_xlabel('SNR (dB)', fontsize=12)
    ax.set_ylabel('Tỷ lệ lỗi bit (BER)', fontsize=12)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.legend()
    # Hiển thị đồ thị trong cửa sổ Tkinter
    top = tk.Toplevel(root)
    top.title("Bit Error Rate (BER) - Lý thuyết và Thực tế")
    canvas = FigureCanvasTkAgg(fig, master=top)
    canvas.draw()
    canvas.get_tk_widget().pack()

root = tk.Tk()
root.title("Tính toán")

label_lat = tk.Label(root, text="Nhập vĩ độ trạm phát (độ):")
label_lat.grid(row=0, column=0, padx=10, pady=10)
entry_lat = tk.Entry(root)
entry_lat.grid(row=0, column=1, padx=10, pady=10)

label_lon = tk.Label(root, text="Nhập kinh độ trạm phát (độ):")
label_lon.grid(row=1, column=0, padx=10, pady=10)
entry_lon = tk.Entry(root)
entry_lon.grid(row=1, column=1, padx=10, pady=10)

label_power = tk.Label(root, text="Nhập công suất (W):")
label_power.grid(row=2, column=0, padx=10, pady=10)
entry_power = tk.Entry(root)
entry_power.grid(row=2, column=1, padx=10, pady=10)

button_calculate = tk.Button(root, text="Tính toán", command=calculate)
button_calculate.grid(row=3, column=0, columnspan=2, pady=20)

label_result = tk.Label(root, text="", justify=tk.LEFT)
label_result.grid(row=4, column=0, columnspan=2, padx=10, pady=10)


root.mainloop()
