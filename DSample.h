#ifndef __DSample_h__
#define __DSample_h__

#include <vector>
#include <string>
#include <sstream>
#include <iostream>
#include <TFile.h>
#include <TTree.h>
#include <TChain.h>
#include <TH1.h>

class DHasName {
    private:
        std::string fName;

    public:
        DHasName(std::string name) : fName(name) { }
        ~DHasName() { }

        void SetName(std::string name) {
            fName = std::string(name);
        }

        std::string GetName() const {
            return fName;
        }
};

class DHasTitle {
    private:
        std::string fTitle;

    public:
        DHasTitle(std::string title) : fTitle(title) { }
        ~DHasTitle() { }

        void SetTitle(std::string title) {
            fTitle = title;
        }

        std::string GetTitle() const {
            return fTitle;
        }
};

class DHasFile {
    private:
        TFile *fFile;

    public:
        DHasFile(TFile *file) : fFile(file) { }
        ~DHasFile() { }

        void SetFile(TFile *file) {
            fFile = file;
        }

        TFile *GetFile() const {
            return fFile;
        }
};

class DHasTree {
    private:
        TTree *fTree;

    public:
        DHasTree(TTree *tree) : fTree(tree) { }
        ~DHasTree() { }

        void SetTree(TTree *tree) {
            fTree = tree;
        }

        TTree *GetTree() const {
            return fTree;
        }
};

class DHasWeight {
    private:
        std::string fWeight;

    public:
        DHasWeight(std::string wgt) : fWeight(wgt) { }
        ~DHasWeight() { }

        void SetWeight(std::string wgt) {
            fWeight = wgt;
        }

        std::string GetWeight() const {
            return fWeight;
        }
};

class DHasCut {
    private:
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

class DHasCrossSection {
    private:
        double fCrossSection;

    public:
        DHasCrossSection(double xsec) : fCrossSection(xsec) { }
        ~DHasCrossSection() { }

        void SetCrossSection(double xsec) {
            fCrossSection = xsec;
        }

        double GetCrossSection() const {
            return fCrossSection;
        }

        std::string GetCrossSectionString() const {
            std::ostringstream o("");
            o << fCrossSection;
            return o.str();
        }
};

class DHasKFactor {
    private:
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

class DAHasProject {
    public:
        virtual void Project(std::string varexp, TH1 *h) const = 0;
};


class DSampleTree : public DHasName, public DHasTitle,
    public DHasTree, public DHasCrossSection, public DHasKFactor,
    public DHasCut, public DHasWeight, public DAHasProject {

    public:
        DSampleTree(std::string name, std::string title, TTree *tree,
                double xsec=1.0, double kfactor=1.0,
                std::string cut="1.0", std::string weight="1.0") :
            DHasName(name),
            DHasTitle(title),
            DHasTree(tree),
            DHasCrossSection(xsec),
            DHasKFactor(kfactor),
            DHasCut(cut),
            DHasWeight(weight) { }

        virtual void Project(std::string varexp, TH1 *h) const {
            std::string selection = (GetCut() + std::string("*") +
                    GetWeight() + std::string("*") +
                    std::string(GetCrossSectionString()));

            GetTree()->Project(h->GetName(), varexp.c_str(), selection.c_str());
            
            return;
        }
};


class DSampleFile : public DHasFile, public DSampleTree {
    public:
        DSampleFile(std::string name, std::string title, TFile *f,
                std::string treename, double xsec=1.0,
                double kfactor=1.0, std::string cut="1.0",
                std::string weight="1.0") :
            DHasFile(f),
            DSampleTree(name, title,
                    (TTree *) f->Get(treename.c_str()),
                    xsec, kfactor, cut, weight) { }

        ~DSampleFile() { }
};


class DSampleFiles : public DSampleTree {
    public:
        DSampleFiles(std::string name, std::string title,
                const std::vector<std::string> &files,
                std::string treename, double xsec=1.0,
                double kfactor=1.0, std::string cut="1.0",
                std::string weight="1.0") :
            DSampleTree(name, title, (TTree *) (new TChain(treename.c_str())),
                    xsec, kfactor, cut, weight) {

            TChain *c = (TChain *) GetTree();
            for (size_t i = 0; i < files.size(); i++)
                c->Add(files[i].c_str());
        }

        ~DSampleFiles() { }

};

#endif
