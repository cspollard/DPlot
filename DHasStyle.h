#ifndef __DHasStyle_h__
#define __DHasStyle_h__

class DHasStyle {
    protected:
        int fStyle;

    public:
        DHasStyle(int style=0) : fStyle(style) { }
        ~DHasStyle() { }

        void SetStyle(int style) {
            fStyle = style;
        }

        int GetStyle() const {
            return fStyle;
        }
};

#endif

