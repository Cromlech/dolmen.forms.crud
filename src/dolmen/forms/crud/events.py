# -*- coding: utf-8 -*-

import grokcore.component as grok

from dolmen.content import IBaseContent
from dolmen.forms.base import IFieldUpdate
from dolmen.forms.crud import IObjectInitializedEvent

from zope.component import getAdapters
from zope.lifecycleevent import ObjectModifiedEvent, ObjectCreatedEvent


class ObjectInitializedEvent(ObjectCreatedEvent):
    """An object has been created and initialized with form values.
    """
    grok.implements(IObjectInitializedEvent)
    
    def __init__(self, object, *descriptions) :
        super(ObjectInitializedEvent, self).__init__(object)
        self.descriptions = descriptions


@grok.subscribe(IBaseContent, ObjectModifiedEvent)
@grok.subscribe(IBaseContent, ObjectInitializedEvent)
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
