import DUtils
import ROOT

class DSystHist:
    self._name = ""
    self._title = ""

    # nominal holds the statistical uncertainty
    self._nom = None

    # systematic histograms
    self._systs = {}

    def __init__(self, name, title, nom, systs):
        self.name = name
        self.title = title
        self.nom = nom
        self.systs = syst
        return

    def nominal(self):
        return self._nom

    def systematics(self):
        return self._systs

    def name(self):
        return self._name

    def title(self):
        return self._title

    def scale(self, x):
        map(lambda h: h.Scale(x), [self._nom] + self._systs.items())
        return

    # returns a histogram with the statistical uncertainty on the
    # nominal as entries.
    def statUncert(self):
        return DUtils.get_hist_uncert(self._nom)

    # returns a histogram with the systematic uncertainty on the
    # nominal as entries.
    # by default combine systematics using quadrature sum, but you can
    # provide your own histogram-combining function.
    # by default all systematics are included, but you can specify
    # which should be.
    def systUncert(self, combFunc=DUtils.add_hist_quad,
            systNames=self._systs.keys()):

        hsyst = self._nom.Clone()
        hist_subtract(hsyst, self._nom)
        for k in systNames:
            h = self._systs[k].Clone()
            DUtils.hist_subtract(h, self_nom)
            hsyst = combFunc(hsyst, h)

        return hsyst


    # returns a histogram with the systematic+statistical uncertainty
    # on the nominal as entries.
    # by default combine systematics using quadrature sum, but you can
    # provide your own histogram-combining function.
    # by default combine statistical and systematic uncertainties
    # using quadrature sum, but you can provide your own
    # histogram-combining function.
    # by default all systematics are included, but you can specify
    # which should be.
    def statSystUncert(self, systCombFunc=DUtils.add_hist_quad,
            statSystCombFunc=DUtils.add_hist_quad,
            systNames=self._systs.keys()):

        hsystuncert = self.systUncert(combFunc=systCombFunc,
                systNames=systNames)
        hstatuncert = self.statUncert()
        return statSystcombFunc(hsystuncert, hstatuncert)


    # returns a histogram with nominal entries and systematic
    # uncertainty.
    # by default combine systematics using quadrature sum, but you can
    # provide your own histogram-combining function.
    # by default all systematics are included, but you can specify
    # which should be.
    def nomSystUncert(self, combFunc=DUtils.add_hist_quad,
            systNames=self._systs.keys()):

        hnom = self._nom.Clone()
        set_hist_uncert(hnom, self.systUncert(combFunc=combFunc,
            systNames=systNames))

        return hnom

    self.nomStatUncert = self.nominal

    # returns a histogram with nominal entries and the
    # systematic+statistical uncertainty.
    # by default combine systematics using quadrature sum, but you can
    # provide your own histogram-combining function.
    # by default combine statistical and systematic uncertainties
    # using quadrature sum, but you can provide your own
    # histogram-combining function.
    # by default all systematics are included, but you can specify
    # which should be.
    def nomStatSystUncert(self, systCombFunc=DUtils.add_hist_quad,
            statSystCombFunc=DUtils.add_hist_quad,
            systNames=self._systs.keys()):

        hnom = self._nom.Clone()
        hsystuncert = self.systUncert(combFunc=systCombFunc,
                systNames=systNames)
        hstatuncert = self.statUncert()
        set_hist_uncert(hnom,
                statSystCombFunc(hsystuncert, hstatuncert))

        return hnom
