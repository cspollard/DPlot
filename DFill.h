#ifndef __DFill_h__
#define __DFill_h__

#include "DHasColor.h"
#include "DHasStyle.h"

class DFill : public DHasColor, public DHasStyle {
    public:
        DFill() : DHasColor(), DHasStyle() { }
        DFill(int color, int style) :
            DHasColor(color), DHasStyle(style) { }
        ~DFill() { }

        void SetFill(TH1 *h) {
            h->SetFillColor(fColor);
            h->SetFillStyle(fStyle);

            return;
        }
};

#endif
