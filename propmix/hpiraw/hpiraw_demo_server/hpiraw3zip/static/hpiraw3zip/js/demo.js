(function() {
  var app = angular.module('hpi', ['angularjs-dropdown-multiselect']);
  app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('||');
    $interpolateProvider.endSymbol('||');
  });
  app.controller('hpiCtrl', ['$scope', '$http', function($scope, $http) {

    $scope.init = function(){  
      $scope.rootURL = "https://insights.propmix.io:8104/"  
      $scope.spanFrom = '1995';
      $scope.spanTo = '2016'; 
      $scope.ZipCodes ='01012';    
      $scope.totalPriceData();      
      $scope.getYears();
    }   

    $scope.submit = function(){
      $scope.totalPriceData();
      
    }
    
    /* api call starts here*/       

   
    $scope.totalPriceData = function(){
    
      $http({
        method  : 'GET',
        url     : $scope.rootURL+'hpiraw/3zipdata/?zip='+$scope.ZipCodes+'&span='+$scope.spanFrom+'-'+$scope.spanTo+'&format=json'

      }).then(function successCallback(response) {
        if(response && response.data){
        console.log(response); 
          
          $scope.createTotalPriceChart(response.data);
          
        }
      }, function errorCallback(response) {
        console.log(response);
       
      });
    };
  

     $scope.getYears = function(){
    
      $http({
        method  : 'GET',
        url     :  'https://insights.propmix.io:8104/hpiraw/3zipyears/'


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
      TotalPriceChartData = [];

      data.forEach(function(d,dindex){
        $scope.indexValueNsa[dindex] = d["Index (NSA)"];       
        $scope.yearValue[dindex] = d.Year+" Q"+d.Quarter;       
        $scope.periodLegend[dindex] = d.Quarter;
        

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

        }]
       });
        };
      }]);
  })();
