# -*- coding: utf-8 -*-

from dolmen.location import get_absolute_url
from dolmen.forms.base import Action
from dolmen.forms.base.markers import SUCCESS, FAILURE
from dolmen.forms.base.utils import set_fields_data, apply_data_event
from dolmen.forms.crud import i18n as _
from zope.event import notify
from zope.lifecycleevent import ObjectCreatedEvent
from zope.location import ILocation


def message(message):
    # This needs to be implemented
    pass


class CancelAction(Action):
    """Cancel the current form and return on the default content view.
    """

    def __call__(self, form):
        content = form.getContentData().getContent()
        form.response.redirect(get_absolute_url(content, form.request))
        return SUCCESS


class AddAction(Action):
    """Add action for an IAdding context.
    """

    def __init__(self, title, factory):
        super(AddAction, self).__init__(title)
        self.factory = factory

    def __call__(self, form):
        data, errors = form.extractData()
        if errors:
            form.submissionError = errors
            return FAILURE

        obj = self.factory()
        set_fields_data(form.fields, obj, data)
        notify(ObjectCreatedEvent(obj))
        form.context.add(obj)

        message(_(u"Content created"))
        form.response.redirect(get_absolute_url(obj, form.request))
        return SUCCESS


class UpdateAction(Action):
    """Update action for any locatable object.
    """

    def __call__(self, form):
        data, errors = form.extractData()
        if errors:
            form.submissionError = errors
            return FAILURE

        apply_data_event(form.fields, form.getContentData(), data)
        message(_(u"Content updated"))
        form.response.redirect(get_absolute_url(form.context, form.request))
        return SUCCESS


class DeleteAction(Action):
    """Delete action for any locatable context.
    """
    successMessage = _(u"The object has been deleted.")
    failureMessage = _(u"This object could not be deleted.")

    def available(self, form):
        content = form.getContentData().getContent()
        if ILocation.providedBy(content):
            container = content.__parent__
            return (hasattr(container, '__delitem__') and
                    hasattr(container, '__contains__'))
        return False

    def __call__(self, form):
        content = form.getContentData().getContent()

        if ILocation.providedBy(content):
            container = content.__parent__
            name = content.__name__
            if name in container:
                try:
                    del container[name]
                    form.status = self.successMessage
                    message(form.status)
                    form.response.redirect(
                        get_absolute_url(container, form.request))
                    return SUCCESS
                except ValueError:
                    pass

        form.status = self.failureMessage
        message(form.status)
        form.response.redirect(get_absolute_url(content, form.request))
        return FAILURE
