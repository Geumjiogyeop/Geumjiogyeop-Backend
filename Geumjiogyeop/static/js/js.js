$("#etc-textarea").hide();

$("#check-box").click(function(){
    $("#circle-fill").css("fill","#FFA24B");
    $("#circle-fill").css("fill-opacity","1");
});

const firstBtns = document.querySelectorAll(".first-btn");
firstBtns.forEach(button => {
    button.addEventListener("click", function() { // 일반 함수로 변경
        firstBtns.forEach(btn => btn.classList.remove("selected"));
        this.classList.add("selected");
    });
});

const fourthBtns = document.querySelectorAll(".fourth-btn");
fourthBtns.forEach(button => {
    button.addEventListener("click", function() { // 일반 함수로 변경
        fourthBtns.forEach(btn => btn.classList.remove("selected"));
        this.classList.add("selected");
    });
});

window.addEventListener('DOMContentLoaded', function() {
    firstBtns[0].classList.add('selected');
    fourthBtns[0].classList.add('selected');
});



var realationship = "me";
var userID = "";
var date = "";
var type = "admission";
var etc = "";
var isClicked = "";
var isSubmit="false";
var username="";

//realationship 
$("#me").click(function(){
    realationship = "me";
});
$("#family").click(function(){
    realationship = "family";
});
$("#rel-etc").click(function(){
    realationship = "rel-etc";
});

//userID
$("#userID").on("change",function(){
    userID = $(this).val();
    checkSubmit();
})

$("#name").on("change",function(){
    username = $(this).val();
    checkSubmit();
})

//date
$("#date").on("change",function(){
    date = $(this).val();
    inputdate = new Date(date);
    var currentDate = new Date();

    if (inputdate > currentDate) {
        alert("미래 날짜는 선택할 수 없습니다.");
    }else{
        console.log(date);
        checkSubmit();
    }
})

//type
$("#admission").click(function(){
    type = "admission";
});
$("#death").click(function(){
    type = "death";
});
$("#type-etc").click(function(){
    type = "type-etc";
    $("#etc-textarea").show();
});
$("#etc-textarea").on("change",function(){
    etc = $(this).val();
    checkSubmit();
})

//isClicked
$("#check-box").click(function(){
    isClicked = "true";
    console.log(realationship);
    console.log(type);
    console.log(isClicked);
    checkSubmit();
});

function check(){
    if(userID!=""&&date!=""&&isClicked=="true"&&username!=""){
        if(type=="type-etc"){
            if(etc!=""){
                isSubmit="true";
                console.log(isSubmit);
            }
        }else{
            isSubmit="true";
            console.log(isSubmit);
        }
    }else{
        console.log(isSubmit);
    }
}

function checkSubmit(){
    check();
    if (isSubmit === "true"){
        $("#submitBtn").css("background-color","#FFA24B");
        $("#submitBtn").css("color","#FFFFFF");
    }
}