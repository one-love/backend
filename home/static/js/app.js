'use strict';
/* global:angular angular:true */

angular.module('OneLove', ['ui.router'])
    .constant('API_URL', '/api/v1/')
    .config(function($stateProvider, $urlRouterProvider) {
        $urlRouterProvider.otherwise('/');

        $stateProvider
        .state('home', {
            url: '/',
            templateUrl: '/static/js-templates/home.html'
        })
        .state('fleet', {
            url: '/fleet',
            controller: 'FleetController',
            templateUrl: '/static/js-templates/fleet-list.html'
        });
    });
