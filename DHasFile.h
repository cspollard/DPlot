#ifndef __DHasFile_h__
#define __DHasFile_h__

class DHasFile {
    protected:
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

#endif
