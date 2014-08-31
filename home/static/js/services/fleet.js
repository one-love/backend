'use strict';

angular.module('OneLove')
    .service('fleetService', function($http, API_URL) {
        var getFleet = function() {
            return $http.get(API_URL + 'fleets/')
        };

        return {
            get: getFleet
        };
    });
