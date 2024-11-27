% Th�ng s? ??u v�o
R_E = 6378;  % B�n k�nh Tr�i ??t (km)
h = 35786;   % Kho?ng c�ch t? tr�i ??t t?i v? tinh (km)
a = input('Nh?p v? ?? tr?m ph�t H� N?i (?? B?c): ');  % Nh?p v? ?? tr?m ph�t H� N?i
b = input('Nh?p kinh ?? tr?m ph�t H� N?i (?? ?�ng): '); % Nh?p kinh ?? tr?m ph�t H� N?i
f = 6;     % T?n s? truy?n (6 GHz)
R_bit = 8e6; % T?c ?? bit (8 Mbps)
P_tx = input('Nh?p cong suat(db): ');  % C�ng su?t ph�t (W)
Ha = 0.1;    % M?c n??c bi?n (m)
H_rain = 5;  % Suy hao m?a (km)
alpha = 3;   % H? s? nhi?u m?a (dB/km)
eta = 0.5;   % Hi?u su?t ?ng-ten
D_tx = 13;   % B�n k�nh ?ng-ten tr?m ph�t (m)
D_rx = 4;    % B�n k�nh ?ng-ten v? tinh (m)
L_tx = 1;  % Suy hao ph�t (dB)
L_rx = 1;    % Suy hao thu (dB)
%N0 = 10^(-21); % M?t ?? nhi?u (W/Hz)
%B = 8e6;        % B?ng th�ng (Hz), 8 Mbps = 8 x 10^6 Hz
T = 900;        % Nhiet do tap am (K)
k = 1.38e-23; %h?ng s? bolzmann
%4QAM
M = 4;
% T�nh g�c phi t? v? ?? v� kinh ??
phi_cos = cosd(a) * cosd(b - 132);  % T�nh g�c phi t? v? ?? v� kinh ??

% T�nh kho?ng c�ch d t? tr?m H� N?i t?i v? tinh
d = sqrt(R_E^2 + (R_E + h)^2 - 2 * R_E * (R_E + h) * phi_cos);  % Kho?ng c�ch d (km)

% T�nh g�c ng?ng theta t? cos(phi)
 
theta = 55;  % g�c ng?ng 55 ??

% T�nh suy hao kh�ng gian t? do (Lfs)
Lfs = 92.44 + 20 * log10(d) + 20 * log10(f);

% T�nh kho?ng c�ch hi?u d?ng c?a m?a Dr v� suy hao m?a Lrain
Dr = (H_rain - Ha) / sind(theta);  % Kho?ng c�ch hi?u d?ng c?a m?a (km)
Lrain = alpha * Dr;  % Suy hao m?a (dB)

% T�nh t?ng suy hao L
L_total = Lfs + L_tx + Lrain + L_rx;

% T�nh c�c gi� tr? c?n thi?t
G_tx = (eta * ((3.14 * D_tx) / (3e8 / (f * 1e9)))^2);  % T?ng �ch ?ng-ten ph�t
G_rx = (eta * ((3.14 * D_rx) / (3e8 / (f * 1e9)))^2);  % T?ng �ch ?ng-ten thu
EIRP = 10 * log10(P_tx) + 10 * log10(G_tx) + L_tx;  % C�ng su?t b?c x? ??ng h??ng

% T�nh c�ng su?t nh?n t?i v? tinh (Prx)
P_rx = P_tx + 10 * log10(G_tx) + 10 * log10(G_rx) - L_total ;  % C�ng su?t nh?n t?i v? tinh

% T�nh C/N0 v� E_b/N_0
P_N = 10 * log10(k * T);
C_N = P_rx - P_N;
C_N0 = C_N + 10 * log10(R_bit / log2(M));  % T�nh C/N0
E_b_N_0 = 10*log10(C_N0) + 10 * log10(8e6);  % T�nh E_b/N_0

% In k?t qu?
fprintf('Kho?ng c�ch t? tr?m H� N?i t?i v? tinh (d) = %.4f km\n', d);
fprintf('G�c ng?ng (theta) = %.4f ??\n', theta);
fprintf('T?ng �ch ?ng-ten ph�t G_tx = %.4f dB\n',10*log10(G_tx));
fprintf('T?ng �ch ?ng-ten thu G_rx = %.4f dB\n', 10*log10(G_rx));
fprintf('C�ng su?t nh?n t?i v? tinh (Prx) = %.2f dBW\n', 10*log10(P_rx));
fprintf('C�ng su?t (Pn) = %.2f dBW\n', P_N);
fprintf('T? l? t�n hi?u tr�n nhi?u (C/N) = %.2f dB-Hz\n', C_N);
fprintf('T? l? t�n hi?u tr�n nhi?u (C/N0) = %.2f dB-Hz\n', C_N0);
fprintf('T? s? n?ng l??ng c?a bit/m?t ?? t?p �m (E_b/N_0) = %.2f dB\n', E_b_N_0);
fprintf('Suy hao kh�ng gian t? do Lfs = %.4f dB\n', Lfs);
fprintf('Kho?ng c�ch hi?u d?ng c?a m?a Dr = %.4f km\n', Dr);
fprintf('Suy hao m?a Lrain = %.4f dB\n', Lrain);
fprintf('T?ng suy hao L = %.4f dB\n', L_total);

%---------------------------------------------
% 3. H�nh ?nh v? Anten v� G�c Xoay
%---------------------------------------------
% T?o h�nh v? Tr�i ??t v� qu? ??o v? tinh
theta_vals = linspace(0, 2*pi, 100);  % T?o c�c gi� tr? g�c ?? v? Tr�i ??t
x_earth = R_E * cos(theta_vals);  % T?a ?? X c?a Tr�i ??t
y_earth = R_E * sin(theta_vals);  % T?a ?? Y c?a Tr�i ??t

theta_orbit = linspace(0, 2*pi, 100);  % T?o c�c gi� tr? g�c ?? v? qu? ??o
x_orbit = (R_E + h) * cos(theta_orbit);  % T?a ?? X c?a qu? ??o v? tinh
y_orbit = (R_E + h) * sin(theta_orbit);  % T?a ?? Y c?a qu? ??o v? tinh

% V? h�nh
figure;
plot(x_earth, y_earth, 'g', 'LineWidth', 2); % Tr�i ??t
hold on;
plot(x_orbit, y_orbit, 'b--', 'LineWidth', 2); % Qu? ??o v? tinh

% V? g�c ng?ng
x_angle = [R_E, (R_E + h) * cosd(theta)];  % V? tr� g�c ng?ng
y_angle = [0, (R_E + h) * sind(theta)];  % V? tr� g�c ng?ng
plot(x_angle, y_angle, 'r', 'LineWidth', 2); % G�c ng?ng

xlabel('X (km)', 'FontSize', 12);
ylabel('Y (km)', 'FontSize', 12);
title('Anten v� G�c Xoay', 'FontSize', 14);
axis equal;
grid on;
legend('Tr�i ??t', 'Qu? ??o v? tinh', 'G�c ng?ng', 'Location', 'Best');
set(gca, 'FontSize', 12);

%---------------------------------------------
% 4. H�nh ?nh v? T�n hi?u v� Nhi?u
%---------------------------------------------
t = 0:1e-6:1e-3; % Th?i gian
signal = sin(2 * pi * 1e6 * t); % T�n hi?u 1 MHz
noise = randn(size(t)); % Nhi?u tr?ng Gaussian

% V? t�n hi?u v� nhi?u
figure;
subplot(2,1,1);
plot(t, signal, 'b-', 'LineWidth', 1.5);
title('T�n hi?u', 'FontSize', 14);
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
% 5% H�nh ?nh v? T? l? T�n hi?u/Nhi?u (C/N0 v� C/N)
%---------------------------------------------
figure;
bar([C_N, C_N0], 'FaceColor', [0.2, 0.6, 0.8]);  % V? bi?u ?? thanh cho gi� tr? C/N v� C/N0
set(gca, 'xticklabel', {'C/N', 'C/N0'}, 'FontSize', 12);  % G?n nh�n tr?c x
ylabel('T? l? t�n hi?u/nhi?u (dB Hz)', 'FontSize', 12);  % G?n nh�n tr?c y
title('T? l? t�n hi?u/nhi?u (C/N v� C/N0)', 'FontSize', 14);  % Ti�u ?? bi?u ??
grid on;  % Hi?n th? l??i



%---------------------------------------------
% 6. H�nh ?nh v? Suy hao t�n hi?u
%---------------------------------------------
figure;
bar([Lfs, L_tx, L_rx, Lrain, L_total], 'FaceColor', [0.8, 0.2, 0.2]);
set(gca, 'xticklabel', {'Lfs', 'L_tx', 'L_rx', 'Lrain', 'T?ng suy hao'}, 'FontSize', 12);
ylabel('Suy hao t�n hi?u (dB)', 'FontSize', 12);
title('Suy hao t�n hi?u', 'FontSize', 14);
grid on;

%---------------------------------------------
% 7. H�nh ?nh v? K?t qu? M� Ph?ng (Bit Error Rate - BER)
%---------------------------------------------
SNR_dB = 0:2:300; % D�y SNR t? 0 ??n 30 dB
BER = 0.5 * erfc(sqrt(10.^(SNR_dB / 10))); % C�ng th?c l� thuy?t cho BPSK

figure;
semilogy(SNR_dB, BER, 'b-', 'LineWidth', 2);
xlabel('SNR (dB)', 'FontSize', 12);
ylabel('T? l? l?i bit (BER)', 'FontSize', 12);
title('T? l? l?i bit (BER)', 'FontSize', 14);
grid on;
set(gca, 'FontSize', 12);
