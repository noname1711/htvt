% Thông số đầu vào
R_E = 6378;  % Bán kính Trái Đất (km)
h = 35786;   % Khoảng cách từ Trái Đất tới vệ tinh (km)
a = input('Nhập vĩ độ trạm phát Hà Nội (độ Bắc): ');  % Nhập vĩ độ trạm phát
b = input('Nhập kinh độ trạm phát Hà Nội (độ Đông): '); % Nhập kinh độ trạm phát
f = 6;       % Tần số truyền (GHz)
R_bit = 8e6; % Tốc độ bit (8 Mbps)
P_tx = input('Nhập công suất phát (W): ');  % Công suất phát (W)
Ha = 0.1;    % Mực nước biển (km)
H_rain = 5;  % Chiều cao tầng mưa (km)
alpha = 3;   % Hệ số suy hao mưa (dB/km)
eta = 0.5;   % Hiệu suất anten
D_tx = 13;   % Đường kính anten trạm phát (m)
D_rx = 4;    % Đường kính anten vệ tinh (m)
L_tx = 1;    % Suy hao trạm phát (dB)
L_rx = 1;    % Suy hao thu (dB)
T = 900;     % Nhiệt độ tạp âm (K)
k = 1.38e-23; % Hằng số Boltzmann
M = 4;       % Số mức tín hiệu cho 4-QAM

% Tính khoảng cách từ trạm Hà Nội tới vệ tinh
phi_cos = cosd(a) * cosd(b - 132);  % Góc cos giữa trạm và vệ tinh
d = sqrt(R_E^2 + (R_E + h)^2 - 2 * R_E * (R_E + h) * phi_cos);  % Khoảng cách d (km)

% Tính góc ngẩng
theta = asind((R_E + h) * sind(55) / d);  % Tính góc ngẩng (độ)

% Tính suy hao không gian tự do (Lfs)
Lfs = 92.44 + 20 * log10(d) + 20 * log10(f);

% Tính khoảng cách hiệu dụng của mưa Dr và suy hao mưa Lrain
Dr = (H_rain - Ha) / sind(theta);  % Khoảng cách hiệu dụng của mưa (km)
Lrain = alpha * Dr;  % Suy hao mưa (dB)

% Tổng suy hao
L_total = Lfs + L_tx + Lrain + L_rx;

% Tính cường độ tín hiệu anten
G_tx = 10 * log10(eta * (pi * D_tx * f / (3e8))^2);  % Tăng ích anten phát (dB)
G_rx = 10 * log10(eta * (pi * D_rx * f / (3e8))^2);  % Tăng ích anten thu (dB)

% Tính công suất nhận tại vệ tinh (Prx)
EIRP = 10 * log10(P_tx) + G_tx;  % Công suất bức xạ đẳng hướng hiệu dụng
P_rx = EIRP + G_rx - L_total;   % Công suất nhận tại vệ tinh (dBW)

% Tính tỷ số C/N và C/N0
P_N = 10 * log10(k * T);  % Công suất tạp âm (dBW)
C_N = P_rx - P_N;         % Tỷ số tín hiệu trên nhiễu (dB)
C_N0 = C_N - 10 * log10(R_bit);  % Tỷ số tín hiệu trên tạp âm đơn vị băng thông (dB-Hz)
E_b_N0 = C_N0 - 10 * log10(R_bit / log2(M));  % Tỷ số năng lượng bit trên tạp âm (dB)

% In kết quả
fprintf('Khoảng cách từ trạm Hà Nội tới vệ tinh (d) = %.4f km\n', d);
fprintf('Góc ngẩng (theta) = %.4f độ\n', theta);
fprintf('Tăng ích anten phát (G_tx) = %.4f dB\n', G_tx);
fprintf('Tăng ích anten thu (G_rx) = %.4f dB\n', G_rx);
fprintf('Công suất nhận tại vệ tinh (Prx) = %.4f dBW\n', P_rx);
fprintf('Công suất tạp âm (P_N) = %.4f dBW\n', P_N);
fprintf('Tỷ số tín hiệu trên nhiễu (C/N) = %.4f dB\n', C_N);
fprintf('Tỷ số tín hiệu trên tạp âm đơn vị băng thông (C/N0) = %.4f dB-Hz\n', C_N0);
fprintf('Tỷ số năng lượng bit trên tạp âm (E_b/N_0) = %.4f dB\n', E_b_N0);

% Các đồ thị mô phỏng
% Đồ thị trái đất và vệ tinh
theta_vals = linspace(0, 2 * pi, 100);
x_earth = R_E * cos(theta_vals);
y_earth = R_E * sin(theta_vals);

x_orbit = (R_E + h) * cos(theta_vals);
y_orbit = (R_E + h) * sin(theta_vals);

figure;
plot(x_earth, y_earth, 'g', 'LineWidth', 2);
hold on;
plot(x_orbit, y_orbit, 'b--', 'LineWidth', 2);
plot([0, (R_E + h) * cosd(theta)], [0, (R_E + h) * sind(theta)], 'r', 'LineWidth', 2);
legend('Trái Đất', 'Quỹ đạo vệ tinh', 'Góc ngẩng');
grid on;
axis equal;
xlabel('X (km)');
ylabel('Y (km)');
title('Trái Đất và Quỹ đạo vệ tinh');
