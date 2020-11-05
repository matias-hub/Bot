class localidades{
    constructor(local,telefono){
        this.Local = local;
        this.telefono = telefono;
    }
}

class productos{
    constructor(nombre,size,precio,imgPath,id, cantidad){
        this.nombre = nombre;
        this.size =size
        this.precio = precio;
        this.imgPath = imgPath;
        this.id = id;
        this.cantidad = cantidad;
    }
}
window.onload = () =>{
    // con Ajax busco los archivos Json
    $.ajax({
        url: './js/productos.json',
        success: function(data) {
           // Genera obetos 
            productos = data.map(object => {
                return new productos(object.nombre,object.size,object.precio,object.imgPath,object.id,object.cantidad);
            });

            // Agrega los producotos al main
            const contenedorProductos = document.getElementById('cartaProducto')
            productos.forEach( producto => {   
                contenedorProductos.innerHTML += crearCarta(producto)
    });

    // Rescasta la cantidad de productos en el session storage
    buscarCantidadSession()
        }
     });

     // con Ajax busco los archivos Json
     $.ajax({
        url: './js/Localidades.json',
        success: function(data) {
            // Genera obetos 
            localidades = data.map(object =>{
                return new localidades(object.local,object.telefono);
            });

            // Popula la lista desplegable
            const listaDesplegable = document.getElementById('ddlViewBy')
            localidades.forEach( local => {   
                listaDesplegable.innerHTML += crearLista(local.Local)
            });

            // Busca si hay alguna localdiad guardad
            buscarLocalidad()

            // Guarda el dato de localidad en LocalStorage
            $("#ddlViewBy").change( function() {
                e = document.getElementById("ddlViewBy");
                cambio = e.options[e.selectedIndex].value;
                localStorage.setItem('localidad', cambio);
            });
        }
     });

    // Muestra las divs ocultos con lo que hay en el carrito
    shopping_cart.addEventListener('click', () => {
        crearTiket(productos)
        
        // Verifica, si esta selleccionada la localidad
        if ($('#ddlViewBy').val() == 1){
            $('#ddlViewBy').css('background-color','red');
            return false;
          }
        productsOnCart.classList.toggle('show');
        productCardMask.classList.toggle('show');    
    });

    // Vuelve el color blanco a la lista desplegable
    $("#ddlViewBy").focus( function() {
        $('#ddlViewBy').css('background-color','white');
    });


    // Oculta los divs cuando se hace click fuera
    productCardMask.addEventListener('click', () => {
    productsOnCart.classList.toggle('show');
    productCardMask.classList.toggle('show');    
    });

    // Envia al usuario a Whatsapp
    $("#contactoWhatsapp").click( function() {
    crearLinkWhatsapp(productos,localidades)
    });
}

// Ovserva las cantidades de cada producto y escribe un texto para whatsapp
function crearTiket(productos){
    ticket = 'Hola!<br>Me gustaria hacer un pedido:'
    total = 0
    productos.forEach( producto => {
        if (producto.cantidad > 0) {
        ticket +=  '<br>' + producto.nombre + ' * ' + producto.cantidad + ' $' + producto.precio*producto.cantidad}
        total += producto.precio*producto.cantidad
    })
    ticket += '<br>' + 'Total = ' + total
    mensajePedido=document.getElementById('mensajePedido')
    mensajePedido.innerHTML = ticket
    return ticket
}

// General el link para whatsapp, con el pediod y el numero correcto
function crearLinkWhatsapp(productos,localidades){
    ticket = crearTiket(productos)
    ticket = ticket.split(' ').join('%20')
    ticket = ticket.split('<br>').join('%0D%0A')
    lovalidad = document.getElementById('ddlViewBy')
    e = document.getElementById("ddlViewBy");
    Local = e.options[e.selectedIndex].value;
    const aux = localidades.find( localidades => localidades.Local == Local)
    telefono = aux.telefono
    var link =`https://wa.me/${telefono}?text=${ticket}`
    document.getElementById("contactoWhatsapp").href=link;
}

// Crea las opciones de la lista desplegable
function  crearLista(local) {
    return`
    <option value="${local}">${local}</option>
    `
}

// Crea los Div de producto
function crearCarta(producto) {
    return`
    <div class="caja-producto">
        <img class="cartaProductoImg" src="${producto.imgPath}" >
        <div class="cartaProductoTitulo pProductos">${producto.nombre} </div>
        <div class="cartaProductoSize pProductos">${producto.size} </div>
        <div class="cartaProductoPrecio pProductos">$${producto.precio} </div>
        <input type="number" class="cartaProductoInput" onclick="modificar(event, '${producto.id}')"  min="0" id='${producto.id}' placeholder="Cant.">
    </div>
    `
}

// Cambia el atributo cantidad de cada producto
function modificar(event,id){
    const aux = productos.find( productos => productos.id === id);
    aux.cantidad = event.target.value;
    sessionStorage.setItem(id, event.target.value );
}

// Busca en el Local Storage, la localidad
function buscarLocalidad() {
    var local = localStorage.getItem('localidad')
    if (local != null) {
        $(`#ddlViewBy  option[value="${local}"]`).attr("selected", true);}
}

// Rescasta la cantidad de prductos en el session storage
function buscarCantidadSession() {
    let productoSesion = Object.keys(sessionStorage)
    // live server injecta esta key en el session storage, asi que la borro
    if ((productoSesion[0] === 'IsThisFirstTime_Log_From_LiveServer')){sessionStorage.removeItem('IsThisFirstTime_Log_From_LiveServer')}
    productoSesion = Object.keys(sessionStorage)
    if (productoSesion[0] === 0){}
    else {productoSesion.forEach(prod => document.getElementById(`${prod}`).value = sessionStorage.getItem(prod))}
}

function reqListener () {
    console.log(this.responseText);
  }

function llamarajax(url){  
    //var req = new XMLHttpRequest('GET','./js/productos.json')
    // //console.log(req)

    // // Use the Fetch API & ES6
    // fetch('./js/productos.json')
    // .then(response => response.json())
    // .then(data => {
    // // Do something with your data
    // console.log(data);
    // });


    $.ajax({
         url: url,
         success: function(data) {
            console.log('entro ajax');
            console.log(data)
            return data
         },
        statusCode: {
           404: function() {
             alert('There was a problem with the server.  Try again soon!');
           }
         }
      });
    };
