#ifndef __DSample_h__
#define __DSample_h__

#include <vector>
#include <string>
#include <sstream>
#include <iostream>
#include <TFile.h>
#include <TTree.h>
#include <TChain.h>
#include <TH1.h>
#include "DHasName.h"
#include "DHasTitle.h"
#include "DHasTree.h"
#include "DHasWeight.h"
#include "DHasCut.h"
#include "DHasCrossSection.h"
#include "DHasKFactor.h"
#include "DAHasProject.h"

class DSampleTree : public DHasName, public DHasTitle,
    public DHasTree, public DHasCrossSection, public DHasKFactor,
    public DHasCut, public DHasWeight, public DAHasProject {

    public:
        DSampleTree(std::string name, std::string title, TTree *tree,
                double xsec=1.0, double kfactor=1.0,
                std::string cut="1.0", std::string weight="1.0") :
            DHasName(name),
            DHasTitle(title),
            DHasTree(tree),
            DHasCrossSection(xsec),
            DHasKFactor(kfactor),
            DHasCut(cut),
            DHasWeight(weight) { }

        virtual void Project(std::string varexp, TH1 *h) const {
            std::string selection = (GetCut() + std::string("*") +
                    GetWeight() + std::string("*") +
                    GetCrossSectionString());

            GetTree()->Project(h->GetName(), varexp.c_str(), selection.c_str());
            
            return;
        }
};



class DSampleFiles : public DSampleTree {
    public:
        DSampleFiles(std::string name, std::string title,
                const std::vector<std::string> &files,
                std::string treename, double xsec=1.0,
                double kfactor=1.0, std::string cut="1.0",
                std::string weight="1.0") :
            DSampleTree(name, title, (TTree *) (new TChain(treename.c_str())),
                    xsec, kfactor, cut, weight) {

            TChain *c = (TChain *) GetTree();
            for (size_t i = 0; i < files.size(); i++)
                c->Add(files[i].c_str());
        }

        ~DSampleFiles() { }

};

#endif
