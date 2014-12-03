from collections import namedtuple
from os import environ
from glob import glob

from sys import stdout

from DSampleDict import getprocess

import ROOT

DSample = namedtuple("DSample", ["name", "title", "mcchanno", "tree",
    "weight"])

rootcoredir = environ["ROOTCOREDIR"]

datapreppath = glob("%s/lib/*/libTopDataPreparation.so" % rootcoredir)

ROOT.gSystem.Load(datapreppath[0])

datapreptool = ROOT.SampleXsection()
datapreptool.readFromFile(rootcoredir +
        "/data/TopDataPreparation/XSection-MC12-8TeV-4gt.data")
datapreptool.readFromFile(rootcoredir +
        "/data/TopDataPreparation/XSection-MC12-8TeV.data")


# returns tuple of infiles, data samples, mc samples
def build_samples(fnames, cfname, tname):
    fins = []

    data_samps = []
    mc_samps = []
    for fname in fnames:
        fin = ROOT.TFile.Open(fname)
        fins.append(fin)

        proc = getprocess(fname)

        t = fin.Get(tname)

        if not t:
            print "missing tree in sample", fname
            stdout.flush()
            continue

        sampname = fname.split('/')[-1]

        if proc == "DATA":
            mcchanno = 0
            name = "_".join(sampname.split('.')[:2])
            title = name
            data_samps.append(DSample(name, title, mcchanno, t, 1.0))

        # monte carlo
        elif proc in ["TTBAR", "ZJETS", "SINGLETOP", "DIBOSON"]:
            mcchannostr = sampname.split('.')[0]

            h = fin.Get(cfname + "_" + mcchannostr)
            if not h:
                print "missing tree in sample", fname
                stdout.flush()
                continue

            mcchanno = int(mcchannostr)
            name = sampname.split('.')[1]
            title = name
            mc_samps.append(DSample(name, title, mcchanno, t,
                    datapreptool.getXsection(mcchanno)/float(h.GetBinContent(1))))


    return fins, data_samps, mc_samps
