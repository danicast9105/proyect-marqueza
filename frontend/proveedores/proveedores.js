/* Proveedores — MARQUEZA
   CRUD local para completar la interfaz siguiendo la estructura del proyecto César.
   Los registros quedan listos para conectar a Flask/MySQL. */
const KEY="marqueza_proveedores";
const body=document.body, sidebar=document.querySelector(".barra_lateral");
const toggle=document.querySelector(".toggle"), hamburger=document.getElementById("hamburger");
const modeSwitch=document.querySelector(".toggle_switch"), modeText=document.querySelector(".modo_texto");
const tbody=document.querySelector(".cont_tabla tbody");
const modal=document.getElementById("modalProveedor"), form=document.getElementById("formProveedor");
const btnAgregar=document.querySelector(".agregar"), btnCerrar=document.getElementById("cerrarModal"), btnCancelar=document.getElementById("btnCancelar");
let editIndex=-1;
const defaults=[];
function data(){return JSON.parse(localStorage.getItem(KEY)||"[]")}
function save(x){localStorage.setItem(KEY,JSON.stringify(x))}
function render(filter=""){const arr=data();tbody.innerHTML="";arr.forEach((x,i)=>{if(filter && !JSON.stringify(x).toLowerCase().includes(filter.toLowerCase()))return;
const tr=document.createElement("tr");tr.innerHTML=`<td>${x["empresa"]||""}</td><td>${x["contacto"]||""}</td><td>${x["telefono"]||""}</td><td>${x["correo"]||""}</td><td>${x["direccion"]||""}</td><td><button class="btn-editar" data-i="${i}">Editar</button></td><td><button class="btn-eliminar" data-i="${i}">Eliminar</button></td>`;tbody.appendChild(tr)});}
function openModal(){modal.classList.add("active")}
function closeModal(){modal.classList.remove("active");form.reset();editIndex=-1}
btnAgregar?.addEventListener("click",openModal);btnCerrar?.addEventListener("click",closeModal);btnCancelar?.addEventListener("click",closeModal);
form?.addEventListener("submit",e=>{e.preventDefault();const arr=data();const obj={};obj["empresa"]=document.getElementById("empresa").value;obj["contacto"]=document.getElementById("contacto").value;obj["telefono"]=document.getElementById("telefono").value;obj["correo"]=document.getElementById("correo").value;obj["direccion"]=document.getElementById("direccion").value;if(editIndex>=0)arr[editIndex]=obj;else arr.push(obj);save(arr);closeModal();render();});
tbody?.addEventListener("click",e=>{const i=e.target.dataset.i;if(i===undefined)return;const arr=data();if(e.target.classList.contains("btn-eliminar")){if(confirm("¿Eliminar registro?")){arr.splice(Number(i),1);save(arr);render()}}else if(e.target.classList.contains("btn-editar")){editIndex=Number(i);const x=arr[editIndex];document.getElementById("empresa").value=x["empresa"]||"";document.getElementById("contacto").value=x["contacto"]||"";document.getElementById("telefono").value=x["telefono"]||"";document.getElementById("correo").value=x["correo"]||"";document.getElementById("direccion").value=x["direccion"]||"";openModal()}});
document.querySelector(".cont_busqueda input")?.addEventListener("input",e=>render(e.target.value));
modeSwitch?.addEventListener("click",()=>{body.classList.toggle("dark");if(modeText)modeText.innerText=body.classList.contains("dark")?"Claro":"Oscuro"});
toggle?.addEventListener("click", () => {
    sidebar?.classList.toggle("close");
    document.body.classList.toggle("sidebar-expanded");
});
hamburger?.addEventListener("click",()=>sidebar?.classList.toggle("open"));
render();
