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

    ssig = fin.Get("sig_" + n)
    smc = fin.Get("mc_" + n)

    # make sure we're only drawing stacks
    if not all(map(lambda s: s and s.IsA().InheritsFrom("THStack"),
            [ssig, smc])):
        continue

    smc.GetHists()[0].Scale(sf)
    hmc = smc.GetHists()[0].Clone()
    hmcerr = get_hist_uncert(hmc)
    for h in smc.GetHists()[1:]:
        h.Scale(sf)
        hmc.Add(h)
        hmcerr = AddHistQuad(hmcerr, get_hist_uncert(h))

    set_hist_uncert(hmc, hmcerr)
    hmc.SetMarkerStyle(0)
    hmc.SetLineStyle(0)
    hmc.SetFillColor(kBlack)
    hmc.SetFillStyle(3004)

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
    smc.Draw("hist")
    hmc.Draw("e2same")
    ssig.Draw("nostackhistesame")
    smc.GetXaxis().SetLabelSize(0)
    smc.GetXaxis().SetTitleSize(0)
    smc.GetXaxis().SetTitle(hmc.GetXaxis().GetTitle())
    smc.GetYaxis().SetTitleSize(0.06)
    smc.GetYaxis().SetTitleOffset(1.0)
    smc.GetYaxis().SetTitle(hmc.GetYaxis().GetTitle())

    # draw ratio plot
    ratiopad.cd()
    hmcratio = hmc.Clone()
    hmcratio.Divide(hmc)
    hmcratio.Draw("e2")

    hmcratio.GetYaxis().SetRangeUser(0.5, 1.5)
    hmcratio.GetYaxis().SetTitle("(s+b)/b")
    hmcratio.GetYaxis().SetLabelSize(0.1)
    hmcratio.GetYaxis().SetTitleSize(0.15)
    hmcratio.GetYaxis().SetTitleOffset(0.25)
    hmcratio.GetYaxis().SetNdivisions(205)
    hmcratio.GetXaxis().SetTitle(smc.GetXaxis().GetTitle())
    hmcratio.GetXaxis().SetLabelSize(0.1)
    hmcratio.GetXaxis().SetTitleSize(0.15)
    hmcratio.GetXaxis().SetTitleOffset(0.75)
    hmcratio.Draw("e2same")

    # new ratio plot for each signal
    # TODO
    # uncertainties correct?
    tmp = []
    for hsig in list(ssig.GetHists()):
        hsigratio = hsig.Clone()
        hsigratioerr = get_hist_uncert(hsigratio)
        hsigratio.Add(hmc)
        hsigratio.Divide(hmc)
        hsigratioerr.Divide(hmc)
        set_hist_uncert(hsigratio, hsigratioerr)
        tmp.append(hsigratio)
        hsigratio.Draw("histesame")

    tmp


    ratioLine = TLine(hmcratio.GetBinLowEdge(1), 1,
            hmcratio.GetBinLowEdge(hmcratio.GetNbinsX()+1), 1)
    ratioLine.SetLineColor(kBlack)
    ratioLine.SetLineStyle(7)
    ratioLine.Draw("same")


    # set up and draw the legend
    legpad = c.cd(2)
    legpad.SetPad(0.7, 0.12, 1.0, 0.93)
    legpad.SetLeftMargin(0.0)
    legpad.SetRightMargin(0.0)
    legpad.SetBorderSize(0)

    leg = TLegend(0, 0, 1, 1)

    leg.SetShadowColor(kWhite)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)

    l = list(smc.GetHists()) + list(ssig.GetHists())
    l.reverse()
    map(lambda h: leg.AddEntry(h, h.GetTitle(), "lfe"), l)

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
    smc.SetMinimum(0.1)

    smc.Draw("hist")
    hmc.Draw("e2same")
    ssig.Draw("nostackhistesame")

    c.Update()
    c.SaveAs(outfolder + n + "_log.png")
    c.SaveAs(outfolder + n + "_log.eps")
    c.SaveAs(outfolder + n + "_log.pdf")
    c.SaveAs(outfolder + n + "_log.C")

fin.Close()
