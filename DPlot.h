#ifndef __DPLOT_H__
#define __DPLOT_H__

#include <string>
#include <vector>
#include "DSampleTree.h"
#include "THStack.h"
#include "TCanvas.h"

class DHasLumi {
    protected:
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
    protected:
        THStack *fStack;

    public:
        DHasStack() : fStack(0) { }
        DHasStack(THStack *stack) : fStack(stack) { }
        ~DHasStack() { }

        void SetStack(THStack *stack) {
            fStack = stack;
        }

        THStack *GetStack() {
            return fStack;
        }
};

class DHasCanvas {
    protected:
        TCanvas *fCanvas;

    public:
        DHasCanvas() : fCanvas(new TCanvas()) { }
        DHasCanvas(TCanvas *canvas) : fCanvas(canvas) { }
        ~DHasCanvas() { }

        void SetCanvas(TCanvas *canvas) {
            fCanvas = canvas;
        }

        TCanvas *GetCanvas() {
            return fCanvas;
        }
};

class DHasVar {
    protected:
        std::string fVar;

    public:
        DHasVar(std::string var) : fVar(var) { }
        ~DHasVar() { }

        void SetVar(std::string var) {
            fVar = var;
        }

        std::string GetVar() {
            return fVar;
        }
};

class DPlot : public DHasName, public DHasTitle, public DHasLumi,
    public DHasVar {

        protected:
            std::vector<DSampleTree *> *fSamples;

        public:
            DPlot(std::string name,
                    std::string title,
                    double lumi,
                    std::string var,
                    std::vector<DSampleTree *> *samples) :
                DHasName(name),
                DHasTitle(title),
                DHasLumi(lumi),
                DHasVar(var),
                fSamples(samples) { }

            ~DPlot () { }

            THStack *Plot(int nbins, double low, double high) const;
            THStack *Plot(int nbins, double bins[]) const;
};

#endif
