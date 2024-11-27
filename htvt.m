% Thông s? ??u vào
R_E = 6378;  % Bán kính Trái ??t (km)
h = 35786;   % Kho?ng cách t? trái ??t t?i v? tinh (km)
a = input('Nh?p v? ?? tr?m phát Hà N?i (?? B?c): ');  % Nh?p v? ?? tr?m phát Hà N?i
b = input('Nh?p kinh ?? tr?m phát Hà N?i (?? ?ông): '); % Nh?p kinh ?? tr?m phát Hà N?i
f = 6;     % T?n s? truy?n (6 GHz)
R_bit = 8e6; % T?c ?? bit (8 Mbps)
P_tx = input('Nh?p cong suat(db): ');  % Công su?t phát (W)
Ha = 0.1;    % M?c n??c bi?n (m)
H_rain = 5;  % Suy hao m?a (km)
alpha = 3;   % H? s? nhi?u m?a (dB/km)
eta = 0.5;   % Hi?u su?t ?ng-ten
D_tx = 13;   % Bán kính ?ng-ten tr?m phát (m)
D_rx = 4;    % Bán kính ?ng-ten v? tinh (m)
L_tx = 1;  % Suy hao phát (dB)
L_rx = 1;    % Suy hao thu (dB)
%N0 = 10^(-21); % M?t ?? nhi?u (W/Hz)
%B = 8e6;        % B?ng thông (Hz), 8 Mbps = 8 x 10^6 Hz
T = 900;        % Nhiet do tap am (K)
k = 1.38e-23; %h?ng s? bolzmann
%4QAM
M = 4;
% Tính góc phi t? v? ?? và kinh ??
phi_cos = cosd(a) * cosd(b - 132);  % Tính góc phi t? v? ?? và kinh ??

% Tính kho?ng cách d t? tr?m Hà N?i t?i v? tinh
d = sqrt(R_E^2 + (R_E + h)^2 - 2 * R_E * (R_E + h) * phi_cos);  % Kho?ng cách d (km)

% Tính góc ng?ng theta t? cos(phi)
 
theta = 55;  % góc ng?ng 55 ??

% Tính suy hao không gian t? do (Lfs)
Lfs = 92.44 + 20 * log10(d) + 20 * log10(f);

% Tính kho?ng cách hi?u d?ng c?a m?a Dr và suy hao m?a Lrain
Dr = (H_rain - Ha) / sind(theta);  % Kho?ng cách hi?u d?ng c?a m?a (km)
Lrain = alpha * Dr;  % Suy hao m?a (dB)

% Tính t?ng suy hao L
L_total = Lfs + L_tx + Lrain + L_rx;

% Tính các giá tr? c?n thi?t
G_tx = (eta * ((3.14 * D_tx) / (3e8 / (f * 1e9)))^2);  % T?ng ích ?ng-ten phát
G_rx = (eta * ((3.14 * D_rx) / (3e8 / (f * 1e9)))^2);  % T?ng ích ?ng-ten thu
EIRP = 10 * log10(P_tx) + 10 * log10(G_tx) + L_tx;  % Công su?t b?c x? ??ng h??ng

% Tính công su?t nh?n t?i v? tinh (Prx)
P_rx = P_tx + 10 * log10(G_tx) + 10 * log10(G_rx) - L_total ;  % Công su?t nh?n t?i v? tinh

% Tính C/N0 và E_b/N_0
P_N = 10 * log10(k * T);
C_N = P_rx - P_N;
C_N0 = C_N + 10 * log10(R_bit / log2(M));  % Tính C/N0
E_b_N_0 = 10*log10(C_N0) + 10 * log10(8e6);  % Tính E_b/N_0

% In k?t qu?
fprintf('Kho?ng cách t? tr?m Hà N?i t?i v? tinh (d) = %.4f km\n', d);
fprintf('Góc ng?ng (theta) = %.4f ??\n', theta);
fprintf('T?ng ích ?ng-ten phát G_tx = %.4f dB\n',10*log10(G_tx));
fprintf('T?ng ích ?ng-ten thu G_rx = %.4f dB\n', 10*log10(G_rx));
fprintf('Công su?t nh?n t?i v? tinh (Prx) = %.2f dBW\n', 10*log10(P_rx));
fprintf('Công su?t (Pn) = %.2f dBW\n', P_N);
fprintf('T? l? tín hi?u trên nhi?u (C/N) = %.2f dB-Hz\n', C_N);
fprintf('T? l? tín hi?u trên nhi?u (C/N0) = %.2f dB-Hz\n', C_N0);
fprintf('T? s? n?ng l??ng c?a bit/m?t ?? t?p âm (E_b/N_0) = %.2f dB\n', E_b_N_0);
fprintf('Suy hao không gian t? do Lfs = %.4f dB\n', Lfs);
fprintf('Kho?ng cách hi?u d?ng c?a m?a Dr = %.4f km\n', Dr);
fprintf('Suy hao m?a Lrain = %.4f dB\n', Lrain);
fprintf('T?ng suy hao L = %.4f dB\n', L_total);

%---------------------------------------------
% 3. Hình ?nh v? Anten và Góc Xoay
%---------------------------------------------
% T?o hình v? Trái ??t và qu? ??o v? tinh
theta_vals = linspace(0, 2*pi, 100);  % T?o các giá tr? góc ?? v? Trái ??t
x_earth = R_E * cos(theta_vals);  % T?a ?? X c?a Trái ??t
y_earth = R_E * sin(theta_vals);  % T?a ?? Y c?a Trái ??t

theta_orbit = linspace(0, 2*pi, 100);  % T?o các giá tr? góc ?? v? qu? ??o
x_orbit = (R_E + h) * cos(theta_orbit);  % T?a ?? X c?a qu? ??o v? tinh
y_orbit = (R_E + h) * sin(theta_orbit);  % T?a ?? Y c?a qu? ??o v? tinh

% V? hình
figure;
plot(x_earth, y_earth, 'g', 'LineWidth', 2); % Trái ??t
hold on;
plot(x_orbit, y_orbit, 'b--', 'LineWidth', 2); % Qu? ??o v? tinh

% V? góc ng?ng
x_angle = [R_E, (R_E + h) * cosd(theta)];  % V? trí góc ng?ng
y_angle = [0, (R_E + h) * sind(theta)];  % V? trí góc ng?ng
plot(x_angle, y_angle, 'r', 'LineWidth', 2); % Góc ng?ng

xlabel('X (km)', 'FontSize', 12);
ylabel('Y (km)', 'FontSize', 12);
title('Anten và Góc Xoay', 'FontSize', 14);
axis equal;
grid on;
legend('Trái ??t', 'Qu? ??o v? tinh', 'Góc ng?ng', 'Location', 'Best');
set(gca, 'FontSize', 12);

%---------------------------------------------
% 4. Hình ?nh v? Tín hi?u và Nhi?u
%---------------------------------------------
t = 0:1e-6:1e-3; % Th?i gian
signal = sin(2 * pi * 1e6 * t); % Tín hi?u 1 MHz
noise = randn(size(t)); % Nhi?u tr?ng Gaussian

% V? tín hi?u và nhi?u
figure;
subplot(2,1,1);
plot(t, signal, 'b-', 'LineWidth', 1.5);
title('Tín hi?u', 'FontSize', 14);
xlabel('Th?i gian (s)', 'FontSize', 12);
ylabel('Bi?n ??', 'FontSize', 12);
grid on;

subplot(2,1,2);
plot(t, noise, 'r-', 'LineWidth', 1.5);
title('Nhi?u', 'FontSize', 14);
xlabel('Th?i gian (s)', 'FontSize', 12);
ylabel('Bi?n ??', 'FontSize', 12);
grid on;
set(gca, 'FontSize', 12);

%---------------------------------------------
%---------------------------------------------
% 5% Hình ?nh v? T? l? Tín hi?u/Nhi?u (C/N0 và C/N)
%---------------------------------------------
figure;
bar([C_N, C_N0], 'FaceColor', [0.2, 0.6, 0.8]);  % V? bi?u ?? thanh cho giá tr? C/N và C/N0
set(gca, 'xticklabel', {'C/N', 'C/N0'}, 'FontSize', 12);  % G?n nhãn tr?c x
ylabel('T? l? tín hi?u/nhi?u (dB Hz)', 'FontSize', 12);  % G?n nhãn tr?c y
title('T? l? tín hi?u/nhi?u (C/N và C/N0)', 'FontSize', 14);  % Tiêu ?? bi?u ??
grid on;  % Hi?n th? l??i



%---------------------------------------------
% 6. Hình ?nh v? Suy hao tín hi?u
%---------------------------------------------
figure;
bar([Lfs, L_tx, L_rx, Lrain, L_total], 'FaceColor', [0.8, 0.2, 0.2]);
set(gca, 'xticklabel', {'Lfs', 'L_tx', 'L_rx', 'Lrain', 'T?ng suy hao'}, 'FontSize', 12);
ylabel('Suy hao tín hi?u (dB)', 'FontSize', 12);
title('Suy hao tín hi?u', 'FontSize', 14);
grid on;

%---------------------------------------------
% 7. Hình ?nh v? K?t qu? Mô Ph?ng (Bit Error Rate - BER)
%---------------------------------------------
SNR_dB = 0:2:300; % Dãy SNR t? 0 ??n 30 dB
BER = 0.5 * erfc(sqrt(10.^(SNR_dB / 10))); % Công th?c lý thuy?t cho BPSK

figure;
semilogy(SNR_dB, BER, 'b-', 'LineWidth', 2);
xlabel('SNR (dB)', 'FontSize', 12);
ylabel('T? l? l?i bit (BER)', 'FontSize', 12);
title('T? l? l?i bit (BER)', 'FontSize', 14);
grid on;
set(gca, 'FontSize', 12);
