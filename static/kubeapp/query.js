var queryApp=angular.module("QueryModule",[]);

queryApp.config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('{[{');
	$interpolateProvider.endSymbol('}]}');
});

queryApp.controller('QueryController',function($scope, $http){
    // callback for success
    function success(response) {
        $scope.title = {name:'name', ip:'ip', host_ip:'host_ip', namespace:'namespace', phase:'status'};
        $scope.items = response.data.pods;
        $scope.namespaces = response.data.namespaces;
        // console.log($scope.namespaces);
    };
    // callback for error
    function error(response) {
    	alert(respone.status);
    };

    var url = '/kubeapp/querypods/';
    //var url = '/kubeapp/querypods/?pod_name=' + $scope.pod_name + '&host_ip=' + $scope.host_ip + '&namespace=' + $scope.namespace;
    var data = {};
    var config = '';
    // $http.get(url).then(success, error);
    $http.post(url, data).then(success, error);
    /*$http({
    method: 'GET',
    url: url
    }).then(function successCallback(response) {
	    $scope.title = {name:'name', ip:'ip', host_ip:'host_ip', namespace:'namespace', phase:'status'};
        $scope.items = response.data.pods;
	    $scope.namespaces = response.data.namespaces;
	    // console.log($scope.namespaces);
   	}, function errorCallback(response) {
    		alert(response.status);
    });*/
    
    $scope.query = function() {
        var data = {'pod_name':$scope.pod_name, 
                    'host_ip':$scope.host_ip, 
                    'namespace':$scope.namespace};
	    var url = '/kubeapp/querypods/';
        console.log(data);
        $http.post(url, data).then(success, error);
        /*$http({
                method: 'POST',
                url: url,
                data: data,
            }).then(function(response){
                $scope.config_json=response;
          });*/
    };
    $(window).keydown(function (e) {
        if(e.which == 13){
            $scope.query();
        }
    });
});
