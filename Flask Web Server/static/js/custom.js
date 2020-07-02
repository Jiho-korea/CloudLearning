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
  // $("#submitButton").bind("click", function () {
  //   var fileVal = $(".file-upload-input").val();
  //   if (fileVal == "") {
  //     alert("CSV 파일을 선택해 주세요.");
  //     return false;
  //   }
  // });

  $("#submitButton").click(function () {
    var fileVal = $(".file-upload-input").val();
    if (fileVal == "") {
      alert("CSV 파일을 선택해 주세요.");
      return false;
    }
    $(this).addClass("onclick", 250, validate);
    $(this).css("width", "40px");
    $(this).css("border-color", "#bbbbbb");
    $(this).css("border-width", "3px");
    $(this).css("font-size", "0");
    $(this).css("border-left-color", "#015379");
  });

  $("#submitButton").hover(function () {
    $(this).css("color", "#015379");
    $(this).css("background", "white");
  });

  $("#submitButton").after(function () {
    $(this).css("content", "");
  });

  function validate() {
    // setTimeout(function () {
    //   $("#submitButton").removeClass("onclick");
    //   $("#submitButton").addClass("validate", 450, callback);
    // }, 10000);
  }
  function callback() {
    // setTimeout(function () {
    //   $("#submitButton").removeClass("validate");
    // }, 10000);
  }

  $("#testButton").click(function () {
    var testFileVal = $(".test-file-input").val();
    if (testFileVal == "") {
      alert("CSV 파일을 선택해 주세요.");
      return false;
    }
    $(this).addClass("onclick", 250, validate);
    $(this).css("width", "40px");
    $(this).css("border-color", "#bbbbbb");
    $(this).css("border-width", "3px");
    $(this).css("font-size", "0");
    $(this).css("border-left-color", "#1ecd97");
  });

  $("#testButton").hover(function () {
    $(this).css("color", "#1ecd97");
    $(this).css("background", "white");
  });

  $("#testButton").after(function () {
    $(this).css("content", "");
  });
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

// document.getElementsByClassName(".test-file-upload-input").onchange = function (
//   e
// ) {
//   testReadURL(e.srcElement.files[0]);
// };

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
