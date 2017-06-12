(function() {
  var app = angular.module('marketShare', []);
  app.controller('marketShareCtrl', ['$scope', '$http', function($scope, $http) {

  	$scope.init = function(){
  		$scope.rootURL = "http://192.168.0.96:8003/"
  		$scope.monthsBack = '12M';
  		$scope.propertySubType = 'All';
  		$scope.totalPriceData();
  		$scope.avgPriceData();
  		$scope.listPriceData();
  	}

  	$scope.submit = function(){
  		$scope.totalPriceData();
  		$scope.avgPriceData();
  		$scope.listPriceData();
  	}


  	/* api call starts here*/
  	$scope.totalPriceData = function(){
    	$http({
		    method 	: 'GET',
		    url 		: $scope.rootURL+'reagents/monetorystats/?PropertyType='+$scope.propertySubType+'&Span='+ $scope.monthsBack +'&format=json'

		  }).then(function successCallback(response) {
		    if(response && response.data){
		    	console.log(response);
		    	
		    	$scope.createTotalPriceChart(response.data);
		    	
		    }
		  }, function errorCallback(response) {
		  	console.log(response);
		  });
    };

    $scope.avgPriceData = function(){
    	$http({
		    method 	: 'GET',
		    url 		: $scope.rootURL + 'reagents/slstats/?PropertyType='+$scope.propertySubType+'&Span='+ $scope.monthsBack +'&format=json'

		  }).then(function successCallback(response) {
		    if(response && response.data){
		    	console.log(response);
		    	
		    	$scope.createAveragePriceChart(response.data);
		    	
		    }
		  }, function errorCallback(response) {
		  	console.log(response);
		  });
    };

    $scope.listPriceData = function(){
    	$http({
		    method 	: 'GET',
		    url 		: $scope.rootURL + 'reagents/sharestats/?PropertyType='+$scope.propertySubType+'&Span='+ $scope.monthsBack +'&format=json'

		  }).then(function successCallback(response) {
		    if(response && response.data){
		    	console.log(response);
		    	
		    	$scope.createListPriceChart(response.data);
		    	$scope.createSoldPriceChart(response.data);
		    	
		    }
		  }, function errorCallback(response) {
		  	console.log(response);
		  });
    };


  	/* api call ends here*/

    $scope.createTotalPriceChart = function(data) {

  console.log(data);

			$scope.totalPriceLegend = [];
			$scope.totalPriceFirst = [];
			$scope.totalPriceSecond = [];

			data.forEach(function(d,dindex){
				$scope.totalPriceLegend[dindex] = d.Agent_Name;
				$scope.totalPriceFirst[dindex] = d.Total_ClosePrice;
				$scope.totalPriceSecond[dindex] = d.Total_ListPrice;
			});
      
      Highcharts.chart('total_price', {
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
          categories: $scope.totalPriceLegend,
          crosshair: true
        },
        yAxis: {
          min: 0,
          title: {
            text: 'Total Price'
          }
        },
        tooltip: {
          headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
          pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y:.1f} mm</b></td></tr>',
          footerFormat: '</table>',
          shared: true,
          useHTML: true
        },
        plotOptions: {
          column: {
            pointPadding: 0.2,
            borderWidth: 0
          }
        },
        series: [{
          name: 'Total List Price',
          data: $scope.totalPriceFirst

        }, {
          name: 'Total Sold Price',
          data: $scope.totalPriceSecond

        }]
      });
    };
   

    $scope.createAveragePriceChart = function(data) {
    		
			$scope.averagePriceLegend = [];
			$scope.averagePrice = [];			

			data.forEach(function(d,dindex){
				$scope.averagePriceLegend[dindex] = d.Agent_Name;
				$scope.averagePrice[dindex] = d.Avg_Sold_to_List_percent;				
			});


      Highcharts.chart('average_price', {
        chart: {
          zoomType: 'xy'
        },
        title: {
          text: ''
        },
        subtitle: {
          text: ''
        },
        xAxis: [{
          categories: $scope.averagePriceLegend,
          crosshair: true
        }],
        yAxis: [{ // Primary yAxis
          labels: {
            format: '{value} %',
            style: {
              color: Highcharts.getOptions().colors[2]
            }
          },
          title: {
            text: '',
            style: {
              color: Highcharts.getOptions().colors[0]
            }
          },
          opposite: false

        }, { // Secondary yAxis
          gridLineWidth: 1,
          title: {
            text: 'Sold/List Avg %',
            style: {
              color: Highcharts.getOptions().colors[0]
            }
          },
          labels: {
            format: '{value} %',
            style: {
              color: Highcharts.getOptions().colors[1]
            }
          }

        }],

        legend: {
          layout: 'vertical',
          align: 'left',
          x: 80,
          verticalAlign: 'top',
          y: 55,
          floating: true,
          backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
        },
        series: [{
          name: '',
          type: 'column',
          yAxis: 1,
          data: $scope.averagePrice


        }]
      });
    };

    $scope.createListPriceChart = function(data) {
    	
			$scope.listPrice = [];		
			console.log(data)	;

			data.forEach(function(d){
				$scope.listPrice.push({"label":d.Agent_Name,"value":d.ListPrice_Percent});
			});

			console.log($scope.listPrice)


      FusionCharts.ready(function() {
        var fusioncharts = new FusionCharts({
          type: 'pie2d',
          renderAt: 'list_price_share',
          width: '450',
          height: '400',
          dataFormat: 'json',
          dataSource: {
            "chart": {
              "caption": "Market Share (List)",

              "subCaption": "",
              "numberPrefix": "$",
              "showPercentValues": "1",
              "showPercentInTooltip": "0",
              "decimals": "1",
              "useDataPlotColorForLabels": "1",
              //Configuring slicing distance
              "slicingDistance ": "20",
              //Theme
              "theme": "fint"
            },
            "data": $scope.listPrice
          }
        });
        fusioncharts.render();
      });
    };

    $scope.createSoldPriceChart = function(data) {

    	$scope.soldPrice = [];	
    	data.forEach(function(d){
				$scope.soldPrice.push({"label":d.Agent_Name,"value":d.ClosePrice_Percent});
			});

      FusionCharts.ready(function() {
        var fusioncharts = new FusionCharts({
          type: 'pie2d',
          renderAt: 'sold_price_share',
          width: '450',
          height: '400',
          dataFormat: 'json',
          dataSource: {
            "chart": {
              "caption": "Market Share (Sold)",

              "subCaption": "",
              "numberPrefix": "$",
              "showPercentValues": "1",
              "showPercentInTooltip": "0",
              "decimals": "1",
              "useDataPlotColorForLabels": "1",
              //Configuring slicing distance
              "slicingDistance ": "20",
              //Theme
              "theme": "fint"
            },
            "data": $scope.soldPrice
          }
        });
        fusioncharts.render();
      });
    };

  }]);
})();