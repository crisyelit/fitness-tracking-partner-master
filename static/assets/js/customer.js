
let form = document.querySelector("form");
let formsetContainer = document.querySelectorAll(".formset_container");
let totalForms = document.querySelector("#id_form-TOTAL_FORMS");
let addButton = document.querySelector("#add_button");

$("#add_button").on("click", function (e) {
  e.preventDefault();
  let formsetContainer = document.querySelectorAll(".formset_container");
  let totalForms = document.querySelector("#id_form-TOTAL_FORMS");

  let formNum = formsetContainer.length;

  let newForm = formsetContainer[0].cloneNode(true);
  let formRegex = RegExp(`form-(\\d){1}-`, "g");
  
  console.log("add_button", formsetContainer, formNum, newForm, form);

  newForm.innerHTML = newForm.innerHTML.replace(
    formRegex,
    `form-${formNum}-`
  );
  form.insertBefore(newForm, addButton.parentNode);

  totalForms.value = `${formNum + 1}`;
});

