function Competition(data) {
    this.title    = ko.observable(data.title);
    this.date     = ko.observable(data.date);
    this.location = ko.observable(data.location);
    this.pk       = ko.observable(data.id);
};

function CompetitionListViewModel() {
    // Data
    var self = this;
    self.competitions = ko.observableArray([]);

    // Load initial state from server, convert it to Task instances, then populate self.tasks
    $.getJSON("/rest/competitions/", function(allData) {
        var mappedTasks = $.map(allData, function(item) { return new Competition(item) });
        self.competitions(mappedTasks);
    });

    self.showCompet = function() {};
};

ko.applyBindings(new CompetitionListViewModel());
