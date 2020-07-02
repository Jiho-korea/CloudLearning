function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      $(".csv-upload-wrap").hide();

      $(".file-upload-content").show();

      $(".csv-title").html(input.files[0].name);
    };

    reader.readAsDataURL(input.files[0]);
  } else {
    removeUpload();
  }
}

function removeUpload() {
  $(".file-upload-input").replaceWith($(".file-upload-input").clone());
  $(".file-upload-content").hide();
  $(".csv-upload-wrap").show();
}
$(".csv-upload-wrap").bind("dragover", function () {
  $(".csv-upload-wrap").addClass("csv-dropping");
});
$(".csv-upload-wrap").bind("dragleave", function () {
  $(".csv-upload-wrap").removeClass("csv-dropping");
});

//

//
$(function () {
  $("#submitButton").click(function () {
    $("#submitButton").addClass("onclic", 250, validate);
  });

  function validate() {
    setTimeout(function () {
      $("#submitButton").removeClass("onclic");
      $("#submitButton").addClass("validate", 450, callback);
    }, 2250);
  }
  function callback() {
    setTimeout(function () {
      $("#submitButton").removeClass("validate");
    }, 1250);
  }
});

//

function testReadURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      $(".test-csv-upload-wrap").hide();

      $(".test-file-upload-content").show();

      $(".test-csv-title").html(input.files[0].name);
    };

    reader.readAsDataURL(input.files[0]);
  } else {
    testRemoveUpload();
  }
}

document.getElementsByClassName(".test-file-upload-input").onchange = function (
  e
) {
  testReadURL(e.srcElement.files[0]);
};

function testRemoveUpload() {
  $(".test-file-upload-input").replaceWith(
    $(".test-file-upload-input").clone()
  );
  $(".test-file-upload-content").hide();
  $(".test-csv-upload-wrap").show();
}
$(".test-csv-upload-wrap").bind("dragover", function () {
  $(".test-csv-upload-wrap").addClass("test-csv-dropping");
});
$(".test-csv-upload-wrap").bind("dragleave", function () {
  $(".test-csv-upload-wrap").removeClass("test-csv-dropping");
});
