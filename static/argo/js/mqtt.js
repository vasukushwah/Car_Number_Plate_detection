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
window.onload = startConnect()


function startConnect() {
    // Generate a random client ID
    clientID = "clientID-" + parseInt(Math.random() * 100);

    // Fetch the hostname/IP address and port number from the form
    host = "mqtt.eclipse.org"
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
    topic = "house/bulbs/bulb1";

    // Print output for the user in the messages div
    // Subscribe to the requested topic
    client.subscribe(topic);
}

// Called when the client loses its connection
function onConnectionLost(responseObject) {
    // document.getElementById("messages").innerHTML += '<span>ERROR: Connection lost</span><br/>';
    console.log("conection lost");
    
    if (responseObject.errorCode !== 0) {
        console.log(" ERROR: ' + + responseObject.errorMessage + '</span><br/>'");
    }
}

// Called when a message arrives
function onMessageArrived(message) {
    console.log("onMessageArrived: " + message.payloadString);
    // document.getElementById("messages").innerHTML += '<span>Topic: ' + message.destinationName + '  | ' + message.payloadString + '</span><br/>';
}

// Called when the disconnection button is pressed
function startDisconnect() {
    client.disconnect();
    console.log("Disconnect");
    
    // document.getElementById("messages").innerHTML += '<span>Disconnected</span><br/>';
}