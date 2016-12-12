var MicrositeApp = angular.module('MicrositeApp', []);

MicrositeApp.controller('MainViewController', function MainViewController($scope) {
  $scope.current_dataset_url = $('#dataset-dropdown')[0].value;
});
