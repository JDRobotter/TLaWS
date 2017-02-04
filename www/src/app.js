function AppController($http, $scope, $mdDialog) {
  var self = this;

  var refresh_timeout_ms = 2000;

  $scope.do_stuff = function() {
    $http.get('/do.json?a=2&b=3').then(response => {}
      ,
      function errorCallback(response) {
        console.log(response);
      });

  }

  $scope.refresh = function() {
    // fetch status
    $http.get('/status.json').then(response => {
        $scope.status = response.data;
      },
      function errorCallback(response) {
        console.log(response);
      });

    setTimeout($scope.refresh, refresh_timeout_ms);
  }
  $scope.refresh();
}

var app = angular.module( 'tlaws-app', ['ngMaterial','ui.router'])
  .config(['$stateProvider','$urlRouterProvider',
    function($stateProvider,$urlRouterProvider) {

      $urlRouterProvider.otherwise('/');

      $stateProvider
        .state('home', {
          url:'/',
          templateUrl:'templates/home.html',
        })
        .state('temperature', {
          url:'/temperature',
          templateUrl:'templates/temperature.html',
        })
    }])
  .config(function($mdThemingProvider) {
      $mdThemingProvider.theme('default')
          .primaryPalette('blue-grey')
          .accentPalette('orange');
    })
  .controller('AppController', AppController);
