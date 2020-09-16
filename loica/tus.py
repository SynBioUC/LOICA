class TU:
    def __init__(self, a, b, K, n):
        self.a = a
        self.b = b
        self.K = K
        self.n = n 

    def output(self, inputs, dt):
        return 0


class RepressibleRepressor(TU):
    def __init__(self, a, b, K, n):
        super().__init__(a, b, K, n)
        self.formula = '(a + b(Q/K)**n)/(1 + (Q/K)n)'

    def output(self, input_repressor, dt):
        r = (input_repressor/self.K)**self.n
        expression_rate = ( self.a + self.b*r ) / (1 + r)
        return expression_rate



class InducibleInductor(TU):
    '''
​    Most inducers works in a receptor AND chemical logic, try to incorporate that.
​    If no receptor quantity is given, use max as default.
​    '''
    def __init__(self, a, b, K, n):
        super().__init__(a, b, K, n)
        self.formula = 'b + (a * (Q**n/(Q**n + K**n)))'

    def output(self, input_inductor, dt):
        expression_rate = (self.b + (self.a * (input_inductor ** self.n / (input_inductor ** self.n + self.K ** self.n))))
        return expression_rate

