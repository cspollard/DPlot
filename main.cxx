// main.cxx

#include <vector>
#include "TFile.h"
// #include "DSampleTree.h"
#include "DSampleFile.h"
#include "DPlot.h"

int main(int argc, char *argv[]) {
    if (argc < 2)
        return 0;

    TFile *fin = new TFile(argv[1]);

    TFile *fout = new TFile("out.root", "recreate");
    std::vector<DSampleTree *> samps;

    /*
    TTree *tin = (TTree *) fin->Get("Nominal_one_btag_cut_el_ntuple");
    samps.push_back(new DSampleTree("d", "d", tin));
    samps.push_back(new DSampleTree("e", "e", tin));
    */

    samps.push_back(new DSampleFile("d", "d", fin,
                "Nominal_one_btag_cut_el_ntuple", 100, 1.5, "el_tight", "wgt"));
    samps.push_back(new DSampleFile("e", "e", fin,
                "Nominal_one_btag_cut_el_ntuple"));

    DPlot *dp = new DPlot("dp", "dp", 1.0, "el_pt", &samps);

    THStack *st = dp->Plot(5, 0, 100000);

    st->Write();

    fout->Close();

    return 0;
}
