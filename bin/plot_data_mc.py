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

# if we pass a SF less than 0, scale mc to data
if sf < 0:
    smc = fin.Get("mc_lep_pt")
    hmclist = smc.GetHists()
    hmctmp = hmclist[0].Clone()

    sdata = fin.Get("data_lep_pt")
    hdatalist = sdata.GetHists()
    hdatatmp = hdatalist[0].Clone()

    print "\nmc histograms:"
    print "%s: %.3f" % (hmctmp.GetTitle(), hmctmp.Integral()); stdout.flush()
    for h in hmclist[1:]:
        print "%s: %.3f" % (h.GetTitle(), h.Integral()); stdout.flush()
        hmctmp.Add(h)

    print "\ndata histograms:"
    print "%s: %.3f" % (hdatatmp.GetTitle(), hdatatmp.Integral()); stdout.flush()
    for h in hdatalist[1:]:
        print "%s: %.3f" % (h.GetTitle(), h.Integral()); stdout.flush()
        hdatatmp.Add(h)

    print "\nmc integral: ", hmctmp.Integral(); stdout.flush()
    print "data integral: ", hdatatmp.Integral(); stdout.flush()

    sf = hdatatmp.Integral()/hmctmp.Integral()


# keep track of stacks we've already plotted
d = {}
for k in fin.GetListOfKeys():
    n = "_".join(k.GetName().split("_")[1:])

    if n in d:
        continue
    else:
        d[n] = True

    sdata = fin.Get("data_" + n)
    smc = fin.Get("mc_" + n)

    if not all(map(lambda s: s and s.IsA().InheritsFrom("THStack"),
            [sdata, smc])):
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
    hmcerr = GetHistErr(hmc)
    for h in smc.GetHists()[1:]:
        h.Scale(sf)
        hmc.Add(h)
        hmcerr = AddHistQuad(hmcerr, GetHistErr(h))

    hdata = sdata.GetHists()[0].Clone()
    hdataerr = GetHistErr(hdata)
    for h in sdata.GetHists()[1:]:
        hdata.Add(h)
        hdataerr = AddHistQuad(hdataerr, GetHistErr(h))

    SetHistErr(hmc, hmcerr)
    hmc.SetMarkerStyle(0)
    hmc.SetLineStyle(0)
    hmc.SetFillColor(kBlack)
    hmc.SetFillStyle(3004)

    SetHistErr(hdata, hdataerr)

    l = list(smc.GetHists())
    l.reverse()
    for h in l[:len(l)/2]:
        leg1.AddEntry(h, h.GetTitle(), "lfe")
    for h in l[len(l)/2:]:
        leg2.AddEntry(h, h.GetTitle(), "lfe")

    leg3.AddEntry(hdata, "data", "lpe")

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

    sMax = max((smc.GetMaximum(), hdata.GetMaximum()))
    sMin = min((smc.GetMinimum(), hdata.GetMinimum()))

    smc.SetMaximum(sMax)
    smc.SetMinimum(0.0)


    smc.Draw("ehist")
    hmc.Draw("e2same")
    hdata.Draw("esame")
    smc.GetXaxis().SetLabelSize(0)
    smc.GetXaxis().SetTitleSize(0)
    smc.GetXaxis().SetTitle(hmc.GetXaxis().GetTitle())
    smc.GetYaxis().SetTitleSize(0.06)
    smc.GetYaxis().SetTitleOffset(1.0)
    smc.GetYaxis().SetTitle(hmc.GetYaxis().GetTitle())

    print "xaxis title:", smc.GetXaxis().GetTitle()
    print "xaxis title:", hmc.GetXaxis().GetTitle()
    print "yaxis title:", smc.GetYaxis().GetTitle()

    leg1.Draw()
    leg2.Draw()
    leg3.Draw()

    pad2.cd()

    hratio = hdata.Clone()
    hratio.Divide(hmc)
    hratio.Draw("e")

    hratio.GetYaxis().SetRangeUser(0.5, 1.5)
    hratio.GetYaxis().SetTitle("data/prediction")
    hratio.GetYaxis().SetLabelSize(0.1)
    hratio.GetYaxis().SetTitleSize(0.15)
    hratio.GetYaxis().SetTitleOffset(0.25)
    hratio.GetYaxis().SetNdivisions(205)
    hratio.GetXaxis().SetTitle(smc.GetXaxis().GetTitle())
    hratio.GetXaxis().SetLabelSize(0.1)
    hratio.GetXaxis().SetTitleSize(0.15)
    hratio.GetXaxis().SetTitleOffset(0.75)
    hratio.Draw("e")

    print "ratio title:", hratio.GetYaxis().GetTitle()
    stdout.flush()

    hmcratio = hmc.Clone()
    hmcratio.Divide(hmc)
    hmcratio.Draw("e2same")

    ratioLine = TLine(hratio.GetBinLowEdge(1), 1,
            hratio.GetBinLowEdge(hratio.GetNbinsX()+1), 1)
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

    smc.Draw("ehist")
    hmc.Draw("e2same")
    hdata.Draw("esame")

    leg1.Draw()
    leg2.Draw()
    leg3.Draw()

    c.Update()
    c.SaveAs(outfolder + n + "_log.png")
    c.SaveAs(outfolder + n + "_log.eps")
    c.SaveAs(outfolder + n + "_log.C")

fin.Close()
