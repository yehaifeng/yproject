var queryApp=angular.module("QueryModule",[]);

queryApp.config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('{[{');
	$interpolateProvider.endSymbol('}]}');
});

queryApp.controller('QueryController',function($scope, $http){
    // callback for success
    function success(response) {
        $scope.title = response.data.title;
        $scope.items = response.data.items;
        $scope.detail = response.data.detail_data;
        console.log(response);
    };
    // callback for error
    function error(response) {
    	alert(respone.status);
    };

    //$scope.query_tab = ['name', 'label'];
    //$scope.status_selects = ['All', 'Ready', 'NotReady'];
    var url = '/kubeapp/querypv/';
    var data = {};
    var config = '';
    $http.post(url, data).then(success, error);

    // kick the "query" label    
    $scope.query = function() {
        var data = {'name':$scope.name};
	    var url = '/kubeapp/querypv/';
        console.log(data);
        $http.post(url, data).then(success, error);
    };
    $(window).keydown(function (e) {
        if(e.which == 13){
            $scope.query();
        }
    });
});
