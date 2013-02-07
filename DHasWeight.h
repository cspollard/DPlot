#ifndef __DHasWeight_h__
#define __DHasWeight_h__

#include "DWeight.h"

class DHasWeight {
    protected:
        DWeight fWeight;

    public:
        DHasWeight(const DWeight &weight=DWeight()) : fWeight(weight) { }
        ~DHasWeight() { }

        void SetWeight(const DWeight &weight) {
            fWeight = weight;
        }

        DWeight GetWeight() const {
            return fWeight;
        }

        void operator << (const DWeight &weight) {
            SetWeight(weight);
            return;
        }
};

#endif
