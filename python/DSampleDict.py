from DProps import *
import ROOT

sampdict = {}

sampdict["TTBAR"] = DSampleProps("t#bart", DLine(ROOT.kBlack, 1, 1),
        DMarker(ROOT.kRed, 0, 0), DFill(ROOT.kRed, 1001))

sampdict["WJETS"] = DSampleProps("W+jets", DLine(ROOT.kBlack, 1, 1),
        DMarker(92, 0, 0), DFill(92, 1001))

sampdict["ZJETS"] = DSampleProps("Z+jets", DLine(ROOT.kBlack, 1, 1),
        DMarker(95, 0, 0), DFill(95, 1001))

sampdict["DIBOSON"] = DSampleProps("Diboson", DLine(ROOT.kBlack, 1, 1),
        DMarker(5, 0, 0), DFill(5, 1001))

sampdict["SINGLETOP"] = DSampleProps("Single Top", DLine(ROOT.kBlack, 1, 1),
        DMarker(62, 0, 0), DFill(62, 1001))

sampdict["SIGNAL"] = DSampleProps("Signal", DLine(ROOT.kBlack, 1, 1),
        DMarker(619, 0, 0), DFill(619, 1001))

sampdict["QCD"] = DSampleProps("QCD", DLine(ROOT.kBlack, 1, 1),
        DMarker(619, 0, 0), DFill(619, 1001))

sampdict["DATA"] = DSampleProps("Data", DLine(ROOT.kBlack, 0, 0),
        DMarker(ROOT.kBlack, 20, 1), DFill(ROOT.kBlack, 0))


def getprocess(samp):
    if "Period" in samp or "period" in samp:
        return "DATA"

    elif "ttbar" in samp:
        return "TTBAR"

    elif "Wenu" in samp or "Wmunu" in samp or "Wtaunu" in samp or \
            "Wbb" in samp or "Wc" in samp or "Wcc" in samp:
        return "WJETS"

    elif "Zee" in samp or "Zmumu" in samp or "Ztautau" in samp:
        return "ZJETS"

    elif "singletop" in samp or "st_schan" in samp or "st_Wtchan" in samp:
        return "SINGLETOP"

    elif "WW" in samp or "WZ" in samp or "ZZ" in samp:
        return "DIBOSON"

    elif "zprime" in samp or "KKGluon" in samp:
        return "SIGNAL"

    else:
        return "QCD"

def fix_style(title, h):
    t, l, m, f = sampdict[getprocess(title)]
    h.SetTitle(t)
    setline(h, l)
    setmarker(h, m)
    setfill(h, f)

    return h
