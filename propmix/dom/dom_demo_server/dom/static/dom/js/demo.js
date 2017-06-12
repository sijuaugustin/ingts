(function() {
  var app = angular.module('domData', []);
  app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('||');
    $interpolateProvider.endSymbol('||');
  });
  app.controller('domDataCtrl', ['$scope', '$http', function($scope, $http) {

    $scope.init = function(){  
      $scope.rootURL = "https://insights.propmix.io:8106/"  
      $scope.ZipCodes = '85383';
      $scope.TimePeriod = 'last 3 Month'; 
      $scope.days = '45';   
      $scope.totalPriceData();    
      
    }   

    $scope.submit = function(){
      $scope.totalPriceData();      
    }
    
    /* api call starts here*/   

       
    $scope.totalPriceData = function(){
    
      $http({
        method  : 'GET',
        url     :  $scope.rootURL+'dom/dm/?span='+$scope.TimePeriod+'&zip='+$scope.ZipCodes+'&days='+$scope.days+'&format=json'

      }).then(function successCallback(response) {
        if(response && response.data){
        console.log(response.data.Property_information);
          
          $scope.createTotalPriceChart(response.data.Property_information);
          
        }
      }, function errorCallback(response) {
        console.log(response);
       
      });
    };
       
    $scope.createTotalPriceChart = function(data) {     
      
      $scope.priceDeviationValue = [];
      $scope.daysOnMarket = [];
      $scope.property_id = [];     
      TotalPriceChartData = [];


      data.forEach(function(d,dindex){
        if(d.DOM>$scope.days)
          console.log(d)
        $scope.priceDeviationValue[dindex] = [d.DOM,d.PriceDeviation];
        $scope.daysOnMarket[dindex] = d.DOM; 
        $scope.property_id[dindex] = d.property_id;

      });

      TotalPriceChartData = data;
      console.log($scope.priceDeviationValue);
      
      Highcharts.chart('domData', {
          chart: {
              type: 'scatter',
              zoomType: 'xy'
          },
          title: {
              text: ''
          },
          subtitle: {
              text: ''
          },
          xAxis: {
              title: {
                  enabled: true,
                  text: 'Days on Market'
              },
              startOnTick: false,
              endOnTick: false,
              showLastLabel: true
          },
          yAxis: {
              title: {
                  text: 'Price Deviation'
              }
          },
          legend: {
              layout: 'vertical',
              align: 'left',
              verticalAlign: 'top',
              x: 100,
              y: 70,
              floating: true,
              backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF',
              borderWidth: 1
          },
          plotOptions: {
              scatter: {
                  marker: {
                      radius: 3,
                      states: {
                          hover: {
                              enabled: true,
                              lineColor: 'rgb(100,100,100)'
                          }
                      }
                  },
                  states: {
                      hover: {
                          marker: {
                              enabled: false
                          }
                      }
                  },
                  tooltip: {
                      headerFormat: '',
                      pointFormat: '{point.x} days, {point.y} price'
                  }
              }
          },
        series:  [{
          name: '',
          data: $scope.priceDeviationValue
         }]
       });
        };
      }]);
  })();
