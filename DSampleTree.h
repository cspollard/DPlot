#ifndef __DSampleTree_h__
#define __DSampleTree_h__

#include <string>
#include "TTree.h"
#include "TH1.h"
#include "DHasName.h"
#include "DHasTitle.h"
#include "DHasTree.h"
#include "DHasWeight.h"
#include "DHasCut.h"
#include "DHasCrossSection.h"
#include "DHasKFactor.h"
#include "DHasMarker.h"
#include "DHasFill.h"
#include "DHasLine.h"
#include "DAHasProject.h"

class DSampleTree : public DHasName, public DHasTitle,
    public DHasTree, public DHasCrossSection, public DHasKFactor,
    public DHasCut, public DHasWeight, public DHasMarker, public DHasFill,
    public DHasLine, public DAHasProject {

    public:
        DSampleTree(std::string name, std::string title, TTree *tree,
                double xsec=1.0, double kfactor=1.0,
                std::string cut="1.0", std::string weight="1.0",
                DMarker marker=DMarker(), DFill fill=DFill(), DLine line=DLine()) :
            DHasName(name),
            DHasTitle(title),
            DHasTree(tree),
            DHasCrossSection(xsec),
            DHasKFactor(kfactor),
            DHasCut(cut),
            DHasWeight(weight),
            DHasMarker(marker),
            DHasFill(fill),
            DHasLine(line) { }

        virtual void Project(std::string varexp, TH1 *h) const {
            std::string selection = GetCut() + "*" +
                    GetWeight() + "*" +
                    GetCrossSectionString() + "*" +
                    GetKFactorString();

            GetTree()->Project(h->GetName(), varexp.c_str(), selection.c_str());
            
            return;
        }
};

#endif
