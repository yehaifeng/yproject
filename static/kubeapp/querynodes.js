var queryApp=angular.module("QueryModule",[]);

queryApp.config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('{[{');
	$interpolateProvider.endSymbol('}]}');
});

queryApp.controller('QueryController',function($scope, $http){
    // callback for success
    function success(response) {
        //$scope.title = {field1:'name', field2:'status', field3:'role', field4:'age', field5:'version', field6:'label'};
        $scope.title = response.data.title;
        $scope.items = response.data.items;
        console.log(response);
    };
    // callback for error
    function error(response) {
    	alert(respone.status);
    };

    var status_selects = ['Ready', 'NotReady'];
    console.log(status_selects);
    var url = '/kubeapp/querynodes/';
    var data = {};
    var config = '';
    $http.post(url, data).then(success, error);
    
    $scope.query = function() {
        var data = {'node_name':$scope.node_name, 
                    'label':$scope.label,
                    'status':$scope.status};
	    var url = '/kubeapp/querynodes/';
        console.log(data);
        $http.post(url, data).then(success, error);
    };
    
    /*$scope.EnterKeyQuery=function($event){    
        if($event.keyCode==13){
            $scope.query();
        }
    }*/
});
