from collections import namedtuple

DSampleProps = namedtuple("DSampleProps",
        ["title", "line", "marker", "fill"])


DLine = namedtuple("DLine", ["color", "style", "width"])
DMarker = namedtuple("DMarker", ["color", "style", "size"])
DFill = namedtuple("DFill", ["color", "style"])


def setline(h, l):
    h.SetLineColor(l.color)
    h.SetLineStyle(l.style)
    h.SetLineWidth(l.width)

    return h

def setmarker(h, m):
    h.SetMarkerColor(m.color)
    h.SetMarkerStyle(m.style)
    h.SetMarkerSize(m.size)

    return h

def setfill(h, f):
    h.SetFillColor(f.color)
    h.SetFillStyle(f.style)

    return h
