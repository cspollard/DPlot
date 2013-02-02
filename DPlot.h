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

class DHasLumi {
    private:
        double fLumi;

    public:
        DHasLumi(double lumi) : fLumi(lumi) { }
        ~DHasLumi() { }

        void SetLumi(double lumi) {
            fLumi = lumi;
        }

        double GetLumi() {
            return fLumi;
        }
};

class DHasStack {
    private:
        THStack *fStack;

    public:
        DHasStack(THStack *stack) : fStack(stack) { }
        ~DHasStack() { }

        void SetStack(THStack *stack) {
            fStack = stack;
        }

        THStack *GetStack() {
            return fStack;
        }
};

class DPlot : public DHasName,
              public DHasTitle,
              public DHasLumi,
              public DHasStack,
              public DHasCanvas {

      public:
          DPlot (std::string name,
                  std::string title,
                  std::vector<DSampleTree *> samples,
                  TCanvas *canvas) { }

};
