import numpy as np


class Metabolism:
    def __init__(self):
        pass

    @classmethod
    def gompertz_growth_rate(cls, t=0, y0=0.01, ymax=1, um=1, l=4):
        A = np.log(ymax/y0)
        gr = um *np.exp((np.exp(1)* um *(l - t))/A - \
            np.exp((np.exp(1)* um *(l - t))/A + 1) + 2)
        return(gr)

    @classmethod
    def gompertz(cls, t=0, y0=0.01, ymax=1, um=1, l=4):
        A = np.log(ymax/y0)
        log_rel_od = (A*np.exp(-np.exp((((um*np.exp(1))/A)*(l-t))+1)))
        od = y0 * np.exp(log_rel_od)
        return(od)

    @classmethod
    def profile(cls, biomass= gompertz, gr= gompertz_growth_rate, t=0):
        return gr * 10 + 1


class SimulatedMetabolism(Metabolism):
    def __init__(self, biomass_func, growth_rate_func, profile_func):
        super().__init__()
        self.biomass_func = biomass_func
        self.growth_rate_func = growth_rate_func
        self.profile_func = profile_func

    def biomass(self, t):
        return self.biomass_func(t)

    def growth_rate(self, t):
        return self.growth_rate_func(t)

    def profile(self, t):
        gr = self.growth_rate(t)
        b = self.biomass(t)
        return self.profile_func(b, gr, t)
'''
class SimulatedMetabolism(Metabolism):
    def __init__(self, biomass_func, growth_rate_func, profile_func):
        super().__init__()
        if biomass_func == 'gompertz':
            self.biomass_func = Metabolism.gompertz(t)
        else: self.biomass_func = biomass_func
        if growth_rate_func == 'gompertz_gr':
            self.growth_rate_func = Metabolism.gompertz_growth_rate(t)
        else: self.growth_rate_func = growth_rate_func
        if profile_func == 'basic':
            self.profile_func = Metabolism.profile(t)
        else: self.profile_func = profile_func


    def biomass(self, t):
        return self.biomass_func(t)

    def growth_rate(self, t):
        return self.growth_rate_func(t)

    def profile(self, t):
        gr = self.growth_rate(t)
        b = self.biomass(t)
        return self.profile_func(b, gr, t)

'''