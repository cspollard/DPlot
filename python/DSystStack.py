from DSystHist import DSystHist
import DUtils
import ROOT

# histogram stack wrapper class that knows about stat and systematic
# uncertainties
class DSystStack:
    # the nominal THStack
    self._nom = None

    self._systs = {}

    def __init__(self, nom, systs):
        self._nom = nom
        self._systs = systs
        return


    def nominal(self):
        return self._nom


    def nomHist(self):
        return sum_hists(list(self._nom.GetHist()))


    def systematics(self):
        return self._systs


    def systHists(self, systNames=self._systs.keys()):
        d = {}
        for k in systNames:
            d[k] = sum_hists(list(self._systs[k].GetHists()))
            continue

        return d


    def scale(self, x):
        for s in [self._nom] + self._systs.items():
            map(lambda h: h.Scale(x), s.Gethists())
        return


    # returns a histogram with the statistical uncertainty on the
    # nominal as the entries.
    # by default combine uncertainties using quadrature sum, but you
    # can provide your own histogram-combining function.
    def statUncert(self, combFunc=DUtils.add_hist_quad):

        hstatuncert = DUtils.get_hist_uncert(self._nom.GetHists().At(0))
        for h in list(self._nom.GetHist())[1:]:
            huncert = DUtils.get_hist_uncert(h)
            hstatuncert = combFunc(hstatuncert, huncert)
            continue

        return hstatuncert


    def systUncert(self, combFunc=DUtils.add_hist_quad,
            systNames=self._systs.keys()):

        hnom = self.nominalHist()
        hsystuncert = hnom.Clone()
        hsysuncert.Reset()

        d = self.systHists(systNames=systNames)
        for k in systNames:
            h = d[k].Clone()
            DUtils.hist_subtract(h, hnom)
            hsystuncert = combFunc(hsystuncert, h)
            continue

        return hsystuncert


    def statSystUncert(self, statCombFunc=DUtils.add_hist_quad,
            systCombFunc=DUtils.add_hist_quad,
            statSystCombFunc=DUtils.add_hist_quad,
            systNames=self._systs.keys()):

        hsystuncert = self.systUncert(combFunc=systCombFunc,
                systNames=systNames)
        hstatuncert = self.statUncert(combFunc=statCombFunc)
        return statSystcombFunc(hsystuncert, hstatuncert)


    self.nomStatUncert = self.nominal


    def nomSystUncert(self, combFunc=DUtils.add_hist_quad,
            systNames=self._systs.keys()):

        hnom = self._nom.Clone()
        set_hist_uncert(hnom, self.systUncert(combFunc=combFunc,
            systNames=systNames))

        return hnom


    def nomStatSystUncert(self, statCombFunc=DUtils.add_hist_quad,
            systCombFunc=DUtils.add_hist_quad,
            statSystCombFunc=DUtils.add_hist_quad,
            systNames=self._systs.keys()):

        hnom = self._nom.Clone()
        hsystuncert = self.systUncert(combFunc=systCombFunc,
                systNames=systNames)
        hstatuncert = self.statUncert(combFunc=statCombFunc)
        set_hist_uncert(hnom,
                statSystCombFunc(hsystuncert, hstatuncert))

        return hnom
