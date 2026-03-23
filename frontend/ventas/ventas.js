let productos=JSON.parse(localStorage.getItem("productos"))||[]

function cargar(){

let cont=document.getElementById("lista")

productos.forEach(p=>{

cont.innerHTML+=`

<div class="producto">

<h3>${p.nombre}</h3>

<p>Precio: ${p.precio}</p>

<p>Cantidad: ${p.cantidad}</p>

<p>Vence: ${p.fecha}</p>

</div>

`

})

}

function volver(){
window.location="../menu/index.html"
}

window.onload=cargar