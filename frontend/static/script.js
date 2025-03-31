// document.getElementById("start-camera").addEventListener("click", function() {
//     fetch("/start_camera")
//         .then(response => response.json())
//         .then(data => {
//             console.log(data.message);
//             document.getElementById("video-feed").src = "/video_feed";
//             document.getElementById("video-feed").style.display = "block";
//             document.getElementById("stop-camera").disabled = false;
//             this.disabled = true;
//             fetchAttendance(); // ✅ Fetch attendance immediately after starting the camera
//         })
//         .catch(error => console.error("Error starting camera:", error));
// });

// document.getElementById("stop-camera").addEventListener("click", function() {
//     fetch("/stop_camera")
//         .then(response => response.json())
//         .then(data => {
//             console.log(data.message);
//             document.getElementById("video-feed").src = "";
//             document.getElementById("video-feed").style.display = "none";
//             document.getElementById("start-camera").disabled = false;
//             this.disabled = true;
//             showMessage("Camera stopped.", "red");
//         })
//         .catch(error => console.error("Error stopping camera:", error));
// });

// function fetchAttendance() {
//     fetch('/attendance_records')
//         .then(response => response.json())
//         .then(data => {
//             console.log("Fetched Attendance Data:", data);
//             if (data.length > 0) {
//                 let latestEntry = data[0];
//                 showMessage(`✔ Attendance recorded for <b>${latestEntry.name}</b> at ${latestEntry.timestamp}`, "green");
//             } else {
//                 showMessage("No attendance recorded yet.", "gray");
//             }
//         })
//         .catch(error => console.error("Error fetching attendance:", error));
// }

// // Show message and auto-hide after 5 seconds
// function showMessage(message, color) {
//     let msgBox = document.getElementById("attendance-message");
//     msgBox.innerHTML = message;
//     msgBox.style.color = color;
//     msgBox.style.display = "block";

//     setTimeout(() => {
//         msgBox.style.display = "none";
//     }, 5000);
// }


// setInterval(fetchAttendance, 3000);









let lastFrameTime = Date.now();
let checkingAttendance = false; // Avoid multiple API calls

document.getElementById("start-camera").addEventListener("click", function() {
    fetch("/start_camera")
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            document.getElementById("video-feed").src = "/video_feed";
            document.getElementById("video-feed").style.display = "block";
            document.getElementById("stop-camera").disabled = false;
            this.disabled = true;
            monitorFrameUpdates(); // Start monitoring for freeze
           listenForAttendanceUpdate(); // Start listening for updates
        })
        .catch(error => console.error("Error starting camera:", error));
});

document.getElementById("stop-camera").addEventListener("click", function() {
    fetch("/stop_camera")
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            document.getElementById("video-feed").src = "";
            document.getElementById("video-feed").style.display = "none";
            document.getElementById("start-camera").disabled = false;
            this.disabled = true;
            document.getElementById("attendance-message").innerHTML = "Camera stopped.";
        })
        .catch(error => console.error("Error stopping camera:", error));
});

// Function to monitor camera frame updates
function monitorFrameUpdates() {
    setInterval(() => {
        let currentTime = Date.now();
        
        if (document.getElementById("video-feed").src && (currentTime - lastFrameTime > 1000)) {
            if (!checkingAttendance) {
                checkingAttendance = true;
                console.log("Camera frozen detected! Fetching attendance...");
                fetchAttendance();
            }
        } else {
            checkingAttendance = false;
        }
    }, 1000);
}

// Fetch the latest attendance record
function fetchAttendance() {
    fetch('/latest_attendance_message')
        .then(response => response.json())
        .then(data => {
            console.log("Fetched Attendance:", data);
            if (data.name) {
                showMessage(`✔ Attendance recorded for <b>${data.name}</b> at ${data.timestamp}`, "green");
                document.getElementById("attendance-message").innerHTML = "`✔ Attendance recorded for <b>${data.name}</b> at ${data.timestamp}";
            } else {
                showMessage("No attendance recorded yet.", "gray");
            }
        })
        .catch(error => console.error("Error fetching attendance:", error));
        
    }

// Listen for attendance updates using polling
function listenForAttendanceUpdate() {
    setInterval(() => {
        fetch('/latest_attendance_message')
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    console.log("Received Attendance Update:", data.message);
                    showMessage(data.message, "green");
                }
            })
            .catch(error => console.error("Error fetching live attendance message:", error));
    }, 1500); // Polling every 1.5 seconds
}

// Utility function to show messages
function showMessage(message, color) {
    let messageBox = document.getElementById("attendance-message");
    messageBox.innerHTML = message;
    messageBox.style.color = color;
}
