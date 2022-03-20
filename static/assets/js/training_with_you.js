let exerciseRoutineForm = document.querySelector("#exerciseRoutineForm");
let formSubmit = document.querySelector("input[type=submit]");

let openBottomAction = document.querySelector('#openBottomAction');
let closeBottomAction = document.querySelector('#closeBottomAction');
let bottomActionContainer = document.querySelector('#bottomActionContainer');

function setCounter(element, seconds, onComplete) {
  return $(element).countdown360({
    radius      : 60,
    seconds     : seconds,
    fontColor   :'#FFFFFF',
    autostart   : false,
    onComplete  : onComplete
  });
}


function setExerciseComplete(values, form) {
  $.ajax({
    method: "POST",
    data: values,
    url: "/api/training/progress-exercise/",
    success: function (data) {
      let nextExercise = $(form).data('next') ? `?exercise=${$(form).data('next')}`: '';      
      window.location = nextExercise;
    },
  });
}

$('#openBottomAction').click(function () {
  let seconds = $("#mobileCountdown").data('time') ? $("#mobileCountdown").data('time') : 1;
  let counter = setCounter('#mobileCountdown', seconds, function () { 
    $('#exerciseRoutineForm button[type="submit"]').prop("disabled", false);
    $('#exerciseRoutineForm').submit();
  })
  counter.start();
  $('#bottomActionContainer').removeClass('close').addClass('active');
});

$('#closeBottomAction').click(function () {
  $('#bottomActionContainer').removeClass('active').addClass('close');
});


$("#exerciseRoutineForm").parsley();

$("#exerciseRoutineForm").submit(function(e) {
  e.preventDefault();
  let values = $(this).serialize();

  console.log(values);
  setExerciseComplete(values, this);
});

$("#exerciseRoutineDesktopForm").parsley();

$("#exerciseRoutineDesktopForm").submit(function(e) {
  e.preventDefault();
  let values = $(this).serialize();

  console.log(values);
  setExerciseComplete(values, this);
});

$('#openDesktopFormBtn').click(function() {
  let seconds = $("#deskCountdown").data('time') ? $("#deskCountdown").data('time') : 1;
  let counter = setCounter('#deskCountdown', seconds, function () { 
    $('#exerciseRoutineDesktopForm button[type="submit"]').prop("disabled", false);
    $('#exerciseRoutineDesktopForm').submit();
  })
  counter.start();
  $('#desktopFormActivation').addClass( "d-none" );
})