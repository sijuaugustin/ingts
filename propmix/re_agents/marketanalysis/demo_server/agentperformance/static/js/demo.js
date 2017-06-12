(function() {
  var app = angular.module('marketShare', []);
  app.controller('marketShareCtrl', ['$scope', '$http', function($scope, $http) {

  	$scope.init = function(){
		$scope.rootURL = "https://insights.propmix.io:8102/"
		$scope.monthsBack = '18M';
		$scope.propertySubType = 'All';
      $scope.state = 'All';
      $scope.listOfficeName = 'TheMLSonline.com';
      $scope.enableActiveListing = 'activeListingFirst';
      $scope.activeListingFlag = false;
  		$scope.totalPriceData();
  		$scope.avgPriceData();
  		$scope.listPriceData();
      $scope.loading = true;
  	}

  	$scope.submit = function(){
  		$scope.totalPriceData();
  		$scope.avgPriceData();
  		$scope.listPriceData();
  		$scope.loading = true;
  	}


  	/* api call starts here*/
  	$scope.totalPriceData = function(){
      $scope.loading = true;
    	$http({
		    method 	: 'GET',
		    url 		: $scope.rootURL+'reagents/monetorystats/?State='+$scope.state +'&ListOfficeName='+ $scope.listOfficeName + '&PropertyType=' + $scope.propertySubType + '&Span=' + $scope.monthsBack +'&format=json'

		  }).then(function successCallback(response) {
		    if(response && response.data){
          // response.data.forEach(function(d){
          //   d.Number_of_Transactions_Active = 20;
          //   d.Total_ListPrice_Active = 1000;
          // });
          $scope.totalPrice = response.data;
		    	$scope.createTotalPriceChart(response.data);
		    	
		    }
        $scope.loading = false;
		  }, function errorCallback(response) {
        $scope.loading = false;
		  	console.log(response);
		  });
    };

    $scope.avgPriceData = function(){
      $scope.loading = true;
    	$http({
		    method 	: 'GET',
		    url 		: $scope.rootURL + 'reagents/slstats/?ListOfficeName=' + $scope.listOfficeName + '&PropertyType=' + $scope.propertySubType +'&Span=' + $scope.monthsBack + '&State=' + $scope.state + '&format=json'

		  }).then(function successCallback(response) {
		    if(response && response.data){
          
		    	$scope.createAveragePriceChart(response.data);
		    	
		    }
        $scope.loading = false;
		  }, function errorCallback(response) {
        $scope.loading = false;
		  	console.log(response);
		  });
    };

    $scope.listPriceData = function(){
      $scope.loading = true;
    	$http({
		    method 	: 'GET',
		    url 		: $scope.rootURL + 'reagents/sharestats/?ListOfficeName=' + $scope.listOfficeName + '&PropertyType=' + $scope.propertySubType + '&Span=' + $scope.monthsBack + '&State=' + $scope.state + '&format=json'

		  }).then(function successCallback(response) {
		    if(response && response.data){
          $scope.PieData = response.data;
		    	$scope.createListPriceChart(response.data);
		    	$scope.createSoldPriceChart(response.data);
		    	
		    }
        $scope.loading = false;
		  }, function errorCallback(response) {
		  	console.log(response);
        $scope.loading = false;
		  });
    };


  	/* api call ends here*/

    $scope.createTotalPriceChart = function(data) {
      console.log(data);

			$scope.totalPriceLegend = [];
			$scope.totalPriceFirst = [];
			$scope.totalPriceSecond = [];
      TotalPriceChartData = [];

			data.forEach(function(d,dindex){
        $scope.totalPriceLegend[dindex] = d.Agent_Name;
        $scope.totalPriceSecond[dindex] = d.Total_ClosePrice_Sold;

        if($scope.activeListingFlag){
          $scope.totalPriceFirst[dindex] = d.Total_ListPrice_Sold + d.Total_ListPrice_Active;

          
          TotalPriceChartData.push({
            "Total_ListPrice_Sold" : d.Total_ListPrice_Sold + d.Total_ListPrice_Active,
            "Number_of_Transactions_List" : d.Number_of_Transactions_Sold + d.Number_of_Transactions_Active,
            "Total_ClosePrice_Sold" : d.Total_ClosePrice_Sold,
            "Number_of_Transactions_Close" : d.Number_of_Transactions_Sold
          });
        }else if($scope.activeListingFlag === false){
          $scope.totalPriceFirst[dindex] = d.Total_ListPrice_Sold;

          TotalPriceChartData.push({
            "Total_ListPrice_Sold" : d.Total_ListPrice_Sold,
            "Number_of_Transactions_List" : d.Number_of_Transactions_Sold,
            "Total_ClosePrice_Sold" : d.Total_ClosePrice_Sold,
            "Number_of_Transactions_Close" : d.Number_of_Transactions_Sold
          });
        }
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
            '<td style="padding:0"><b>{point.y:.1f} $</b></td></tr>',
          footerFormat: '</table>',
          shared: true,
          useHTML: true
        },
        plotOptions: {          
          column: {
             dataLabels: {
                    enabled: true,
            pointPadding: 0.2,
            borderWidth: 0
          }          
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
				$scope.averagePrice[dindex] = parseFloat(d.Sold_to_List_deviation_percent.toFixed(2));				
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
         tooltip: {
          headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
          pointFormat: '<tr><td style="color:{series.color};padding:0">{point.Agent_Name} </td>' +
            '<td style="padding:0"><b>{point.y:.1f}%</b></td></tr>',
          footerFormat: '</table>',
          shared: true,
          useHTML: true
        },
        plotOptions: {
          column: {
             dataLabels: {
                    enabled: true,
            pointPadding: 0.2,
            borderWidth: 0
          }
        }
        },
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

        }, 
        { // Secondary yAxis
          gridLineWidth: 1,
          title: {
            text: 'List vs Sold Price Movement',
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
      data.forEach(function(d,dindex){
        $scope.listPrice[dindex] = d;
          if($scope.activeListingFlag){
            $scope.listPrice[dindex]["y"] = d.ListPrice_Percent_Sold;
          }else if($scope.activeListingFlag === false){
            $scope.listPrice[dindex]["y"] = d.ListPrice_Percent_Active;
          }
      });

      console.log($scope.listPrice);
          Highcharts.chart('list_price_share', { 
           chart: {
             plotBackgroundColor: null,
             plotBorderWidth: null,
             plotShadow: false,
             type: 'pie'
           },
           title: {
              text: 'List Price Share'
           },
          tooltip: {
              pointFormat: '<b>{point.Agent_Name}</b>: {point.percentage:.1f}%'
           },
          plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.Agent_Name}</b>: {point.percentage:.1f}%',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    }
                }
            }
        },
        series: [{
            name: '',
            colorByPoint: true,
            data: $scope.listPrice
        }]
    });
};
  

     $scope.createSoldPriceChart = function(data) {
      
      $scope.soldPrice = [];    

      data.forEach(function(d,dindex){
        $scope.soldPrice[dindex] = d;
         $scope.listPrice[dindex]["y"] = d.ClosePrice_Percent_Sold;

      });
           Highcharts.chart('sold_price_share', {
           chart: {
             plotBackgroundColor: null,
             plotBorderWidth: null,
             plotShadow: false,
             type: 'pie'
           },
           title: {
              text: 'Sold Price Share'
           },
          tooltip: {
              pointFormat: '{point.Agent_Name}: <b>{point.percentage:.1f}%</b>'
           },
          plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.Agent_Name}</b>: {point.percentage:.1f} %',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    }
                }
            }
        },
        series: [{
            name: '',
            colorByPoint: true,
            data: $scope.soldPrice
        }]
    });
    };    

    $scope.activeListFlagChange = function(){
      $scope.createTotalPriceChart($scope.totalPrice);
      $scope.createListPriceChart($scope.PieData);
    };

  }]);
})();