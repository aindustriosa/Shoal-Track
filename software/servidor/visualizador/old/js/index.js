// VARIABLES GLOBALES
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
var startButton = document.getElementById("boton");
var actualizando = false;
var datosPorGrafico = 10;
var puntosPorEstela = 5;
var rutasBarcos = {};
var interval=2000;

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

// var overlayMaps = {
          
            // 'OpenSeaMap':OpenSeaMap,
			
			// 'Línea Costa' : lineaCosta
        // }
		
// var layerControl = new L.control.layers(baseMaps, overlayMaps,{
	// position: 'topleft'});

// Icono de las boyas
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


//BOTÓN INICIALIZAR VISUALIZACIÓN
startButton.addEventListener("click", raceStart);

function raceStart(){
    console.log("Started");
	startButton.removeEventListener("click", raceStart);
    startButton.addEventListener("click", raceStop);
    startButton.innerHTML = "STOP RACE";
	raceInterval=setInterval(getRaceFile,interval);
	raceInterval;
}

function raceStop(){
	console.log("Stopped");
    startButton.removeEventListener("click", raceStop);
    startButton.addEventListener("click", raceClean);
    startButton.innerHTML = "CLEAN RACE";
	clearInterval(raceInterval);
}

function raceClean() {
	console.log("Carrera borrada");
	cleanMap();
	startButton.removeEventListener("click", raceClean);
	startButton.addEventListener("click", raceStart);
	startButton.innerHTML = "START RACE";	
}

//CARGAR DATOS DE CARRERA

//Comprobación del estado de la carrera
function raceStatus(){
	estado=raceData["status"];
	if (estado_prev!=estado) {cleanMap(); console.log("map cleaned")}
	estado_prev=estado;
	console.log(estado);
	switch(estado) {
		case "abort":
			break;
			
		case "design":
			nombreCarrera();
			getCountdown();
			break;
		case "briefing":
			nombreCarrera();
			getCountdown();
			break;
		case "waiting":
			nombreCarrera();
			getCountdown();
			mostrarViento();
			bindBarcos();
			bindBoyas();
			bindLines();			
			break;
			
		case "launch":
			nombreCarrera();
			getCountdown();
			mostrarViento();
			bindBarcos();
			bindBoyas();
			bindLines();			
			break;
		
		case "start":
			nombreCarrera();
			mostrarViento();
			bindBarcos();
			bindBoyas();
			bindChart();
			bindRanking();
			bindLines();
			break;
		default:
			console.log("no está haciendo el switch");
		
	}
	
}

// Operación get para obtener datos del archivo
function getRaceFile() {  
	$.ajax({
	type: 'GET',
	url: "http://192.168.0.148:4999/historico",
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
	$('#zoom').click(mapBounds());
	
}
	
function mapBounds(){
	map.fitBounds(layerBarcos.getBounds(), {padding: [150,150]});
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
							"<td class='color' style='background-color:" + barcos[barco].color + ";'>?</td>"+
							"<td>"+barcos[barco].nombre+"</td>" +
							"<td style='display:none;'>" + barcos[barco].posicion*-1 + "</td>"+
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
  $('#tablaRanking').show();
  }



// Popups con información de la capa (de momento sólo el nombre)

// function openPopUp(e) {
		// var layer = e.target;
		// layer.openPopup();
	// }

// function mostrarPopups (feature,layer) {
			// contenido='<p class="popup">'+feature.properties.name + 
				// '</p>'
			// layer.bindPopup(contenido,{closeButton: false, offset: new L.Point(1, -50)});
		 // }
				
// function popup_propiedades (feature, layer) { 
	// if (feature.properties && feature.properties.name) { 
		// mostrarPopups(feature,layer);}
	// layer.on({
		// mouseover: openPopUp,
	// });
// }

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
	 time = cont++;
	 //grafico.data.labels.push(raceData.time)
	 grafico.data.labels.push(time)
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
	document.getElementById("rosa_vientos").style.visibility = "hidden"
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
		titulo.insertAdjacentHTML("beforeend",'<p id="raceName">'+nombre+'</p>');}
	console.log (nombre);
}


// POP UP MUESTRA COORDENADAS
var popup = L.popup();

function onMapClick(e) {
    popup
        .setLatLng(e.latlng) // Sets the geographical point where the popup will open.
        .setContent("Coordenadas:<br> " +  e.latlng.lng.toString() + "," + e.latlng.lat.toString() ) // Sets the HTML content of the popup.
        .openOn(map); // Adds the popup to the map and closes the previous one. 
}

map.on('click', onMapClick);
