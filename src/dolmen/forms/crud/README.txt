=================
dolmen.forms.crud
=================

`dolmen.forms.crud` is a module which helps developers create their
C.R.U.D forms using `Grok` and `dolmen.forms`. It
provides a collection of base classes to add, edit, and access
content. It provides adapters to customize the fields of a form.


Setting up the components
=========================

Grokking of the package
-----------------------

  >>> from dolmen.forms.crud import testing
  >>> testing.grok('dolmen.forms.crud.events')


Defining some actors
--------------------
   
  >>> import zope.schema
  >>> from zope.interface import implements, Interface
  >>> from zope.location import ILocation, Location


  >>> class IDesertWarrior(Interface):
  ...     """Defines a warrior living in the desert.
  ...     """
  ...     title = zope.schema.TextLine(
  ...         title=u"Name of the warrior",
  ...         default=u"",
  ...         required=True)
  ... 
  ...     water = zope.schema.Int(
  ...         title=u"Number water gallons owned",
  ...         default=1,
  ...         required=True)


  >>> class Sietch(Location):
  ...    """A grotto located on Arrakis.
  ...    """
  ...    def __init__(self):
  ...      self.contents = {}
  ...
  ...    def __getitem__(self, name):
  ...      return self.contents.__getitem__(name)
  ...
  ...    def __contains__(self, name):
  ...      return self.contents.__contains__(name)
  ...
  ...    def __delitem__(self, name):
  ...       return self.contents.__delitem__(name)
  ...
  ...    def keys(self):
  ...       return self.contents.keys()


  >>> class Fremen(Location):
  ...    """Inhabitants on the deep deserts. They live in sietches.
  ...    """
  ...    implements(IDesertWarrior)
  ...
  ...    def __init__(self, title=u"", water=1):
  ...        self.title = title
  ...        self.water = water


Creation of the root
--------------------

  >>> from cromlech.io.interfaces import IPublicationRoot
  >>> from zope.location import Location
  >>> from zope.interface import directlyProvides

  >>> root = Sietch()
  >>> directlyProvides(root, IPublicationRoot)


Adding component
================

`dolmen.forms.crud` provides an abstraction for the 'adding'
action. It allows pluggability at the container level and handles
naming and persistence. This 'adding' action is prototyped by an
interface called `IAdding` and precised in the `IFactoryAdding`.

  >>> from dolmen.forms.crud import IFactoryAdding
  >>> from zope.component.factory import Factory
  >>> from zope.interface import implements
  >>> from zope.interface import verify

  >>> class Adding(object):
  ...     """The component capable of adding objects using a factory
  ...
  ...     objects id are incremental
  ...     """
  ...
  ...     implements(IFactoryAdding)
  ...
  ...     def __init__(self, context, request, factory):
  ...         self.context = context
  ...         self.request = request
  ...         self.factory = factory
  ...
  ...     def add(self, obj):
  ...         id = str(len(self.context.contents) + 1)
  ...         self.context.contents[id] = obj
  ...         obj.__name__ = id
  ...         obj.__parent__ = self.context
  ...         return obj


  >>> verify.verifyClass(IFactoryAdding, Adding)
  True
  >>> factory = Factory(Fremen)

  >>> from cromlech.browser.testing import TestHTTPRequest, TestHTTPResponse

  >>> request = TestHTTPRequest()
  >>> adding = Adding(root, request, factory)
  
  >>> verify.verifyObject(IFactoryAdding, adding)
  True
  

Let's create and register a very basic generic crud
add form, context of the form is our adding component:

  >>> import dolmen.forms.crud as crud
  >>> class AddForm(crud.Add):
  ...     '''Generic add form.
  ...     '''
  ...     responseFactory = TestHTTPResponse

  >>> addform = AddForm(adding, request)
  >>> addform
  <dolmen.forms.crud.tests.AddForm object at ...>

  >>> naib = Fremen()
  >>> added_item = adding.add(naib)
  >>> added_item
  <dolmen.forms.crud.tests.Fremen object at ...>

The created content is correctly located::

  >>> added_item.__parent__ is root
  True


Generic forms
=============

Create
------

The add form implementation is tightly tied to the adding view. As the add
form behavior has been mostly covered above, we'll only test the
presence of the fields and actions on the form itself::

  >>> addform.fields.keys()
  ['title', 'water']
  
  >>> addform.updateForm()
  >>> for action in addform.actions: print action
  <AddAction Add>
  <CancelAction Cancel>


Update
------

An edit form can be registered simply by sublassing the Edit base class::

  >>> class EditForm(crud.Edit):
  ...     '''Generic edit form.
  ...     '''
  ...     responseFactory = TestHTTPResponse

This form registered, we can check if all the fields are ready to be
edited::

  >>> post = TestHTTPRequest(form={
  ...     'form.field.water': '25',
  ...     'form.field.title': u'Stilgar',
  ...     'form.action.update': u'Update'},
  ...	  method='POST')

  >>> editform = EditForm(naib, post)
  >>> editform
  <dolmen.forms.crud.tests.EditForm object at ...>

  >>> editform.update()
  >>> editform.updateForm()
  Traceback (most recent call last):
  ...  
  HTTPFound

  >>> editform.fields.keys()
  ['title', 'water']

As we called updateForm, the values should now be set::

  >>> naib.title
  u'Stilgar'
  >>> naib.water
  25


Read
-----

A special kind of form allows you display your content::

  >>> class DefaultView(crud.Display):
  ...     '''Generic display form.
  ...     '''
  ...     responseFactory = TestHTTPResponse
  
  >>> view = DefaultView(naib, request)
  >>> view
  <dolmen.forms.crud.tests.DefaultView object at ...>

The Display form removes the 'title' from the list of fields. This
particular attribute is used directly by the template::

  >>> view.fields.keys()
  ['water']

A display form has no actions::

  >>> len(view.actions)
  0

`dolmen.forms.crud` provides a very basic template for that form. As
we can see, the title attribute is used as the HTML header (h1) of the
page::

  >>> print view()
  <html>
    <head>
    </head>
    <body>
      <form action="http://localhost/1/" 
            enctype="multipart/form-data" id="form" method="post">
        <h1>1</h1>
        <div class="fields">
          <div class="field">
            <label class="field-label" for="form-field-water">Number water gallons owned</label>
            <span class="field-required" >(required)</span>
            <br />
            25
          </div>
        </div>
      </form>
    </body>
  </html>

Delete
------

A delete form is a simple form with no fields, that only provides a
'confirm' action::

  >>> class DeleteForm(crud.Delete):
  ...     '''Generic delete form.
  ...     '''
  ...     responseFactory = TestHTTPResponse

  >>> deleteform = DeleteForm(naib, request)
  >>> deleteform
  <dolmen.forms.crud.tests.DeleteForm object at ...>

  >>> deleteform.updateForm()
  >>> for action in deleteform.actions: print action
  <DeleteAction Delete>
  <CancelAction Cancel>

  >>> len(deleteform.fields)
  0

When confirmed, the form tries to delete the object::

  >>> post = TestHTTPRequest(form={
  ...     'form.action.delete': u'Delete'},
  ...	  method='POST',
  ...     )

  >>> list(root.keys())
  ['1']

  >>> deleteform = DeleteForm(naib, post)
  >>> deleteform.update()
  >>> deleteform.updateForm()
  Traceback (most recent call last):
  ...  
  HTTPFound
  >>> import sys
  >>> sys.exc_info()[1].location
  'http://localhost'

  >>> from zope.i18n import translate
  >>> translate(deleteform.status, context=post)
  u'The object has been deleted.'

  >>> list(root.keys())
  []
  

Form customization
==================

To customize forms, the usual solution is to subclass them and to work
with the subclass. `dolmen.forms.crud` proposes a new component to
customize your forms. Defined by the `IFieldsCustomization` interface,
it's an adapter that can modify the fields collection.

In a `IFieldsCustomization`, the customization happens at the __call__
level. The forms, while they update the objects fields, query a
`IFieldsCustomization` adapter and call it, giving the fields as an
argument. It must return the new fields collection.

Let's implement an example::

  >>> import grokcore.component

  >>> class RemoveWater(crud.FieldsCustomizer):
  ...    grokcore.component.adapts(Fremen, crud.Add, None)
  ...
  ...    def __call__(self, fields):
  ...       """Alters the form fields"""
  ...       return fields.omit('water')

  >>> verify.verifyClass(crud.IFieldsCustomization, RemoveWater)
  True

We can now register and test the customization::

  >>> grokcore.component.testing.grok_component('custom', RemoveWater)
  True

  >>> adding = Adding(root, request, Factory(Fremen))
  >>> addform = AddForm(adding, request)
  >>> for field in addform.fields: print field
  <TextLineSchemaField Name of the warrior>

We can test a more complex example, returning a brand new instance of
Fields::

  >>> import dolmen.forms.base

  >>> class AddFieldToView(crud.FieldsCustomizer):
  ...    grokcore.component.adapts(Fremen, crud.Display, None)
  ...
  ...    def __call__(self, fields):
  ...       """Returns a new instance of Fields.
  ...       """
  ...       return dolmen.forms.base.Fields(IDesertWarrior)

  >>> grokcore.component.testing.grok_component('viewer', AddFieldToView)
  True

Checking the fields, we should get *all* the fields defined by the
Fremen schema (even the title, unlike the default view)::

  >>> naib = Fremen(title=u'Paul')
  >>> view = DefaultView(naib, request)
  >>> view.fields.keys()
  ['title', 'water']


Events and field updates
========================

When using the generic `dolmen.forms.crud` forms, some events are
triggered for you. They represent the lifecycle of the manipulated object.

To check on all the events triggered, we can set up a simple event
logging list and a generic handler::

  >>> from zope.component import provideHandler
  >>> from zope.lifecycleevent import IObjectModifiedEvent
  >>> logger = []
  
  >>> def event_logger(object, event):
  ...   logger.append(event)

  >>> provideHandler(event_logger, (Fremen, IObjectModifiedEvent))


Editing events
--------------

Let's have the same introspection check with the edit form::

  >>> logger = []

We provide data for the update::

  >>> request = TestHTTPRequest(form={
  ...     'form.field.water': '10',
  ...     'form.field.title': u'Sihaya',
  ...     'form.action.update': u'Update'},
  ...	  method='POST',
  ...     )

  >>> chani = Fremen()
  >>> chani.__name__ = u'Chani'
  >>> chani.__parent__ = root

  >>> editform = EditForm(chani, request)
  >>> editform.update()
  >>> editform.updateForm()
  Traceback (most recent call last):
  ...  
  HTTPFound

We check the trigged events::

  >>> for event in logger: print event
  <...ObjectModifiedEvent object at ...>

In depth, we can check if the updated fields are correctly set in the
event's descriptions::

  >>> for desc in logger[0].descriptions:
  ...   print "%r: %s" % (desc.interface, desc.attributes)
  <InterfaceClass dolmen.forms.crud.tests.IDesertWarrior>: ('water', 'title')

  >>> chani.title
  u'Sihaya'
  >>> chani.water
  10


Field update
------------

`dolmen.forms.base` provides the description of a new component that
can be used to propagate the updating process at the field level:
`IFieldUpdate`. An implementation is available in `dolmen.forms.crud`,
using an event handler, listening on ObjectModifiedEvent and
ObjectCreatedEvent::

  >>> updates = []

  >>> from zope.schema import TextLine
  >>> from zope.interface import implementer
  >>> from dolmen.forms.base import IFieldUpdate
  >>> from grokcore.component import adapts, provides, MultiSubscription

  >>> class UpdateTextfield(MultiSubscription):
  ...     """Logs updates of Title on IDesertWarrior in a list"""
  ...     provides(IFieldUpdate)
  ...     adapts(IDesertWarrior, TextLine)
  ...
  ...     def __init__(self, context, field):
  ...         self.context = context
  ...         self.field = field
  ...
  ...     def __call__(self):
  ...         updates.append((self.context, self.field))

  >>> grokcore.component.testing.grok_component('text', UpdateTextfield)
  True


Using an add form, the IFieldUpdate adapters should be called during an object
creation::

  >>> request = TestHTTPRequest(form={
  ...     'form.field.title': u'Liet',
  ...     'form.action.add': u'Add'},
  ...	  method='POST',
  ...     )

  >>> tabr = Sietch()
  >>> tabr.__name__ = 'Sietch Tabr'
  >>> tabr.__parent__ = root

  >>> adding = Adding(tabr, request, Factory(Fremen))
  >>> addform = AddForm(adding, request)
  >>> addform.update()
  >>> addform.updateForm()
  Traceback (most recent call last):
  ...  
  HTTPFound

  >>> kynes = tabr['1']
  >>> kynes
  <dolmen.forms.crud.tests.Fremen object at ...>
  >>> kynes.title
  u'Liet'  

  >>> print updates
  [(<dolmen.forms.crud.tests.Fremen object at ...>,
    <zope.schema._bootstrapfields.TextLine object at ...>)]


We can do the same thing for the edit form::

  >>> updates = []

  >>> request = TestHTTPRequest(form={
  ...     'form.field.water': '50',
  ...     'form.field.title': u'Imperial weather specialist',
  ...     'form.action.update': u'Update'},
  ...	  method='POST',
  ...     )

  >>> editform = EditForm(kynes, request)
  >>> editform.update()
  >>> editform.updateForm()
  Traceback (most recent call last):
  ...  
  HTTPFound

  >> kynes.title
  u'Imperial weather specialist'

  >>> updates
  [(<dolmen.forms.crud.tests.Fremen object at ...>,
    <zope.schema._bootstrapfields.TextLine object at ...>)]

Updating a field without a registered IFieldUpdate adapter shouldn't do
anything::

 >>> updates = []

  >>> request = TestHTTPRequest(form={
  ...     'form.field.water': '40',
  ...     'form.action.update': u'Update'},
  ...	  method='POST',
  ...     )

  >>> editform = EditForm(kynes, request)
  >>> editform.updateForm()

  >>> updates
  []
