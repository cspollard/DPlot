#ifndef __DHasFill_h__
#define __DHasFill_h__

#include "DFill.h"

class DHasFill {
    protected:
        DFill fFill;

    public:
        DHasFill(const DFill &fill) : fFill(fill) { }
        ~DHasFill() { }

        void SetFill(const DFill &fill) {
            fFill = fill;
        }

        DFill GetFill() const {
            return fFill;
        }

        void operator << (const DFill &fill) {
            SetFill(fill);
            return;
        }
};

#endif
