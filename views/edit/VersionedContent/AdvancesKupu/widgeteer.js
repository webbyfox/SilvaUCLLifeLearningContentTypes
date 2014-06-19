/*****************************************************************************
 *
 * Copyright (c) 2004-2005 Guido Wesdorp. All rights reserved.
 *
 * This software is distributed under the terms of the widgeteer
 * License. See LICENSE.txt for license text.
 *
 * E-mail: johnny@debris.demon.nl
 *
 *****************************************************************************

    Widgets.js - extensible API for HTML form elements in JS

    On initialization, the JSForm class looks for input elements with an
    additional attribute (jstype) and sees if there is a Widget class
    registered for each of those types/elements. If there is not, the form
    field will be untouched, if there is one, it will be instantiated with
    the form element as one of its arguments.

    Widget wrappers (classes) can/should implement the following methods:

    initialize(input) - Initialize the widget and build it. This should get
                    the value of the original field and use that as the
                    (serialized) default of the widget value, to allow 
                    retaining form values when a user reloads the page.

    value() - Return the value of the widget as a (serialized) string. This
                    will be written to the original input field upon form
                    submittance. It will also be saved to the original input
                    field on leaving the page, so pressing 'reload' in the
                    browser should not delete the contents of the widget.

    validate() - Validate the current value for form submittance. If the form
                    should not be submitted, this method should throw a
                    ValidationError with an explanation, if not it should just
                    return.

    beforeSubmit() - Hook that is called just before the form gets saved, this 
                    should remove any generated form-elements from the form 
                    (else they will end up in the POST body too).

*/

// create a namespace for the lot
window.widgeteer = new function() {
    /* The widget library */

    WIDGETNS = 'http://debris.demon.nl/xmlns/widget';

    // store reference to this lib to use from inside the classes
    var widgetlib = this;

    var WidgetRegistry = function() {
        /* object to register classes to

            also takes care of initialization
        */
    };

    WidgetRegistry.prototype.initialize = function() {
        this._klasses = [];
        this._widgets = [];
    };
    
    WidgetRegistry.prototype.prepareForms = function(win) {
        /* scan for all forms in a window and replace marked inputs */
        if (!win) {
            win = window;
        };
        var doc = win.document;
        // get all elements that might be wrapped
        var els = [];
        var elnames = ['input', 'textarea', 'select'];
        for (var i=0; i < elnames.length; i++) {
            var elsofname = document.getElementsByTagName(elnames[i]);
            for (var j=0; j < elsofname.length; j++) {
                els.push(elsofname[j]);
            };
        };
        // see if they need to be wrapped
        for (var i=0; i < els.length; i++) {
            var input = els[i];
            // I'd rather use a namespace, but that won't work well in browsers
            var jstype = input.getAttribute('widget:type');
            // if the widget:type is not known or there is none, leave the form
            // element alone
            if (this._klasses[jstype]) {
                // create an instance of the registered class, and initialize
                // it with the input as argument
                var klass = this._klasses[jstype];
                var instance = new klass();
                instance.initialize(input);
                // store a reference to the instance and input for later (form
                // submit)
                this._widgets.push([instance, input]);
            };
        };
    };

    WidgetRegistry.prototype.register = function(jstype, klass) {
        /* register a class for a specific jstype */
        this._klasses[jstype] = klass;
    };

    WidgetRegistry.prototype.prepareForm = function(form) {
        /* submit a form

            this needs to be called from the submit button
        */
        var processed = [];
        var messages = [];
        var submit = true;
        // walk through all widgets and see if they're in the current form,
        // if so validate and process them
        for (var i=0; i < widgetlib.widget_registry._widgets.length; i++) {
            var widget = widgetlib.widget_registry._widgets[i][0];
            var input = widgetlib.widget_registry._widgets[i][1];
            if (input.form === form) {
                // it's in the form to be submitted, see if it validates
                var validated = false;
                try {
                    widget.validate();
                    validated = true;
                } catch(e) {
                    if (e instanceof widgetlib.ValidationError) {
                        messages.push(e.message);
                        submit = false;
                    } else {
                        throw(e);
                    };
                };
                if (validated) {
                    // if validated, get the value and write it to the original
                    // form field
                    var value = widget.value();
                    var nodeName = input.nodeName.toLowerCase();
                    if (nodeName == 'input' || nodeName == 'textarea') {
                        // no support for anything besides plain text fields
                        // etc. so far
                        input.value = value;
                    } else if (nodeName == 'select') {
                        // with a select, the value should be a pipe (|) 
                        // seperated list of values to select
                        var values = value.split('|');
                        for (var i=0; i < input.options.length; i++) {
                            var option = input.options[i];
                            for (var j=0; j < values.length; j++) {
                                if (values[j] == option.value) {
                                    // XXX not sure about the property??
                                    option.selected = true;
                                } else {
                                    option.selected = false;
                                };
                            };
                        };
                    };
                    // store a reference to the instance so the beforeSubmit 
                    // handler can be called if all went well
                    processed.push(widget);
                };
            };
        };
        // see if we should submit the form, if not, raise an exception
        if (!submit) {
            // one or more errors have occurred, throw a validation error
            throw(new widgetlib.FormValidationError(messages));
        } else {
            // continue submitting the form
            for (var i=0; i < processed.length; i++) {
                processed[i].beforeSubmit();
            };
        };
    };

    WidgetRegistry.prototype.saveAll = function() {
        /* Save the current value of all widgets to the original fields 
        
            This is useful when a user reloads a page, first all values are
            written to the original fields, then the browser will reload the
            page and write all filled in values to all the fields in the HTML,
            which then function as default values for the widgets again. This
            way the value of complex widgets can still be retained on form
            reload.
        */
        for (var i=0; i < this._widgets.length; i++) {
            var widget = this._widgets[i][0];
            var input = this._widgets[i][1];
            var value = widget.value;
            if (value instanceof Function) {
                value = value.call(widget);
            };
            input.value = value;
        };
    };

    // instance to actually use, don't *ever* create another instance of
    // the registry, it will not work properly
    this.widget_registry = new WidgetRegistry();
    this.widget_registry.initialize();

    this.Widget = function() {
        /* Base class/example implementation for widgets.
        
            This widget does nothing, except wrapping the input.
        */
    };

    this.Widget.prototype.initialize = function(input) {
        /* Initialize the instance and build the widget.

            This should get its initial value from the input.
        */
        this.input = input;
    };

    this.Widget.prototype.value = function() {
        /* Return the value, serialize if necessary. */
        return value;
    };

    this.Widget.prototype.validate = function() {
        /* Validate the field, throw a ValidationError if the value is bad. */
    };

    this.Widget.prototype.beforeSubmit = function() {
        /* Called before the form is saved, should clean up any mess made. */
    };

    this.ValidationError = function(message) {
        /* This should be thrown from the Widget.validate() methods
            if a form should not get submitted */
        this.message = message;
    };

    this.FormValidationError = function(messages) {
        /* This will be thrown if one or more widgets raised a 
            ValidationError */
        this.messages = messages;
    };
}();
