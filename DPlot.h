#include <string>
#include <vector>
#include "DSample.h"

std::string ReForm(const char *varexp) {
    // I know this is sloooow.
    size_t i = 0;
    char c;
    std::string s;
    while ((c = varexp[i]) != '\0') {
        if (!isalnum(c))
            s += "_";
        else
            s += c;
    }

    return s;
}

class DPlot : public DHasName,
              public DHasTitle,
              public DHasLumi {
