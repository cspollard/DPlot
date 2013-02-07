#ifndef __DHasLine_h__
#define __DHasLine_h__

#include "DLine.h"

class DHasLine {
    protected:
        DLine *fLine;

    public:
        DHasLine(DLine *line) : fLine(line) { }
        ~DHasLine() { }

        void SetLine(DLine *line) {
            fLine = line;
        }

        DLine *GetLine() const {
            return fLine;
        }
};

#endif

