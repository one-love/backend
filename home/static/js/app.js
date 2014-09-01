'use strict';
/* global:angular angular:true */

angular.module('OneLove', ['ui.router'])
    .constant('API_URL', '/api/v1/')
    .config(function($stateProvider, $urlRouterProvider) {
        $urlRouterProvider.otherwise('/');

        $stateProvider
        .state('home', {
            url: '/',
            controller: 'FleetController',
            templateUrl: '/static/js-templates/fleet-list.html'
        });
    });
