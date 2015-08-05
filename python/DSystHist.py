from DUtils import sum_hists, add_hist_quad, get_hist_uncert, \
        set_hist_uncert, hist_subtract
import ROOT

# histogram wrapper class that knows about stat and systematic
# uncertainties
class DSystHist:
    def __init__(self, nom, systs):
        # nominal holds the statistical uncertainty
        self._nom = nom

        # systematic histograms
        self._systs = systs
        return


    def nominal(self):
        return self._nom


    def systematics(self):
        return self._systs


    def scale(self, x):
        map(lambda h: h.Scale(x), [self._nom] + self._systs.values())
        return


    # returns a histogram with the statistical uncertainty on the
    # nominal as entries.
    def statUncert(self):
        return get_hist_uncert(self._nom)


    # returns a histogram with the systematic uncertainty on the
    # nominal as entries.
    # by default combine systematics using quadrature sum, but you can
    # provide your own histogram-combining function.
    # by default all systematics are included, but you can specify
    # which should be.
    def systUncert(self, combFunc=add_hist_quad,
            systNames=None):

        if systNames == None:
            systNames = self._systs.keys()

        hsystuncert = self._nom.Clone()
        hsystuncert.Reset()
        for k in systNames:
            h = self._systs[k].Clone()
            hist_subtract(h, self._nom)
            hsystuncert = combFunc(hsystuncert, h)

        return hsystuncert


    # returns a histogram with the systematic+statistical uncertainty
    # on the nominal as entries.
    # by default combine systematics using quadrature sum, but you can
    # provide your own histogram-combining function.
    # by default combine statistical and systematic uncertainties
    # using quadrature sum, but you can provide your own
    # histogram-combining function.
    # by default all systematics are included, but you can specify
    # which should be.
    def statSystUncert(self, systCombFunc=add_hist_quad,
            statSystCombFunc=add_hist_quad,
            systNames=None):

        if systNames == None:
            systNames = self._systs.keys()

        hsystuncert = self.systUncert(combFunc=systCombFunc,
                systNames=systNames)
        hstatuncert = self.statUncert()
        return statSystcombFunc(hsystuncert, hstatuncert)


    def nomStatUncert(self):
        return self.nominal().Clone()


    # returns a histogram with nominal entries and systematic
    # uncertainty.
    # by default combine systematics using quadrature sum, but you can
    # provide your own histogram-combining function.
    # by default all systematics are included, but you can specify
    # which should be.
    def nomSystUncert(self, combFunc=add_hist_quad,
            systNames=None):

        if systNames == None:
            systNames = self._systs.keys()

        hnom = self._nom.Clone()
        set_hist_uncert(hnom, self.systUncert(combFunc=combFunc,
            systNames=systNames))

        return hnom


    # returns a histogram with nominal entries and the
    # systematic+statistical uncertainty.
    # by default combine systematics using quadrature sum, but you can
    # provide your own histogram-combining function.
    # by default combine statistical and systematic uncertainties
    # using quadrature sum, but you can provide your own
    # histogram-combining function.
    # by default all systematics are included, but you can specify
    # which should be.
    def nomStatSystUncert(self, systCombFunc=add_hist_quad,
            statSystCombFunc=add_hist_quad,
            systNames=None):

        if systNames == None:
            systNames = self._systs.keys()
        hnom = self._nom.Clone()
        hsystuncert = self.systUncert(combFunc=systCombFunc,
                systNames=systNames)
        hstatuncert = self.statUncert()
        set_hist_uncert(hnom,
                statSystCombFunc(hsystuncert, hstatuncert))

        return hnom
