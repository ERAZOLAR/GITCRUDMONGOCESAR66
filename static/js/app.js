base64 = null

function validarDatos(){

}






async function visualizarFoto(evento){
    const files = evento.target.files
    const archivo = files[0]

    let filename = archivo.name
    let extension = filename.split('.').pop()
    extension = extension.tolowerCase()

    archivo = fileFoto.value
    extension = archivo.spl
    var allowedExtensions = /(.jpg| .jpeg| .png| .gif)$/i;
    if(!allowedExtensions.exec(filePath)){
        alert('subir archivo con formato admitido')
        fileInput.value = '';
        return false;
    //base64URL = await encodeFileAsBase64URL(archivo);
    const objectURL = URL.createObjectURL(archivo)
    imagenProducto.setAttibute("src", objectURL)
}


async function encodeFileAsBase64URL(file){
    return new Promise((resolve) => {
        const reader = new FileReader();
        reader.addEventListener('loadend', () => {
            resolve(reader.result);

        });
        reader.readAsDataURL(file);
    });

    };


}    





{/*}
function agregarProducto(){
    const producto = {
        codigo: txtCodigo.value,
        nombre: txtNomobre.value,
        precio: txtPrecio.value,
        categoria: cbCategoria,
        foto: fileFoto
    }
}
*/}
