var baseURL="http://160.98.31.214:5000";

function startAdminData(){
	getAdminList();	
}

function getAdminList(data){
	//Get the parameters descriptions
	$.ajax({
		async: true, 
		method: 'GET',
		url:baseURL + '/get-admin-data',
		headers: {  
			"Accept" : "application/json"
		},
		success:function(data){
			populateList(data);	  
	 	},

		error: function(XMLHttpRequest, textStatus, errorThrown) { 
			alert("Status: " + textStatus+", Error: " + errorThrown);  
		    } 
	});
}

function populateList(data)
{
	var result = JSON.parse(data);
   	for(var i=0;i<result.length;i++){
		 var tableauDonnee = document.getElementById('table_admin');
		 
		 var newLine = document.createElement("tr");
		 var cell_id = document.createElement("td");
		 var cell_admin = document.createElement("td");
		 var cell_check = document.createElement("td");
		 cell_id.style.width = '150px';
		 cell_admin.style.width = '150px';
		 cell_id.appendChild(document.createTextNode(i+1));
		 cell_admin.appendChild(document.createTextNode(result[i].pseudo));
		 
		 var checkBoxRef = document.createElement('input');
		 
		 checkBoxRef.type = 'checkbox';
		 checkBoxRef.value = result[i].pseudo;
		 cell_check.appendChild(checkBoxRef);	
		 newLine.appendChild(cell_id);
		 newLine.appendChild(cell_admin);
		 newLine.append(cell_check);
		 newLine.style.borderBottom = "thin solid #333";

		 tableauDonnee.appendChild(newLine);
		 tableauDonnee.style.margin= " 10px";
	

	}
}

function addAdmin(){
	var oldVal = '';
	var username = prompt("Nom d'utilistateur:", oldVal);
	if (username === "") {
	     username = prompt("Veuiller entrer un nom d'utilistateur");
	} else if (username) {
		oldVal = '';
		var password = prompt("Mot de pass:", oldVal);
		if (password === "") {
		     password = prompt("Veuiller entrer un nom d'utilistateur");
		} else if (password) {
		    $.ajax({
				url: baseURL+"/add-admin",
				dataType:'json',
				data:{"username":username,"password":password},
                                mimeType: 'application/json',
                                contentType: 'application/json; charset=UTF-8', 
				type: 'POST',
				success: function(data){
					prompt("L'administrateur "+username+" à été ajouté avec succès !")
				},
			error: function(XMLHttpRequest, textStatus, errorThrown) { 
			alert("Status: " + textStatus+", Error: " + errorThrown);  
			} 
		});
		} 
	}
}

function deleteAdmin(){$
	var username = prompt("Nom d'utilistateur");
	while(username == ""){
		if(username != null && username != ""){
			alert("salut");
		}else{
			break;
		}
		var username = prompt("Veuiller entrer un nom d'utilistateur");
	}
var password = prompt("Mot de passe");
			while(password == ""){
				if(password == null){
					break;
				}
				if(password != ""){
					$.ajax({
					    url: baseURL+ "/add-admin" ,
					    dataType: 'json',					
					    data: JSON.stringify(username, password),
					    type: 'POST',
					    success: function(data){
					       alert("L'administrateur "+username+" à été ajouté avec succès !")
					    },
					});
				}
				var password = prompt("Veuiller entrer un mot de passe");	
			}
}


