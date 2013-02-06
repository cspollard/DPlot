#ifndef __DHasKFactor_h__
#define __DHasKFactor_h__

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
};

#endif
