class Message {
    constructor(event, data) {
        this.event = event;
        this.data = data;
    }
}

class Observer {
    update() {
        throw "Method update not implemented!";
    }
}

class Observable {
    constructor() {
        this.observers = [];
    }

    attach(observer) {
        this.observers.push(observer);
    }

    detach(observer) {
        const index = this.observers.indexOf(observer);
        if (index !== -1) {
            this.observers.splice(index, 1);
        }
    }

    notify(message) {
        this.observers.forEach(observer => {
            observer.update(message);
        });
    }
}