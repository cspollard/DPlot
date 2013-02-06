// main.cxx

#include <vector>
#include "TFile.h"
#include "DSampleTree.h"
#include "DPlot.h"

int main(int argc, char *argv[]) {
    if (argc < 2)
        return 0;

    TFile *fin = new TFile(argv[1]);
    TTree *tin = (TTree *) fin->Get("Nominal_one_btag_cut_el_ntuple");

    TFile *fout = new TFile("out.root", "recreate");
    std::vector<DSampleTree *> samps;

    samps.push_back(new DSampleTree("d", "d", tin));
    samps.push_back(new DSampleTree("e", "e", tin));

    DPlot *dp = new DPlot("dp", "dp", 1.0, "el_pt", &samps);

    THStack *st = dp->Plot(5, 0, 100000);

    st->Write();

    fout->Close();

    return 0;
}
