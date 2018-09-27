class Virus(object):
    '''
     Once instantiated by the user, the virus object will be used in the stimulation
     to predict and test the effects of a virus on a specific population size.
     _____Attributes_____
     virus_name: String. virus name
     mortality_rate: Float. Is fatality percentage of the virus
     reproductive_rate: Float. Is the rate of contagiousness of a virus
    '''

    def __init__(self, name, mortality_rate, repro_num):
        self.name = name
        self.mortality_rate = mortality_rate
        self.repro_num = repro_num
