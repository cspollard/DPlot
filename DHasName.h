#ifndef __DHasName_h__
#define __DHasName_h__

#include <string>

class DHasName {
    protected:
        std::string fName;

    public:
        DHasName(std::string name) : fName(name) { }
        ~DHasName() { }

        void SetName(std::string name) {
            fName = name;
        }

        std::string GetName() const {
            return fName;
        }
};

#endif
