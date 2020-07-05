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

//  프로그레스 바

// on page load...
moveCPUProgressBar();
moveMemoryProgressBar;
// on browser resize...
$(window).resize(function () {
  moveCPUProgressBar();
  moveMemoryProgressBar;
});

// CPU 사용량 SIGNATURE PROGRESS
function moveCPUProgressBar(cpuPercentage) {
  console.log("moveCPUProgressBar");
  var getPercent = cpuPercentage / 100;
  var getProgressWrapWidth = $(".cpu-progress-wrap").width();
  var progressTotal = getPercent * getProgressWrapWidth;
  var animationLength = 0;

  // on page load, animate percentage bar to data percentage length
  // .stop() used to prevent animation queueing
  $(".cpu-progress-bar").stop().animate(
    {
      left: progressTotal,
    },
    animationLength
  );
}
// 메모리 사용령 SIGNATURE PROGRESS
function moveMemoryProgressBar(memoryPercentage) {
  console.log("moveMEMORYProgressBar");
  var getPercent = memoryPercentage / 100;
  var getProgressWrapWidth = $(".memory-progress-wrap").width();
  var progressTotal = getPercent * getProgressWrapWidth;
  var animationLength = 0;

  // on page load, animate percentage bar to data percentage length
  // .stop() used to prevent animation queueing
  $(".memory-progress-bar").stop().animate(
    {
      left: progressTotal,
    },
    animationLength
  );
}

// firebase
var firebaseConfig = {
  apiKey: "AIzaSyDU9epT6v6ByF1ETbO7Wb8bfnjl03jDzeQ",
  authDomain: "cloudlearning-c6b5b.firebaseapp.com",
  databaseURL: "https://cloudlearning-c6b5b.firebaseio.com",
  projectId: "cloudlearning-c6b5b",
  storageBucket: "cloudlearning-c6b5b.appspot.com",
  messagingSenderId: "886108415440",
  appId: "1:886108415440:web:c68e7a51da2ff23a97c5d5",
  measurementId: "G-7CPKRDBZQ2",
};

firebase.initializeApp(firebaseConfig);
// insert 문
// firebase.database().ref("CloudLearning/Monitoring").set({
//   CPU: 4444,
//   MEMORY: 4444,
// });
var CPU = document.getElementById("CPU");
var MEMORY = document.getElementById("MEMORY");

var ref = firebase.database().ref().child("CloudLearning").child("Monitoring");

// ref.child("CPU").on("value", (snap) => (CPU.innerText = "CPU : " + snap.val()));
// ref
//   .child("MEMORY")
//   .on("value", (snap) => (MEMORY.innerText = "MEMORY : " + snap.val()));
ref.child("CPU").on("value", function (snapshat) {
  var cpuPercentage = snapshat.val();
  CPU.innerText = "CPU : " + cpuPercentage + "%";
  moveCPUProgressBar(cpuPercentage);
});
ref.child("MEMORY").on("value", function (snapshat) {
  var memoryPercentage = snapshat.val();
  MEMORY.innerText = "MEMORY : " + memoryPercentage + "%";
  moveMemoryProgressBar(memoryPercentage);
});
