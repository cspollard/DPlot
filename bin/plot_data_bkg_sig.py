#!/usr/bin/env python

from sys import argv, stdout
myargv = argv[:]
argv = []

from ROOT import *

from DUtils import get_hist_uncert, set_hist_uncert

gROOT.SetBatch(1)
TH1.SetDefaultSumw2()

gROOT.SetStyle("Plain")
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)

def AddHistQuad(h1, h2):
    h = h1.Clone()

    for iBin in range(h.GetNbinsX()+2):
        h.SetBinContent(iBin, sqrt(h1.GetBinContent(iBin)**2 +
                h2.GetBinContent(iBin)**2))

    return h


fin = TFile(myargv[1])
outfolder = myargv[2].rstrip("/") + "/"

c = TCanvas("c", "c", 800, 600)

# optionally scale the MC by some number
if len(myargv) > 3:
    sf = float(myargv[3])
else:
    sf = 1.0


# keep track of stacks we've already plotted
d = {}
for k in fin.GetListOfKeys():
    n = "_".join(k.GetName().split("_")[1:])

    if n in d:
        continue
    else:
        d[n] = True

    sbkg = fin.Get("bkg_" + n)
    if not sbkg:
        print "we must have a stack of background histograms.  continuing."
        continue

    ssig = fin.Get("sig_" + n)
    sdata = fin.Get("data_" + n)

    # make sure we're only drawing stacks
    if not all(map(lambda s: not s or s.IsA().InheritsFrom("THStack"),
            [ssig, sbkg, sdata])):
        print "these aren't THStacks. continuing."
        continue

    # TODO
    # this will normalize each individual histogram...
    if sf < 0:
        if not sdata:
            print "cannot determine scale factor for plot %s: there is no data histogram stack!  continuing." % n
            continue

        ndata = 0
        for hdata in sdata.GetHists():
            ndata += hdata.Integral()

        nbkg = 0
        for hbkg in sbkg.GetHists():
            nbkg += hbkg.Integral()

        if not ndata or not nbkg:
            print "cannot determine scale factor for plot %s: there are no data events!  continuing." % n
            continue

        sf = float(ndata)/float(nbkg)


    sbkg.GetHists()[0].Scale(sf)
    hbkg = sbkg.GetHists()[0].Clone()
    hbkgerr = get_hist_uncert(hbkg)
    for h in sbkg.GetHists()[1:]:
        h.Scale(sf)
        hbkg.Add(h)
        hbkgerr = AddHistQuad(hbkgerr, get_hist_uncert(h))

    set_hist_uncert(hbkg, hbkgerr)
    hbkg.SetMarkerStyle(0)
    hbkg.SetLineStyle(0)
    hbkg.SetFillColor(kBlack)
    hbkg.SetFillStyle(3004)

    if sdata:
        hdata = sdata.GetHists()[0].Clone()
        hdataerr = get_hist_uncert(hdata)
        for h in sdata.GetHists()[1:]:
            hdata.Add(h)
            hdataerr = AddHistQuad(hdataerr, get_hist_uncert(h))


    if ssig:
        for h in ssig.GetHists():
            h.Scale(sf)

    c.Clear()
    c.SetLeftMargin(0.0)
    c.SetRightMargin(0.0)

    # divide into legend and plot pads
    c.Divide(2, 1)

    # format the pad for the plots
    plotpad = c.cd(1)
    plotpad.Clear()
    plotpad.SetPad(0.0, 0.0, 0.7, 1.0)

    # divide into main and ratio plots
    plotpad.Divide(1, 2)

    # set up the ratio pad
    ratiopad = plotpad.cd(2)
    ratiopad.Clear()
    ratiopad.SetPad(0.0, 0.05, 1.0, 0.3)
    ratiopad.SetTopMargin(0.02)
    ratiopad.SetLeftMargin(0.15)
    ratiopad.SetRightMargin(0.075)
    ratiopad.SetBottomMargin(0.3)

    # set up the main pad
    mainpad = plotpad.cd(1)
    mainpad.Clear()
    mainpad.SetPad(0.0, 0.32, 1.0, 1.0)
    mainpad.SetBottomMargin(0.02)
    mainpad.SetLeftMargin(0.15)
    mainpad.SetRightMargin(0.075)

    # draw stack plot in main pad
    hmax = sbkg.GetMaximum()
    if ssig:
        hmax = max(hmax, ssig.GetMaximum())
    if sdata:
        hmax = max(hmax, sdata.GetMaximum())
    sbkg.SetMaximum(hmax)

    sbkg.Draw("hist")
    hbkg.Draw("e2same")
    print "Background integral:", hbkg.Integral()
    sbkg.GetXaxis().SetLabelSize(0)
    sbkg.GetXaxis().SetTitleSize(0)
    sbkg.GetXaxis().SetTitle(hbkg.GetXaxis().GetTitle())
    sbkg.GetYaxis().SetTitleSize(0.06)
    sbkg.GetYaxis().SetTitleOffset(1.0)
    sbkg.GetYaxis().SetTitle(hbkg.GetYaxis().GetTitle())

    if ssig:
        ssig.Draw("nostackhistesame")
        for hsig in ssig.GetHists():
            print hsig.GetTitle(), "integral:", hsig.Integral()
    if sdata:
        hdata.Draw("esame")
        print "Data integral:", hdata.Integral()

    # draw ratio plot
    ratiopad.cd()
    hbkgratio = hbkg.Clone()
    hbkgratio.Divide(hbkg)
    hbkgratio.Draw()

    hbkgratio.GetYaxis().SetRangeUser(0.5, 1.5)
    hbkgratio.GetYaxis().SetTitle("ratio")
    hbkgratio.GetYaxis().SetLabelSize(0.1)
    hbkgratio.GetYaxis().SetTitleSize(0.15)
    hbkgratio.GetYaxis().SetTitleOffset(0.25)
    hbkgratio.GetYaxis().SetNdivisions(205)
    hbkgratio.GetXaxis().SetTitle(sbkg.GetXaxis().GetTitle())
    hbkgratio.GetXaxis().SetLabelSize(0.1)
    hbkgratio.GetXaxis().SetTitleSize(0.15)
    hbkgratio.GetXaxis().SetTitleOffset(0.75)
    hbkgratio.Draw("e2")

    ratioLine = TLine(hbkgratio.GetBinLowEdge(1), 1,
            hbkgratio.GetBinLowEdge(hbkgratio.GetNbinsX()+1), 1)
    ratioLine.SetLineColor(kBlack)
    ratioLine.SetLineStyle(7)
    ratioLine.Draw("same")

    # new ratio plot for each signal
    if ssig:
        ssigratio = THStack()
        for hsig in list(ssig.GetHists()):
            hsigratio = hsig.Clone()
            # don't propogate mc uncertainty to signal ratios.
            hsigratioerr = get_hist_uncert(hsigratio)
            hsigratio.Add(hbkg)
            hsigratio.Divide(hbkg)
            hsigratioerr.Divide(hbkg)
            set_hist_uncert(hsigratio, hsigratioerr)
            ssigratio.Add(hsigratio)
            continue

        ssigratio.Draw("nostackehistsame")

    # new ratio plot for data
    if sdata:
        hdataratio = hdata.Clone()
        # don't propogate mc uncertainty to data ratios.
        hdataratioerr = get_hist_uncert(hdataratio)
        hdataratio.Divide(hbkg)
        hdataratioerr.Divide(hbkg)
        set_hist_uncert(hdataratio, hdataratioerr)
        hdataratio.Draw("esame")



    # set up and draw the legend
    legpad = c.cd(2)
    legpad.SetPad(0.7, 0.12, 1.0, 0.93)
    legpad.SetLeftMargin(0.0)
    legpad.SetRightMargin(0.0)
    legpad.SetBorderSize(0)

    leg = TLegend(0, 0, 1, 1)

    leg.SetShadowColor(kWhite)
    leg.SetLineColor(kWhite)
    leg.SetFillStyle(0)
    leg.SetEntrySeparation(0.05)
    leg.SetMargin(0.15)

    l = list(sbkg.GetHists()) 
    l.reverse()
    map(lambda h: leg.AddEntry(h, h.GetTitle(), "f"), l)

    if ssig:
        l = list(ssig.GetHists())
        l.reverse()
        map(lambda h: leg.AddEntry(h, h.GetTitle(), "l"), l)
    if sdata:
        leg.AddEntry(hdata, hdata.GetTitle(), "p")

    leg.SetTextSize(1.0/len(leg.GetListOfPrimitives()))

    leg.Draw()

    # save linear plot
    mainpad.SetLogy(0)
    c.Update()
    c.SaveAs(outfolder + n + ".png")
    c.SaveAs(outfolder + n + ".eps")
    c.SaveAs(outfolder + n + ".pdf")
    c.SaveAs(outfolder + n + ".C")

    # save log plot
    mainpad.cd()
    mainpad.SetLogy(1)
    if sbkg.GetMinimum() < 0.1:
        sbkg.SetMinimum(0.1)
    elif ssig and ssig.GetMinimum() < 0.1:
        sbkg.SetMinimum(0.1)
    else:
        sbkg.SetMinimum(1)

    sbkg.Draw("hist")
    hbkg.Draw("e2same")
    if ssig:
        ssig.Draw("nostackhistesame")
    if sdata:
        hdata.Draw("esame")

    c.Update()
    c.SaveAs(outfolder + n + "_log.png")
    c.SaveAs(outfolder + n + "_log.eps")
    c.SaveAs(outfolder + n + "_log.pdf")
    c.SaveAs(outfolder + n + "_log.C")

fin.Close()
