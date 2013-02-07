#ifndef __DMarker_h__
#define __DMarker_h__

#include "DHasColor.h"
#include "DHasStyle.h"
#include "DHasSize.h"

class DMarker : public DHasColor, public DHasStyle, public DHasSize {
    public:
        DMarker() : DHasColor(), DHasStyle(), DHasSize() { }
        DMarker(int color, int style, int size) :
            DHasColor(color), DHasStyle(style), DHasSize(size) { }
        ~DMarker() { }

        void SetMarker(TH1 *h) {
            h->SetMarkerColor(fColor);
            h->SetMarkerStyle(fStyle);
            h->SetMarkerSize(fSize);

            return;
        }
};

#endif
