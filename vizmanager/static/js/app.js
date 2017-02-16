// TODO: make generic using metaprogramming or something similar so that we can use Babbage.<Any>Directive()
var visualizationDirective = new window.Babbage.TreemapDirective();
var MicrositeApp = angular.module('MicrositeApp', ['angular.filter']);
visualizationDirective.init(MicrositeApp);


MicrositeApp.controller('MainViewController', function MainViewController($scope) {
  dataset_dropdown = $('#dataset-dropdown')[0];
  if (dataset_dropdown) {
    $scope.current_dataset_url = dataset_dropdown.value;
  }
});


MicrositeApp.controller('BabbageController', function ($scope, $http, $timeout) {

  // we declare the Dataset class inside the controller because we need access
  // to $timeout
  class Dataset {
    constructor(obj) {
      this.level = 0;
      this.code = obj.code;
      this.os_model_url = obj.os_model_url;
    }

    /**
     * Query OpenSpending to retrieve the hierarchies and dimensions from this
     * particular dataset (cube, in OS terms)
     * @returns {Promise} $http.get() promise which already contains success and
     * error handling
     */
    getModel() {
      let self = this;
      return $http.get(self.os_model_url).then(
        function(response) {
          self.hierarchies = response.data.model.hierarchies;
          self.dimensions = response.data.model.dimensions;
          self.aggregates = response.data.model.aggregates;
          // console.log("hierarchies: ", self.hierarchies);
          // console.log("dimensions: ", self.dimensions);
          self.hierarchy = Object.keys(self.hierarchies)[0];
          self.aggregate = Object.keys(self.aggregates)[1];
          self.level_name = self.buildLevelName();
          self.state = {
            group: [self.level_name],
            aggregates: self.aggregate,
            filter: ''
          };
          console.log("state: ", self.state);
          console.log("hierarchies: ", self.hierarchies);
          console.log("dimensions: ", self.dimensions);
          self.isVisible = true;
        },
        function(error) {
          alert('An error occurred when querying to the API');
          console.log(error);
        }
      );
    }

    /**
     * Go one level down (deeper) in the hierarchy, according to the *item*
     * selected
     * @param {Object} $event, the event produced by clicking
     * @param {Object} component, area of the visualization component
     * @param {Object} item, selected (clicked) segment of the component
     * @returns {String} name representing the current level in the hierarchy
     */
    goDeeper($event, component, item) {
      this.item_key = item.key;
      this.level_name = this.buildLevelName();
      this.level++;
      if (this.level != 1) {
        this.state.filter += ";";
      }
      this.state.filter += this.state.group[this.level-1] + ":" + item.key;
      this.state.group = [this.level_name];
      this.updateVisualization();
      console.log("state: ", this.state);
    }

    /**
     * Go one level up (back) in the hierarchy
     */
    goBack() {
      if (this.level < 1) return;
      let last_filter = this.state.group[this.level-1] + ":" + this.item_key;
      let full_filter = this.state.filter;
      this.state.filter =
        full_filter.substr(0, full_filter.length - last_filter.length - 1);
      this.level--;
      this.level_name = this.buildLevelName();
      this.state.group = [this.level_name];
      this.updateVisualization();
      console.log("state: ", this.state);
    };

    /**
     * Traverse the hierarchies object using the current hierarchy and level to
     * obtain a level name
     * @returns {String} name representing the current level in the hierarchy
     */
    buildLevelName() {
      console.log(this.level, this.hierarchies[this.hierarchy].levels);
      return this.dimensions[this.hierarchies[this.hierarchy].levels[this.level]].key_ref;
    }

    /**
     * Re-renders the visualization in order to be able to navigate through the
     * dataset.
     * This is a trick extracted from OpenSpending Viewer's code base.
     */
    updateVisualization() {
      let self = this;
      $timeout(function() {
        self.isVisible = false;
        $timeout(function() {
          self.isVisible = true;
        });
      });
    }
  }

  let bc = this;
  init();

  /**
   * Set initial values for the visualization, render the initial state and set
   * click event handlers
   */
  function init() {
    bc.OS_API = OS_API;
    bc.datasets = {};

    for (let key in datasets) {
      if (datasets.hasOwnProperty(key)) {
        let dataset = new Dataset(datasets[key]);
        bc.datasets[key] = dataset;
        dataset.getModel();
        $scope.$on('babbage-ui.click', dataset.goDeeper.bind(dataset));
      }
    }
  }
});