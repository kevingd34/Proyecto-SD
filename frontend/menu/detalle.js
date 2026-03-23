function calcularDescuento(fecha){

let hoy=new Date()
let vencimiento=new Date(fecha)

let dias=(vencimiento-hoy)/(1000*60*60*24)

if(dias<=0) return 50
if(dias<=2) return 35
if(dias<=5) return 20
if(dias<=10) return 10

return 5
}


function cargar(){

let producto=JSON.parse(localStorage.getItem("productoSeleccionado"))

/* VALIDACIÓN SEGURA */
if(!producto){

alert("No hay producto seleccionado")

window.location="./index.html"

return

}


let descuento=calcularDescuento(producto.fecha)

let precioFinal=producto.precio-(producto.precio*(descuento/100))


document.getElementById("nombre").innerText=producto.nombre
document.getElementById("precio").innerText="Precio: "+producto.precio
document.getElementById("cantidad").innerText="Cantidad: "+producto.cantidad
document.getElementById("fecha").innerText="Vence: "+producto.fecha

document.getElementById("descripcion").innerText=
"Producto disponible en tienda. Se recomienda su compra antes de la fecha de vencimiento."

document.getElementById("descuento").innerText="Descuento: "+descuento+"%"
document.getElementById("final").innerText="Precio final: "+precioFinal.toFixed(0)

}


/* COMPRA */

function comprar(){

alert("Compra realizada correctamente")

}


/* VOLVER */

function volver(){

window.location="./index.html"

}


window.onload=cargar