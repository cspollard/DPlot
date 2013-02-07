#ifndef __DHasKFactor_h__
#define __DHasKFactor_h__

#include <string>
#include <sstream>

class DHasKFactor {
    protected:
        double fKFactor;

    public:
        DHasKFactor(double kfac) : fKFactor(kfac) { }
        ~DHasKFactor() { }

        void SetKFactor(double kfac) {
            fKFactor = kfac;
        }

        double GetKFactor() const {
            return fKFactor;
        }

        std::string GetKFactorString() const {
            std::ostringstream o("");
            o << fKFactor;
            return o.str();
        }
};

#endif
