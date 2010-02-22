from dolmen.forms.crud.interfaces import IAdding, IFactoryAdding
from dolmen.forms.crud.interfaces import (
    IFieldsCustomization, IObjectInitializedEvent)
from dolmen.forms.crud.events import ObjectInitializedEvent
from dolmen.forms.crud.addview import Adder
from dolmen.forms.crud.crudforms import Display, Add, Edit, Delete
from dolmen.forms.crud.customize import FieldsCustomizer

from zope.i18nmessageid import MessageFactory
i18n = MessageFactory("dolmen.forms.crud")
