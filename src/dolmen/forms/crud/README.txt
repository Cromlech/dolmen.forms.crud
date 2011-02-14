=================
dolmen.forms.crud
=================

`dolmen.forms.crud` is a module which helps developers create their
C.R.U.D forms using `Grok`, `zeam.form` and `dolmen.content`. It
provides a collection of base classes to add, edit, and access
content. It provides adapters to customize the fields of a form.


Adding view
===========

`dolmen.forms.crud` provides an abstraction for the 'adding'
action. It allows pluggability at the container level and handles
naming and persistence. More explicitly, it's a named adapter that
will query the add form, check the constraints, choose a name (using a
INameChooser) and finally, if everything went smoothly, add it on the
context.

A base adding view is registered out-of-the-box as a named traversable
adapter called 'add'. It uses the following pattern:
++add++factory_name. `factory_name` must be the name of a
`dolmen.content.IFactory` component.

Let's first create a container in which we'll test the adding view::

  >>> import dolmen.content
  >>> from dolmen.forms.crud.tests import Sietch

  >>> sietch = Sietch()
  >>> dolmen.content.IContent.providedBy(sietch)
  True
  
  >>> from zope.site.hooks import getSite
  >>> root = getSite()
  >>> root['sietch'] = sietch

With the container created, the adding view should be available and
operational. Let's have a quick overview::
    
  >>> from zope.component import getMultiAdapter
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> addingview = getMultiAdapter((sietch, request), name='add')
  >>> addingview
  <dolmen.forms.crud.addview.Adder object at ...>


The adding view component explicitly checks the security requirement
on the factory. To test that behavior, we set up two
accounts. 'zope.manager' has all the permissions granted while
'zope.manfred' only has the 'zope.View' credentials. Our factory
explicitly requires a 'zope.ManageContent' permission to be
called. Let's try to access it with Manfred::

  >>> import zope.security.management as security  
  >>> from zope.security.testing import Principal, Participation

  >>> manager = Principal('zope.manager', 'Manager')
  >>> manfred = Principal('zope.manfred', 'Manfred')

  >>> security.newInteraction(Participation(manfred))
  >>> addingview.traverse('fremen', [])
  Traceback (most recent call last):
  ...
  Unauthorized: <class 'dolmen.forms.crud.tests.Fremen'> requires the 'zope.ManageContent' permission.

  >>> security.endInteraction()

Manfred is not authorized, however Manager should successfully be able
to access the addingview::

  >>> security.newInteraction(Participation(manager))
  >>> addingview.traverse('fremen', [])
  Traceback (most recent call last):
  ...
  NotFound: Object: <dolmen.forms.crud.tests.Sietch object at ...>, name: 'fremen'

The adding view is available for our item. Though, as we have no add form
registered, a NotFound error will be raised if we try to access our
current factory.

Let's create and register a very basic generic crud
add form::

  >>> import dolmen.forms.crud as crud
  >>> class AddForm(crud.Add):
  ...     '''Generic add form.
  ...     '''
  
  >>> import grokcore.component
  >>> grokcore.component.testing.grok_component('addform', AddForm)
  True

  >>> addform = addingview.traverse('fremen', [])
  >>> addform
  <dolmen.forms.crud.tests.AddForm object at ...>

Our AddForm is returned as we traverse toward the factory
'fremen'.

Perfect. Our adding view is ready to be used. Before testing the AddForm
itself, let's have a try at the `add` method::

  >>> from dolmen.forms.crud.tests import Fremen

  >>> naib = Fremen()
  >>> added_item = addingview.add(naib)
  >>> added_item
  <dolmen.forms.crud.tests.Fremen object at ...>

The created content is correctly located and persisted::

  >>> added_item.__name__
  u'Fremen'
  >>> added_item.__parent__ is sietch
  True

As a matter of fact, a IAdding component should always be
locatable. Conveniently, you can access the location information::

  >>> addingview.__parent__
  <dolmen.forms.crud.tests.Sietch object at ...>
  >>> addingview.__name__
  u''

The `add` method checks if the constraints are respected. If the
container has defined restrictions or if some interface contract is
violated, we get an error::

  >>> from dolmen.forms.crud.tests import Harkonnen

  >>> rabban = Harkonnen()
  >>> addingview.add(rabban)
  Traceback (most recent call last):
  ...
  InvalidItemType: (<...Sietch object at ...>, <...Harkonnen object at ...>, (<InterfaceClass dolmen.forms.crud.tests.IDesertWarrior>,))

The `add` method of the adding view can be called from the AddForm to delegate
the adding operation. The generic adding view already handles the common
operations such as naming and persistence.


Generic forms
=============


`dolmen.forms.crud` provides a set of ready-to-use base classes that
will auto-generate forms based on `dolmen.content` schemas.

`dolmen.forms.crud` forms are layout aware (see `megrok.layout` for
more info). Therefore, we need to register a basic layout in order to
render our forms::

  >>> from megrok.layout import Layout
  >>> from zope.interface import Interface

  >>> class GenericLayout(Layout):
  ...     grokcore.component.context(Interface)
  ...
  ...     def render(self):
  ...         return self.view.content()

  >>> grokcore.component.testing.grok_component('layout', GenericLayout)
  True

The context of the tests is our previously created content::

  >>> naib
  <dolmen.forms.crud.tests.Fremen object at ...>
  >>> naib.__parent__
  <dolmen.forms.crud.tests.Sietch object at ...>


Create
------

The add form implementation is tightly tied to the adding view. As the add
form behavior has been mostly covered above, we'll only test the
presence of the fields and the label on the form itself::

  >>> addform = addingview.traverse('fremen', [])
  >>> addform
  <dolmen.forms.crud.tests.AddForm object at ...>

  >>> print addform.label
  Add: Fremen Warrior

  >>> addform.fields.keys()
  ['title', 'water']
  
  >>> addform.updateForm()
  >>> for action in addform.actions: print action
  <AddAction Add>
  <CancelAction Cancel>

  >>> security.endInteraction()

Update
------

An edit form can be registered simply by sublassing the Edit base class::

  >>> class EditForm(crud.Edit):
  ...     '''Generic edit form.
  ...     '''

  >>> grokcore.component.testing.grok_component('editform', EditForm)
  True

By default, the registered name of an Edit form is 'edit'::

  >>> grokcore.component.name.bind().get(EditForm)
  'edit'

This form registered, we can check if all the fields are ready to be
edited::

  >>> post = TestRequest(form={
  ...     'form.field.water': '25',
  ...     'form.field.title': u'Stilgar',
  ...     'form.action.update': u'Update'},
  ...	  REQUEST_METHOD='POST',
  ...     )

  >>> security.newInteraction(post)

  >>> editform = getMultiAdapter((naib, post), name='edit')
  >>> editform
  <dolmen.forms.crud.tests.EditForm object at ...>

  >>> editform.updateForm()
  >>> for action in editform.actions: print action
  <UpdateAction Update>
  <CancelAction Cancel>

  >>> editform.fields.keys()
  ['title', 'water']

The values should now be set::

  >>> naib.title
  u'Stilgar'
  >>> naib.water
  25

  >>> security.endInteraction()

Read
-----

A special kind of form allows you display your content::

  >>> class DefaultView(crud.Display):
  ...     '''Generic display form.
  ...     '''
  
  >>> grokcore.component.testing.grok_component('display', DefaultView)
  True

  >>> security.newInteraction(TestRequest())

  >>> view = getMultiAdapter((naib, request), name='defaultview')
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
  <form action="http://127.0.0.1" method="post" enctype="multipart/form-data">
    <h1>Stilgar</h1>
    <div class="fields">
      <div class="field">
        <label class="field-label" for="form-field-water">Number water gallons owned</label>
        <span class="field-required">(required)</span>
        25
      </div>
    </div>
  </form>

  >>> security.endInteraction()

Delete
------

A delete form is a simple form with no fields, that only provides a
'confirm' action::

  >>> class DeleteForm(crud.Delete):
  ...     '''Generic delete form.
  ...     '''

  >>> grokcore.component.testing.grok_component('delete_form', DeleteForm)
  True

  >>> deleteform = getMultiAdapter((naib, request), name='deleteform')
  >>> deleteform
  <dolmen.forms.crud.tests.DeleteForm object at ...>

  >>> deleteform.updateForm()
  >>> for action in deleteform.actions: print action
  <DeleteAction Delete>
  <CancelAction Cancel>

  >>> len(deleteform.fields)
  0

When confirmed, the form tries to delete the object::

  >>> post = TestRequest(form={
  ...     'form.action.delete': u'Delete'},
  ...	  REQUEST_METHOD='POST',
  ...     )

  >>> security.newInteraction(post)

  >>> list(sietch.keys())
  [u'Fremen']

  >>> deleteform = getMultiAdapter((naib, post), name='deleteform')
  >>> deleteform.updateForm()
  
  >>> from zope.i18n import translate
  >>> translate(deleteform.status, context=post)
  u'The object has been deleted.'

  >>> list(sietch.keys())
  []

  >>> deleteform.response.getStatus()
  302
  >>> deleteform.response.getHeader('location')
  'http://127.0.0.1/sietch'

  >>> security.endInteraction()
  

Generic forms without Dublin Core
=====================================

Tests run above where using a content defining a title, let's verify it still
works with bare contents.

   >>> sietch = root['sietch']


Create
------

Form customization
==================

To customize forms, the usual solution is to subclass them and to work
with the subclass. `dolmen.forms.crud` proposes a new component to
customize your forms. Defined by the `IFieldsCustomization` interface,
it's an adapter that allows you to interact at the field level.

In a `IFieldsCustomization`, the customization happens at the __call__
level. The forms, while they update the objects fields, query a
`IFieldsCustomization` adapter and call it, giving the fields as an
argument.

Let's implement an example::

  >>> class RemoveWater(crud.FieldsCustomizer):
  ...    grokcore.component.adapts(Fremen, crud.Add, None)
  ...
  ...    def __call__(self, fields):
  ...       """Alters the form fields"""
  ...       return fields.omit('water')

  >>> from zope.interface import verify
  >>> verify.verifyClass(crud.IFieldsCustomization, RemoveWater)
  True

We can now register and test the customization::

  >>> grokcore.component.testing.grok_component('custom', RemoveWater)
  True

  >>> security.newInteraction(Participation(manager))

  >>> addform = addingview.traverse('fremen', [])
  >>> for field in addform.fields: print field
  <TextLineSchemaField Name of the warrior>

One important thing is noticeable here : the 'RemoveWater' adapter was
registered for the 'Fremen' component. To be able to lookup the
registery for suitable adapters, the add form uses a special lookup
function : `dolmen.forms.crud.utils.queryClassMultiAdapter`.

We can test a more complex example, returning a brand new instance of
Fields::

  >>> import dolmen.forms.base
  >>> class AddFieldToView(crud.FieldsCustomizer):
  ...    grokcore.component.adapts(Fremen, crud.Display, None)
  ...
  ...    def __call__(self, fields):
  ...       """Returns a new instance of Fields.
  ...       """
  ...       schema = dolmen.content.schema.bind().get(self.context)
  ...       return dolmen.forms.base.Fields(*schema)

  >>> grokcore.component.testing.grok_component('viewer', AddFieldToView)
  True

Checking the fields, we should get *all* the fields defined by the
Fremen schema::

  >>> view = getMultiAdapter((naib, request), name='defaultview')
  >>> view.fields.keys()
  ['title', 'water']

  >>> security.endInteraction()

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

  >>> request = TestRequest(form={
  ...     'form.field.water': '10',
  ...     'form.field.title': u'Sihaya',
  ...     'form.action.update': u'Update'},
  ...	  REQUEST_METHOD='POST',
  ...     )

  >>> security.newInteraction(request)

  >>> chani = Fremen()
  >>> root['chani'] = chani

  >>> editform = getMultiAdapter((chani, request), name='edit')
  >>> editform.updateForm()

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

  >>> security.endInteraction()

Field update
------------

`dolmen.forms.base` provides the description of a new component that
can be used to atomize the updating process of an object:
`IFieldUpdate`. An implementation is available in `dolmen.forms.crud`,
using an event handler, listening on ObjectModifiedEvent and
ObjectCreatedEvent::

  >>> updates = []

  >>> from zope.schema import TextLine
  >>> from zope.component import adapter, provideAdapter
  >>> from zope.interface import implementer
  >>> from dolmen.forms.base import IFieldUpdate

  >>> @implementer(IFieldUpdate)
  ... @adapter(Fremen, TextLine)
  ... def updated_textfield(context, field):
  ...    updates.append((context, field))

  >>> provideAdapter(updated_textfield, name="updatetext")


Using an add form, the IFieldUpdate adapters should be called during an objects creation::

  >>> request = TestRequest(form={
  ...     'form.field.title': u'Liet',
  ...     'form.action.add': u'Add'},
  ...	  REQUEST_METHOD='POST',
  ...     )

  >>> request.setPrincipal(manager)
  >>> interaction = security.newInteraction(request)

  >>> desert = root['desert'] = dolmen.content.Container()
  >>> addingview = getMultiAdapter((desert, request), name='add')
  >>> addform = addingview.traverse('fremen', [])
  >>> addform.updateForm()

  >>> kynes = desert['Fremen']
  >>> kynes
  <dolmen.forms.crud.tests.Fremen object at ...>
  >>> kynes.title
  u'Liet'  

  >>> print updates
  [(<dolmen.forms.crud.tests.Fremen object at ...>,
  <zope.schema._bootstrapfields.TextLine object at ...>)]

  >>> security.endInteraction()


We can do the same thing for the edit form::

  >>> updates = []

  >>> request = TestRequest(form={
  ...     'form.field.water': '50',
  ...     'form.field.title': u'Imperial weather specialist',
  ...     'form.action.update': u'Update'},
  ...	  REQUEST_METHOD='POST',
  ...     )

  >>> request.setPrincipal(manager)
  >>> security.newInteraction(request)

  >>> editform = getMultiAdapter((kynes, request), name='edit')
  >>> editform.updateForm()

  >> kynes.title
  u'Imperial weather specialist'

  >>> updates
  [(<dolmen.forms.crud.tests.Fremen object at ...>, <zope.schema._bootstrapfields.TextLine object at ...>)]

Updating a field without a registered IFieldUpdate adapter shouldn't do
anything::

 >>> updates = []

  >>> request = TestRequest(form={
  ...     'form.field.water': '40',
  ...     'form.action.update': u'Update'},
  ...	  REQUEST_METHOD='POST',
  ...     )

  >>> editform = getMultiAdapter((kynes, request), name='edit')
  >>> editform.updateForm()

  >>> updates
  []
