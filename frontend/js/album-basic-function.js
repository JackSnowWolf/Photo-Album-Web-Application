// const baseUrl = "https://yxbu338w0i.execute-api.us-east-1.amazonaws.com/v1";
// const api_upload = baseUrl + "upload/";
// const s3_url="https://hw3-b2-for-photos.s3.amazonaws.com";
// const tmpurl = "https://yxbu338w0i.execute-api.us-east-1.amazonaws.com/v1/search";


function loadPhoto(json_str) {
    var results = json_str["results"];
    for (var i = 0; i < results.length; i++) {
        var obj = results[i];
        var photoSrc = obj["url"];
        var labels = obj["labels"];
        if (photoSrc != null) {
            var newElement =
                "<img class='img-fluid w-100' src='" + photoSrc + "' alt='Failed to open image: " + photoSrc + "'>"
            $("#imageCol").prepend(newElement);
        }
    }
}

function submitForm(e) {
    e.preventDefault();
    $("#imageCol").empty();
    var labels = $("#labelBox").val();
    var data = JSON.stringify({
        "q": labels
    });

    var params = {
        headers: {
            param0: 'Accept:application/json',
        },
    };

    var apigClient = apigClientFactory.newClient();
    apigClient.searchGet(params, data).then((response) => {
        console.log(response);
        loadPhoto(response);
    }).catch((error) => {
        console.log('an error occurred', error);
        var errMsg = "Failed.<br>" + error.toString();
        alert(errMsg);

    })
}

function upload(e) {
    e.preventDefault();
    var fileToLoad = document.getElementById('images').files[0];

    var filename = fileToLoad.name;
    var extension = fileToLoad.type;

    console.log(filename);
    console.log(extension);

    var fileReader = new FileReader();

    fileReader.onload = function (fileLoadedEvent) {
        var srcData = fileLoadedEvent.target.result; // base64
        // TODO
        var params = {
            headers: {
                param0: 'Accept:application/json',
            }
        };
        var solution = srcData.split("base64,")[1];
        // console.log(solution)
        var body = JSON.stringify({"img": solution, "name": fileToLoad.name});


        var apigClient = apigClientFactory.newClient();
        apigClient.uploadPut(params, body)
            .then(function (result) {
                console.log("uploaded");
                uploadShowAlert("alert-success", "Upload successfully!");
            }).catch(function (error) {
            console.log("fail");
            var errMsg = "Failed.<br>" + error.body;
            uploadShowAlert("alert-danger", errMsg);
        });

    }
    fileReader.readAsDataURL(fileToLoad);
}

// type: the alert type of bootstrap.
function uploadShowAlert(type, msg) {
    $("#formAlert").remove();

    date = new Date();
    time = date.toLocaleTimeString();
    newElement =
        "<div id='formAlert' class='alert top-1 " + type + "' role='alert'>" +
        time + "<br>" + msg +
        "</div>";
    $("#uploadAlertCol").append(newElement);
}

// // type: the alert type of bootstrap.
// function searchShowAlert(type, msg) {
//     $("#formAlert").remove();
//
//     date = new Date();
//     time = date.toLocaleTimeString();
//     newElement =
//         "<div id='formAlert' class='alert top-1 " + type + "' role='alert'>" +
//         time + "<br>" + msg +
//         "</div>";
//     $("#searchAlertCol").append(newElement);
// }














