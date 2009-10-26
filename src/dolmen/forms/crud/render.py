# -*- coding: utf-8 -*-

import megrok.pagetemplate as pt
from dolmen.forms.crud import Display


class DisplayTemplate(pt.PageTemplate):
    """The basic template for a display form.
    """
    pt.view(Display)
