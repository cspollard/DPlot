import ROOT
from array import array
from collections import namedtuple
from itertools import combinations

DPlot = namedtuple("DPlot", ["name", "title", "varexp", "binning",
"overflow"])


pt_plot = DPlot("lep_pt", "lepton p_{T} / MeV", "lep_pt",
        [25000, 30000, 35000, 40000, 45000, 50000, 60000,
            80000, 100000],
        True) # include overflow


eta_plot = DPlot("lep_eta", "lepton #eta", "lep_eta",
        [-2.47, -1.81, -1.52, -1.37, -1.15, -0.6, -0.1, 0,
            0.1, 0.6, 1.15, 1.37, 1.52, 1.81, 2.47],
        False) # no overflow


plots = [[pt_plot], [eta_plot]]


def plot2hist(p):
    h = ROOT.TH1D(p.name, p.title, len(p.binning)-1,
            array('d', p.binning))

    h.GetXaxis().SetTitle(p.title)

    return h
