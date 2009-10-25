# -*- coding: utf-8 -*-

import grokcore.component as grok
from zope.component import getAdapters
from zope.lifecycleevent import ObjectModifiedEvent
from dolmen.content import IBaseContent
from dolmen.forms.base import IFieldUpdate


@grok.subscribe(IBaseContent, ObjectModifiedEvent)
def notify_fields_update(ob, event):
    """This handler propagates the ObjectModifiedEvent to a more atomic
    level, by calling an adapter on each modified field. This permits to
    actually interact at the field level, after it gets modified.
    """
    for desc in event.descriptions:
        for name in desc.attributes:
            field = desc.interface[name]
            handlers = getAdapters((ob, field), IFieldUpdate)
            for handler in handlers:
                # Iteration through the generator
                pass
