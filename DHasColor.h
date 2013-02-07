#ifndef __DHasColor_h__
#define __DHasColor_h__

class DHasColor {
    protected:
        int fColor;

    public:
        DHasColor(int color=0) : fColor(color) { }
        ~DHasColor() { }

        void SetColor(int color) {
            fColor = color;
        }

        int GetColor() const {
            return fColor;
        }
};


#endif
