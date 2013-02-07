#include "DPlot.h"

THStack *DPlot::Plot(int nbins, double bins[]) const {
    unsigned int nh = fSamples->size();
    THStack *stack = new THStack((fName + "_" + fVar).c_str(),
            (fName + "_" + fVar).c_str());

    DSampleTree *s;
    for (unsigned int ih = 0; ih < nh; ih++) {
        s = fSamples->at(ih);

        TH1D *htmp = new TH1D((s->GetName() + "_" + fVar).c_str(),
                s->GetTitle().c_str(), nbins, bins);

        s->GetMarker().SetMarker(htmp);
        s->GetFill().SetFill(htmp);
        s->GetLine().SetLine(htmp);

        s->Project(fVar, htmp);

        stack->Add(htmp);
    }

    return stack;
}

THStack *DPlot::Plot(int nbins, double low, double high) const {
    double bins[nbins];
    double diff = (high-low)/nbins;
    bins[0] = low;
    for (int ib = 1; ib < nbins+1; ib++)
        bins[ib] = bins[ib-1] + diff;

    return Plot(nbins, bins);
}

std::string ReForm(const char *varexp) {
    // I know this is sloooow.
    size_t i = 0;
    char c;
    std::string s;
    while ((c = varexp[i]) != '\0') {
        if (!isalnum(c))
            s += "_";
        else
            s += c;
    }

    return s;
}

