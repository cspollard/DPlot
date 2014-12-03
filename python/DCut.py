import ROOT

def mul_cut(c1, c2, name=None):
    c = c1*c2
    if not name:
        c.SetName(c1.GetName() + "_" + c2.GetName())
    else:
        c.SetName(name)

    return c

def combine_cuts(cuts):
    return reduce(mul_cut, cuts)

DCut = ROOT.TCut
