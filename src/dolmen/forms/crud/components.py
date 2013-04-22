# -*- coding: utf-8 -*-

from dolmen.forms.base import Form, DISPLAY
from dolmen.forms.crud import actions as formactions, i18n as _
from dolmen.forms.crud.utils import getFactoryFields, getAllFields
from cromlech.i18n import translate

from dolmen.forms.base import Actions
from zope.cachedescriptors.property import CachedProperty
from zope.i18nmessageid import Message


def title_or_name(obj):
    title = getattr(obj, 'title', None)
    if title is not None:
        return title
    return getattr(obj, '__name__', None)


class Add(Form):
    """The add form itself is not protected. The security is checked on
    'update'. It checks if the 'require' directive of the factored item
    is respected on the context.
    """
    @property
    def label(self):
        name = getattr(self.context.factory, 'name', None)
        if name is not None:
            if isinstance(name, Message):
                name = translate(name, context=self.request)
            return translate(
                _(u"add_action", default="Add: $name",
                  mapping={'name': name}), context=self.request)
        return 'Add'

    @CachedProperty
    def fields(self):
        return getFactoryFields(
            self, self.context.factory, '__parent__', '__name__')

    @CachedProperty
    def actions(self):
        add = formactions.AddAction(_("Add"), self.context.factory)
        return Actions(add, formactions.CancelAction(_("Cancel")))


class Edit(Form):
    """
    """
    ignoreContent = False
    ignoreRequest = False
    actions = Actions(formactions.UpdateAction(_("Update")),
                      formactions.CancelAction(_("Cancel")))

    @property
    def label(self):
        label = _(u"edit_action", default=u"Edit: $name",
                  mapping={"name": title_or_name(self.context)})
        return translate(label, context=self.request)

    @CachedProperty
    def fields(self):
        edited = self.getContentData().getContent()
        return getAllFields(edited, '__parent__', '__name__')


class Display(Form):
    """
    """
    mode = DISPLAY
    ignoreRequest = True
    ignoreContent = False

    @property
    def label(self):
        return title_or_name(self.context)

    @CachedProperty
    def fields(self):
        displayed = self.getContentData().getContent()
        return getAllFields(displayed, '__parent__', '__name__', 'title')


class Delete(Form):
    """A confirmation for to delete an object.
    """
    description = _(u"Are you really sure ?")
    actions = Actions(formactions.DeleteAction(_("Delete")),
                      formactions.CancelAction(_("Cancel")))

    @property
    def label(self):
        label = _(u"delete_action", default=u"Delete: $name",
                  mapping={"name": title_or_name(self.context)})
        return translate(label, context=self.request)
