# Generate fading channel
def generate_channel(num_samples, fading_type="rayleigh", sigma=1):
    if fading_type == "rayleigh":
        return np.random.rayleigh(sigma, num_samples)
    elif fading_type == "lognormal":
        return np.random.lognormal(mean=0, sigma=sigma, size=num_samples)
    elif fading_type == "rician":
        K = 100  # Rician K-factor
        s = np.sqrt(K / (K + 1))  # LOS component
        sigma = np.sqrt(1 / (K + 1))  # NLOS component
        return np.sqrt((np.random.normal(s, sigma, num_samples))**2 +
                       (np.random.normal(0, sigma, num_samples))**2)
    else:
        raise ValueError("Unsupported fading type.")
