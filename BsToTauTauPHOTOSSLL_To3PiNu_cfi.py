import FWCore.ParameterSet.Config as cms

from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

generator = cms.EDFilter(
    "Pythia8GeneratorFilter",
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    pythiaPylistVerbosity = cms.untracked.int32(0),
    comEnergy = cms.double(13000.0),
    crossSection = cms.untracked.double(54000000000),
    filterEfficiency = cms.untracked.double(3.0e-5),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            list_forced_decays = cms.vstring('MyB_s0', 'Myanti-B_s0'),
            operates_on_particles = cms.vint32(531,-531),
            convertPythiaCodes = cms.untracked.bool(False),
	    user_decay_embedded = cms.vstring(
"""
#
Define alpha 1.365
#
#
Alias      MyY4S    Upsilon(4S)
Alias      MyB_s0   B_s0
Alias      Myanti-B_s0   anti-B_s0
ChargeConj Myanti-B_s0   MyB_s0 
#
#Decay Upsilon(4S)
Decay MyY4S
1.000 MyB_s0 Myanti-B_s0 VSS_BMIX dm;
Enddecay
#
Decay MyB_s0
1.000      tau+  tau-               PHOTOS SLL;
Enddecay
CDecay Myanti-B_s0
#
Decay tau-
1.00      pi-     pi-      pi+     nu_tau                TAUHADNU -0.108 0.775 0.149 1.364 0.400 1.23 0.4;
Enddecay
CDecay tau+
#
End
"""
            )
        ),
        parameterSets = cms.vstring('EvtGen130')
    ),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
            "SoftQCD:nonDiffractive = on",
            'PTFilter:filter = on', # this turn on the filter
            'PTFilter:quarkToFilter = 5', # PDG id of q quark
            'PTFilter:scaleToFilter = 1.0'),
        parameterSets = cms.vstring(
            'pythia8CommonSettings',
            'pythia8CP5Settings',
            'processParameters',
        )
    )
)

bfilter = cms.EDFilter(
    "PythiaFilter",
    MaxEta = cms.untracked.double(9999.),
    MinEta = cms.untracked.double(-9999.),
    ParticleID = cms.untracked.int32(531)
)

maindecayfilter = cms.EDFilter(
    "PythiaDauVFilter",
    verbose         = cms.untracked.int32(1),
    NumberDaughters = cms.untracked.int32(2),
    ParticleID      = cms.untracked.int32(531),
    DaughterIDs     = cms.untracked.vint32(15,-15),
    MinPt           = cms.untracked.vdouble(0.2, 0.2),
    MaxEta          = cms.untracked.vdouble(3.5, 3.5),
    MinEta          = cms.untracked.vdouble(-3.5, -3.5)
)

taudecayfilter = cms.EDFilter(
    "PythiaDauVFilter",
    verbose         = cms.untracked.int32(1),
    NumberDaughters = cms.untracked.int32(4),
    ParticleID      = cms.untracked.int32(15),
    DaughterIDs     = cms.untracked.vint32(211,-211, -211, 16),
    MinPt           = cms.untracked.vdouble(0.2, 0.2, 0.2, 0.0001),
    MaxEta          = cms.untracked.vdouble(3.5, 3.5, 3.5, 999.0),
    MinEta          = cms.untracked.vdouble(-3.5, -3.5, -3.5, -999.0), 
)

#mufilter = cms.EDFilter("PythiaFilter",  # bachelor muon with kinematic cuts.
#    MaxEta = cms.untracked.double(2.5),
#    MinEta = cms.untracked.double(-2.5),
#    MinPt = cms.untracked.double(1.),
#    ParticleID = cms.untracked.int32(13),
#)

ProductionFilterSequence = cms.Sequence(generator*bfilter*maindecayfilter*taudecayfilter)
#ProductionFilterSequence = cms.Sequence(generator*bfilter*maindecayfilter*taudecayfilter*mufilter)
