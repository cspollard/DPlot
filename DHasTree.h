#ifndef __DHasTree_h__
#define __DHasTree_h__

class DHasTree {
    protected:
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

#endif
