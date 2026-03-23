let productos=JSON.parse(localStorage.getItem("productos"))||[]

function cargar(){

let cont=document.getElementById("lista")

productos.forEach((p,i)=>{

cont.innerHTML+=`

<div class="producto">

<input id="n${i}" value="${p.nombre}">

<input id="p${i}" value="${p.precio}">

<input id="c${i}" value="${p.cantidad}">

<input type="date" id="f${i}" value="${p.fecha}">

<button onclick="actualizar(${i})">Actualizar</button>

</div>

`

})

}

function actualizar(i){

productos[i].nombre=document.getElementById("n"+i).value
productos[i].precio=document.getElementById("p"+i).value
productos[i].cantidad=document.getElementById("c"+i).value
productos[i].fecha=document.getElementById("f"+i).value

localStorage.setItem("productos",JSON.stringify(productos))

alert("Producto actualizado")

}

function volver(){
window.location="../menu/index.html"
}

window.onload=cargar