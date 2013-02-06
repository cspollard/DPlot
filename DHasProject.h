#ifndef __DAHasProject_h__
#define __DAHasProject_h__

class DAHasProject {
    public:
        virtual void Project(std::string varexp, TH1 *h) const = 0;
};

#endif
