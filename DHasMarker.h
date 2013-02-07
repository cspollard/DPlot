#ifndef __DHasMarker_h__
#define __DHasMarker_h__

#include "DMarker.h"

class DHasMarker {
    protected:
        DMarker fMarker;

    public:
        DHasMarker(const DMarker &marker) : fMarker(marker) { }
        ~DHasMarker() { }

        void SetMarker(const DMarker &marker) {
            fMarker = marker;
        }

        DMarker GetMarker() const {
            return fMarker;
        }

        void operator << (const DMarker &marker) {
            SetMarker(marker);
            return;
        }
};


#endif
