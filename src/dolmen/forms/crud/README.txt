=================
dolmen.forms.crud
=================

`dolmen.forms.crud` is module destined to help developpers create
their C.R.U.D forms using `Grok`, `megrok.z3cform` and
`dolmen.content`. It provides a collection of base classes to add,
edit and access your content. It also provides some hooks to customize
the fields per context and form using special adapters, to avoid
overriding existing form and to increase the pluggability of your
applications.


Adding view
===========

`dolmen.forms.crud` provides an abstraction for the 'adding'
action. It allows pluggability at the container level and does handle
the naming/persistence duet. More explicitly, it's a named adapter
that will query the AddForm, call the object checking methods, choose
a name using a INameChooser and finally, if everything went smoothly,
set it on the context.

A base AddView is registered out-of-the-box as a named traversable
adapter called 'add'. It uses the following pattern:
++add++factory_name. `factory_name` must be the name of a
`dolmen.content.IFactory` component.


Let's first create a container in which we'll test the adding view::

  >>> import dolmen.content
  >>> from dolmen.forms.crud.tests import Sietch

  >>> sietch = Sietch()
  >>> sietch.title = u'Tabr'
  >>> dolmen.content.IBaseContent.providedBy(sietch)
  True
  
  >>> from zope.app.testing.functional import getRootFolder
  >>> root = getRootFolder()
  >>> root['sietch'] = sietch


The container created, the adding view should be available and operational.
Let's have a quick overview::
    
  >>> from zope.component import getMultiAdapter
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> addingview = getMultiAdapter((sietch, request), name='add')
  >>> addingview
  <dolmen.forms.crud.addview.Adder object at ...>


The adding view component checks explicitly the security requirement
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

We are not authorized. Now, if we try to access it with the Manager,
we should access it with success::

  >>> security.newInteraction(Participation(manager))
  >>> addingview.traverse('fremen', [])
  Traceback (most recent call last):
  ...
  NotFound: Object: <dolmen.forms.crud.tests.Sietch object at ...>, name: 'fremen'

The adding view is available for our item. Though, if we try to access our
current factory, a NotFound error will be raised as we have no add form
registered.

Let's try to check, now, if we create and register a very basic generic crud
AddForm:

  >>> import dolmen.forms.crud as crud
  >>> class AddForm(crud.Add):
  ...     '''Generic add form.
  ...     '''
  
  >>> import grokcore.component
  >>> grokcore.component.testing.grok_component('addform', AddForm)
  True

  >>> form = addingview.traverse('fremen', [])
  >>> form
  <AddForm object at ...>

Here we go. Our AddForm is returned as we traverse toward the factory
'fremen'.

Perfect. Our adding view is ready to be used. Before testing the AddForm
itself, let's have a try at the `add` method::

  >>> from dolmen.forms.crud.tests import Fremen

  >>> naib = Fremen()
  >>> added_item = addingview.add(naib)
  >>> added_item
  <dolmen.forms.crud.tests.Fremen object at ...>

  >>> added_item.__name__
  u'Fremen'
  >>> added_item.__parent__ is sietch
  True

An IAdding component should always be locatable::

  >>> addingview.__parent__
  <dolmen.forms.crud.tests.Sietch object at ...>
  >>> addingview.__name__
  u''

The `add` method checks if the constraints are respected. If the container has
a defined restriction (using zope.app.container.constraints), we get an error
if the contract is violated.

  >>> from dolmen.forms.crud.tests import Harkonnen

  >>> rabban = Harkonnen()
  >>> addingview.add(rabban)
  Traceback (most recent call last):
  ...
  InvalidItemType: (<...Sietch object at ...>, <...Harkonnen object at ...>, (<InterfaceClass dolmen.forms.crud.tests.IDesertWarrior>,))


The `add` method of the adding view can be called from the AddForm, to delegate
the adding operation. The generic adding view already handles the common
operations such as naming and persistence. Still, our AddForm is responsible
of the factoring of the item. Let's test very quickly the important attributes
and methods :

  >>> form.update()
  >>> form.updateForm()
  >>> form.fields
  <z3c.form.field.Fields object at ...>
  >>> factored_item = form.create({'title': u'Shani', 'water': 5})
  >>> factored_item
  <dolmen.forms.crud.tests.Fremen object at ...>
  >>> factored_item.title
  u'Shani'
  >>> factored_item.water
  5

The adding view works as intended. The real interest in using such an
abstraction is to be able to easily switch adding behaviors just by
registering a new component.

  >>> addingview.nextURL()
  'http://127.0.0.1/sietch'


Generic forms
=============
 
Add form
--------

The add form implementation is tightly tied to the adding view. The add
form behavior has been mostly covered above. Let's test briefly the
presence of the fields and the label::

  >>> addform = addingview.traverse('fremen', [])
  >>> addform
  <AddForm object at ...>

  >>> print addform.label
  Fremen training camp

  >>> addform.update()
  >>> addform.updateForm()
  >>> [field for field in addform.fields]
  ['title', 'water']
  

Edit form
---------

  >>> class EditForm(crud.Edit):
  ...     '''Generic edit form.
  ...     '''
  
  >>> grokcore.component.testing.grok_component('editform', EditForm)
  True

  >>> editform = getMultiAdapter((factored_item, request), name='editform')
  >>> editform
  <EditForm object at ...>

  >>> editform.update()
  >>> editform.updateForm()
  >>> [field for field in editform.fields]
  ['title', 'water']

XXX NEED TO TEST THE EVENTS


Display form
------------

  >>> class DefaultView(crud.Display):
  ...     '''Generic display form.
  ...     '''
  
  >>> grokcore.component.testing.grok_component('display', DefaultView)
  True

  >>> view = getMultiAdapter((factored_item, request), name='defaultview')
  >>> view
  <DefaultView object at ...>

  >>> view.update()
  >>> view.updateForm()
  >>> [field for field in view.fields]
  ['water']

  >>> print view()
  <div class="defaultview">
    <h1>Shani</h1>
  <BLANKLINE>
  <BLANKLINE>
      <div class="field">
       <label for="form-widgets-water">
  	<span>Number water gallons owned</span>
       </label>
       <p class="discreet"></p>
       <div class="widget">
      <span id="form-widgets-water"
            class="text-widget required int-field">5</span>
  <BLANKLINE>
  </div>
      </div>
  <BLANKLINE>
  </div>
  <BLANKLINE>


Form customization
==================

  >>> class RemoveWater(crud.FieldsCustomizer):
  ...    grokcore.component.adapts(Fremen, crud.Add, None)
  ...    def __call__(self, fields):
  ...       return fields.omit('water')

  >>> grokcore.component.testing.grok_component('custom', RemoveWater)
  True

  >>> addform = addingview.traverse('fremen', [])
  >>> [field for field in addform.fields]
  ['title']


  >>> import dolmen.forms.base
  >>> class AddFieldToView(crud.FieldsCustomizer):
  ...    grokcore.component.adapts(Fremen, crud.Display, None)
  ...    def __call__(self, fields):
  ...       schema = dolmen.content.schema.bind().get(self.context)
  ...       return dolmen.forms.base.Fields(*schema)

  >>> grokcore.component.testing.grok_component('viewer', AddFieldToView)
  True

  >>> view = getMultiAdapter((factored_item, request), name='defaultview')
  >>> view.update()
  >>> view.updateForm()
  >>> [field for field in view.fields]
  ['title', 'water']
