function login(){

let usuario=document.getElementById("usuario").value
let clave=document.getElementById("clave").value
let tipo=document.getElementById("tipo").value

/* CREDENCIALES SIMPLES */

if(tipo==="admin" && usuario==="admin" && clave==="123"){

localStorage.setItem("rol","admin")

window.location="../menu/index.html"

}

else if(tipo==="usuario" && usuario==="user" && clave==="123"){

localStorage.setItem("rol","usuario")

window.location="../menu/index.html"

}

else{

alert("Datos incorrectos")

}

}