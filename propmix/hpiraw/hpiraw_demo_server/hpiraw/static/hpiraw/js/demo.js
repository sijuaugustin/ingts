(function() {
  var app = angular.module('hpi', ['angularjs-dropdown-multiselect']);
  app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('||');
    $interpolateProvider.endSymbol('||');
  });
  app.controller('hpiCtrl', ['$scope', '$http', function($scope, $http) {

    $scope.init = function(){  
      $scope.rootURL = "https://insights.propmix.io:8104/"  
      $scope.spanFrom = '1975';
      $scope.spanTo = '2016';
      $scope.Frequency = 'quarterly';
      $scope.locationSearch = 'Alaska';
      $scope.totalPriceData();    
      $scope.getLocations();
      $scope.getYears();
    }   

    $scope.submit = function(){
      $scope.totalPriceData();
      
    }
    
    /* api call starts here*/    

     $scope.clickLocationFilter = function(item){
      $scope.showLocationSource = false;
      $scope.locationSearch = item;
    };

    $scope.locationFilterOpen = function(){
      $scope.showLocationSource = true;
    };
     $scope.locationFilterClose = function(){
      $scope.showLocationSource = false;
    };

    $scope.closeSourceFilter = function(){
      $scope.locationSearch = '';
    }
   
    $scope.totalPriceData = function(){
    
      $http({
        method  : 'GET',
        url     :  $scope.rootURL+'hpiraw/data/?location='+$scope.locationSearch+'&frequency='+$scope.Frequency+'&span='+$scope.spanFrom+'-'+$scope.spanTo+'&format=json'

      }).then(function successCallback(response) {
        if(response && response.data){
        console.log(response); 
          
          $scope.createTotalPriceChart(response.data);
          
        }
      }, function errorCallback(response) {
        console.log(response);
       
      });
    };

    $scope.getLocations = function(){
    
      $http({
        method  : 'GET',
        url     :  'https://insights.propmix.io:8104/hpiraw/locations/'

      }).then(function successCallback(response) {
        if(response && response.data){
          
          $scope.locations = response.data;
          
        }
      }, function errorCallback(response) {
        console.log(response);
       
      });
    };

     $scope.getYears = function(){
    
      $http({
        method  : 'GET',
        url     :  'https://insights.propmix.io:8104/hpiraw/years/'


      }).then(function successCallback(response) {
        if(response && response.data){
          console.log(response.data);
          $scope.years = response.data;
          
        }
      }, function errorCallback(response) {
        console.log(response);
       
      });
    };
    

    $scope.greaterThan = function(val){
      return function(item){
        return item >= val;
      }

    }
    
    $scope.createTotalPriceChart = function(data) {     
      
      $scope.indexValueNsa = [];
      $scope.yearValue = [];
      $scope.periodLegend = [];
      $scope.indexValueSa = [];
      TotalPriceChartData = [];

      data.forEach(function(d,dindex){
        $scope.indexValueNsa[dindex] = d.index_nsa;
        if($scope.Frequency && $scope.Frequency === "monthly"){
          $scope.yearValue[dindex] = d.yr+" M"+d.period;
        }else if($scope.Frequency && $scope.Frequency === "quarterly"){
           $scope.yearValue[dindex] = d.yr+" Q"+d.period;
         }       
       
        $scope.periodLegend[dindex] = d.period;
        $scope.indexValueSa[dindex] = d.index_sa;

      });

      TotalPriceChartData = data;

      console.log(TotalPriceChartData);

      
      Highcharts.chart('hpiData', {
        chart: {
            type: 'line'
        },
        title: {
            text: ''
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            categories: $scope.yearValue
        },
        yAxis: {
            title: {
                text: 'HPI'
            }
        },
        plotOptions: {
            line: {
                dataLabels: {
                    enabled: true
                },
                enableMouseTracking: false
            }
        },
        series:  [{
          name: 'Index NSA',
          data: $scope.indexValueNsa

        }, {
          name: 'Index SA',
          data: $scope.indexValueSa 

        }]
       });
        };
      }]);
  })();
