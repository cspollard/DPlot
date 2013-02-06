#ifndef __DHasTitle_h__
#define __DHasTitle_h__

class DHasTitle {
    protected:
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

#endif
