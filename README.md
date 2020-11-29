# LOICA
Logical Operators for Intelligent Cell Algorithms

## High level idea

Compile Code into DNA fragments that execute Cell Algorithms

Easy progamation of genetic network models

Generation of synthetic data

Generation of Human/Machine readable protocols for DNA assembly

Communication with FlapJack

Use and output SBOL/SBML

Use all sorts of cellular computation

Easy, fluid and customisable DNA design


## Usage

### Repressilator

Get or Create FlapJack parts for IDs

```python
dna = fj.get('dna', name='Rep')
if len(dna)==0:
    dna = fj.create('dna', name='Rep')
    
vector = fj.get('vector', name='Rep')    
if len(vector)==0:
    vector = fj.create('vector', name='Rep', dnas=dna.id)
    
cfp = fj.get('signal', name='CFP')

yfp = fj.get('signal', name='YFP')

rfp = fj.get('signal', name='RFP')

media = fj.get('media', name='Loica')
if len(media)==0:
    media = fj.create('media', name='Loica', description='Simulated loica media')
    
strain = fj.get('strain', name='Loica strain')
if len(strain)==0:
    strain = fj.create('strain', name='Loica strain', description='Loica test strain')

biomass_signal = fj.get('signal', name='OD')
```

Create a GeneticNetwork for the Repressilator(rep)

Create and add Regulators (laci, tetr and ci)

Create and add Reporters (CFP, YFP, RFP)

Create and add Operators (Not)

```python
rep = GeneticNetwork(vector=vector.id[0])

laci = Regulator(name='LacI', degradation_rate=1, init_concentration=5)
tetr = Regulator(name='TetR', degradation_rate=1)
ci = Regulator(name='cI', degradation_rate=1)
rep.add_regulators([laci, tetr, ci])

cfp = Reporter(name='CFP', degradation_rate=1, signal_id=cfp.id[0])
yfp = Reporter(name='YFP', degradation_rate=1, signal_id=yfp.id[0])
rfp = Reporter(name='RFP', degradation_rate=1, signal_id=rfp.id[0])
rep.add_reporters([cfp, yfp, rfp])

pCi_laci = Not(input=ci, output=laci, a=100, b=0, K=1, n=2)
pLac_tetr = Not(input=laci, output=tetr, a=100, b=0, K=1, n=2)
pTet_ci = Not(input=tetr, output=ci, a=100, b=0, K=1, n=2)
rep.add_operators([pCi_laci, pLac_tetr, pTet_ci])

pCi_cfp = Not(input=ci, output=cfp, a=100, b=0, K=1, n=2)
pLac_yfp = Not(input=laci, output=yfp, a=100, b=0, K=1, n=2)
pTet_rfp = Not(input=tetr, output=rfp, a=100, b=0, K=1, n=2)
rep.add_operators([pCi_laci, pLac_yefp, pTet_rfp])
```

Create SimulatedMetabolism, Sample and Assay

```python
metab = SimulatedMetabolism(biomass, growth_rate)

sample = Sample(circuit=rep, 
                metabolism=metab,
                media=media.id[0],
                strain=strain.id[0]
               )
assay = Assay([sample], 
              n_measurements=100, 
              interval=0.25,
              name='Loica repressilator',
              description='Simulated repressilator generated by loica',
              biomass_signal_id=biomass_signal.id[0]
             )
assay.run()
```

Plot your data

```python
m = assay.measurements
fig,ax = plt.subplots(1,1)
m[m.Signal=='CFP'].plot(x='Time', y='Measurement', ax=ax)
m[m.Signal=='YFP'].plot(x='Time', y='Measurement', ax=ax)
m[m.Signal=='RFP'].plot(x='Time', y='Measurement', ax=ax)
plt.savefig('LOICARepressilator.png', dpi=300)
```
Output
<img src="https://github.com/SynBioUC/LOICA/blob/dev/images/LOICARepressilator.png" height="300" />

Export and upload your data to FlapJack

```python
assay.upload(fj, study.id[0])
```
To get this:

<img src="https://github.com/SynBioUC/LOICA/blob/dev/images/Screen%20Shot%202020-09-25%20at%2000.10.20.png" height="600" />

### NOR gate

Get or Create FlapJack parts for IDs

Create and wire GeneticNetwork


```python
nor = GeneticNetwork(vector=vector.id[0])

sfp1 = Reporter(name='CFP', degradation_rate=0, signal_id=cfp.id[0])
nor.add_reporter(sfp1)

ahl1 = Supplement(name='AHL1')
ahl2 = Supplement(name='AHL2')

nor.add_operator(Nor(input=[ahl1, ahl2], output=sfp1,
                     alpha=[0.0001,1,1,0],
                     a=[100,100], b=[1,1], K=[1,1], n=[2,2]))
```
Ensamble Assay and run it

```python
metab = SimulatedMetabolism(biomass, growth_rate)

samples = []
for conc1 in np.logspace(-3, 3, 12):
    for conc2 in np.logspace(-3,3,12):
        sample = Sample(circuit=nor, 
                metabolism=metab,
                media=media.id[0],
                strain=strain.id[0])
        sample.add_supplement(ahl1, conc1)
        sample.add_supplement(ahl2, conc2)
        samples.append(sample)
        
assay = Assay(samples, 
              n_measurements=100, 
              interval=0.25,
              name='Loica nor',
              description='Simulated nor generated by loica',
              biomass_signal_id=biomass_signal.id[0]
             )
assay.run()
assay.upload(fj, study.id[0])
```

Export and upload your data

<img src="https://github.com/SynBioUC/LOICA/blob/dev/images/Screen%20Shot%202020-10-05%20at%2000.32.42.png" height="600" />

Nice!
