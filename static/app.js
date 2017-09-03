var translateApp = angular.module('translateApp', ['ngRoute'])


translateApp.config(function ($routeProvider) {
    // console.log('akjlsdkfajsf')
    // alert($location.path)
    $routeProvider
        .when('/', {
            // template: 'alsjdflasdf',
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

})

translateApp.controller('inputController', function($scope, $http, translationService) {

    // // $scope.langs = []
    // $scope.selected = {
    //     lang: ''
    // }
    $scope.langs = translationService.langs;
    $scope.getLanguage = function() {
        console.log('askdlfj;asdflks')
        $scope.langs = translationService.langs;
        return $scope.langs;
    }
    

    $scope.source_text = '';
    $scope.target_lang = '';

    $scope.translate = function() {
        translationService.translate($scope.source_text, $scope.target_lang);
    }

    $scope.hasError = function() {
        $scope.status = translationService.status;
        return translationService.status.translate.error;
    }

    $scope.hasWarning = function() {
        $scope.status = translationService.status;
        return translationService.status.translate.warning;
    }


    console.log('Input controller');

})


translateApp.controller('outputController', function($scope, translationService) {
    
    $scope.source_text = 'Source language...'
    $scope.target_text = 'Target language...'
    $scope.source_lang = 'From'
    $scope.target_lang = 'To'

    $scope.source_lang_long = 'From'
    $scope.target_lang_long = 'To'

    $scope.updateResults = function() {
        var data = translationService.data;
        if (!data) {return;}
        $scope.source_text = data.source_text;
        $scope.target_text = data.target_text;
        $scope.source_lang = data.source_lang;
        $scope.target_lang = data.target_lang;

        $scope.source_lang_long = translationService.langs[$scope.source_lang];
        $scope.target_lang_long = translationService.langs[$scope.target_lang];
    }
    
    $scope.updateResults();
        
})

translateApp.controller('historyController', function($scope, $http, translationService) {

    // alert('control me');

    $scope.history = []

    $scope.getLanguage = function(lang) {
        return translationService.langs[lang];
    }

    $http({
        method: 'GET',
        url: '/api/translate'
    }).then(function success(response) {
        console.log(response);
        $scope.history = response.data;
        // $rootScope.$apply();
        // console.log($scope.langArr)
        // $scope.langs = {}
        // for (lang in $scope.langArr) {
        //     short = lang[0][0];
        //     long = lang[0][1];
            
        //     $scope.langs[long] = short;
        // }
        // console.log($scope.langs);
        // $scope.$apply();
    }, function error(respnse) {

        
    })


})



translateApp.service('translationService', function($http, $rootScope, $location) {

    this.langs = {};
    var self = this;

    // Get supported languages
    $http({
        method: 'GET',
        url: '/api/languages'
    }).then(function success(response) {
        console.log(response);
        self.langs = response.data.langs;
        // $rootScope.$apply();
        // console.log($scope.langArr)
        // $scope.langs = {}
        // for (lang in $scope.langArr) {
        //     short = lang[0][0];
        //     long = lang[0][1];
            
        //     $scope.langs[long] = short;
        // }
        // console.log($scope.langs);
        // $scope.$apply();
    }, function error(respnse) {

        
    })


    this.status = {
        translate: {
            warning: '',
            error: ''
        },
        getLanguages: {
            warning: '',
            error: ''
        }
    }

    // translate
    this.translate = function(source_text, target_lang) {
            
        this.status.translate.warning = '';
        this.status.translate.error = '';

        if (!source_text) {
            this.status.translate.warning = 'Please input text to translate';
            return;
        }

        if (!target_lang) {
            this.status.translate.warning = 'Please select a target language.';
            return;
        }

        var data = {
            source_text: source_text,
            target_lang: target_lang
        }

        $http({
            method: 'POST',
            url: '/api/translate/',
            data: data
        }).then(function success(response) {
            // $scope.langs = response.data.langs;
            console.log(response);
            self.data = JSON.parse(response.data);
            
            alert('it worked!');
            $location.path('/result')

            // $scope.$apply();
        }, function error(respnse) {
    
        })

    }


})


