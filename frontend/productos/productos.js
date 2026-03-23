function guardar(){

let productos = JSON.parse(localStorage.getItem("productos")) || []

let nombre = document.getElementById("nombre").value
let precio = parseFloat(document.getElementById("precio").value)
let cantidad = parseInt(document.getElementById("cantidad").value)
let fecha = document.getElementById("fecha").value

if(nombre === "" || isNaN(precio) || isNaN(cantidad) || fecha === ""){
alert("Completa todos los campos")
return
}

let nuevo = {
nombre,
precio,
cantidad,
fecha
}

productos.push(nuevo)

localStorage.setItem("productos", JSON.stringify(productos))

alert("Producto guardado correctamente")

limpiar()

}

function limpiar(){

document.getElementById("nombre").value=""
document.getElementById("precio").value=""
document.getElementById("cantidad").value=""
document.getElementById("fecha").value=""

}

function volver(){

window.location="../menu/index.html"

}