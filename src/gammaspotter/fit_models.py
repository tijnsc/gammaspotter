import numpy as np


class FitModels:
    def gaussian(x, amp, cen, wid, startheight):
        return (amp / (np.sqrt(2 * np.pi) * wid)) * np.exp(
            -((x - cen) ** 2) / (2 * wid**2)
        ) + startheight

    def lorenzian(x, amp, cen, wid, startheight):
        return (amp / np.pi) * (wid / ((x - cen) ** 2 + wid**2)) + startheight
