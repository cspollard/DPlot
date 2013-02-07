#ifndef __DSampleFiles_h__
#define __DSampleFiles_h__

#include <string>
#include <vector>
#include "TChain.h"
#include "DSampleTree.h"

class DSampleFiles : public DSampleTree {
    public:
        DSampleFiles(std::string name, std::string title,
                const std::vector<std::string> &files,
                std::string treename, double xsec=1.0,
                std::string weight="1.0") :
            DSampleTree(name, title, (TTree *) (new TChain(treename.c_str())),
                    xsec, weight) {

            TChain *c = (TChain *) GetTree();
            for (size_t i = 0; i < files.size(); i++)
                c->Add(files[i].c_str());
        }

        ~DSampleFiles() { }

};

#endif
