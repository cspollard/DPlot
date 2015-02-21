#!/usr/bin/env python

from sys import argv, stdout
myargv = argv[:]
argv = []

from ROOT import *

from DUtils import get_hist_uncert, set_hist_uncert

gROOT.SetBatch(1)
TH1.SetDefaultSumw2()

gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)

gROOT.SetStyle("Plain")

def AddHistQuad(h1, h2):
    h = h1.Clone()

    for iBin in range(h.GetNbinsX()+2):
        h.SetBinContent(iBin, sqrt(h1.GetBinContent(iBin)**2 +
                h2.GetBinContent(iBin)**2))

    return h


fin = TFile(myargv[1])
outfolder = myargv[2].rstrip("/") + "/"

c = TCanvas("c", "c", 600, 600)

# optionally scale the MC by some number
if len(myargv) > 3:
    sf = float(myargv[3])
else:
    sf = 1.0


# keep track of stacks we've already plotted
d = {}
for k in fin.GetListOfKeys():
    n = "_".join(k.GetName().split("_")[1:])
    print n; stdout.flush()

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

    leg1 = TLegend(0.6, 0.6, 0.75, 0.7)
    leg2 = TLegend(0.75, 0.6, 0.9, 0.7)
    leg3 = TLegend(0.675, 0.5, 0.825, 0.6)

    leg1.SetShadowColor(kWhite)
    leg1.SetBorderSize(0)
    leg1.SetFillStyle(0)

    leg2.SetShadowColor(kWhite)
    leg2.SetBorderSize(0)
    leg2.SetFillStyle(0)

    leg3.SetShadowColor(kWhite)
    leg3.SetBorderSize(0)
    leg3.SetFillStyle(0)

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

    l = list(smc.GetHists()) + list(ssig.GetHists())
    l.reverse()
    for h in l[:len(l)/2]:
        leg1.AddEntry(h, h.GetTitle(), "lfe")
    for h in l[len(l)/2:]:
        leg2.AddEntry(h, h.GetTitle(), "lfe")

    c.Clear()
    c.Divide(1, 2)

    pad1 = c.cd(1)
    pad1.Clear()
    pad1.SetPad(0.0, 0.32, 1.0, 1.0)
    pad1.SetBottomMargin(0.02)
    pad1.SetLeftMargin(0.15)
    pad1.SetRightMargin(0.075)

    pad2 = c.cd(2)
    pad2.Clear()
    pad2.SetPad(0.0, 0.05, 1.0, 0.3)
    pad2.SetTopMargin(0.02)
    pad2.SetLeftMargin(0.15)
    pad2.SetRightMargin(0.075)
    pad2.SetBottomMargin(0.3)

    pad1.cd()

    smc.Draw("hist")
    hmc.Draw("e2same")
    ssig.Draw("nostackhistesame")
    smc.GetXaxis().SetLabelSize(0)
    smc.GetXaxis().SetTitleSize(0)
    smc.GetXaxis().SetTitle(hmc.GetXaxis().GetTitle())
    smc.GetYaxis().SetTitleSize(0.06)
    smc.GetYaxis().SetTitleOffset(1.0)
    smc.GetYaxis().SetTitle(hmc.GetYaxis().GetTitle())


    leg1.Draw()
    leg2.Draw()
    leg3.Draw()

    pad2.cd()

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

    for hsig in list(ssig.GetHists()):
        hsigratio = hsig.Clone()
        hsigratioerr = get_hist_uncert(hsigratio)
        hsigratio.Add(hmc)
        hsigratio.Divide(hmc)
        set_hist_uncert(hsigratio, hsigratioerr)
        hsigratio.Draw("histesame")


    ratioLine = TLine(hmcratio.GetBinLowEdge(1), 1,
            hmcratio.GetBinLowEdge(hmcratio.GetNbinsX()+1), 1)
    ratioLine.SetLineColor(kBlack)
    ratioLine.SetLineStyle(7)
    ratioLine.Draw("same")

    pad1.SetLogy(0)
    c.Update()
    c.SaveAs(outfolder + n + ".png")
    c.SaveAs(outfolder + n + ".eps")
    c.SaveAs(outfolder + n + ".C")

    pad1.cd()
    pad1.SetLogy(1)

    smc.SetMinimum(0.1)

    smc.Draw("hist")
    hmc.Draw("e2same")
    ssig.Draw("nostackhistesame")

    leg1.Draw()
    leg2.Draw()
    leg3.Draw()

    c.Update()
    c.SaveAs(outfolder + n + "_log.png")
    c.SaveAs(outfolder + n + "_log.eps")
    c.SaveAs(outfolder + n + "_log.C")

fin.Close()
