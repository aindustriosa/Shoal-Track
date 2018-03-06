// VARIABLES GLOBALES
var urlData ="http://192.168.0.148/shoaltrack/services/json/last_data.json"
var date=null;
var servicio=null;
var estado_prev= null;
var nombre_prev=null;
var ctx = document.getElementById("grafico").getContext('2d');
var grafico= new Chart(ctx,{
	type: "line",
	options : {
		responsive: true,
		maintainAspectRatio: false,
		tooltips: {enabled:true}
	}
	});
var actualizando = false;
var datosPorGrafico = 10;
var puntosPorEstela = 5;
var rutasBarcos = {};
var interval=1000;

//Borrar en producción
var cont = 0;

// VARIABLES LAYERS MAPA BASE
// var osm= L.tileLayer('Tiles/tiles/{z0}/{x0}/{x1}/{y0}/{y1}.png', {
	// maxZoom: 24,
	// attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
// });

// var satellite = L.tileLayer('Tiles/sat_tiles/{z0}/{x0}/{x1}/{y0}/{y1}.png', {
	// maxZoom: 24,
	// attribution: 'Leaflet &copy; Google 2017 and IGN'
// });

// var OpenSeaMap = L.tileLayer('http://tiles.openseamap.org/seamark/{z}/{x}/{y}.png', {
	// maxZoom: 24,
	// attribution: 'Map data: &copy; <a href="http://www.openseamap.org">OpenSeaMap</a> contributors'
// });

var map=L.map('map').setView(new  L.LatLng(﻿ 42.1247, -8.8463), 20);

// var baseMaps = {
            // 'OpenStreetMap': osm,'Satellite':satellite
    // }

var costaStyle = {
    "color": "black",
	"weight": 2,
    "opacity": 0.8,
	"fillColor": "#233a62",
	"fillOpacity": 0.8,
};

var lineaCosta = L.geoJson(coastLine, {
	style: costaStyle})

var buoy_icon = L.icon({
	iconUrl: 'images/buoy.svg',
	color: 'white',
	iconSize: [55,40],
	iconAnchor: [27,20],
	popupAnchor: [0,30],
	});


// CARGA DE MAPA BASE Y CONTROLES
// map.addControl(layerControl);
// map.addLayer(osm);
map.addLayer(lineaCosta);
L.control.scale().addTo(map).setPosition('topright');
map.zoomControl.setPosition('bottomleft');
var layerBarcos = L.featureGroup().addTo(map);
var layerBoyas = L.featureGroup().addTo(map);


 $( "#boton" ).click(function() {
             if (this.innerText === 'SHOW'){
                 servicio = setInterval(getRaceFile,interval);
                 this.innerText = 'PAUSE';
             }else{
                 clearInterval(servicio);
                 this.innerText = 'SHOW';
             }
        });


//CARGAR DATOS DE CARRERA

//Comprobación del estado de la carrera
function raceStatus(){
	estado=raceData["status"];
	if (estado_prev!=estado) {cleanMap(); console.log("map cleaned")}
	estado_prev=estado;
	console.log(estado);
	switch(estado) {			
		case "diseño":
		case "abierta":
			nombreCarrera();
			getCountdown();
			break;
		case "esperando":
		case "lanzamiento":
			nombreCarrera();
			mostrarViento();
			bindBarcos();
			bindBoyas();
			bindChart();
			bindRanking();
			bindLines();	
			break;
		case "comenzando":
		case "en curso":
		case "terminando":
			nombreCarrera();
			mostrarViento();
			bindBarcos();
			bindBoyas();
			bindChart();
			bindRanking();
			bindLines();
			break;
		default:
			cleanMap();
			console.log("Sin procesar - " + estado);
		
	}
	
}

// Operación get para obtener datos del archivo
function getRaceFile() {  
	$.ajax({
	type: 'GET',
	cache: false,
	url: urlData,
		dataType: 'json',
		beforeSend: function() //
			{
				
			},
		complete: function() //
			{ 	
			},
		success: function(data) //
			{
				console.log(data)
				raceData= data;
				raceStatus();
			},
		
		error: function (xhr, ajaxOptions, thrownError) //
			{
			   console.log(xhr)
			   // alert(xhr.status + xhr.responseText);
			}
	
    });
	
}

function bindBarcos(){
	var barcos = raceData.barcos;
	for (var barco in barcos) {
	if (barcos.hasOwnProperty(barco)) {
		var nombre = barcos[barco].nombre;
		if (!(nombre in rutasBarcos)){
			var marker = L.marker (barcos[barco].localizacion,{
					
					icon: L.icon({
						 iconUrl: 'images/'+barcos[barco].tipo+'_'+barcos[barco].nombreColor+'.png', 
						 iconSize: [23,36], popupAnchor: [0,40], 
						 iconAnchor: [11,15]
					 }),
			rotationAngle:barcos[barco].direccion}).bindLabel(nombre, { noHide: true 	});

			var polyline = L.polyline([barcos[barco].localizacion],{color:barcos[barco].color});
			rutasBarcos[nombre] = {"marker": marker,"polyline": polyline};
			layerBarcos.addLayer(marker);
			layerBarcos.addLayer(polyline);
		}else{
			rutasBarcos[nombre].marker.setLatLng(barcos[barco].localizacion).update();
			var puntos = rutasBarcos[nombre].polyline.getLatLngs()
			if(puntos.length < puntosPorEstela){
				rutasBarcos[nombre].polyline.addLatLng(barcos[barco].localizacion);
			}else{
				 puntos.shift();
				 puntos.push(barcos[barco].localizacion);
				 rutasBarcos[nombre].polyline.setLatLngs(puntos);
			}
			rutasBarcos[nombre].marker.setRotationAngle(barcos[barco].direccion)
		}
		
		}
	}
	$('#zoom').show();
}

	
function bindBoyas(){
	layerBoyas.clearLayers();
	var boyas = raceData.boyas;
	for (var boya in boyas) {
		if (boyas.hasOwnProperty(boya)) {
			var marker = L.marker(boyas[boya].localizacion, {icon:buoy_icon});
			marker.addTo(layerBoyas);
		}
	}
}


// COUNTDOWN
function getCountdown() {
	document.getElementById("reloj").style.visibility="visible";
	fecha=raceData["raceDate"];
    $('.countdown').downCount({
            date: fecha,
            offset: +2
        }, function () // 
		
		{
            document.getElementById("reloj").style.visibility="hidden";
			
        });
}


// TABLA DE LA CARRERA

function bindRanking(){
	
	$body = $('#ranking');

	if(actualizando) {
	  return;
	}
	actualizando = true;
	// Duplicamos la tabla
	$oldTable = $body.find('#tablaRanking');
	$newTable = $oldTable.clone();
	$newTable.hide();
	$body.append($newTable);
	$tbody = $newTable.find('tbody');
	$tbody.empty();

	var barcos = raceData.barcos;
	for (var barco in barcos) {
		 if (barcos.hasOwnProperty(barco)) {
			$tbody.append(
						"<tr>"+
							"<td class='color'><div style='background-color:" + barcos[barco].color + ";'>&nbsp;</div></td>"+
							"<td>?</td>"+
							"<td>"+barcos[barco].nombre+"</td>" +
							"<td style='display:none;'>" + barcos[barco].posicion + "</td>"+
						+"</tr>");
		}
	 }
	
	
	// Ordenamos la tabla de resultados
	$newTable.animatedSort();

	// Actualizamos la numeración
	$newTable.updateRank();
	// Animamos el cambio de posiciones
	$oldTable.rankingTableUpdate($newTable, {
	  onComplete: function(){
	  	  $('#tablaRanking').show();
		  actualizando = false;
	  },
		animationSettings: {
			up: {
				left: 0,
				backgroundColor: '#3182bd'
			},
			down: {
				left: 0,
				backgroundColor: '#9ecae1'
			},
			fresh: {
				left: 0,
				backgroundColor: '#deebf7'
			},
			drop: {
				left: 0,
				backgroundColor: '#deebf7'
			}
		}

		});
  }


//ROSA VIENTOS

function mostrarViento() {
	$('#rosa_vientos').show();
	var intensidad= raceData["windIntensity"];
	var direccion=raceData["windDirection"];
	document.getElementById("direccion").style.transform= "rotate("+direccion+"deg)";
	document.getElementById("viento").innerHTML="<p>"+intensidad+" m/s<span>Wind</span></p>";
}


//GRÁFICA DE LA CARRERA (CHART)

function cleanChart() {
	for (barco in grafico.data.datasets){
	  grafico.data.datasets[barco].data =[];
	  grafico.data.labels = [];
	}
	grafico.update();
}

//Select de variables en graph
$('#variable').on('change', cleanChart)

 function bindChart() {
	 document.getElementById("chartContainer").style.visibility="visible";
	 $(".leaflet-bottom").css('bottom', '20%'); // Subimos el boton de zoom
	 $("#zoom").css('bottom', '20%');
	 var barcos = raceData.barcos;
	 var variable = $("#variable").val();
	 //Tiempo
	 //Quitar cuando actualice ignacio
	 //time = cont++;
	 //grafico.data.labels.push(raceData.time)
	 grafico.data.labels.push(raceData['time'])
	 for (var barco in barcos) {
		if (barcos.hasOwnProperty(barco)) {
			if (typeof grafico.data.datasets[barco] === 'undefined') {
				dataset = {label: barcos[barco].nombre, data: [barcos[barco][variable]],borderColor: barcos[barco].color, fill:false}
				grafico.data.datasets.push(dataset)
			} else {
				grafico.data.datasets[barco].data.push(barcos[barco][variable])
				if (grafico.data.labels.length > datosPorGrafico) grafico.data.datasets[barco].data.shift();
			}
		}
	 }
	if (grafico.data.labels.length > datosPorGrafico) grafico.data.labels.shift();
	grafico.update();
 }

function bindLines() {
	addLine("startLine","green");
	addLine("finishLine","red");
}
 
function addLine(value,color){
	
var latlngs = raceData[value];

var polyline = L.polyline(latlngs, {dashArray: '5,5', color: color, weight:'1'}).addTo(map);

polyline.addTo(layerBoyas);
}

// LIMPIAR LOS DATOS DEL MAPA
function cleanMap() {
	//Ocultamos todos los elementos de la carrera
	$('#rosa_vientos').hide();
	document.getElementById("chartContainer").style.visibility = "hidden";
	// document.getElementById("tablaRanking").style.visibility = "hidden";
	document.getElementById("reloj").style.visibility = "hidden";
	//Limpiamos la gráfica para que comience de nuevo
	cleanChart();
	$(".leaflet-bottom").css('bottom', '0%');
	$("#zoom").css('bottom', '0%'); // Bajamos el boton de zoom
	$('#tablaRanking').hide();
	$('#zoom').hide();
	layerBoyas.clearLayers();
	layerBarcos.clearLayers();
	rutasBarcos = {};
}

//MOSTRAR NOMBRE CARRERA

function cleanNombre() {
	
	$("#raceName").remove();

}

function nombreCarrera() {
	var nombre= raceData["raceName"];
		if (nombre_prev!=nombre) {
			cleanMap(); cleanNombre();
			var titulo=document.getElementById("carrera");
			titulo.insertAdjacentHTML("beforeend",'<p id="raceName">'+nombre+'</p>');
			
		
		}
		nombre_prev=nombre;
	console.log (nombre);
}

$('#zoom').click(function() {
  map.fitBounds(layerBarcos.getBounds(), {padding: [150,150]});
});
