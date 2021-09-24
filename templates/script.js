fetch("http://127.0.0.1:5000/api/v1/statistics?region=na1&name=whippedyesman&api_key=RGAPI-36d4248f-3f33-4ecd-9a08-1ee53368c9dd")
  .then((response) => {
    if (response.ok) {
      return response.json();
    } else {
      throw new Error("NETWORK ERROR");
    }
  })
  .then(data => {
    console.log(data);
  })
  .catch((error) => console.error("FETCH ERROR:", error));

  function showPlayer(data){
    let output = `<h1> HELLO ${data.name} <h1>`;
    document.getElementById("player").innerHTML = output
  }



