var MicrositeApp = angular.module('MicrositeApp', []);

MicrositeApp.controller('MainViewController', function MainViewController($scope) {
  dataset_dropdown = $('#dataset-dropdown')[0];
  if (dataset_dropdown) {
    $scope.current_dataset_url = dataset_dropdown.value;
  }
});
