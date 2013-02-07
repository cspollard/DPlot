#ifndef __DSampleTree_h__
#define __DSampleTree_h__

#include <string>
#include "TTree.h"
#include "TH1.h"
#include "DHasName.h"
#include "DHasTitle.h"
#include "DHasTree.h"
#include "DHasWeight.h"
#include "DHasCrossSection.h"
#include "DHasMarker.h"
#include "DHasFill.h"
#include "DHasLine.h"
#include "DAHasProject.h"

class DSampleTree : public DHasName, public DHasTitle,
    public DHasTree, public DHasCrossSection,
    public DHasWeight, public DHasMarker, public DHasFill,
    public DHasLine, public DAHasProject {

    public:
        DSampleTree(std::string name, std::string title, TTree *tree,
                double xsec=1.0, std::string weight="1.0",
                DMarker marker=DMarker(), DFill fill=DFill(), DLine line=DLine()) :
            DHasName(name),
            DHasTitle(title),
            DHasTree(tree),
            DHasCrossSection(xsec),
            DHasWeight(weight),
            DHasMarker(marker),
            DHasFill(fill),
            DHasLine(line) { }

        virtual void Project(std::string varexp, TH1 *h) const {
            std::string wgt = GetWeight() + "*" +
                    GetCrossSectionString();

            GetTree()->Project(h->GetName(), varexp.c_str(), wgt.c_str());
            
            return;
        }
};

#endif
