from DProps import *
import ROOT

sampdict = {}

# data
sampdict["DATA"] = DSampleProps("data", DLine(ROOT.kBlack, 0, 0),
        DMarker(ROOT.kBlack, 20, 1), DFill(ROOT.kBlack, 0))

# signal

sampdict["SMVH"] = DSampleProps("SM VH", DLine(ROOT.kBlack, 1, 3),
        DMarker(ROOT.kBlack, 0, 0), DFill(ROOT.kBlack, 0))

sampdict["HVT1.0TEVRES"] = DSampleProps("1.0 TeV HVT res", DLine(ROOT.kAzure, 1, 3),
        DMarker(ROOT.kAzure, 0, 0), DFill(ROOT.kAzure, 0))

sampdict["HVT2.0TEVRES"] = DSampleProps("2.0 TeV HVT res", DLine(ROOT.kGreen+3, 1, 3),
        DMarker(ROOT.kGreen+3, 0, 0), DFill(ROOT.kGreen+3, 0))

"""
sampdict["HVT0.5TEVRES"] = DSampleProps("0.5 TeV HVT res", DLine(ROOT.kGray+1, 1, 3),
        DMarker(ROOT.kGray+1, 0, 0), DFill(ROOT.kGray+1, 0))

sampdict["HVT1.5TEVRES"] = DSampleProps("1.5 TeV HVT res", DLine(ROOT.kAzure, 1, 3),
        DMarker(ROOT.kAzure, 0, 0), DFill(ROOT.kAzure, 0))

sampdict["HVT2.5TEVRES"] = DSampleProps("2.5 TeV HVT res", DLine(ROOT.kGreen+3, 1, 3),
        DMarker(ROOT.kGreen+3, 0, 0), DFill(ROOT.kGreen+3, 0))
"""

# backgrounds
sampdict["TTBAR"] = DSampleProps("t#bart", DLine(ROOT.kBlack, 1, 1),
        DMarker(ROOT.kRed, 0, 0), DFill(ROOT.kRed, 1001))

sampdict["WJETS"] = DSampleProps("W+jets", DLine(ROOT.kBlack, 1, 1),
        DMarker(92, 0, 0), DFill(92, 1001))

sampdict["ZJETS"] = DSampleProps("Z+jets", DLine(ROOT.kBlack, 1, 1),
        DMarker(95, 0, 0), DFill(95, 1001))

sampdict["DIBOSON"] = DSampleProps("diboson", DLine(ROOT.kBlack, 1, 1),
        DMarker(5, 0, 0), DFill(5, 1001))

sampdict["SINGLETOP"] = DSampleProps("single top", DLine(ROOT.kBlack, 1, 1),
        DMarker(ROOT.kRed+2, 0, 0), DFill(ROOT.kRed+2, 1001))

sampdict["QCD"] = DSampleProps("QCD", DLine(ROOT.kBlack, 1, 1),
        DMarker(619, 0, 0), DFill(619, 1001))

# other
sampdict["OTHER"] = DSampleProps("other", DLine(ROOT.kBlack, 1, 1),
        DMarker(619, 0, 0), DFill(619, 1001))



def getprocess(title):
    if "Period" in title or "period" in title:
        return "DATA"

    elif "ttbar" in title:
        return "TTBAR"

    elif "Wenu" in title or "Wmunu" in title or "Wtaunu" in title or \
            "Wbb" in title or "Wc" in title or "Wcc" in title:
        return "WJETS"

    elif "Zee" in title or "Zmumu" in title or "Ztautau" in title or \
            "Znunu" in title:
        return "ZJETS"

    elif "singletop" in title or "st_schan" in title or "st_Wtchan" in title:
        return "SINGLETOP"

    elif "WW" in title or "WZ" in title or "ZZ" in title:
        return "DIBOSON"


    # TODO
    # UGLY
    elif "HVT" in title:
        s = "HVT"
        if "2000" in title:
            return s + "2.0TEVRES"
        elif "1000" in title:
            return s + "1.0TEVRES"
        else:
            return "OTHERSIGNAL"

    elif "H125" in title:
        return "SMVH"

    elif "jetjet_JZ" in title:
        return "QCD"

    else:
        return "OTHER"


def fix_style(samp, h):
    t, l, m, f = sampdict[getprocess(samp.title)]
    h.SetTitle(t)
    setline(h, l)
    setmarker(h, m)
    setfill(h, f)

    return h
