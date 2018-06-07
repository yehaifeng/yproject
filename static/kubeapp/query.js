var queryApp=angular.module("QueryModule",[]);

queryApp.config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('{[{');
	$interpolateProvider.endSymbol('}]}');
});

queryApp.controller('QueryController',function($scope, $http){
    function success(response) {
        $scope.title = {name:'name', ip:'ip', host_ip:'host_ip', namespace:'namespace', status:'status'};
        $scope.items = response.data.pods;
        $scope.namespaces = response.data.namespaces;
        // console.log($scope.namespaces);
    };
    function error(response) {
    	alert(respone.status);
    };

    var url = '/kube/querypods/';
    var data = {};
    var config = '';
    $http({
    method: 'POST',
    url: '/kube/querypods/'
    }).then(function successCallback(response) {
	$scope.title = {name:'name', ip:'ip', host_ip:'host_ip', namespace:'namespace', status:'status'};
        $scope.items = response.data.pods;
	$scope.namespaces = response.data.namespaces;
	// console.log($scope.namespaces);
   	}, function errorCallback(response) {
    		alert(response.status);
    });
    
    $scope.query = function() {
        var data = {'pod_name':$scope.pod_name, 
                    'host_ip':$scope.host_ip, 
                    'namespace':$scope.namespace};
	    var url = '/kube/querypods/';
        console.log(data);
        // $http.post(url, data).then(success, error);
        $http({
                method: 'POST',
                url: url,
                data: data,
            }).then(function(response){
                $scope.config_json=response;
          });
    };
});
