window.widgeteer_datetime = new function() {
    /* a date/time widget for widgeteer */
    this.DateTimeWidget = function() {
        /* a simple compound date/time field */
        this.date_seperator = '/';
        this.time_seperator = ':';
    };

    this.DateTimeWidget.prototype = new widgeteer.Widget;

    this.DateTimeWidget.prototype.initialize = function(input) {
        this.input = input;
        var datetime = input.value;
        var parsed = undefined;
        if (datetime) {
            parsed = this.parseDateTime(input.value);
        };
        if (parsed === undefined) {
            parsed = ['', '', '', '', '', ''];
        };
        
        var containerdiv = document.createElement('div');
        containerdiv.style.whiteSpace = 'nowrap';
        containerdiv.className = 'datetimewidget-datetimediv';

        var dateel = document.createElement('span');
        dateel.style.whiteSpace = 'nowrap';
        dateel.className = 'datetimewidget-dateel';
        containerdiv.appendChild(dateel);
        
        var dayinput = document.createElement('input');
        this.dayinput = dayinput;
        dayinput.setAttribute('maxlen', '2');
        dayinput.setAttribute('size', '2');
        dayinput.value = parsed[2];
        dateel.appendChild(dayinput);

        dateel.appendChild(document.createTextNode(this.date_seperator));

        var monthinput = document.createElement('input');
        this.monthinput = monthinput;
        monthinput.setAttribute('maxlen', '2');
        monthinput.setAttribute('size', '2');
        monthinput.value = parsed[1];
        dateel.appendChild(monthinput);

        dateel.appendChild(document.createTextNode(this.date_seperator));

        var yearinput = document.createElement('input');
        this.yearinput = yearinput;
        yearinput.setAttribute('maxlen', '4');
        yearinput.setAttribute('size', '4');
        yearinput.value = parsed[0];
        dateel.appendChild(yearinput);

        containerdiv.appendChild(document.createTextNode('\xa0'));

        var hourel = document.createElement('span');
        hourel.style.whiteSpace = 'nowrap';
        hourel.className = 'datetimewidget-hourel';
        containerdiv.appendChild(hourel);

        var hourinput = document.createElement('input');
        this.hourinput = hourinput;
        hourinput.setAttribute('maxlen', '2');
        hourinput.setAttribute('size', '2');
        if (parsed[3]) {
            hourinput.value = parsed[3];
        };
        hourel.appendChild(hourinput);

        hourel.appendChild(document.createTextNode(this.time_seperator));

        var mininput = document.createElement('input');
        this.mininput = mininput;
        mininput.setAttribute('maxlen', '2');
        mininput.setAttribute('size', '2');
        if (parsed[4]) {
            mininput.value = parsed[4];
        };
        hourel.appendChild(mininput);

        input.parentNode.insertBefore(containerdiv, input);
        input.style.display = 'none';
    };

    // mapping from reg to field locations ([y, m, d, h, m, s], h, m, s 
    // are optional)
    regs = {
        '^(\\d{4})\\\/(\\d{1,2})\\\/(\\d{1,2}) (\\d{1,2}):(\\d{2}):(\\d{2})': 
            [1, 2, 3, 4, 5, 6],
        '^(\\d{4})\\\/(\\d{1,2})\\\/(\\d{1,2}) (\\d{1,2})\\:(\\d{2})':
            [1, 2, 3, 4, 5],
        '^(\\d{4})\\\/(\\d{1,2})\\\/(\\d{1,2})':
            [1, 2, 3]
        }
    this.DateTimeWidget.prototype.parseDateTime = function(datetime) {
        /* parse a datetime into seperate fields

            returns a list [year, month, day, hour, minute, seconds] if
            the datetime is understood, false if not
        */
        for (var reg in regs) {
            var locations = regs[reg];
            var regobj = new RegExp(reg, 'g');
            var match = regobj.exec(datetime);
            if (match) {
                ret = [
                    match[locations[0]],
                    match[locations[1]],
                    match[locations[2]],
                ];
                if (locations.length > 3) {
                    ret.push(match[locations[3]]);
                    ret.push(match[locations[4]]);
                };
                if (locations.length > 5) {
                    ret.push(match[locations[5]]);
                };
                return ret;
            };
        };
    };

    this.DateTimeWidget.prototype.value = function() {
        if (!this.yearinput.value || !this.monthinput.value || 
                !this.monthinput.value) {
            // it may be a bit rigorous to just remove the date here, but
            // it *is* safe ;)
            return '';
        };
        var ret = this.yearinput.value + '/' + this.monthinput.value + '/' +
                    this.dayinput.value;
        if (this.hourinput.value) {
            ret += ' ' + this.hourinput.value;
            if (!this.mininput.value) {
                ret += ':00';
            } else {
                ret += ':' + this.mininput.value;
            };
        };
        return ret;
    };

    // register the widget
    widgeteer.widget_registry.register('datetime', this.DateTimeWidget);
}();
