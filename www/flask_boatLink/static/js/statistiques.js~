var baseURL = "http://160.98.31.214:5000";
var json_param_file = "/static/js/parametres.json"
var paramT = ["tension_batterie", "tension_boost", "courant_batterie", "courant_max_moteur", "courant_moteur", "capacite_totale_batterie","capacite_dispo_pourc","puissance_inst_moteur","temps_course_possible", "vitesse_bateau",  "mode_man_course_end", "mode_avant_stop_arr", "accel_x", "accel_y", "accel_z"];
var courseT = ["type_course_qf", "type_course_ll"];
var champSelect;

var par = "";
var co = "";

function populateParamCombobox(){ 
	var select = document.getElementById("param_combobox");
	$.getJSON(json_param_file, function(json) {
		for(var i = 0; i < paramT.length; i++){
			$(select).append('<option value="'+paramT[i]+'">'+json[paramT[i]].description+'</option');
    		}
	});
	$(select).on('change', function(){
		pa = this.value;
		if(co != ""){
			setValueToChart(pa, co);
		}
	});	
}

function populateCourseCombobox(){ 
	$.ajax({
		async: true, 
		method: 'GET',
		url:baseURL + '/get-course-data',
		headers: {  
			"Accept" : "application/json"
		},
	    	success:function(data){
			var select = document.getElementById("course_combobox");
			var result = JSON.parse(data);
			var list = [];
			console.log("res" + result);
			for(var i = 0; i < result.length; i++){
				list.push(result[i].vitesse_bateau);
				console.log(result[i].vitesse_bateau);
    			}
			list.sort(compare);
			for(var i = 0; i < list.length; i++){
				$(select).append('<option value="'+list[i]+'">'+list[i]+'</option');
                                 
    			}		
			$(select).on('change', function(){
				co = $(this).val();
				if(par != ""){
					setValueToChart(pa,co);
				}	
			});			  
		},
		error: function(XMLHttpRequest, textStatus, errorThrown) { 
			alert("Status: " + textStatus+", Error: " + errorThrown);  
		} 
	});	
}


function compare(x, y) {
    return x - y;
}

	
function setValueToChart(param,course){
	$.ajax({	
            url : baseURL + '/get-stat-data',
            dataType: 'json',
	    data: JSON.stringify({'param':param,'vitesse_bateau':course}),
            type : "POST",
	    success:function(data){
		console.log(data);
		constructChart(data, param);		  
	 },
	    error: function(XMLHttpRequest, textStatus, errorThrown) { 
			alert("Status: " + textStatus+", Error: " + errorThrown);  
		} 
	});

}

function constructChart(data, column){
	$.getJSON(json_param_file, function(json) {
		var processed_json = new Array();
		var x_axes = new Array();
                console.log(data);
                
		for (i = 0; i < data.length; i++){
			processed_json.push([data[i][column]]);
				console.log([data[i][column]]);
		            }
		console.log(processed_json);
		for (i = 0; i < data.length; i++){
			var temps = data[i]['heure']+":"+data[i]['minute']+":"+data[i]['seconde'];
			x_axes.push(temps);
		}
			$(function(){Highcharts.chart('chart', {
				chart: {
					type: 'line'
				},
				title: {
					text: 'Graphique du paramètre : '+json[column].description
				},
				xAxis: {
					categories: x_axes
				},
				yAxis: {
					title: {
					    text: json[column].unite
					}
				},
				plotOptions: {
					line: {
						dataLabels: {
							enabled: true
					},
						enableMouseTracking: false
					}
				},
				series: [{
					name: json[column].description,
					data: processed_json
				    }]
				}); 
			});
		
	});
}


        
