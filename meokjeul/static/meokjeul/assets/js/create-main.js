$(document).ready(function () {

    // findAddressBtn 버튼 클릭시 주소 찾기 페이지 새 창으로 열기
    $('#findAddressBtn').on("click", function () {
        window.open("findAddress", "주소 찾기", "width=650px,height=720px");
    });

    initeMap(37.5666171, 126.9782463);

});

function initeMap(lan, lon) {

    let lating = new naver.maps.LatLng(lan, lon); // 초기위치 : 37.8217485, 127.0689602

    let mapOptions = {
        center: lating,
        zoom: 12
    };

    let map = new naver.maps.Map('map', mapOptions);

    let marker = new naver.maps.Marker({
        map: map,
        position: lating
    });
}

function getCoord() {
    let csrf_token = $('[name=csrfmiddlewaretoken]').val();

    // findAddress.html에 있는 input 태그의 id인 addressInput을 이용하여 값을 가져온다.
    // input에 값이 없을 경우 null이 들어온다.
    let addressInput = $('#addressInput').val();
    if (addressInput == "" || addressInput.length == 0) {
        alert("상세 주소를 입력해주세요.");
    } else if (addressInput.length < 2) {
        alert("2글자 이상 입력해주세요.");
    } else {
        $.ajax({
            url: "/create/findAddressProc/",
            type: "post",
            dataType: "text",
            data: {
                "address": addressInput
            },
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            },
            success: function (data) {
                let obj = JSON.parse(data); // coord
                console.log(data);

                if (obj.resultCode == 0) {
                    // 정확한 주소 입력 요청
                    $('#findAddressResultRoad').html("");
                    $('#findAddressResultJibun').html("");
                    $('#confirmAddress').html("");
                    alert("정확한 주소를 입력해주세요.");
                } else { // resultCode == 1일 경우
                    let x = obj.x; // 경도
                    let y = obj.y; // 위도
                    $(opener.document).find('input[name=coord_y]').val(y);
                    $(opener.document).find('input[name=coord_x]').val(x);

                    initeMap(y, x);

                    let road = obj.road; // 도로명주소
                    let jibun = obj.jibun; // 지번주소

                    $('#findAddressResultRoad').html("<p>" + road + "</p>");
                    $('#findAddressResultJibun').html("<p>" + jibun + "</p>");
                    $('#confirmAddress').html(
                        "<p>이 위치로 등록하시겠습니까? </p>" +
                        "<button type='button' id='addLocation' onclick='addLocation()'" +
                        "style='margin-right:0.5em'>등록</button>" +
                        "<button type='button' id='closeBtn' onclick='javascript:window.close()'>취소</button>");
                }

            },
            error: function (e) {
                console.log(e);
            }
        });

    }
}

function addLocation() {
    let roadAddress = $('#findAddressResultRoad').text();
    $(opener.document).find("input[name=address]").val(roadAddress);
    window.close();
}