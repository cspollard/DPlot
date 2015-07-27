from math import sqrt
from itertools import groupby
from array import array
from sys import stdout

from DUncertain import Uncertain
from DProject import project

import ROOT
ROOT.TH1.SetDefaultSumw2(True)
ROOT.gROOT.SetBatch(True)

def get_hist_uncert(h):
    herr = h.Clone()
    herr.SetTitle(herr.GetTitle() + " errors")
    herr.SetName(herr.GetName() + "_errors")

    for xbin in range(h.GetNbinsX()+2):
        for ybin in range(h.GetNbinsY()+2):
            for zbin in range(h.GetNbinsZ()+2):
                ibin = h.GetBin(xbin, ybin, zbin)
                herr.SetBinContent(ibin, h.GetBinError(ibin))

    return herr

def set_hist_uncert(h, herr):
    for xbin in range(h.GetNbinsX()+2):
        for ybin in range(h.GetNbinsY()+2):
            for zbin in range(h.GetNbinsZ()+2):
                ibin = h.GetBin(xbin, ybin, zbin)
                h.SetBinError(ibin, herr.GetBinContent(ibin))

    return h


def quadsum(x, y):
    return x**2 + y**2

def hist_cmp(h1, h2):
    return cmp(h1.Integral(), h2.Integral())

def scale_hist(h, sf):
    h.Scale(sf)
    return h

def sum_hists(hs, name=None, title=None):
    h1, hs1 = hs[0].Clone(), hs[1:]
    map(h1.Add, hs1)

    return h1

def hist_subtract(h1, h2):
    h1.Add(h2, -1)

    return h1


def grouphists(hs, groupfunc=ROOT.TH1.GetTitle):
        groups = [list(g) for k, g in groupby(sorted(hs, cmp,
            groupfunc), groupfunc)]
        return map(sum_hists, groups)


def make_stack(name, title, hs, sortfunc=hist_cmp, groupfunc=None):
    s = ROOT.THStack(name, title)

    if groupfunc:
        hists = grouphists(hs, groupfunc)
    else:
        hists = hs

    if sortfunc:
        hists.sort(cmp=sortfunc)

    map(s.Add, hists)

    return s


def transpose(l):
    return map(list, zip(*l))


def make_hist(plots, samp, cut):
    names, titles, varexps, binnings, oflows = transpose(plots)

    dims = len(names)
    name = '_'.join(names) + "_%s_%s" % (cut.GetName(), samp.name)
    title = samp.title
    varexp = ':'.join(varexps[::-1])

    if dims == 1:
        h = ROOT.TH1D(name, title,
                len(binnings[0])-1, array('d', binnings[0]))

        h.Draw()
        h.GetXaxis().SetTitle(titles[0])
        h.GetYaxis().SetTitle("entries")

    elif dims == 2:
        h = ROOT.TH2D(name, title,
                len(binnings[0])-1, array('d', binnings[0]),
                len(binnings[1])-1, array('d', binnings[1]))

        h.Draw()
        h.GetXaxis().SetTitle(titles[0])
        h.GetYaxis().SetTitle(titles[1])
        h.GetZaxis().SetTitle("entries")

    elif dims == 3:
        h = ROOT.TH3D(name, title,
                len(binnings[0])-1, array('d', binnings[0]),
                len(binnings[1])-1, array('d', binnings[1]),
                len(binnings[2])-1, array('d', binnings[2]))

        h.Draw()
        h.GetXaxis().SetTitle(titles[0])
        h.GetYaxis().SetTitle(titles[1])
        h.GetZaxis().SetTitle(titles[2])

    else:
        print "cannot project more than a TH3D."; stdout.flush()
        return None


    h = project(samp.chain, str(cut), varexp, h, oflows)
    h.Scale(samp.weight)

    return h


def make_hist_foreach_sample(plots, samps, cut):
    hists = map(lambda s: make_hist(plots, s, cut), samps)

    return hists


def projections(h, axis='x'):
    if not h.IsA().InheritsFrom("TH2"):
        print "projections() only works for ROOT::TH2s."
        return None

    axis = axis.lower()

    if axis == 'y':
        nbins = h.GetNbinsX()
        projfunc = h.ProjectionY
        ytitle = h.GetZaxis().GetTitle()
        xtitle = h.GetYaxis().GetTitle()
        param = h.GetXaxis().GetTitle()
        taxis = h.GetXaxis()

    else:
        nbins = h.GetNbinsY()
        projfunc = h.ProjectionX
        xtitle = h.GetXaxis().GetTitle()
        ytitle = h.GetZaxis().GetTitle()
        param = h.GetYaxis().GetTitle()
        taxis = h.GetYaxis()

    hs = []
    # don't do over/undeflow
    for ibin in range(1, nbins+1):
        h1 = projfunc("%s_p%d" % (h.GetName(), ibin),
                ibin, ibin, "e")

        h1.GetXaxis().SetTitle(xtitle)
        h1.GetYaxis().SetTitle(ytitle)

        ledge = taxis.GetBinLowEdge(ibin)
        hedge = taxis.GetBinUpEdge(ibin)


        h1.SetTitle("%.2f < %s < %.2f" %
                (ledge, param, hedge))

        hs.append(h1)

    return hs


def hist_to_uncertains(h):
    # under/overflow not included.
    if h.InheritsFrom("TH3"):
        us = []
        for xBin in range(1, h.GetNbinsX()+1):
            us.append([])
            for yBin in range(1, h.GetNbinsY()+1):
                us[-1].append([])
                for zBin in range(1, h.GetNbinsZ()+1):
                    us[-1][-1].append(
                            Uncertain(
                                h.GetBinContent(xBin, yBin, zBin),
                                h.GetBinError(xBin, yBin, zBin)
                                )
                            )

    elif h.InheritsFrom("TH2"):
        us = []
        for xBin in range(1, h.GetNbinsX()+1):
            us.append([])
            for yBin in range(1, h.GetNbinsY()+1):
                us[-1].append(
                        Uncertain(
                            h.GetBinContent(xBin, yBin),
                            h.GetBinError(xBin, yBin)
                            )
                        )

    elif h.InheritsFrom("TH1"):
        us = []
        for xBin in range(1, h.GetNbinsX()+1):
            us.append(
                    Uncertain(
                        h.GetBinContent(xBin),
                        h.GetBinError(xBin)
                        )
                    )

    else:
        print "hist_to_uncertains(): attempting to read from an object that doesn't inherit from TH1. returning None."
        stdout.flush()
        return None

    return us


def fill_from_uncertains(h, us):
    if len(us) != h.GetNbinsX():
        print "attempting to fill histogram with values list of different length. aborting."
        stdout.flush()
        return h

    if h.InheritsFrom("TH3"):
        for xBin in range(1, h.GetNbinsX()+1):
            for yBin in range(1, h.GetNbinsY()+1):
                for zBin in range(1, h.GetNbinsZ()+1):
                    u = us[xBin-1][yBin-1][zBin-1]
                    h.SetBinContent(xBin, yBin, zBin, u.x)
                    h.SetBinError(xBin, yBin, zBin, u.dx)


    elif h.InheritsFrom("TH2"):
        for xBin in range(1, h.GetNbinsX()+1):
            for yBin in range(1, h.GetNbinsY()+1):
                u = us[xBin-1][yBin-1]
                h.SetBinContent(xBin, yBin, u.x)
                h.SetBinError(xBin, yBin, u.dx)


    elif h.InheritsFrom("TH1"):
        for xBin in range(1, h.GetNbinsX()+1):
            u = us[xBin-1]
            h.SetBinContent(xBin, u.x)
            h.SetBinError(xBin, u.dx)

    else:
        print "fill_from_uncertains(): attempting to fill an object that doesn't inherit from TH1. returning None."
        stdout.flush()
        return None

    return h


def hist_integral(h, xbinLow=1, xbinHigh=-1, ybinLow=1, ybinHigh=-1,
        zbinLow=1, zbinHigh=-1):
    uncert = array('d', [0])

    if (h.InheritsFrom("TH3")):
        # don't include overflow by default.
        if xbinHigh < 0:
            xbinHigh = h.GetNbinsX()

        if ybinHigh < 0:
            ybinHigh = h.GetNbinsY()

        if zbinHigh < 0:
            zbinHigh = h.GetNbinsZ()

        integ = h.IntegralAndError(xbinLow, xbinHigh,
                ybinLow, ybinHigh, zbinLow, zbinHigh, uncert)

    elif (h.InheritsFrom("TH2")):
        # don't include overflow by default.
        if xbinHigh < 0:
            xbinHigh = h.GetNbinsX()

        if ybinHigh < 0:
            ybinHigh = h.GetNbinsY()

        integ = h.IntegralAndError(xbinLow, xbinHigh,
                ybinLow, ybinHigh, uncert)

    elif (h.InheritsFrom("TH1")):
        # don't include overflow by default.
        if xbinHigh < 0:
            xbinHigh = h.GetNbinsX()

        integ = h.IntegralAndError(xbinLow, xbinHigh, uncert)

    else:
        print "hist_integral(): attempt to integrate a non-histogram."
        stdout.flush()
        return None


    return Uncertain(integ, uncert[0])


def safe_div(num, denom):
    if denom.x:
        return num/denom
    else:
        return Uncertain(0.0, 0.0)

def scale_by_uncertain(h, u):
    bins = hist_to_uncertains(h)

    if h.InheritsFrom("TH3"):
        bins = map(lambda x:
                map(lambda y:
                    map(lambda z: u*z, y),
                    x),
                bins)

    elif h.InheritsFrom("TH2"):
        bins = map(lambda x:
                map(lambda y: u*y, x),
                bins)

    else:
        bins = map(lambda b: b*u, bins)

    return fill_from_uncertains(h, bins)


def norm_to_hist_bins(hs, hnorm):
    binNorms = hist_to_uncertains(hnorm)

    # don't include over/underflow
    for (iBin, h) in enumerate(hs, start=1):

        integral = hist_integral(h)

        norm = safe_div(binNorms[iBin], integral)

        scale_by_uncertain(h, norm)

    return hs
