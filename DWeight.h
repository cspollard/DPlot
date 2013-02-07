#ifndef __DWeight_h__
#define __DWeight_h__

#include <string>

class DWeight {
    private:
        std::string fWeight;

    public:
        DWeight(std::string weight="1.0") :
            fWeight("(" + weight + ")") { }
        ~DWeight() { }

        operator std::string () {
            return fWeight;
        }
};

#endif

