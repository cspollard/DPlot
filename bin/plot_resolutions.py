#/usr/bin/env python

# do this or ROOT might steal my argvs!
from sys import argv, stdout
myargv = argv[:]
argv = []

# set up ROOT style options
from ROOT import *
gROOT.SetBatch(1)
TH1.SetDefaultSumw2()
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)

gStyle.SetPalette(55)
gStyle.SetPaintTextFormat("4.1f")


from DUtils import projections

fin = TFile(myargv[1])
outfolder = myargv[2].rstrip("/") + "/"

fout = TFile.Open("%s%s" % (outfolder, myargv[1]), "create")

c = TCanvas()
c.cd()
fout.cd()
for k in fin.GetListOfKeys():
    h = fin.Get(k)

    if h.IsA().InheritsFrom("TH2"):
        # draw and save the 2D histo with the profile
        outname = "%s%s" % (outfolder, h.GetName())
        hprof = h.ProfileX()

        h.Draw("colztext00")
        hprof.Draw("samehiste")

        c.SaveAs("%s.pdf" % outname)
        c.SaveAs("%s.png" % outname)
        c.SaveAs("%s.C" % outname)

        h.Write()
        hprof.Write()

        hprojs = projections(h)
        for proj in hprojs:
            outname = "%s%s" % (outfolder, proj.GetName())

            proj.Draw("histe")
            c.SaveAs("%s.pdf" % outname)
            c.SaveAs("%s.png" % outname)
            c.SaveAs("%s.C" % outname)

            h.Write()


    elif h.IsA().InheritsFrom("TH1"):
        outname = "%s%s" % (outfolder, h.GetName())

        h.Draw("histe")
        c.SaveAs("%s.pdf" % outname)
        c.SaveAs("%s.png" % outname)
        c.SaveAs("%s.C" % outname)

        h.Write()

    continue


fin.Close()
fout.Close()
