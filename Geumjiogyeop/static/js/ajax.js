$("#submitBtn").click(function () {
  check();
  console.log("isSubmit:" + isSubmit);
  if (isSubmit == "true") {
    if (type == "type-etc") {
      $.ajax({
        type: "post", // 타입 (get, post, put 등등)
        url: "http://=175.45.194.93//report/", // 요청할 서버url
        async: true, // 비동기화 여부 (default : true)
        headers: {
          // Http header
          "Content-Type": "application/json",
          "X-HTTP-Method-Override": "POST",
        },
        dataType: "json", // 데이터 타입 (html, xml, json, text 등등)
        data: JSON.stringify({
          // 보낼 데이터 (Object , String, Array)
          name: username,
          relation: realationship,
          victim_id: userID,
          date: date,
          type: type,
          etc: etc,
        }),
        success: function (result) {
          // 결과 성공 콜백함수
          console.log(result);
        },
        error: function (request, status, error) {
          // 결과 에러 콜백함수
          console.log(error);
        },
      });
      console.log("통신 코드 성공");
      console.log("realationship:" + realationship);
      console.log("userID:" + userID);
      console.log("date:" + date);
      console.log("type:" + type);
      console.log("etc:" + etc);

      alert("신고접수 되었습니다.");
    } else {
      $.ajax({
        type: "post", // 타입 (get, post, put 등등)
        url: "http://175.45.194.93//report/", // 요청할 서버url
        async: true, // 비동기화 여부 (default : true)
        headers: {
          // Http header
          "Content-Type": "application/json",
          "X-HTTP-Method-Override": "POST",
        },
        dataType: "json", // 데이터 타입 (html, xml, json, text 등등)
        data: JSON.stringify({
          // 보낼 데이터 (Object , String, Array)
          name: username,
          relation: realationship,
          victim_id: userID,
          date: date,
          type: type,
        }),
        success: function (result) {
          // 결과 성공 콜백함수
          console.log(result);
        },
        error: function (request, status, error) {
          // 결과 에러 콜백함수
          console.log(error);
        },
      });
      console.log("realationship:" + realationship);
      console.log("userID:" + userID);
      console.log("date:" + date);
      console.log("type:" + type);
      alert("신고접수 되었습니다.");
    }
  } else {
    console.log("isSubmit:" + isSubmit + "상태이므로 오류");
  }
});
