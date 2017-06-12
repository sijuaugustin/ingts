(function() {
  var app = angular.module('marketGrowth', ['angularjs-dropdown-multiselect']);
  app.controller('marketGrowthCtrl', ['$scope', '$http', function($scope, $http) {

  	$scope.init = function(){  
  		$scope.rootURL = "https://insights.propmix.io:8102/"     
  		$scope.state = 'All';
  		$scope.TimePeriod = 'Year over Year';
      $scope.PriceType = 'ClosePrice';
      $scope.ListOfficeName = 'TheMLSonline.com';
      $scope.propertySubType = 'All';     
  		$scope.totalPriceData();
      
  	}

  	$scope.submit = function(){
  		$scope.totalPriceData();
  	}


  	/* api call starts here*/
  	$scope.totalPriceData = function(){
    	$http({
		    method 	: 'GET',
        url     : $scope.rootURL+'marketgrowth/growthstats/?ListOfficeName='+$scope.ListOfficeName+'&Price='+$scope.PriceType+'&PropertyType='+$scope.propertySubType+'&Span='+$scope.TimePeriod+'&State='+$scope.state+'&format=json'
                  

		  }).then(function successCallback(response) {
		    if(response && response.data){
        console.log(response); 
		    	
		    	$scope.createTotalPriceChart(response.data);
		    	
		    }
		  }, function errorCallback(response) {
		  	console.log(response);        
		  });
    };    

    
    $scope.createTotalPriceChart = function(data) {

      $scope.marketgrowthAgentnames = [];
      $scope.series = [];

       data.forEach(function(d,dindex){
        $scope.marketgrowthAgentnames[dindex] = d.Agent_Name;

        if(dindex === 0){
          for (var key in d) {
            if(key != 'Agent_Name'){
              $scope.series.push({name:key,data:[]});
            }
          }
        }

        $scope.series.forEach(function(x){
          x.data[dindex] = d[x.name];
        });

       });
            
      Highcharts.chart('marketgrowth', {
        chart: {
          type: 'column'
        },
        title: {
          text: ''
        },
        subtitle: {
          text: ''
        },
        xAxis: {
          categories:  $scope.marketgrowthAgentnames,
          crosshair: true
        },
        yAxis: {
          min: 0,
          title: {
            text: 'Total Price ($)'
          }
        },
        tooltip: {
          headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
          pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y:.1f} $</b></td></tr>',
          footerFormat: '</table>',
          shared: true,
          useHTML: true
        },
        plotOptions: {
          column: {
             dataLabels: {
                    enabled: false,
            pointPadding: 0.2,
            borderWidth: 0
          }
        }
        },
          series: $scope.series
      });
    };
  }]);
})();