
//var formData = new FormData( document.getElementById("wineForm") );
//console.log(formData);

var data = $("form").serializeArray()

console.log(data)

function completeAndRedirect(){
console.log("HELLO!")
var xml = new XMLHttpRequest();
var data = $("form").serializeArray()

console.log(data)
//xml.open("POST", "/");
//xml.onreadystatechange = handle_res_post;
//xml.send(JSON.stringify(data));
}


//Handle return data from upload
function handle_res_post() {
  //console.log("TOuch handle_res");
  switch(this.readyState){
    case 1:
        console.log("Opened Query MSG");
        break;
    case 2:
        console.log("Reading Query HEADER");
        break;
    case 3:
        console.log("Loading Query Data");
        break;
    case 4:
    if (this.status == 200) {
      //console.log(this.responseText)
      var myArr = JSON.parse(this.responseText);
      console.log(this.responseText);
      //CHECK IF response was an update response!
      break;
      } else if(this.status == 404){
        console.log("Error 404");
        break;
      }
      else{
        console.log('Error 503');
        break;
      }
      break;
    default:
      console.log("Something Went wrong...");
      break;
  }
  }