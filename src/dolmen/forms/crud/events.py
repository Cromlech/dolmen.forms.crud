# -*- coding: utf-8 -*-

import grokcore.component as grok
from dolmen.content import schema, IContent
from dolmen.forms.base import Fields, IFieldUpdate
from zope.component import getAdapters
from zope.lifecycleevent import IObjectModifiedEvent, IObjectCreatedEvent


@grok.subscribe(IContent, IObjectCreatedEvent)
def notify_fields_creation(ob, event):
    """This handler propagates the ObjectCreatedEvent to a more atomic
    level, by calling an adapter on each field of the schema. This permits
    to actually interact at the field level, after it gets a value for the
    first time.
    """
    schemas = schema.bind().get(ob)
    fields = Fields(*schemas)

    for field_repr in fields:
        field = field_repr._field
        if field.get(ob) != field.missing_value:
            handlers = getAdapters((ob, field), IFieldUpdate)
            for handler in handlers:
                # Iteration through the generator
                pass


@grok.subscribe(IContent, IObjectModifiedEvent)
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
