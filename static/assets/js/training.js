
let form = document.querySelector("form");
let formsetContainer = document.querySelectorAll(".formset_container");
let totalForms = document.querySelector("#id_exerciseroutine_set-TOTAL_FORMS");
let initialForms = document.querySelector("#id_exerciseroutine_set-INITIAL_FORMS");
let addButton = document.querySelector("#add_button");


$("#add_button").on("click", function (e) {
  e.preventDefault();
  let formsetContainer = document.querySelectorAll(".formset_container");
  let totalForms = document.querySelector("#id_exerciseroutine_set-TOTAL_FORMS");

  let formNum = formsetContainer.length;

  let newForm = formsetContainer[0].cloneNode(true);
  let formRegex = RegExp(`exerciseroutine_set-(\\d){1}-`, "g");
  
  console.log("add_button", formsetContainer, formNum, newForm, form);

  newForm.innerHTML = newForm.innerHTML.replace(
    formRegex,
    `exerciseroutine_set-${formNum}-`
  );
  form.insertBefore(newForm, addButton.parentNode);

  totalForms.value = `${formNum + 1}`;
});

$("form").on("click", "#button-id-delete", function (e) {
  e.preventDefault();
  let formsetContainer = $(".formset_container");
  let formNum = formsetContainer.length - 1;
  let totalForms = $("#id_exerciseroutine_set-TOTAL_FORMS");

  if (formNum >= 1) {
    $(this).closest(".formset_container").remove();
    
    formsetContainer = document.querySelectorAll(".formset_container");
    for(i=0; i<formsetContainer.length; i++){
      formsetContainer[i].innerHTML = formsetContainer[i].innerHTML.replace(
        RegExp(`exerciseroutine_set-(\\d){1}-`, "g"),
        `exerciseroutine_set-${i}-`
      );
    }

    totalForms.attr("value", `${formsetContainer.length}`);
  }
});
