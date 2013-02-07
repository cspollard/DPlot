#ifndef __DLine_h__
#define __DLine_h__

#include "DHasColor.h"
#include "DHasStyle.h"
#include "DHasSize.h"

class DLine : public DHasColor, public DHasStyle, public DHasSize {
    public:
        DLine() : DHasColor(), DHasStyle(), DHasSize() { }
        DLine(int color, int style, int size) :
            DHasColor(color), DHasStyle(style), DHasSize(size) { }
        ~DLine() { }

        void SetLine(TH1 *h) {
            h->SetLineColor(fColor);
            h->SetLineStyle(fStyle);
            h->SetLineWidth(fSize);

            return;
        }
};

#endif
