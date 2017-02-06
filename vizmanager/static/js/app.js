let MicrositeApp = angular.module('MicrositeApp', ['angular.filter']);


MicrositeApp.controller('MainViewController', function MainViewController($scope) {
  dataset_dropdown = $('#dataset-dropdown')[0];
  if (dataset_dropdown) {
    $scope.current_dataset_url = dataset_dropdown.value;
  }
});


MicrositeApp.controller('BabbageController', function ($scope, $http, $timeout) {
  // TODO: make generic using metaprogramming or something similar so that we can use Babbage.<Any>Directive()
  let visualizationDirective = new window.Babbage.TreemapDirective();
  visualizationDirective.init(app);

  let level, level_name, hierarchy, hierarchies, dimensions, item_key;
  init();


  /**
   * Set initial values for the visualization, render the initial state and set
   * click event handlers
   */
  function init() {
    $scope.datasets = {};
    $scope.cube = 'boost:boost-moldova-2005-2014';
    $scope.apiUrl = 'http://next.openspending.org/api/3';

    $http.get($scope.apiUrl + '/cubes/' + $scope.cube + '/model')
    .then(
      function(response) {
        hierarchies = response.data.model.hierarchies;
        dimensions = response.data.model.dimensions;
        //console.log(hierarchies);
        //console.log(dimensions);
        hierarchy = firstKey(hierarchies);
        level = 0;
        level_name = buildLevelName(level, hierarchies, hierarchy);
        $scope.isVisible = true;
        $scope.state = {
          group: [level_name],
          aggregates: 'adjusted.sum',
          filter: ''
        };
        console.log($scope.state);
      },
      function(error) {
        alert('An error occurred when querying to the API');
        console.log(error);
      }
    );

    $scope.$on('babbage-ui.click', goDeeper);
  }


  /**
   * Traverse the hierarchies object using the current hierarchy and level to obtain a level name
   * @param {Number} level, depth inside the hierarchy
   * @param {Object} hierarchies, object describing the hierarchies taken from the API
   * @param {String} hierarchy, exact hierarchy to traverse hierarchy
   * @return {String} name representing the current level in the hierarchy
   */
  function buildLevelName(level, hierarchies, hierarchy) {
    return dimensions[hierarchies[hierarchy].levels[level]].key_ref;
  }

  /**
   * Look for the first useful key in an object
   * @param {Object} obj, object to be inspected
   * @return {Any} the chosen key
   */
  function firstKey(obj) {
    return Object.keys(obj)[7];
  }

  /**
   * Re-renders the visualization in order to be able to navigate through the dataset.
   * This is a trick extracted from OpenSpending Viewer's code base.
   */
  function updateVisualization() {
    $timeout(function() {
      $scope.isVisible = false;
      $timeout(function() {
        $scope.isVisible = true;
      });
    });
  }

  /**
   * Go one level down (deeper) in the hierarchy, according to the *item* selected
   * @param {Object} $event, the event produced by clicking
   * @param {Object} component, area of the visualization component
   * @param {Object} item, selected (clicked) segment of the component
   */
  function goDeeper($event, component, item) {
    item_key = item.key;
    level++;
    level_name = buildLevelName(level, hierarchies, hierarchy);
    if (level != 1) {
      $scope.state.filter += ";";
    }
    $scope.state.filter += $scope.state.group[level-1] + ":" + item.key;
    $scope.state.group = [level_name];
    update();
    console.log("state: ", $scope.state);
  }

  /**
   * Go one level up (back) in the hierarchy
   */
  $scope.goBack = function() {
    if (level < 1) return;
    let last_filter = $scope.state.group[level-1] + ":" + item_key;
    let full_filter = $scope.state.filter;
    $scope.state.filter =
      full_filter.substr(0, full_filter.length - last_filter.length - 1);
    level--;
    level_name = buildLevelName(level, hierarchies, hierarchy);
    $scope.state.group = [level_name];
    updateVisualization();
    console.log("state: ", $scope.state);
  };
});