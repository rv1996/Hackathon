$(document).ready(function () {

	// Write your custom Javascript codes here...

});

var adddomfunc = function () {

	alert("working");
	var optsel = document.getElementById('select_min').options;
	for (var i = 0; i < optsel.length; i++) {
		if (optsel[i].selected)
			creatediv(optsel[i].value);
	}
	var optrec = document.getElementById('rec_min').options;
	for (var k = 0; k < optrec.length; k++) {
		if (optrec[k].selected)
			creatediv(optrec[k].value);
	}


}
var clearmin = function () {
	var par = document.getElementById('minpanel');
	while (par.childElementCount != 2) {
		par.removeChild(par.firstChild);
	}
}
var creatediv = function (val) {
	var min = document.createElement('div');
	var par = document.getElementById('minpanel');
	par.insertBefore(min, par.firstChild);
	min.innerHTML = val;
	min.className = "col-md-6 addedmin";
}
