#ifndef __DHasSize_h__
#define __DHasSize_h__

class DHasSize {
    protected:
        int fSize;

    public:
        DHasSize(int size=1) : fSize(size) { }
        ~DHasSize() { }

        void SetSize(int size) {
            fSize = size;
        }

        int GetSize() const {
            return fSize;
        }
};

#endif
