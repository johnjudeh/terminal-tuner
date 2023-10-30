# This is the start of the approach to implement Harmonic Product Spectrum
# Does not work yet!

import numpy as np


def _calculate_harmonic_product_spectrum(data: np.ndarray, N: int = 1) -> np.ndarray:
    for n in range(N):
        data = data * (data / (n + 1))
    return data


def _find_fundamental_frequency(x_freq: np.ndarray, y_freq: np.ndarray) -> float:
    harmonic_product_spectrum = _calculate_harmonic_product_spectrum(y_freq)
    max_value_index = np.argmax(harmonic_product_spectrum)
    # plot_dft(x_freq, harmonic_product_spectrum)
    return x_freq[max_value_index]
