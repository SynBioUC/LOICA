class TU:
    def __init__(self, input, output, a, b, K, n):
        self.input = input
        self.output = output
        self.a = a
        self.b = b
        self.K = K
        self.n = n 


class RepressibleRepressor(TU):
    def __init__(self, input, output, a, b, K, n):
        super().__init__(input, output, a, b, K, n)
        #self.formula = ((self.a + self.b (self.input.concentration/self.K)**self.n)/(1 + (self.input.concentration/self.K)**self.n)) #se puede cambiar la forma de definir expression_rate

    def expression_rate(self):
        input_repressor = self.input.concentration
        r = (input_repressor/self.K)**self.n
        expression_rate = ( self.a + self.b*r ) / (1 + r)
        return expression_rate



class InducibleInductor(TU):
    '''
​    Most inducers works in a receptor AND chemical logic, try to incorporate that.
​    If no receptor quantity is given, use max as default.
​    '''
    def __init__(self, input, output, a, b, K, n):
        super().__init__(input, output, a, b, K, n)
        self.formula = '(self.b + (self.a * (self.input.concentration ** self.n / (self.input.concentration ** self.n + self.K ** self.n))))'

    def expression_rate(self):
        expression_rate = (self.b + (self.a * (self.input.concentration ** self.n / (self.input.concentration ** self.n + self.K ** self.n))))
        return expression_rate

