#ifndef __DHasMarker_h__
#define __DHasMarker_h__

#include "DMarker.h"

class DHasMarker {
    protected:
        DMarker *fMarker;

    public:
        DHasMarker(DMarker *marker) : fMarker(marker) { }
        ~DHasMarker() { }

        void SetMarker(DMarker *marker) {
            fMarker = marker;
        }

        DMarker *GetMarker() const {
            return fMarker;
        }
};

#endif
