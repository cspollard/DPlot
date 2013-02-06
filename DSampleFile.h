#ifndef __DSampleFile_h__
#define __DSampleFile_h__

#include <string>
#include "TFile.h"
#include "DHasFile.h"
#include "DSampleTree.h"

class DSampleFile : public DHasFile, public DSampleTree {
    public:
        DSampleFile(std::string name, std::string title, TFile *f,
                std::string treename, double xsec=1.0,
                double kfactor=1.0, std::string cut="1.0",
                std::string weight="1.0") :
            DHasFile(f),
            DSampleTree(name, title,
                    (TTree *) f->Get(treename.c_str()),
                    xsec, kfactor, cut, weight) { }

        ~DSampleFile() { }
};

#endif
