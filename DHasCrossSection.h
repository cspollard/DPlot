#ifndef __DHasCrossSection_h__
#define __DHasCrossSection_h__

#include <sstream>

class DHasCrossSection {
    protected:
        double fCrossSection;

    public:
        DHasCrossSection(double xsec) : fCrossSection(xsec) { }
        ~DHasCrossSection() { }

        void SetCrossSection(double xsec) {
            fCrossSection = xsec;
        }

        double GetCrossSection() const {
            return fCrossSection;
        }

        std::string GetCrossSectionString() const {
            std::ostringstream o("");
            o << fCrossSection;
            return o.str();
        }
};

#endif
