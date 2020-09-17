import pandas as pd
import numpy as np
from . import genetic_network, metabolism



class Assay:
    def __init__(self, 
            samples, 
            n_measurements, 
            interval,
            name='Loica assay',
            description='',
            biomass_signal_id=None
            ):
        '''
        Assay measures a set of samples in parallel at a set of timepoints
        Connects to flapjack to generate data, and to fit parameters to data

        '''
        self.samples = samples
        self.n_measurements = n_measurements
        self.interval = interval
        self.measurements = pd.DataFrame()
        self.name = name
        self.description = description
        self.biomass_signal_id = biomass_signal_id

    def run(self, substeps=10):
        '''
        Run the assay measuring at specified time points, with simulation time step dt
        '''
        #substeps = self.interval / dt
        dt = self.interval / substeps
        for sample_id, sample in enumerate(self.samples):
            # Integrate models
            for t in range(self.n_measurements):
                for tt in range(substeps):
                    time = t * self.interval + tt * dt
                    sample.step(time, dt)
                # Record measurements of fluorescence
                for reporter in sample.reporters:
                    sig = reporter.concentration
                    signal_id = reporter.signal_id
                    signal_name = reporter.name
                    row = {
                            'Time': time, 
                            'Signal_id': signal_id, 
                            'Signal':signal_name, 
                            'Measurement': sig * sample.biomass, 
                            'Sample':sample_id
                            }
                    self.measurements = self.measurements.append(row, ignore_index=True)
                # Record measurement of biomass
                row = {
                        'Time': time, 
                        'Signal_id': self.biomass_signal_id, 
                        'Measurement': sample.biomass, 
                        'Signal':'Biomass', 
                        'Sample':sample_id
                        }
                self.measurements = self.measurements.append(row, ignore_index=True)
                
    def upload(self, flapjack, study):
        assay = flapjack.create('assay', 
                                    name=self.name, 
                                    study=study, 
                                    temperature=0, 
                                    machine='Loica',
                                    description=self.description)
        for row,sample in enumerate(self.samples):
            fj_sample = flapjack.create('sample',
                                row=row, col=1,
                                media=sample.media,
                                strain=sample.strain,
                                vector=sample.vector,
                                assay=assay.id[0],
                                )
            for signal_id,data in self.measurements.groupby('Signal'):
                if signal_id:
                    sig = flapjack.get('signal', id=signal_id)
                    flapjack.upload_measurements(data, signal=sig.id, sample=fj_sample.id)

