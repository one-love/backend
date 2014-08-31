'use strict';

angular.module('OneLove')
    .controller('FleetController', function($scope, fleetService) {
    fleetService.get()
        .then(function(result) {
            $scope.fleetList = result.data.results;
        });
});
