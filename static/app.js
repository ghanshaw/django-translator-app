var translateApp = angular.module('translateApp', ['ngRoute'])

// Url Routing
translateApp.config(function ($routeProvider) {

    $routeProvider
        .when('/', {
            templateUrl: 'static/pages/input.html',
            controller: 'inputController'
        })
        .when('/result', {
            templateUrl: 'static/pages/result.html',
            controller: 'outputController'
        })
        .when('/history', {
            templateUrl: 'static/pages/history.html',
            controller: 'historyController'
        })
        .otherwise({
            redirectTo: '/'
        })

})

translateApp.controller('inputController', function($scope, $http, translationService) {

    // Get supported languaged from service
    $scope.langs = [];
    $scope.getLanguage = function() {

        // Store language object in array for ng-repeat
        let langs = [];

        // Exit if array already exists or langauges aren't available
        if ($scope.langs.length || !translationService.langs) { return $scope.langs; }
        for (let key in translationService.langs) {
            let val = translationService.langs[key];
            langs.push([val, key]);
        }
        $scope.langs = langs;
        return langs;
    }
    

    // Initialize input fields
    $scope.source_text = '';
    $scope.target_lang = '';

    // Perform text translation, defer to service
    $scope.translate = function() {
        translationService.translate($scope.source_text, $scope.target_lang);
    }

    // Check for errors
    $scope.hasError = function() {
        $scope.status = translationService.status;
        return translationService.status.translate.error;
    }

    // Check for warnings
    $scope.hasWarning = function() {
        $scope.status = translationService.status;
        return translationService.status.translate.warning;
    }

    // Check if service is still translating
    $scope.isWaiting = function() {
        return translationService.status.translate.waiting;
    }

})


translateApp.controller('outputController', function($scope, translationService) {
    
    // Set flag to true
    // Flag indicates if no data is available
    $scope.no_data = true;

    // Initialize fields when no translation has occured
    $scope.source_text = 'Source language...'
    $scope.target_text = 'Target language...'
    $scope.source_lang = 'From'
    $scope.target_lang = 'To'

    $scope.source_lang_long = 'From'
    $scope.target_lang_long = 'To'

    // Update fields based on translation outcome
    $scope.updateResults = function() {
        var data = translationService.data;

        // Exit is translation hasn't occured (no data)
        if (!data) {return;}
        $scope.no_data = false;
        $scope.source_text = data.source_text;
        $scope.target_text = data.target_text;
        $scope.source_lang = data.source_lang;
        $scope.target_lang = data.target_lang;

        $scope.source_lang_long = translationService.langs[$scope.source_lang];
        $scope.target_lang_long = translationService.langs[$scope.target_lang];
    }
    
    // Perform update upon visiting page
    $scope.updateResults();
        
})

translateApp.controller('historyController', function($scope, $http, translationService) {

    // Store list of all historical translations
    $scope.history = []

    // Get full language name from shortcode
    $scope.getLanguage = function(lang) {
        return translationService.langs[lang];
    }

    // Perform GET, retrieve list of historical translations
    $http({
        method: 'GET',
        url: '/api/translate'
    }).then(function success(response) {
        $scope.history = response.data;
    }, function error(response) {
        $scope.error = 'An error has occured. Error ' + response.status + ': ' + response.statusText;
    })
})



translateApp.service('translationService', function($http, $rootScope, $location) {

    
    var self = this;

    // Store supported languages
    this.langs = {};

    // Get supported languages via HTTP request
    $http({
        method: 'GET',
        url: '/api/languages'
    }).then(function success(response) {
        self.langs = response.data.langs;
    }, function error(response) {
        self.status.translate.error
        let error = 'Unable to aquire language list. '
        error += 'Error ' + response.status + ': ' + response.statusText;
        error += '. Please reload page.'
        self.status.translate.error = error;
    })

    // Object storing translation status
    this.status = {
        translate: {
            warning: '',
            error: '',
            waiting: false
        },
        getLanguages: {
            warning: '',
            error: ''
        }
    }

    // Main translate function
    this.translate = function(source_text, target_lang) {
            
        // Limit length of input
        let limit = 300;

        // Clear messages
        this.status.translate.warning = '';
        this.status.translate.error = '';  
        
        // Only one translation at a time
        if (this.status.translate.waiting) {
            return;
        }

        // Exit if input is too long
        if (source_text.length > limit) {
            this.status.translate.warning = 'Please limit your input to ' + limit + ' characters.';
            return;
        }

        // Exit is input is missing
        if (!source_text) {
            this.status.translate.warning = 'Please input text to translate';
            return;
        }

        if (!target_lang) {
            this.status.translate.warning = 'Please select a target language.';
            return;
        }

        // Start waiting indicator
        this.status.translate.waiting = true;

        // Data for HTTP request
        var data = {
            source_text: source_text,
            target_lang: target_lang
        }

        // Update server with HTTP request
        $http({
            method: 'POST',
            url: '/api/translate/',
            data: data
        }).then(function success(response) {
            // Stop waiting indiciator
            self.status.translate.waiting = false;    

            // Parse response
            self.data = JSON.parse(response.data);

            // Redirect to result page
            $location.path('/result')
        }, function error(response) {
            // Stop waiting indicator
            self.status.translate.waiting = false;

            // Construct error message
            self.status.translate.error = 'Error ' + response.status + ': ' + response.statusText;
        })
    }
})


