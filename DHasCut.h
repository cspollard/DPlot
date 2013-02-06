#ifndef __DHasCut_h__
#define __DHasCut_h__

class DHasCut {
    protected:
        std::string fCut;

    public:
        DHasCut(std::string cut) : fCut(cut) { }
        ~DHasCut() { }

        void SetCut(std::string cut) {
            fCut = cut;
        }

        std::string GetCut() const {
            return fCut;
        }
};

#endif
