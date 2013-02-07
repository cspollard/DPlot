#ifndef __DHasWeight_h__
#define __DHasWeight_h__

class DHasWeight {
    protected:
        std::string fWeight;

    public:
        DHasWeight(std::string wgt) : fWeight("(" + wgt + ")") { }
        ~DHasWeight() { }

        void SetWeight(std::string wgt) {
            fWeight = "(" + wgt + ")";
        }

        std::string GetWeight() const {
            return fWeight;
        }
};

#endif
