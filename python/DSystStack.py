from DSystHist import DSystHist
from DUtils import sum_hists, add_hist_quad, get_hist_uncert, \
        set_hist_uncert, hist_subtract
import ROOT

# histogram stack wrapper class that knows about stat and systematic
# uncertainties
class DSystStack:
    def __init__(self, nom, systs):
        self._nom = nom
        self._systs = systs
        return


    def nominal(self):
        # can't make clones of THStack???
        return self._nom


    def nomHist(self, combFunc=add_hist_quad):
        return self.nomHistStatUncert(combFunc)


    def systematics(self, systNames=None):

        if systNames == None:
            systNames = self._systs.keys()

        d = {}
        for k in systNames:
            d[k] = self._systs[k]
            continue

        return d


    def systHists(self, systNames=None):

        if systNames == None:
            systNames = self._systs.keys()

        d = {}
        for k in systNames:
            d[k] = sum_hists(self._systs[k].GetHists())
            continue

        return d


    def scale(self, x):
        for s in [self._nom] + self._systs.values():
            map(lambda h: h.Scale(x), s.GetHists())
        return


    # returns a histogram with the statistical uncertainty on the
    # nominal as the entries.
    # by default combine uncertainties using quadrature sum, but you
    # can provide your own histogram-combining function.
    def statUncert(self, combFunc=add_hist_quad):

        hstatuncert = get_hist_uncert(self._nom.GetHists().At(0))
        for h in self._nom.GetHists():
            huncert = get_hist_uncert(h)
            hstatuncert = combFunc(hstatuncert, huncert)
            continue

        return hstatuncert


    def systUncert(self, combFunc=add_hist_quad,
            systNames=None):

        if systNames == None:
            systNames = self._systs.keys()

        hnom = self.nomHist()
        hsystuncert = hnom.Clone()
        hsystuncert.Reset()

        d = self.systHists(systNames=systNames)
        for k in systNames:
            h = d[k].Clone()
            hist_subtract(h, hnom)
            hsystuncert = combFunc(hsystuncert, h)
            continue

        return hsystuncert


    def statSystUncert(self, statCombFunc=add_hist_quad,
            systCombFunc=add_hist_quad,
            statSystCombFunc=add_hist_quad,
            systNames=None):

        if systNames == None:
            systNames = self._systs.keys()

        hsystuncert = self.systUncert(combFunc=systCombFunc,
                systNames=systNames)
        hstatuncert = self.statUncert(combFunc=statCombFunc)
        return statSystcombFunc(hsystuncert, hstatuncert)


    def nomHistStatUncert(self, combFunc=add_hist_quad):
        hnom = sum_hists(self.nominal().GetHists())
        set_hist_uncert(hnom, self.statUncert(combFunc=combFunc))

        return hnom


    def nomHistSystUncert(self, combFunc=add_hist_quad,
            systNames=None):

        if systNames == None:
            systNames = self._systs.keys()

        hnom = self.nomHist()
        set_hist_uncert(hnom, self.systUncert(combFunc=combFunc,
            systNames=systNames))

        return hnom


    def nomHistStatSystUncert(self, statCombFunc=add_hist_quad,
            systCombFunc=add_hist_quad,
            statSystCombFunc=add_hist_quad,
            systNames=None):

        if systNames == None:
            systNames = self._systs.keys()

        hnom = self.nomHist()
        huncert = self.statSystUncert(statCombFunc=statCombFunc,
                systCombFunc=systCombFunc,
                statSystCombFunc=statSystCombFunc,
                systNames=systNames)

        set_hist_uncert(hnom, huncert)

        return hnom
