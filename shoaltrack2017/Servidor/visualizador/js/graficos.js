
    var graficos = {};
    var datosPorGrafico = 7;
    var segundosUpdate = 1;
    var altoGrafico = 100;

    $(document).ready(function () {
        var servicio = null;

         /* LISTENERS */
         $( "#btActualiza" ).click(function() {
             if (this.innerHTML === 'Start'){
                 servicio = setInterval(getData,1000 * segundosUpdate);
                 this.innerHTML = 'Stop';
                 $(this).addClass('is-danger').removeClass('is-primary');
             }else{
                 clearInterval(servicio);
                 this.innerHTML = 'Start';
                 $(this).addClass('is-primary').removeClass('is-danger');
             }
        });

         $('#variable').on('change', function() {
          for (barco in grafico.data.datasets){
              grafico.data.datasets[barco].data =[];
              grafico.data.labels = [];
          }
          grafico.update();
         })
        function cambiaVariable(){
            var variable = this.id.replace('select_','');
            var grafico = graficos[variable].chart;
            for (barco in grafico.data.datasets){
              grafico.data.datasets[barco].data =[];
              grafico.data.labels = [];
            }
            graficos[variable].variable_actual = this.value;
            graficos[variable].chart.update();
        }

         function getData(){
             $.ajax({
                type: 'GET',
                url: 'shoaltrack/services/json/last_variables.json',
                dataType: 'json',
                success: function (data, textStatus, xhr) {
                    dataActual = data;
                    bindCharts();
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log(xhr.responseText)
                }
            })
         }
         /* BINDS */
         function bindCharts(){
             var variables = dataActual.variables;
             variables.forEach(function(variable) {
                if (!$('#canv_' + variable).length){
                    var div = document.createElement("div");
                    document.body.appendChild(div);
                    var selectList = document.createElement("select");
                    selectList.id = "select_" + variable;
                    div.appendChild(selectList);
                    for (var i = 0; i < variables.length; i++) {
                        var option = document.createElement("option");
                        option.value = variables[i];
                        option.text = variables[i];
                        selectList.appendChild(option);
                    }
                    selectList.value = variable;
                    selectList.addEventListener("change", cambiaVariable);
                    var canv = document.createElement('canvas');
                    canv.id = 'canv_' + variable;
                    canv.getContext("2d");
                    canv.height = altoGrafico;
                    div.appendChild(canv);
                    graficos[variable] = {chart : new Chart(canv,{type: "line",options:{
                        responsive: true,
                        maintainAspectRatio: false
                    }}), variable_actual : variable};
                }
                bindChart(graficos[variable].chart ,graficos[variable].variable_actual);
             });
         }
         function bindChart(grafico,variable) {

             var barcos = dataActual.barcos;
             //Tiempo
             //Quitar cuando actualice ignacio
             grafico.data.labels.push(dataActual["time"]);
             for (var barco in barcos) {
                 if (barcos.hasOwnProperty(barco)) {
                     if (typeof grafico.data.datasets[barco] === 'undefined') {
                         dataset = {label: barcos[barco].nombre, data: [barcos[barco][variable]],borderColor: barcos[barco].color}
                         grafico.data.datasets.push(dataset);
                     } else {
                         grafico.data.datasets[barco].data.push(barcos[barco][variable])
                         if (grafico.data.labels.length > datosPorGrafico) grafico.data.datasets[barco].data.shift();
                     }
                }
             }
             if (grafico.data.labels.length > datosPorGrafico) grafico.data.labels.shift();
             grafico.update();
         }
    })