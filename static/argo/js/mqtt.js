// window.onload = function() {
//     client = new Paho.MQTT.Client("mqtt.eclipse.org",80, "clientId-" + parseInt(Math.random() * 100, 10));

//     // var logElem = document.querySelector(".log");
//     // set callback handlers
//     client.onConnectionLost = onConnectionLost;
//     client.onMessageArrived = onMessageArrived;

//     // connect the client
//     client.connect({ onSuccess: onConnect });


//     // called when the client connects
//     function onConnect() {
//         // Once a connection has been made, make a subscription and send a message.
//         console.log("onConnect");
//         client.subscribe("/data");
//     }

//     // called when the client loses its connection
//     function onConnectionLost(responseObject) {
//         if (responseObject.errorCode !== 0) {
//             console.log("onConnectionLost:" + responseObject.errorMessage);
//         }
//     }

//     // called when a message arrives
//     function onMessageArrived(message) {
//         console.log("onMessageArrived:" + message.payloadString);
//         logElem.innerHTML += message.payloadString
//         logElem.innerHTML += "\n"
//     }
// }


var div = document.getElementsByClassName("data")[0];
window.onload = startConnect()
function startConnect() {
    // Generate a random client ID
    clientID = "clientID-" + parseInt(Math.random() * 100);

    // Fetch the hostname/IP address and port number from the form
    host = "mqtt.eclipse.org";
    port = 80;
    // Print output for the user in the messages div
    // Initialize new Paho client connection
    client = new Paho.MQTT.Client(host, port, clientID);

    // Set callback handlers
    client.onConnectionLost = onConnectionLost;
    client.onMessageArrived = onMessageArrived;

    // Connect the client, if successful, call onConnect function
    client.connect({
        onSuccess: onConnect,
    });
}

// Called when the client connects
function onConnect() {
    // Fetch the MQTT topic from the form
    topic = "/data";

    // Print output for the user in the messages div
    // div.innerHTML += '<span>Subscribing to: ' + topic + '</span><br/>';

    // Subscribe to the requested topic
    client.subscribe(topic);
}

// Called when the client loses its connection
function onConnectionLost(responseObject) {
    startConnect()
}

// Called when a message arrives
function onMessageArrived(message) {
    console.log("onMessageArrived: " + message.payloadString);

    dataset = JSON.parse(message.payloadString)
    div.innerHTML += `<p class="mb-0"> Number: <span class="font-weight-bold">`+ dataset.number + `</span></p>
                    <p class="mb-0"> Name: <span class="font-weight-bold">`+ dataset.name + `</span></p>  
                    <p class="mb-0"> Car Model: <span class="font-weight-bold">`+ dataset.car_model + `</span></p>
                    <p class="mb-0"> Mobile no.: <span class="font-weight-bold">`+ dataset.mob + `</span></p></br>`;
                    

}

// Called when the disconnection button is pressed
function startDisconnect() {
    client.disconnect();
    div.innerHTML += '<span>Disconnected</span><br/>';
}
