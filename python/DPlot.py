import ROOT
from array import array
from collections import namedtuple
from itertools import combinations

DPlot = namedtuple("DPlot", ["name", "title", "varexp", "binning",
"overflow"])


pt_plot = DPlot("lep_pt", "lepton p_{T} / MeV", "lep_pt",
        [15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000,
            55000, 60000, 65000, 70000, 75000, 80000, 85000],
        True) # include overflow


eta_plot = DPlot("lep_eta", "lepton #eta", "lep_eta",
        [-2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5],
        False) # no overflow


plots = [[pt_plot], [eta_plot]]


def plot2hist(p):
    h = ROOT.TH1D(p.name, p.title, len(p.binning)-1,
            array('d', p.binning))

    h.GetXaxis().SetTitle(p.title)

    return h
