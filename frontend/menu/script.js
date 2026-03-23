/* NAVEGACIÓN */

function irProductos(){
window.location="../productos/productos.html"
}

function irPromociones(){
window.location="../promociones/promociones.html"
}

function irVentas(){
window.location="../ventas/ventas.html"
}


/* LOGIN / ROL */

function verificarRol(){

let rol=localStorage.getItem("rol")

if(rol==="usuario"){

document.getElementById("btnAdmin1").style.display="none"
document.getElementById("btnAdmin2").style.display="none"
document.getElementById("btnAdmin3").style.display="none"

}

}


/* LOGOUT */

function logout(){

localStorage.removeItem("rol")
window.location="../login/login.html"

}


/* DESCUENTO */

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


/* MOSTRAR TODOS (CON FECHA) */

function cargarProductos(){

let productos=JSON.parse(localStorage.getItem("productos"))||[]

let cont=document.getElementById("ofertas")

cont.innerHTML=""

productos.forEach((p,i)=>{

let descuento=calcularDescuento(p.fecha)

let precioFinal=p.precio-(p.precio*(descuento/100))

cont.innerHTML+=`

<div class="producto" onclick="verProducto(${i})">

<h3>${p.nombre}</h3>

<p>Precio: ${p.precio}</p>

<p>Descuento: ${descuento}%</p>

<p style="color:red">Final: ${precioFinal.toFixed(0)}</p>

<p>Vence: ${p.fecha}</p>

</div>

`

})

}


/* FILTRAR (RESALTAR) */

function filtrar(min){

let productos=JSON.parse(localStorage.getItem("productos"))||[]

let cont=document.getElementById("ofertas")

cont.innerHTML=""

productos.forEach((p,i)=>{

let d=calcularDescuento(p.fecha)

let final=p.precio-(p.precio*(d/100))

let estilo = d >= min 
? "border:2px solid green; transform:scale(1.05);" 
: "opacity:0.3;"

cont.innerHTML+=`

<div class="producto" style="${estilo}" onclick="verProducto(${i})">

<h3>${p.nombre}</h3>

<p>Precio: ${p.precio}</p>

<p>Descuento: ${d}%</p>

<p style="color:red">Final: ${final.toFixed(0)}</p>

</div>

`

})

}


/* VER DETALLE */

function verProducto(index){

let productos=JSON.parse(localStorage.getItem("productos"))||[]

let producto=productos[index]

localStorage.setItem("productoSeleccionado",JSON.stringify(producto))

window.location="./detalle.html"

}


/* INICIO */

window.onload=function(){

verificarRol()
cargarProductos()

}