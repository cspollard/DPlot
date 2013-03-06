// main.cxx

#include <iostream>
#include <vector>
#include "TFile.h"
#include "TColor.h"
// #include "DSampleTree.h"
#include "DSampleFile.h"
#include "DSampleGroup.h"
#include "DPlot.h"

int main(int argc, char *argv[]) {
    if (argc < 2)
        return 0;

    TH1::SetDefaultSumw2();

    TFile *fin = new TFile(argv[1]);

    TFile *fout = new TFile("out.root", "recreate");
    std::vector<DSampleTree *> samps;

    /*
    TTree *tin = (TTree *) fin->Get("Nominal_one_btag_cut_el_ntuple");
    samps.push_back(new DSampleTree("d", "d", tin));
    samps.push_back(new DSampleTree("e", "e", tin));
    */

    DSampleFile *d = new DSampleFile("d", "d", fin,
                "Nominal_one_btag_cut_el_ntuple", 100, "el_tight*wgt");

    d->SetLine(DLine(kRed, 1, 4));
    *d << DLine(kOrange, 1, 4);

    DSampleFile e = DSampleFile("e", "e", fin,
                "Nominal_one_btag_cut_el_ntuple");


    e << DFill(kBlue, 1001);

    samps.push_back(d);
    samps.push_back(&e);

    DSampleGroup dg("dg", "g");
    dg.AddSample(d);
    // dg.AddSample((DSampleTree *) &e);
    dg << DFill(kGreen, 1001);
    std::cout << dg.GetFill().GetStyle() << std::endl;

    samps.push_back(&dg);

    DPlot *dp = new DPlot("dp", "dp", 1.0, "el_pt", &samps);

    THStack *st = dp->Plot(5, 0, 100000);

    st->Write();

    fout->Close();

    return 0;
}
