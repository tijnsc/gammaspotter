from numpy import exp, pi


class FitModels:
    def gaussian(x, amp, cen, wid, startheight):
        return amp * exp(-((x - cen) ** 2) / (2 * wid**2)) + startheight

    def lorenzian(x, amp, cen, wid, startheight):
        return (amp / pi) * (wid / ((x - cen) ** 2 + wid**2)) + startheight
