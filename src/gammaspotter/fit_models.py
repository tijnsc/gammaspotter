from numpy import exp, pi, sqrt


class FitModels:
    def gaussian(x, amp, cen, wid, startheight):
        """1-d gaussian: gaussian(x, amp, cen, wid)"""
        return (amp / (sqrt(2 * pi) * wid)) * exp(
            -((x - cen) ** 2) / (2 * wid**2)
        ) + startheight

    def lorenzian(x, amp, cen, wid, startheight):
        return (amp / pi) * (wid / ((x - cen) ** 2 + wid**2)) + startheight
