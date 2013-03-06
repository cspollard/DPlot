#ifndef __DSampleGroup_h__
#define __DSampleGroup_h__

#include <vector>
#include "DSampleTree.h"

class DSampleGroup : public DSampleTree {
    protected:
        std::vector<DSampleTree *> *fSamps;
        unsigned int fNSamps;
        

    public:
        DSampleGroup(std::string name, std::string title,
                std::vector<DSampleTree *> *samples=new std::vector<DSampleTree *>(0),
                DMarker marker=DMarker(), DFill fill=DFill(),
                DLine line=DLine()) :
            DSampleTree(name, title, 0, 1.0, "1.0", marker, fill,
                    line),
            fSamps(samples),
            fNSamps(samples->size()) { }

        ~DSampleGroup() { }

        virtual void Project(std::string varexp, TH1 *h) const {
            DSampleTree *samp;
            for (unsigned int i = 0; i < fNSamps; i++) {
                samp = fSamps->at(i);
                samp->Project(varexp, h);
            }

            return;
        }

        virtual void AddSample(DSampleTree *dst) {
            // guard against loops.
            if (this == dst)
                return;

            fNSamps++;
            fSamps->push_back(dst);
            return;
        }
};

#endif
