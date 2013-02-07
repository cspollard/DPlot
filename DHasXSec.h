#ifndef __DHasXSec_h__
#define __DHasXSec_h__

#include <string>
#include <sstream>

class DHasXSec {
    protected:
        double fXSec;

    public:
        DHasXSec(double xsec) : fXSec(xsec) { }
        ~DHasXSec() { }

        void SetXSec(double xsec) {
            fXSec = xsec;
        }

        double GetXSec() const {
            return fXSec;
        }

        std::string GetXSecString() const {
            std::ostringstream o("");
            o << fXSec;
            return o.str();
        }
};

#endif
