var dataVelocidad = null;
    var ctx = document.getElementById("grafico").getContext("2d");
    var grafico = new Chart(ctx,{type: "line"})
    var datosPorGrafico = 7;
    var puntosPorEstela = 5;
    var actualizando = false;
    var rutasBarcos = {};
    //Borrar en producción
    var cont = 0;
    $(document).ready(function () {
        var servicio = null;
         /* MAPA */
        map = L.map('map').setView(new L.LatLng(42.123795, -8.845277), 13);
        var layerBarcos = L.featureGroup().addTo(map);
        var layerBoyas = L.featureGroup().addTo(map);

         /* LISTENERS */
         $( "#btActualiza" ).click(function() {
             if (this.value === 'inicia'){
                 servicio = setInterval(getData,1000);
                 this.value = 'detine';
             }else{
                 clearInterval(servicio);
                 this.value = 'inicia';
             }
        });
         $('#variable').on('change', function() {
          //Con el cambio de variables limpiamos el gráfico
          for (barco in grafico.data.datasets){
              grafico.data.datasets[barco].data =[];
              grafico.data.labels = [];
          }
          grafico.update();
         })

         function getData(){
             $.ajax({
                type: 'GET',
                url: 'historico',
                dataType: 'json',
                success: function (data, textStatus, xhr) {
                    dataActual = data;
                    bindChart();
                    bindRanking();
                    bindBarcos();
                    bindBoyas();
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log(xhr.responseText)
                }
            })
         }
         /* BINDS */
         function bindChart() {
             var barcos = dataActual.barcos;
             var variable = $("#variable").val();
             //Tiempo
             //Quitar cuando actualice ignacio
             time = cont++;
             //grafico.data.labels.push(dataActual.time)
             grafico.data.labels.push(time)
             for (var barco in barcos) {
                 if (barcos.hasOwnProperty(barco)) {
                     if (typeof grafico.data.datasets[barco] === 'undefined') {
                         dataset = {label: barcos[barco].nombre, data: [barcos[barco][variable]],borderColor: barcos[barco].color}
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
          function bindRanking() {

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

            var barcos = dataActual.barcos;
            for (var barco in barcos) {
                 if (barcos.hasOwnProperty(barco)) {
                     $tbody.append("<tr><td>?</td><td>"+barcos[barco].nombre+"</td>" +
                         "<td style='display:none;'>"+barcos[barco].posicion*-1+"</td>" +
                         "<td style='background-color:" + barcos[barco].color +";'></td>");
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
                        backgroundColor: '#CCFFCC'
                    },
                    down: {
                        left: 0,
                        backgroundColor: '#FFCCCC'
                    },
                    fresh: {
                        left: 0,
                        backgroundColor: '#CCFFCC'
                    },
                    drop: {
                        left: 0,
                        backgroundColor: '#FFCCCC'
                    }
                }
            });
          }
          function bindBarcos(){
            var barcos = dataActual.barcos;
            for (var barco in barcos) {
                 if (barcos.hasOwnProperty(barco)) {
                     var nombre = barcos[barco].nombre;
                     if (!(nombre in rutasBarcos)){
                         //var marker = L.marker(barcos[barco].localizacion,{icon: creaIcono('hoja')});
                         var marker = L.boatMarker(barcos[barco].localizacion,{color: barcos[barco].color});
                         marker.bindLabel(nombre, { noHide: true });
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
                     }
                     rutasBarcos[nombre].marker.setHeading(barcos[barco].direccion);
                     map.fitBounds(layerBarcos.getBounds());
                }
             }
          }
          function bindBoyas(){
              layerBoyas.clearLayers();
              var boyas = dataActual.boyas;
              for (var boya in boyas) {
                  if (boyas.hasOwnProperty(boya)) {
                    var marker = L.marker(boyas[boya].localizacion);
                    marker.addTo(layerBoyas);
                  }
              }
          }
          /* HELPERS */
          function creaIcono(icono){
            return L.icon({
                iconUrl: 'static/img/' + icono + '.png',
                iconSize: [50, 50]
            })
          }
         function getRandomInt(min, max) {
            return Math.floor(Math.random() * (max - min + 1)) + min;
         }

    })