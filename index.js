
function sendRequest() {
    const bucket = document.getElementById("bucket");
    const url = "http://127.0.0.1:5000"; //+ new URLSearchParams({rank, title});
    fetch(url)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error ${response.status}`);
        }
        return response.text(); // Or `.json()` or one of the others
      })
      .then((data) => {
        console.log("data", data);
        bucket.textContent = data;
      })
      .catch((error) => {
        // ...handle/report error...
      });
}
sendRequest()


