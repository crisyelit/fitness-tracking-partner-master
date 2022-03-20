$(function () {
  "use strict";

  $.ajax({
    method: "GET",
    url: "/api/training/progress",
    contentType: "application/json",
    success: function (data) {
      console.log(data);

      
      if (data && data.length > 0) {

        let currentRoutine = data[0];

        let currentRoutineTotalDay = currentRoutine.customer_routine.routine_total_day;
        let currentRoutineTotalDayPercent = parseInt( data.length * 100 / currentRoutineTotalDay);
        let currentRoutineTotalDayPercentRest = 100 - currentRoutineTotalDayPercent;

        console.log(currentRoutineTotalDayPercent);
        
        let weekRoutineProgressChartHtml = `
          <span class="peity-donut"
            data-peity='{ "fill": ["#65e0e0","#e5e9f2"], "height": 110, "width": 110, "innerRadius": 46 }'>${currentRoutineTotalDayPercent},${currentRoutineTotalDayPercentRest}</span>

          <div class="pos-absolute a-0 d-flex flex-column align-items-center justify-content-center">
            <h3 class="tx-rubik tx-spacing--1 mg-b-0">${currentRoutineTotalDayPercent}%</h3>
            <span class="tx-9 tx-semibold tx-sans tx-color-03 tx-uppercase">${data.length}/${currentRoutineTotalDay} dias</span>
          </div>
        `
        let weekRoutineProgressSpanHtml = `${currentRoutineTotalDayPercent}%`;

        $('#weekRoutineProgressChart').html(weekRoutineProgressChartHtml);
        $('#weekRoutineProgressSpan').html(weekRoutineProgressSpanHtml);

        $(".peity-donut").peity("donut");


        data = data.map((item, index) => {
          console.log(item);

          let progressBar = item.completed_exercise * 100 / item.total_day_exercise;

          let mediaHtml = `
          <div class="bd-t media py-2">
            <div class="media-body">
              <div class="d-flex justify-content-between">
                <div>
                  <h6 class="tx-14 mg-b-2">${item.day.name}</h6>
                  <p class="tx-color-03 tx-12 mg-b-10">${item.day.routine.name}</p>
                </div>
                <span class="tx-gray-400">${item.created_at_date}</span>
              </div>
              <div class="progress ht-4 op-7 mg-b-5">
                <div class="progress-bar wd-${parseInt(progressBar)}p" role="progressbar" aria-valuenow="${parseInt(progressBar)}" aria-valuemin="0"
                  aria-valuemax="100"></div>
              </div>
              <div class="d-flex justify-content-between tx-12">
                <span class="tx-color-03">Ejercicios</span>
                <strong class="tx-medium">${item.completed_exercise}/${item.total_day_exercise}</strong>
              </div>
            </div><!-- media-body -->
          </div><!-- media -->
          `;

          return mediaHtml;
        });

        console.log(data);

        $('#weekProgress .card-body').html(data.join(''));
      }
    },
  });
});
