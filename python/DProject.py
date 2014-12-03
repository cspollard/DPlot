from math import sqrt
from array import array

import ROOT
ROOT.TH1.SetDefaultSumw2(True)
ROOT.gROOT.SetBatch(True)


def project(tree, cut, varexp, h, overflow=-1):
    tree.Project(h.GetName(), varexp, cut)

    if overflow == -1:
        overflow = [True]*h.GetDimensions()

    return include_overflow(h, overflow)


def include_overflow(h, oflows):
    if h.GetDimension() == 1:
        return include_overflow_1d(h, oflows)

    elif h.GetDimension() == 2:
        return include_overflow_2d(h, oflows)

    elif h.GetDimension() == 3:
        return include_overflow_3d(h, oflows)

    else:
        return h


def add_overflow_bin(h, ifbin, ofbin):
    if ifbin == ofbin:
        return h

    h.SetBinContent(ifbin,
            h.GetBinContent(ifbin) +
            h.GetBinContent(ofbin))
    h.SetBinContent(ofbin, 0.0)

    h.SetBinError(ifbin,
            sqrt(h.GetBinError(ifbin)**2 +
                h.GetBinError(ofbin)**2))
    h.SetBinError(ofbin, 0.0)

    return h


def include_overflow_1d(h, oflow=True):
    if not oflow:
        return h

    nx = h.GetNbinsX()

    ifbin = h.GetBin(1)
    ofbin = h.GetBin(0)

    add_overflow_bin(h, ifbin, ofbin)

    ifbin = h.GetBin(nx)
    ofbin = h.GetBin(nx+1)

    add_overflow_bin(h, ifbin, ofbin)

    return h


def include_overflow_2d(h, oflows=(True, True)):
    if not any(oflows):
        return h

    if len(oflows) != 2:
        print "include_overflow_2d: overflow option has incorrect length."
        return h

    nx = h.GetNbinsX()
    ny = h.GetNbinsY()

    # only if we're adding y overflows
    if oflows[1]:
        for xbin in xrange(nx+2):
            ifbin = h.GetBin(xbin, 1)
            ofbin = h.GetBin(xbin, 0)

            add_overflow_bin(h, ifbin, ofbin)

            ifbin = h.GetBin(xbin, ny)
            ofbin = h.GetBin(xbin, ny+1)

            add_overflow_bin(h, ifbin, ofbin)

    # only if we're adding x overflows
    if oflows[0]:
        for ybin in xrange(ny+2):
            ifbin = h.GetBin(1, ybin)
            ofbin = h.GetBin(0, ybin)

            add_overflow_bin(h, ifbin, ofbin)

            ifbin = h.GetBin(nx, ybin)
            ofbin = h.GetBin(nx+1, ybin)

            add_overflow_bin(h, ifbin, ofbin)

    return h

def include_overflow_3d(h, oflows=(True, True, True)):

    if not any(oflows):
        return h

    if len(oflows) != 3:
        print "include_overflow_3d: overflow option has incorrect length."
        return h

    nx = h.GetNbinsX()
    ny = h.GetNbinsY()
    nz = h.GetNbinsZ()

    if oflows[2]:
        for xbin in xrange(nx+2):
            for ybin in xrange(ny+2):
                ifbin = h.GetBin(xbin, ybin, 1)
                ofbin = h.GetBin(xbin, ybin, 0)

                add_overflow_bin(h, ifbin, ofbin)

                ifbin = h.GetBin(xbin, ybin, nz)
                ofbin = h.GetBin(xbin, ybin, nz+1)

                add_overflow_bin(h, ifbin, ofbin)

    if oflows[1]:
        for zbin in xrange(nz+2):
            for xbin in xrange(nx+2):
                ifbin = h.GetBin(xbin, 1, zbin)
                ofbin = h.GetBin(xbin, 0, zbin)

                add_overflow_bin(h, ifbin, ofbin)

                ifbin = h.GetBin(xbin, ny, zbin)
                ofbin = h.GetBin(xbin, ny+1, zbin)

                add_overflow_bin(h, ifbin, ofbin)

    if oflows[0]:
        for ybin in xrange(ny+2):
            for zbin in xrange(nz+2):
                ifbin = h.GetBin(1, ybin, zbin)
                ofbin = h.GetBin(0, ybin, zbin)

                add_overflow_bin(h, ifbin, ofbin)

                ifbin = h.GetBin(nx, ybin, zbin)
                ofbin = h.GetBin(nx+1, ybin, zbin)

                add_overflow_bin(h, ifbin, ofbin)


    return h
