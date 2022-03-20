$("#openFilterSidebar").click(function () {
  $("#filterSidebar").removeClass("close").addClass("active");
});

$("#closeFilterSidebar").click(function () {
  $("#filterSidebar").removeClass("active").addClass("close");
});

$("#id_tags").select2({
  tags: true,
  multiple: "multiple",
  tokenSeparators: [","],
});
