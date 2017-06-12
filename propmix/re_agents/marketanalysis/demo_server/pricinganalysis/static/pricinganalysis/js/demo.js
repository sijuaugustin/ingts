
(function() {
  var app = angular.module('pricing', ['angularjs-dropdown-multiselect']);
  app.controller('pricingCtrl', ['$scope', '$http', function($scope, $http) {

  	$scope.init = function(){  
  		$scope.rootURL = "https://insights.propmix.io:8102/"    
  		$scope.PriceType = 'ClosePrice';
  		$scope.TimePeriod = 'last 12 Month';
      $scope.ListOfficeName = 'TheMLSonline.com';
      $scope.propertyData = [ {id: "All", label: "All"}, {id: "Single Family Residence", label: "Single Family Residence"}, {id: "Condominium", label: "condominium"}, {id: "Townhouse", label: "Townhouse"}];
      $scope.propertyModel = [{"id": "All"}];  		
      $scope.zipcodes = ["All", "98391", "55414", "55337", "55443", "55433", "55304", "55369", "55421", "55430", "55075", "55343", "55412", "55426", "55428", "55427", "55322", "55106", "55398", "55404", "55016", "55373", "55444", "55374", "55076", "55123","55033","55311", "55379", "55409", "55126", "55420", "55112", "55066", "55008", "55327", "55434", "55436", "55303", "55378", "55128", "55425", "55437", "55079", "55038", "55449", "55441", "55386", "55129", "55120", "55107", "55125", "55305", "55109", "55352", "55068", "55419", "55316", "55124", "55407", "55422", "55330", "55044", "55448", "55318", "55429", "55410", "55320", "55423", "55447", "55117", "56304", "55122", "55024", "55040", "55364", "55417", "55403", "55113", "55376", "55406", "55118", "55082", "55362", "55056", "55306", "55345", "55313", "55309", "55105", "55071", "55411", "55104", "55408", "98042"];
      $scope.zipCurrent =  $scope.zipcodes[0];
      $scope.totalPriceData();

  	}   

  	$scope.submit = function(){
  		$scope.totalPriceData();
  	}    

  	/* api call starts here*/


    $scope.clickZipFilter = function(item){     
      $scope.zipCurrent = item;
      $scope.showZipSource = false;
      $scope.zipSearch = '';
    };

    $scope.zipFilterClick = function(){
      $scope.zipCurrent = null;     
      $scope.showZipSource = !$scope.showZipSource; 

    };

  	$scope.totalPriceData = function(){

      $scope.propertyModelString = '';

      $scope.chartValue = [];
      $scope.chartSeries = [];

      $scope.propertyModel.forEach(function(d,dindex){
        if(dindex === 0){
          $scope.propertyModelString = d.id;
        }else if(dindex > 0){
          $scope.propertyModelString += ',' + d.id;
        }
      });

      console.log($scope.propertyModelString);

    	$http({
		    method 	: 'GET',
        url     : $scope.rootURL+'pricing/pricingstats/?ListOfficeName='+$scope.ListOfficeName+'&Price='+$scope.PriceType+'&PropertyType='+$scope.propertyModelString+'&Span='+$scope.TimePeriod+'&Zip='+$scope.zipCurrent+'&format=json'

		  }).then(function successCallback(response) {
		    if(response && response.data){
        console.log(response); 
		    	
		    	$scope.createTotalPriceChart(response.data);
		    	
		    }
		  }, function errorCallback(response) {
		  	console.log(response);
        console.log($scope.propertyModel);
		  });
    };

    function predicatBy(prop){
       return function(a,b){
          if( a[prop] > b[prop]){
              return 1;
          }else if( a[prop] < b[prop] ){
              return -1;
          }
          return 0;
       }
    }

    
    $scope.createTotalPriceChart = function(data) {

      var legendIndex = 0;

      $scope.propertyModel.forEach(function(d,dindex){
        if(d && d.id && data[d.id] && $scope.TimePeriod && data[d.id][$scope.TimePeriod] && $scope.PriceType && data[d.id][$scope.TimePeriod][$scope
          .PriceType]){
          var rowData = data[d.id][$scope.TimePeriod][$scope.PriceType];

          var seriesData = [];
        
          for (var key in rowData) {
            console.log(key)

            seriesData.push({"firstLimit": parseInt(key.split(/[-+]/)[0]), "key":key,id:d.id, val : rowData[key]});
          }
          $scope.chartValue[dindex] = seriesData.sort( predicatBy("firstLimit"));
        }
      });

      $scope.chartValue.forEach(function(d){
        var chartSeriesTemp = [];
        d.forEach(function(x,xindex){
          chartSeriesTemp[xindex] = x.val;
        });
        $scope.chartSeries.push({"name":d[0].id,"data":chartSeriesTemp});
      });

      console.log($scope.chartSeries);

      
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
          categories: ["0-100K","100K-200K","200K-300K","300K-400K","400K-500K","500K-600K","600K-700K","700K-800K","800K-900K","900K-1M","1M+"],
          crosshair: true
        },
        yAxis: {
          min: 0,
          title: {
            text: 'No of Properties'
          }
        },
        tooltip: {
          headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
          pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y:.1f} </b></td></tr>',
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
        series: $scope.chartSeries
      });
    };
  }]);
})();