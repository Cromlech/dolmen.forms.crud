# -*- coding: utf-8 -*-

import megrok.z3cform
import grokcore.component as grok
from grokcore.security import require

import dolmen.content as content
from dolmen.forms.crud import interfaces as crud
from dolmen.forms.crud.utils import queryClassMultiAdapter

from zope.event import notify
from zope.lifecycleevent import Attributes, ObjectCreatedEvent
from zope.i18nmessageid import MessageFactory
from zope.security.interfaces import Unauthorized
from zope.security.management import checkPermission
from zope.cachedescriptors.property import CachedProperty
from zope.component import queryMultiAdapter, getUtility

_ = MessageFactory("dolmen.forms")


class Add(megrok.z3cform.PageAddForm):
    """The add form itself is not protected. The security is checked on
    'update'. It checks if the 'require' directive of the factored item
    is respected on the context.
    """
    grok.baseclass()
    grok.name('dolmen.add')
    grok.context(crud.IAdding)

    form_name = _(u"Add")

    @property
    def label(self):
        return self.factory.title

    @CachedProperty
    def fields(self):
        ifaces = self.factory.getSchema()
        fields = megrok.z3cform.field.Fields(*ifaces).omit('__parent__')
        
        modifier = queryClassMultiAdapter(
            (self.factory.factory, self, self.request),
            self.context,
            crud.IFieldsCustomization
            )

        if modifier is not None:
            return modifier(fields)
        return fields

    def nextURL(self):
        return self.url(self.context.nextURL())

    def add(self, object):
        return self.context.add(object)

    def create(self, data):
        obj = self.factory()
        notify(ObjectCreatedEvent(obj))
        megrok.z3cform.apply_data_event(self, obj, data)
        return obj

    def update(self):
        content_name = self.context.content_name
        self.factory = getUtility(content.IFactory, name=content_name)
        permission = require.bind().get(self.factory.factory)

        # Check explicitly the permission on the context.
        if not checkPermission(permission, self.context):
            raise Unauthorized(u"You don't have the permission to add %r" %
                               content)
        
        megrok.z3cform.PageAddForm.update(self)

    @megrok.z3cform.button.buttonAndHandler(_('Save'), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        obj = self.createAndAdd(data)
        if obj is not None:
            self.redirect(self.url(obj))


class Edit(megrok.z3cform.PageEditForm):
    grok.baseclass()
    grok.context(content.IBaseContent)
    megrok.z3cform.extends(megrok.z3cform.PageEditForm)
    
    form_name = _(u"Edit")

    @property
    def label(self):
        return _(u"edit_action", mapping={"name": self.context.title})

    @CachedProperty
    def fields(self):
        iface = content.schema.bind().get(self.context)
        fields = megrok.z3cform.field.Fields(*iface).omit('__parent__')
        modifier = queryMultiAdapter(
            (self.context, self, self.request),
            crud.IFieldsCustomization
            )
        if modifier is not None:
            return modifier(fields)
        return fields

    def nextURL(self):
        return self.redirect(self.url(self.context))

    @megrok.z3cform.button.buttonAndHandler(_('Apply'), name='apply')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        changes = megrok.z3cform.apply_data_event(self, self.context, data)
        if changes:
            self.flash(self.successMessage)
        else:
            self.flash(self.noChangesMessage)
        self.redirect(self.url(self.context))


class Display(megrok.z3cform.PageDisplayForm):
    grok.baseclass()
    grok.context(content.IBaseContent)

    ignoreContext = False

    @property
    def label(self):
        return self.context.title

    @CachedProperty
    def fields(self):
        iface = content.schema.bind().get(self.context)
        fields = megrok.z3cform.field.Fields(*iface).omit('__parent__')
        modifier = queryMultiAdapter(
            (self.context, self, self.request),
            crud.IFieldsCustomization
            )
        if modifier is not None:
            return modifier(fields)
        return fields
