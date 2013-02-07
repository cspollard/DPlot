#ifndef __DHasLine_h__
#define __DHasLine_h__

#include "DLine.h"

class DHasLine {
    protected:
        DLine fLine;

    public:
        DHasLine(const DLine line) : fLine(line) { }
        ~DHasLine() { }

        void SetLine(const DLine line) {
            fLine = line;
        }

        DLine GetLine() const {
            return fLine;
        }

        void operator << (const DLine &line) {
            SetLine(line);
            return;
        }
};

#endif
