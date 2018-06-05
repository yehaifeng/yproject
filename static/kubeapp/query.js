var queryApp=angular.module("QueryModule",[]);
queryApp.controller('QueryController',function($scope, $http){
    $http({
    method: 'POST',
    url: '/kube/querypods/'
    }).then(function successCallback(response) {
	$scope.title = {name:'name', ip:'ip', host_ip:'host_ip', namespace:'namespace', status:'status'}
        $scope.items = response.data;
	// console.log($scope.items);
   	}, function errorCallback(response) {
	alert("ERROR");
    });
    //$scope.person={name:"Ahui"};
    //申明了一个函数
    //var updateClock=function(){
    //    $scope.clock=new Date();        
    //};
    //申明一个计时器
    //var timer=setInterval(function(){
    //    $scope.$.apply(updateClock);
    //},1000);
    //updateClock();
});
