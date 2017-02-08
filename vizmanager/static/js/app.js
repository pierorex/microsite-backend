/**
 * Look for the first useful key in an object
 * @param {Object} obj, object to be inspected
 * @return {Any} the chosen key
 */
function firstKey(obj) {
  return Object.keys(obj)[0];
}


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

  // we declare the Dataset class inside the controller because we need access to
  // $timeout
  class Dataset {
    constructor(obj) {
      this.level = 0;
      this.isVisible = obj.isVisible;
      this.code = obj.code;
      this.os_model_url = obj.os_model_url;
    }

    /**
     * Go one level down (deeper) in the hierarchy, according to the *item* selected
     * @param {Object} $event, the event produced by clicking
     * @param {Object} component, area of the visualization component
     * @param {Object} item, selected (clicked) segment of the component
     */
    goDeeper($event, component, item) {
      item_key = item.key;
      this.level++;
      this.level_name = buildLevelName(this.level, this.hierarchies, this.hierarchy);
      if (this.level != 1) {
        this.state.filter += ";";
      }
      this.state.filter += this.state.group[this.level-1] + ":" + item.key;
      this.state.group = [this.level_name];
      this.updateVisualization();
      console.log("state: ", this.state);
    }

    getModel() {
      let that = this;
      return $http.get(that.os_model_url).then(
        function(response) {
          that.hierarchies = response.data.model.hierarchies;
          that.dimensions = response.data.model.dimensions;
          console.log("hierarchies: ", that.hierarchies);
          console.log("dimensions: ", that.dimensions);
          that.hierarchy = firstKey(that.hierarchies);
          that.level_name = that.buildLevelName();
          that.state = {
            group: [that.level_name],
            aggregates: 'adjusted.sum',
            filter: ''
          };
          console.log("state: ", that.state);
        },
        function(error) {
          alert('An error occurred when querying to the API');
          console.log(error);
        }
      );
    }

    /**
     * Traverse the hierarchies object using the current hierarchy and level to obtain a level name
     * @return {String} name representing the current level in the hierarchy
     */
    buildLevelName() {
      return this.dimensions[this.hierarchies[this.hierarchy].levels[this.level]].key_ref;
    }

    /**
     * Re-renders the visualization in order to be able to navigate through the dataset.
     * This is a trick extracted from OpenSpending Viewer's code base.
     */
    updateVisualization() {
      let that = this;
      $timeout(function() {
        that.isVisible = false;
        $timeout(function() {
          that.isVisible = true;
        });
      });
    }

    /**
     * Go one level up (back) in the hierarchy
     */
    goBack() {
      if (this.level < 1) return;
      let last_filter = this.state.group[this.level-1] + ":" + item_key;
      let full_filter = this.state.filter;
      this.state.filter =
        full_filter.substr(0, full_filter.length - last_filter.length - 1);
      this.level--;
      this.level_name = buildLevelName(level, hierarchies, hierarchy);
      this.state.group = [this.level_name];
      this.updateVisualization();
      console.log("state: ", this.state);
    };
  }

  let bc = this;
  init();

  /**
   * Set initial values for the visualization, render the initial state and set
   * click event handlers
   */
  function init() {
    bc.datasets = {};

    for (let key in datasets) {
      if (datasets.hasOwnProperty(key)) {
        let dataset = new Dataset(datasets[key]);
        bc.datasets[key] = dataset;
        dataset.getModel();
        $scope.$on('babbage-ui.click', dataset.goDeeper);
      }
    }
  }
});