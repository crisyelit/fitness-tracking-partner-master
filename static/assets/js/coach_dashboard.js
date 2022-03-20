$(function () {
    "use strict";
  
    $.ajax({
      method: "GET",
      url: "/api/training/coach/progress",
      contentType: "application/json",
      success: function (data) {
        console.log(data);
  
        
        if (data && data.length > 0) {
  
          data = data.map((item, index) => {
            
            let customer = item.customer.get_full_name ? item.customer.get_full_name : item.customer.username;
            let progressBar = item.routine_total_day_progress.toFixed(2);
  
            let tableBody = `
            <tr>
              <td class="align-middle tx-medium">${customer}</td>
              <td class="align-middle text-right">
                <div class="wd-150 d-inline-block">
                  <div class="progress ht-4 mg-b-0">
                    <div class="progress-bar bg-teal wd-${parseInt(progressBar)}p" role="progressbar" aria-valuenow="${parseInt(progressBar)}" aria-valuemin="0" aria-valuemax="100"></div>
                  </div>
                </div>
              </td>
              <td class="align-middle text-right"><span class="tx-medium">${progressBar}%</span></td>
              <td class="align-middle text-right"><span class="tx-medium">${item.routine_total_day_completed}/${item.routine_total_day}</span></td>
            </tr>
            `;
  
            return tableBody;
          });
  
          console.log(data);
  
          $('#customerProgress .card-body .table-responsive table tbody').html(data.join(''));
        }
      },
    });
  });
  