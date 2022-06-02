const MULTIPLE_CHOICE_FIELDS = ["difficulty", "surface", "direction", "tags"];

/*
 * Observable classes events
 */
const RESIZE = "RESIZE";
const UPDATE = "UDPATE";
const MULTIPLE_CHOICE_OPEN = "MULTIPLE_CHOICE_OPEN";
const MULTIPLE_CHOICE_CLOSE = "MULTIPLE_CHOICE_CLOSE";
const MULTIPLE_CHOICE_IS_UPDATED = "MULTIPLE_CHOICE_IS_UPDATED";

function isArraysEqual(a, b) {
    /*
     * Comparises two arrays.
     * Params a, b are expected to be Array type.
     * Returns true if arrays are equal, else - false. 
     */

    let isEqual = true
    if (a.length != b.length) {
        isEqual = false;
    }
    else {
        let i = 0;
        while(isEqual && i < a.length) {
            if (a[i] != b[i]) {
                isEqual = false;
            }
            i += 1;
        }
    }
    return isEqual;
}

class FilterChoice extends Observable {
    /*
     * Abstract class of filter choice.
     * Filter choice is widget, that is used to setup
     * specific routes data searching parameters.
     */

    getSearchParams() {
        /*
         * Generates parameter for url request accoriding to filter choice value.
         */

        throw "Method getSearchParams not implemented!";
    }

    setChoice() {
        /*
         * Sets filter choice value accoriding to request parameter.
         */

        throw "Method setChoice not implemented!";
    }
}

class DistanceChocie extends FilterChoice {
    /*
     * Numeric range choice controller.
     */

    constructor(minDistancewidgetId, maxDistancewidgetId, prevMinDistance, prevMaxDistance) {
        super();

        this.minDistance = document.getElementById(minDistancewidgetId);
        this.maxDistance = document.getElementById(maxDistancewidgetId);
        this.prevMinDistance = prevMinDistance;
        this.prevMaxDistance = prevMaxDistance;

        this.minDistance.addEventListener("change", () => {
            if (this.isNaturalNumber(this.minDistance.value)) {
                if (parseInt(this.maxDistance.value, 10) < parseInt(this.minDistance.value, 10)) {
                    this.maxDistance.value = this.minDistance.value;
                }
                this.prevMinDistance = this.minDistance.value;
                this.notify(new Message(UPDATE, "1"));
            }
            else {
                this.minDistance.value = this.prevMinDistance;
            }
        });
    
        this.maxDistance.addEventListener("change", () => {
            if (this.isNaturalNumber(this.maxDistance.value)) {
                if (parseInt(this.maxDistance.value, 10) < parseInt(this.minDistance.value, 10)) {
                    this.minDistance.value = this.maxDistance.value;
                }
                this.prevMaxDistance = this.maxDistance.value;
                this.notify(new Message(UPDATE, "1"));
            }
            else {
                this.maxDistance.value = this.prevMaxDistance;
            }
        });
    }

    getSearchParams() {
        /*
         * Generates parameter for url request accoriding to filter choice value.
         */

        return `min_distance=${this.minDistance.value}&max_distance=${this.maxDistance.value}`;
    }

    setChoice(searchParams) {
        /*
         * Sets filter choice value accoriding request parameter.
         */

        // console.log(`min_distance == ${searchParams.get("min_distance")}`);
        // console.log(`max_distance == ${searchParams.get("max_distance")}`);

        let minDistance = searchParams.min_distance;
        if (minDistance === undefined) {
            minDistance = "1";
        }
        let maxDistance = searchParams.max_distance;
        if (maxDistance === undefined) {
            maxDistance = "1000";
        }
        this.minDistance.value = minDistance;
        this.maxDistance.value = maxDistance;
    }

    isNaturalNumber(n) {
        /*
         * Checks if n is natural number.
         */

        n = n.toString();
        let n1 = Math.abs(n),
            n2 = parseInt(n, 10);
        return !isNaN(n1) && n2 === n1 && n1.toString() === n;
    }
}

class MultipleChoice extends FilterChoice {
    /*
     * Drop down multiple choice controller.
     */

    constructor(widgetId, field) {
        super();
        this.widget = document.getElementById(widgetId);
        this.field = field;
        this.labels = Array.from(this.widget.getElementsByTagName("label"));
        this.checkboxes = Array.from(this.widget.getElementsByTagName("input"));
        this.checkboxesLength = this.checkboxes.length;
        this.prevCeckedChoices = this.getCheckedChoices();
    }

    setCheckedChoices(checkedChoices) {
        /*
         * Set satus of widget choices to checked or not checked.
         * Param checkedChoices is expected to be array of string.
         */

        if (checkedChoices.length == 0 || checkedChoices.length == this.checkboxesLength || checkedChoices[0] == "all") {
            this.checkboxes.forEach(checkbox => {
                checkbox.checked = false;
            });
        }
        else {
            this.checkboxes.forEach(checkbox => {
                if (checkedChoices.includes(checkbox.value)) {
                    checkbox.checked = true;
                }
                else {
                    checkbox.checked = false;
                }
            });
        }
    }

    open() {
        /*
         * Opens widget (make it visible);
         */

        this.widget.style.display = "block";
        this.widget.style.boxShadow = "0px 0px 5px lightgrey";
    }

    close() {
        /*
         * Closes widget (make invisible), generete close event.
         * Returns is select was changed.
         */

        this.widget.style.display = "none";
        this.widget.style.boxShadow = "0px 0px 0px lightgrey";
        let checkedChoices = this.getCheckedChoices();
        if (!isArraysEqual(checkedChoices, this.prevCeckedChoices)) {
            this.prevCeckedChoices = checkedChoices;
            this.notify(new Message(UPDATE, "1"));
        }
        this.notify(new Message(MULTIPLE_CHOICE_CLOSE, this.getCheckedChoicesLabels()));
    }

    getCheckedChoices() {
        /*
         * Get list of checked choices values.
         * Returns array of checked choices values (array of string).
         * If all checkboxes or none are checked, returns ["all"].
         */

        let checkedChoices = [];
        this.checkboxes.forEach(checkbox => {
            if (checkbox.checked) {
                checkedChoices.push(checkbox.value);
            }
        });
        if (checkedChoices.length == 0 || checkedChoices.length == this.checkboxesLength) {
            checkedChoices = ["all"];
        }
        return checkedChoices;
    }

    getCheckedChoicesLabels() {
        /*
         * Get list of checked choices labels.
         * Returns array of checked choices labels (array of string).
         * If all checkboxes or none are checked, returns ["all"].
         */

        let checkedChoicesLabels = [];
        for (let i = 0; i < this.checkboxesLength; i++) {
            if (this.checkboxes[i].checked) {
                checkedChoicesLabels.push(this.labels[i].innerText);
            }
        }
        if (checkedChoicesLabels.length == 0 || checkedChoicesLabels.length == this.checkboxesLength) {
            checkedChoicesLabels = ["all"];
        }
        return checkedChoicesLabels;
    }

    getSearchParams() {
        /*
         * Generates parameter for url request accoriding to filter choice value.
         */

        let searchParam = `${this.field}=`;
        this.getCheckedChoices().forEach(choice => {
            searchParam += `${choice}_`;
        });
        return searchParam.substring(0, searchParam.length - 1);
    }

    setChoice(searchParams) {
        /*
         * Sets filter choice value accoriding request parameter.
         */
        // console.log(`this.field == ${searchParams.get(this.field)}`);

        let searchParam = searchParams[this.field];
        if (searchParam === undefined) {
            searchParam = [];
        }
        this.setCheckedChoices(searchParam);
        this.notify(new Message(MULTIPLE_CHOICE_CLOSE, this.getCheckedChoicesLabels()));
    }
}

class MultipleChoiceHeader extends Observer {
    /*
     * Drop down multiple choice header button controller.
     */

    constructor(widgetId, multipleChoice) {
        super();
        this.widget = document.getElementById(widgetId);
        this.multipleChoice = multipleChoice;
        this.isMultipleChoiceOpened = false;
        this.widget.addEventListener("click", () => {
            if (this.isMultipleChoiceOpened) {
                this.multipleChoice.close();
                this.isMultipleChoiceOpened = false;
            }
            else {
                this.multipleChoice.open();
                this.isMultipleChoiceOpened = true;
            }
        });
    }

    open() {
        /*
         * Changes style of element, when multiple choice is opened.
         */

        this.widget.style.boxShadow = "0px 0px 5px lightgrey";
    }

    close(checkedChoicesLabels) {
        /*
         * Changes style end text of header, when multiple choice is closed.
         */
        this.widget.value = this.generateHeaderText(checkedChoicesLabels);
        this.widget.style.boxShadow = "0px 0px 0px lightgrey";
    }

    generateHeaderText(checkedChoicesLabels) {
        /*
         * Generates text from labels of checked choices;
         */

        let text;
        if (checkedChoicesLabels[0] == "all") {
            text = "Все";
        }
        else if (checkedChoicesLabels.length == 1) {
            text = checkedChoicesLabels[0];
        }
        else {
            let value = `(${checkedChoicesLabels.length})`;
            checkedChoicesLabels.forEach(label => {
                value += ` ${label},`;
            });
            text = value.substring(0, value.length - 1);
        }
        if (text.length > 25) {
            text = text.substring(0, 23) + "...";
        }
        return text;
    }

    placeMultipleChoiceContainer() {
        /*
         * Updates position of multiple choice widget when window is resiezed.
         */

        const box = this.widget.getBoundingClientRect();
        this.multipleChoice.widget.style.top = (box.top + window.pageYOffset + 40).toString() + "px";
        this.multipleChoice.widget.style.left = (box.left).toString() + "px";
    }

    update(message) {
        /*
         * Message listener, updates appearance of multiple choice header,
         * when recieve messages MULTIPLE_CHOICE_CLOSE, MULTIPLE_CHOICE_OPEN,
         * updates position of according multiple choice widget when recieve RESIZE.
         */
        
        if (message.event == MULTIPLE_CHOICE_CLOSE) {
            this.close(message.data);
        }
        if (message.event == MULTIPLE_CHOICE_OPEN) {
            this.open();
        }
        if (message.event == RESIZE) {
            this.placeMultipleChoiceContainer();
        }
    }
}

class IsTransportAvailability extends FilterChoice {
    /*
     * Transport availability selector choice controller.
     */

    constructor(widgetId) {
        super();
        this.widget = document.getElementById(widgetId);
        this.widget.addEventListener("change", () => {
            this.notify(new Message(UPDATE, "1"));
        });
    }

    getSearchParams() {
        /*
         * Generates parameter for url request accoriding to filter choice value.
         */

        return `is_transport_availability=${this.widget.value}`;
    }

    setChoice(searchParams) {
        /*
         * Sets filter choice value accoriding request parameter.
         */

        let searchParam = searchParams.is_transport_availability;
        if (searchParam === undefined) {
            searchParam = "unknown";
        }
        this.widget.value = searchParam;
    }
}

class Updater extends Observer {
    constructor() {
        super();
        this.choices = [];
    }

    updateFilterChoices() {
        /*
         * Updates filter choices values and appearance according to request.
         */

        // let searchParams = new URLSearchParams(document.location.search);
        // let searchParams = new URLSearchParams(SEARCH_PARAMS);
        // console.log(SEARCH_PARAMS);
        this.choices.forEach(choice => {
            choice.setChoice(SEARCH_PARAMS);
        });
        this.request("1", this.onResponse);
    }

    generateUrl(page) {
        /*
         * Retruns search parameters according to filter choices values.
         * Param page is expected to be string with number of target page.
         */

        let url = "/routs/update-rout-list/?";
        this.choices.forEach(choice => {
            url += choice.getSearchParams() + "&";
        });
        return url + `page=${page}`;
    }

    request(page, callback) {
        /*
         * Retruns search parameters according to filter choices values.
         * Params:
         *     - page is expected to be string with number of target page;
         *     - callback is expected to be function, that update content of searched routes.
         */

        const xhttp = new XMLHttpRequest();
        xhttp.onload = callback.bind(this, xhttp);
        xhttp.open("GET", this.generateUrl(page));
        xhttp.send();
    }

    onResponse(xhttp) {
        /*
         * Updates content of searched routes, navigation buttons listeners.
         */

        document.getElementById("rout-list-container").innerHTML = xhttp.responseText;
        let ids = ["first-page-button", "previous-page-button", "next-page-button", "last-page-button"];
        for (let i = 0; i < 4; i++) {
            let item = document.getElementById(ids[i]);
            if (!item.disabled) {
                let page = item.name;
                item.addEventListener("click", () => {this.request(page, this.onResponse)});
            }
        }
    }

    update(message) {
        /*
         * Messages listener, updates route list data, when recieve UPDATE message.
         */

        if (message.event == UPDATE) {
            this.request(message.data, this.onResponse);
        }
    }
}

let updater;
let distanceChocie;
let multipleChoices = [];
let multipleChoiceHeaders = [];
let isTransportAvailability;

onResize = new Observable;

window.onload = () => {
    updater = new Updater();

    distanceChocie = new DistanceChocie("id_min_distance", "id_max_distance", 0, 1000);
    distanceChocie.attach(updater);
    
    MULTIPLE_CHOICE_FIELDS.forEach(field => {
        const multipleChoiceWidgetId = `drop-down-multiple-choice-list-container-${field}`;
        const multipleChoiceHeaderWidgetId = `drop-down-multiple-choice-button-${field}`;
        let multipleChoice = new MultipleChoice(multipleChoiceWidgetId, field);
        let multipleChoiceHeader = new MultipleChoiceHeader(multipleChoiceHeaderWidgetId, multipleChoice);

        document.addEventListener("click", (e) => {
            if (!e.composedPath().includes(multipleChoice.widget) && !e.composedPath().includes(multipleChoiceHeader.widget)) {
                if (multipleChoiceHeader.isMultipleChoiceOpened) {
                    multipleChoiceHeader.isMultipleChoiceOpened = false;
                    multipleChoice.close();
                }
            }
        });

        multipleChoice.attach(multipleChoiceHeader);
        multipleChoice.attach(updater);
        multipleChoices.push(multipleChoice);
        multipleChoiceHeaders.push(multipleChoiceHeader);
        onResize.attach(multipleChoiceHeader);
    });

    isTransportAvailability = new IsTransportAvailability("id_is_transport_availability");
    isTransportAvailability.attach(updater);

    onResize.notify(new Message(RESIZE, NaN));

    let choices = [distanceChocie];
    multipleChoices.forEach(choice => {choices.push(choice)});
    choices.push(isTransportAvailability);
    updater.choices = choices;
    updater.updateFilterChoices();
}

window.onresize = () => {
    onResize.notify(new Message(RESIZE, NaN));
};